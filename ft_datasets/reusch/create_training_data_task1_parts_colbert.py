import json
import random
from random import shuffle
from collections import defaultdict
from tqdm import tqdm
from os import makedirs
import pandas as pd
from renaming_utils import build_and_rename_str, build_str


# get_all_renaming(q_vars, answer_parts, answer_vars)

# create training set: one question - two answers, one is correct answer, one is from a different question.
# to make it harder for the model to decide: take question that shares at least one category with the original question

data_path = '.'
out_path = 'parts'
train_p = 0.9  # --> valid_p = 1 - train_p, no test set, because ARQMath provides test set
max_examples = 10 # for each question we generate up to max_examples positive and negative examples

#data = json.load(open(f'{data_path}/cleaned_in_parts.json', encoding='utf-8'))
makedirs(out_path, exist_ok=True)


        #correct_pairs.append(
        #    ((d['post_id'], d['title'], d['question'], d['title_variables'] + d['question_variables']), correct_answer, '1'))  # Label 1 for correct question-answer pairs
        #wrong_pairs.append(
        #    ((d['post_id'], d['title'], d['question'], d['title_variables'] + d['question_variables']), wrong_answer, '0'))  # Label 0 for correct question-answer pairs

# 5. Shuffle data and save splits to file
#all_pairs = [*correct_pairs, *wrong_pairs]
#shuffle(all_pairs)

all_pairs = json.load(open(f'{out_path}/arqmath_task1_{max_examples}_parts_raw.json'))


no_all = len(all_pairs)
no_train = int(no_all * 0.9)
no_val = no_all - no_train


print(f'all pairs: {no_all} train pairs: {no_train} examples, val pairs: {no_val} examples')



p_id_to_c_and_nc = defaultdict(dict)

for i, pair in enumerate(all_pairs):
    try:
        post_id = pair[0][0]
        label = pair[-1]
        if post_id in p_id_to_c_and_nc:
            if label in p_id_to_c_and_nc[post_id]:
                p_id_to_c_and_nc[post_id][label].append(pair)
            else:
                p_id_to_c_and_nc[post_id][label] = [pair]
        else:
            p_id_to_c_and_nc[post_id][label] = [pair]
    except Exception as e:
        print(e, pairs)

train_triples = []
val_triples = []
all_triples = []

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


done_ids = defaultdict(bool)
for pair in tqdm(all_pairs):
    post_id = pair[0][0]

    if done_ids[post_id]:
        continue

    for nc, c in zip(p_id_to_c_and_nc[post_id]['0'], p_id_to_c_and_nc[post_id]['1']):
        title = pair[0][1]
        q_parts = pair[0][2]
        question = build_question(title, q_parts)
        answer_nc = nc[1]
        answer_c = c[1]
        q_t_vars = pair[0][3]

        all_triples.append((post_id, question, q_t_vars, answer_nc, answer_c))
    done_ids[post_id] = True


print(all_triples[:2])
print(len(all_triples))

no_all_colbert = len(all_triples)
no_train_colbert = int(no_all_colbert * 0.9)
no_val_colbert = no_all_colbert - no_train_colbert

print(f'train: {no_train_colbert} examples, val: {no_val_colbert} examples')

train_triples = all_triples[:no_train_colbert]
val_triples = all_triples[no_train_colbert:]

del all_triples

out_name = f'arqmath_task1_{max_examples}_parts_colbert'

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


var_maps = json.load(open('parts/arqmath_task1_10_parts_varmaps.json'))

ids_to_varmap = {}
for p_id, a_id, label, var_map in var_maps:
    ids_to_varmap[(p_id, a_id)] = var_map

def rename_triples(triples):
    out_triples = {}
    out_triples[(0,0)], out_triples[(0,100)], out_triples[(100,100)] = [],[],[]
    for post_id, question, q_t_vars, answer_nc, answer_c in triples:
        answer_parts_nc, answer_vars_nc, answer_id_nc = answer_nc
        answer_parts_c, answer_vars_c, answer_id_c = answer_c
        varmap_nc = ids_to_varmap[(post_id, answer_id_nc)]
        varmap_c = ids_to_varmap[(post_id, answer_id_c)]

        for c,nc in out_triples:
            if c == 0:
                renamed_c = build_str(answer_parts_c)
            elif c == 100:
                renamed_c = build_and_rename_str(answer_parts_c, varmap_c)
            else:
                raise NotImplementedError('Only 0 and 100 percent renamings are implemented.')
            if nc == 0:
                renamed_nc = build_str(answer_parts_nc)
            elif nc == 100:
                renamed_nc = build_and_rename_str(answer_parts_nc, varmap_nc)
            else:
                raise NotImplementedError('Only 0 and 100 percent renamings are implemented.')
            
            out_triples[(c,nc)].append((question, renamed_c, renamed_nc))

    return out_triples

renamed_train_triples = rename_triples(train_triples)
renamed_val_triples = rename_triples(val_triples)



def build_split(split, triples, c, nc):
    with open(f'{out_path}/{out_name}_{split}_{max_examples}_{c}_{nc}.tsv', 'w') as outfile:
        for question, answer_c, answer_nc in triples:
            if '\t' in question:
                question.replace('\t', '  ')
            if '\t' in answer_c:
                answer_c.replace('\t', '  ')
            if '\t' in answer_nc:
                answer_nc.replace('\t', '  ')
            outfile.write(f'{question}\t{answer_c}\t{answer_nc}\n')
    #df = pd.DataFrame(data_pairs, columns=['question', 'answer', 'label'])
    #df.to_csv(f'{out_path}/{out_name}_{split}_{max_examples}_{c}_{nc}.csv', index_label='idx')

def split_list(zipped, total_len, no_train):
    train = []
    dev = []
    for i, elem in enumerate(zipped):
        if i < no_train:
            train.append(elem)
        else:
            dev.append(elem)
    return train, dev

for c, nc in renamed_train_triples:
    
    build_split('train', renamed_train_triples[(c,nc)], c, nc)
    build_split('dev', renamed_val_triples[(c,nc)], c, nc)

    build_split('test', [], c, nc)

print('Done creating training data for task 1.')
