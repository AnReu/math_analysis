from texlex import lexer
import bs4 as bs

def tokenize(math):
    lexer.input(math)
    tokens = []
    last_end = 0
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        tok_start = tok.lexpos
        tok_end = tok.lexpos+len(tok.value)
        if last_end != tok_start:
            number_spaces = tok_start - last_end
            tokens.append(math[last_end:tok_start])
        tokens.append(math[tok_start:tok_end])
        last_end = tok_end
    if last_end != len(math):
        tokens.append(math[last_end:])
    return tokens


def sort_and_build(parts):
    output = ''
    for part, p_type in parts:
        if p_type == 'math':
            no_dollar = part.count('$')
            if no_dollar > 0 and no_dollar %2 == 0:
                tokens_no_dollar = part.replace('$', '')
                tokens = sorted([t for t in tokenize(tokens_no_dollar) if t.strip() != ''])
                tokens = ['$'] * (int(no_dollar/2)) + tokens + (['$'] * (int(no_dollar/2)))
            else:
                tokens = sorted([t for t in tokenize(part) if t.strip() != ''])
            sorted_part = ' '.join(tokens)
            output += f'${sorted_part}$'
        else:
            output += part
    return output

def sort_and_get_body(body):
    soup = bs.BeautifulSoup(body, "lxml")
    for math in soup.find_all('span', {'class':"math-container"}):
        no_dollar = math.text.count('$')

        if no_dollar > 0 and no_dollar %2 == 0:
            tokens_no_dollar = math.text.replace('$', '')
            tokens = sorted([t for t in tokenize(tokens_no_dollar) if t.strip() != ''])
            tokens = ['$'] * (int(no_dollar/2)) + tokens + (['$'] * (int(no_dollar/2)))
        else:
            tokens = sorted([t for t in tokenize(math.text) if t.strip() != ''])
        sorted_part = ' '.join(tokens)
        math.replace_with(f'${sorted_part}$')
    return soup.text

def rename(math, var_map):
    variables_to_rename = var_map.keys()
    renamed_math = ''
    for t in tokenize(math):
        if t in variables_to_rename:
            replacement = var_map[t]
        else:
            replacement = t
            
        renamed_math += replacement
    return renamed_math


def build_str(parts):
    output = ''
    for p, p_type in parts:
        if p_type == 'math':
            output += f'${p}$'
        else:
            output += p
    return output

def build_and_rename_str(parts, var_map):
    output = ''
    for p, p_type in parts:
        if p_type == 'math':
            renamed = rename(p, var_map)
            output += f'${renamed}$'
        else:
            output += p
    return output