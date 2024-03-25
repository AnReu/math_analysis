import json
from pathlib import Path
from tqdm import tqdm

from random import choice
import string


from collections import defaultdict, Counter
from transformers import AlbertTokenizerFast

math_path = '../data_raw/MATH' 
split = 'train'

tokenizer = AlbertTokenizerFast.from_pretrained("AnReu/albert-for-arqmath-3")

def get_classes():
    return list(string.ascii_lowercase) + ['other_class']

all_classes = get_classes()

print(f'Split:{split}')
print(f'Classes:', all_classes)
print('Data path:',math_path)

def get_formulas(text):
    formulas = []
    if list(text).count('$') % 2 == 1: # discard if the math env is not closed
        return []
    start_formula = False
    current_formula = ''
    for char in list(text):
        if char == '$':
            if start_formula:
                formulas.append(current_formula)
                current_formula = ''
            start_formula = not start_formula
        elif start_formula:
            current_formula += char
    return formulas

pathlist = Path('.').glob(f'{math_path}/{split}/*/*.json')

train_formulas_problem = []
train_formulas_solution = []

for path in tqdm(pathlist):
    question = json.load(open(path))
    train_formulas_problem.extend(get_formulas(question['problem']))
    train_formulas_solution.extend(get_formulas(question['solution']))

unique_train_formulas = list(set(train_formulas_problem + train_formulas_solution))
filtered_unqiue_train_formulas = [f for f in unique_train_formulas if 'boxed' not in f and len(f) > 2]
remove_sentence_comma_train_formulas = [f[:-1] if f[-1] in list('.,;:') else f for f in  filtered_unqiue_train_formulas]

filtered_examples_map = []
filtered_examples = []
def create_examples(example, tokenizer, classes):
    char_map = defaultdict(bool)
    unique_counter = 0
    for tok in tokenizer.tokenize(example):
        tok = tok.replace('▁','')
        if tok in classes:
            if not char_map[tok]:
                char_map[tok] = True
                unique_counter += 1
        else:
            if not char_map['other_class']:
                char_map['other_class'] = True
                unique_counter += 1

    if not unique_counter == 1 or not char_map['other_class']:
        filtered_examples_map.append(char_map)
        filtered_examples.append(example)

def get_class_str(classes_list):
    return '@@'.join(sorted(classes_list))

for ex in remove_sentence_comma_train_formulas:
    create_examples(ex,tokenizer,all_classes)

class2idx = defaultdict(list)
all_class_combis_str = []
all_class_combis = []
sample_data_dict = {}
for i, ex in enumerate(filtered_examples_map):
    classes_list = [key for key in ex if ex[key]]
    classes = get_class_str(classes_list)
    class2idx[classes].append(i)
    if classes not in all_class_combis_str:
        all_class_combis.append(classes_list)
        all_class_combis_str.append(classes)

    sample_data_dict[i] = ex


def select_best(available_classes, class2idx, all_class_combis):
    available_classes_set = set(available_classes)
    filtered_class_combis = list(filter(lambda s: set(s).issubset(available_classes_set), all_class_combis))
    #print('filtered_class_combis', len(filtered_class_combis), len(filtered_class_combis)/len(all_class_combis))
    if filtered_class_combis == []:
        return None
    class_combi_list = choice(filtered_class_combis)
    class_combi = get_class_str(class_combi_list)
    #print('selected', class_combi)
    selected_idx = choice(range(len(class2idx[class_combi])))
    selected_sample = class2idx[class_combi].pop(selected_idx)
    if len(class2idx[class_combi]) == 0:
        del class2idx[class_combi]
        all_class_combis.remove(class_combi_list)
    return selected_sample

def update_available_classes(available_classes, sample):
    for label in sample:
        if sample[label] and label in available_classes:
            available_classes.remove(label)

last_number_of_samples = -1
available_classes = get_classes()
training_data = []

while all_class_combis and last_number_of_samples != len(training_data):
    last_number_of_samples = len(training_data)
    print('len_train_data', last_number_of_samples)
    while available_classes:
        #current_class = available_classes.pop()
        #print(current_class)
        print('avaiable classes', len(available_classes))
        sample_idx = select_best(available_classes, class2idx, all_class_combis)
        if sample_idx:
            sample = sample_data_dict[sample_idx]
            training_data.append((sample_idx, sample, filtered_examples[sample_idx]))
            update_available_classes(available_classes, sample)
        else:
            break
    available_classes = get_classes() #list(filtered_examples_map[0].keys())
    print('len(class_combis)', len(all_class_combis))

seen_examples = defaultdict(bool)
class_distr = []
for i,ex,_ in training_data:
    seen_examples[i] = True
    for cl in ex:
        if ex[cl]:
            class_distr.append(cl)

for i,ex in enumerate(filtered_examples):
    if not seen_examples[i]:
        print(i)#, unique_test_formulas_list[i])
        print(ex)
    break


cl_ctr = Counter(class_distr)
print(cl_ctr.most_common())

json.dump(training_data, open(f'filtered_data_{split}.json','w'))
