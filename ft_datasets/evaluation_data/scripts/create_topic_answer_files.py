import argparse
import json
from pathlib import Path
import pandas as pd
from tqdm import tqdm 
from collections import defaultdict
import csv
import renaming_utils

parser = argparse.ArgumentParser(description='Create the evaluation files for mathematical answer retrieval (ARQMath Task 1)')

parser.add_argument('--json-path', dest='json_path',
                    default='../../',
                    help='path to the parts json')

parser.add_argument('--topics-path', dest='topics_path',
                    default='../../',
                    help='path to the topics file')

parser.add_argument('--year', dest='year',
                    default='2020',
                    help='ARQMath compedition year')
                    
parser.add_argument('--qrels-path', dest='qrels_path',
                    default='/projects/p_da_poldata/ARQ/task1/qrel_task1',
                    help='path of the qrels file for the specified year')

parser.add_argument('--judged_only', action='store_true', 
                    help='whether to only consider answers that have a relevance judgment in the qrels file')

parser.add_argument('--formula-mode', dest='formula_mode', choices=['default', 'replaced', 'sorted', 'none'], default='default',
                    help='mode in which fomulas are included in the answers, default is to add the latex of the formulas as they apprear in the data set.')

parser.add_argument('--latex-token-mode', dest='latex_token_mode', choices=['default', '$'], default='default',
                    help='mode which seperates each latex token in math environments by a $ character or by nothing. $ is required by CoCoMAE models. Default is to add nothing.')

parser.add_argument('--tag-matching-mode', dest='tag_matching_mode', choices=['one', 'none', 'all'], default='none',
                    help='mode which tags between wrong answers and the question have to match. one = at least one tag has to match, none = no tag matching is needed, i.e., consider all answers, all = all tags have to match (might be too restrictive).')

parser.add_argument('--out-path', dest='out_path',
                    default='evaluation_files',
                    help='path where the directory structure for the output is created (one directory for each topic).')

parser.add_argument('--dummy-formula', dest='dummy_formula',
                    default='$a + b$',
                    help='if replaced is selected as formula-mode, each formula will be replaced by the dummy formula specified in this argument.')



args = parser.parse_args()


year = args.year
topics_file_path = args.topics_path
judged = args.judged_only
formula_mode = args.formula_mode
qrels_file = args.qrels_path

latex_token_mode = args.latex_token_mode
dummy_formula = args.dummy_formula

def reformat_formula(formula):
    while formula.endswith('$') and formula.startswith('$'):
        formula = formula[1:-1]
    tokenized = renaming_utils.tokenize(formula)
    return  '$' + '$$'.join(tokenized) +'$'
    
def reformat_sorted(formula_tokens):
    while formula_tokens[-1] == '$' and formula_tokens[0] == '$':
        formula_tokens = formula_tokens[1:-1]
    return  '$' + '$$'.join(formula_tokens) +'$'

if latex_token_mode == '$' and formula_mode == 'replaced':
    dummy_formula = reformat_formula(dummy_formula)

qrels = defaultdict(list)
with open(qrels_file) as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        t_id, _, a_id, rel = row
        qrels[t_id].append(int(a_id))


topics = json.load(open(topics_file_path, encoding='utf-8'))
tag_matching = args.tag_matching_mode

cleaned_data = json.load(open(f'{args.json_path}/cleaned_in_parts.json', encoding='utf-8'))

line_pattern = '0\t{id_a}\t{id_b}\t{text_a}\t{text_b}\n'


def matching_tags(tags_a, tags_b):
    # returns whether tags_a and tags_b match or not
    if tag_matching == 'none':
        return True
    elif tag_matching == 'one':
        for tag in tags_a:
            if tag in tags_b:
                return True
        return False
    elif tag_matching == 'all':
        for t_a, t_b in zip(sorted(tags_a), sorted(tags_b)):
            if t_a != t_b:
                return False
        return True
    else:
        raise Exception(
            'Please specify the tag_matching parameter: either match at least one tag (one), all or disable matching '
            'generate all question-answer pairs (none). ')

def clean(text):
    to_replace = ['\u2029', '\t', '\n']
    for char in to_replace:
        text = text.replace(char, ' ')
    return text


def build(parts):
    output = ''
    for part, p_type in parts:
        if p_type == 'math':

            if formula_mode == 'replaced':
                output += dummy_formula
            elif formula_mode == 'none':
                output += ' '
            elif formula_mode == 'sorted':
                tokens = renaming_utils.sort_tokens(part)
                if latex_token_mode == '$':
                    output += reformat_sorted
                else:
                    output += ' '.join(tokens)
            elif formula_mode == 'default':
                if latex_token_mode == '$':
                    output += reformat_formula(part)
                else:
                    output += f'${part}$'
            else:
                raise Exception(
                    'Please specify the formula_mode paramter (default, none, sorted, replaced)'
                )
        else:
            output += part
    return output

def build_and_clean(parts):
    text = build(parts)
    return clean(text)

if judged:
    judged_answers = set([a_id for t_id in qrels for a_id in qrels[t_id]]) # all ids for judged answers
    id2answer = {}
    for q in cleaned_data:
        if 'answers' not in q:
            continue
        for a_id, answer in zip(q['answer_ids'], q['answers']):
            if a_id in judged_answers:
                id2answer[a_id] = answer

nl_count = 0
tab_count = 0
p_count = 0
for topic in tqdm(topics):
    lines = []
    id_a = topic['id']

    out_path = f'{args.out_path}/{tag_matching}_{formula_mode}_formulas/{year}/{id_a.replace(" ", "_")}/data/'
    Path(out_path).mkdir(parents=True, exist_ok=True)
    
    question = f"{topic['title']} {topic['question']}"
    question = clean(question)
    if judged:
        for id_b in qrels[id_a]:
            answer = build_and_clean(id2answer[id_b])
            lines.append((id_a, id_b, question, answer))
    else:
        tags = topic['tags'].split(',')
        for q in cleaned_data:
            if 'answers' not in q or not matching_tags(tags, q['tags']):
                continue
            for id_b, answer in zip(q['answer_ids'], q['answers']):
                answer = build_and_clean(answer)
                lines.append((id_a, id_b, question, answer))

df = pd.DataFrame(lines, columns=['id_q', 'id_a', 'question', 'answer'])
df.to_csv(f'{out_path}/test.csv', index=False)
