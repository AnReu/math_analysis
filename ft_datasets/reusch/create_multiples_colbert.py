from random import shuffle

epochs = 3

filename = 'arqmath_task1_10_parts_colbert_train_10_0_0.tsv'
all_train = open(f'colbert/{filename}').read().split('\n')[:-1]


def write_and_shuffle(out_file, all_lines):
    shuffle(all_lines)
    out_file.write('\n'.join(all_lines))

with open(f'colbert/multiples_{epochs}/{filename}', 'w') as out_file:
    write_and_shuffle(out_file, all_train)
    for i in range(epochs - 1):
        out_file.write('\n')
        write_and_shuffle(out_file, all_train)

