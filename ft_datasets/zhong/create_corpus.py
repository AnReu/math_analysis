import json
from collections import defaultdict

raw_pairs = json.load(open('../reusch/parts/arqmath_task1_10_raw.json'))
all_posts = json.load(open('../cleaned_in_parts.json'))
votes = json.load(open('cleaned_votes_only.json'))

# id to votes, id to duplicates

id_to_vote = {}
id_to_duplicates = {}
is_accepted = defaultdict(bool)

is_duplicate = []

for q_id in votes:
    answers = votes['q_id']['answer_ids']
    vote_dicts = votes['q_id']['votes']
    for a_id, vote_dict in zip(answers, vote_dicts):
        id_to_vote[a_id] = vote_dict['vote_count']
        if vote_dict['accepted']:
            is_accepted[a_id] = vote_dict['accepted']
    id_to_duplicates[q_id] = votes['duplicates']
    for d_id in votes['duplicates']:
        is_duplicate.append(d_id)

is_duplicate = sorted(is_duplicate)

duplicates_only = {}

for q_id in all_posts:
    if q_id in is_duplicate:
        duplicates_only[q_id] = (d['post_id'], d['title'], d['question'], d['title_variables'] + d['question_variables'])

# re-create corpus and remove not needed relevant answers

no_all = len(raw_pairs)
no_train = int(no_all * 0.9)
no_val = no_all - no_train
# pair = (question, answer, label)
# (d['post_id'], d['title'], d['question'], d['title_variables'] + d['question_variables'])
# d['answers'], d['answer_variables'], d['answer_ids']

recreated_corpus = {}

recreated_corpus['relevant'] = defaultdict(list)
recreated_corpus['nonrelevant'] = defaultdict(list)

id_removed_from = defaultdict(list)

for i, pair in enumerate(raw_pairs):
    question, answer, label = pair
    q_id, title, question_test, variables = question

    split = 'train' if i < no_train else 'val'
    if label == '0':
        # non-relevant answer for question
        recreated_corpus['nonrelevant'][q_id].append((question, answer, label, split))

    answer_text, a_vars, a_id = answer
    if id_to_vote[a_id] < 7 and not is_accepted[a_id]:
        id_removed_from[q_id].append(split)
        continue
    else:
        recreated_corpus['relevant'][q_id].append((question, answer, label, split))


# add duplicates, remove not needed non relevant answers
added_duplicates = defaultdict(list)
for q_id in recreated_corpus['relevant']:
    # question, answer, label, split = pair
    # q_id, title, question_test, variables = question
    add_duplicates = id_to_duplicates[q_id] != []
    if add_duplicates:
        question, answer, label, split = recreated_corpus['relevant']['q_id'][0]
        for d_id in id_to_duplicates[q_id]:
            duplicate = duplicates_only[d_id]
            #TODO: determine which split is correct
            added_duplicates[q_id].append((question, duplicate, label, split))
    
    