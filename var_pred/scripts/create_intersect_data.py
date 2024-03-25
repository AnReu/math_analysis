import json
import string
from collections import defaultdict
from datasets import Dataset
from transformers import AlbertTokenizerFast
import torch
import random

side = 'left' # left or right
other_side = 'right' if side == 'left' else 'left'



tokenizer = AlbertTokenizerFast.from_pretrained('AnReu/math_albert') # in theory every tokenizer for latex should work. You only need to change the _ token that resambles whitespace in the ALBERT tokenizer if you change it to another one (see line 17) 


classes = json.load(open('classes_lower.json')) + list(string.ascii_lowercase) + ['other_class']
classes = list(string.ascii_lowercase) + ['other_class']
print(classes)


def tokenize(examples):
    return tokenizer(examples["left"], examples['right'], padding="max_length", truncation=True, max_length=512)


def create_bow_vector(example, tokenizer, classes):
    char_map = defaultdict(bool)
    unique_counter = 0
    tokenized_l = set(tokenizer.tokenize(example['left']))
    tokenized_r = set(tokenizer.tokenize(example['right']))
    for tok in tokenized_l.intersection(tokenized_r):
        tok = tok.replace('▁','')
        if tok in classes:
            if not char_map[tok]:
                char_map[tok] = True
                unique_counter += 1
        else:
            if not char_map['other_class']:
                char_map['other_class'] = True
                unique_counter += 1

    labels = torch.zeros(len(classes))
    for i, cl in enumerate(classes):
        if char_map[cl]: 
            labels[i] = 1 / unique_counter
    return dict({'labels': labels, f'len_intersection': len(tokenized_l.intersection(tokenized_r))}, **char_map)


for split in ['train', 'test', 'eval']:
    formula_file = f'filtered_data_{split}.json'
    _, _, examples = zip(*json.load(open(formula_file)))
    example_dict = defaultdict(list)
    for ex in examples:
        other = random.choice(examples)
        example_dict[side].append(ex)
        example_dict[other_side].append(other)

    dataset = Dataset.from_dict(example_dict)

    tokenized_dataset = dataset.map(tokenize, batched=True)

    features_dataset = tokenized_dataset.map(create_bow_vector, fn_kwargs={'tokenizer': tokenizer, 'classes':classes})
    #shuffled_dataset = features_dataset.shuffle()

    features_dataset.save_to_disk(f"{formula_file[:-5]}_intersect_processed")
