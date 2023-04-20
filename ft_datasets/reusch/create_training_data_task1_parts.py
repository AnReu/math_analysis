import json
import random
from random import shuffle
from collections import defaultdict
from tqdm import tqdm
from os import makedirs
import pandas as pd
from renaming_utils import get_all_renaming

# get_all_renaming(q_vars, answer_parts, answer_vars)

# create training set: one question - two answers, one is correct answer, one is from a different question.
# to make it harder for the model to decide: take question that shares at least one category with the original question

data_path = '../data_processing'
out_path = '../task1/training_files/parts'
train_p = 0.9  # --> valid_p = 1 - train_p, no test set, because ARQMath provides test set
max_examples = 10 # for each question we generate up to max_examples positive and negative examples

data = json.load(open(f'{data_path}/cleaned_in_parts.json', encoding='utf-8'))
makedirs(out_path, exist_ok=True)

# 1. Remove questions without answers
# 2. Group questions by tag
questions_with_answers = defaultdict(list)
for q in data:
    if 'answers' not in q:
        continue  # we only want questions with answers
    for tag in q['tags']:
        questions_with_answers[tag].append(q)

# 3. Check number of questions for each tag
print('Questions with answers, sizes by tag:')
for tag in questions_with_answers:
    print(tag, len(questions_with_answers[tag]))


def get_all_answers_except(tags, q_id):
    answers = []
    processed_ids = defaultdict(bool)
    processed_ids[q_id] = True  # omit answers from the original question with id q_id
    for tag in tags:
        for q in questions_with_answers[tag]:
            if not processed_ids[q['post_id']]:
                zipped_answers = list(zip(q['answers'], q['answer_variables'], q['answer_ids']))
                answers.extend(zipped_answers)
                processed_ids[q['post_id']] = True
    return answers

def rename_answers(q_vars, correct_answer, wrong_answer):
    c_answer, c_vars, v_id = correct_answer
    nc_answer, nc_vars, nc_id = wrong_answer

    # c_100, c_75, c_50, c_25, c_0
    c_renamings, c_var_map_100 = get_all_renaming(q_vars, c_answer, c_vars)
    nc_renamings, nc_var_map_100 = get_all_renaming(q_vars, nc_answer, nc_vars)
    return c_renamings, c_var_map_100, nc_renamings, nc_var_map_100


# 4. For each questions: get one correct answer (random out of all answers of this question) and one incorrect answer with at least one common tag
correct_pairs = []
wrong_pairs = []
for d in tqdm(data):
    if 'answers' not in d:
        continue # colbert needs one correct and one incorrect answer, if there are no correct answers, continue

    wrong_candidates = get_all_answers_except(d['tags'], d['post_id'])
    correct_candidates = list(zip(d['answers'], d['answer_variables'], d['answer_ids']))
    N =  min(len(wrong_candidates), len(correct_candidates), max_examples) if max_examples != None else min(len(wrong_candidates), len(correct_candidates))
    correct_answers = random.sample(correct_candidates, N)
    wrong_answers = random.sample(wrong_candidates, N)

    for correct_answer, wrong_answer in zip(correct_answers, wrong_answers):
        correct_pairs.append(
            ((d['post_id'], d['title'], d['question'], d['title_variables'] + d['question_variables']), correct_answer, '1'))  # Label 1 for correct question-answer pairs
        wrong_pairs.append(
            ((d['post_id'], d['title'], d['question'], d['title_variables'] + d['question_variables']), wrong_answer, '0'))  # Label 0 for correct question-answer pairs



# 5. Shuffle data and save splits to file
all_pairs = [*correct_pairs, *wrong_pairs]
shuffle(all_pairs)

no_all = len(all_pairs)
no_train = int(no_all * 0.9)
no_val = no_all - no_train

out_name = f'arqmath_task1_{max_examples}_parts'

json.dump(all_pairs, open(f'{out_path}/{out_name}_raw.json', 'w'))

datasets = {
(0,100): [],
(25,100) : [],
(50,100) : [],
(75,100) : [],
(100,100) : [],
(25,75) : [],
(50,50) : [],
(75,25) : [],
(100,0) : [],
(0,0) : []
}

def build_question(title, q_parts):
    output = ''
    for part, t_type in title:
        if t_type == 'math':
            output += f'${part}$' 
        else:
            output += part
    output += ' '
    for part, q_type in q_parts:
        if q_type == 'math':
            output += f'${part}$' 
        else:
            output += part
    return output

posts = []
var_maps = []
for question, answer, label in all_pairs:
    p_id, title, q_parts, q_vars = question
    posts.append(build_question(title, q_parts)) 
    a_parts, a_vars, a_id = answer
    renamed = {}
    renamings, var_map = get_all_renaming(q_vars, a_parts, a_vars)
    renamed[100], renamed[75], renamed[50], renamed[25], renamed[0] = renamings
    for c,nc in datasets:
        if label == 0:
            datasets[(c,nc)].append((renamed[nc],label))
        else:
            datasets[(c,nc)].append((renamed[c],label))
    var_maps.append((p_id, a_id, label, var_map))

json.dump(var_maps, open(f'{out_path}/{out_name}_varmaps.json', 'w'))


def build_split(split, data_pairs, c, nc):
    df = pd.DataFrame(data_pairs, columns=['question', 'answer', 'label'])
    df.to_csv(f'{out_path}/{out_name}_{split}_{max_examples}_{c}_{nc}.csv', index_label='idx')

def split_list(zipped, total_len, no_train):
    train = []
    dev = []
    for i, elem in enumerate(zipped):
        if i < no_train:
            train.append(elem)
        else:
            dev.append(elem)
    return train, dev

for c, nc in datasets:
    train, dev = split_list(zip(posts, *zip(*datasets[(c,nc)])), no_all, no_train)
    build_split('train', train, c, nc)
    build_split('dev', dev, c, nc)

    build_split('test', [], c, nc)

print('Done creating training data for task 1.')
