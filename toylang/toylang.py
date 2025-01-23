from typing import List
import re


TOKENS = {
    'def': r'吾有一术曰',
    'param': r'欲练此术必先得|欲练此术,必先得',
    'assign': r'设|设为',
    'equal': r'为',
    'func_call': r'施',
    'if': r'若',
    'and': r'且',
    'or': r'或',
    'operator': r'加|减|乘|除',
    'tab': r'\t|\s{4}',
    'newline': r'[\r|\n]+',
    'delimiter': r',，',
    'return': r'乃得',
    'print': r'录得',
    'number': r'(零|一|二|三|四|五|六|七|八|九|十)+',
    'variable': '\w+',
}

token_pattern = re.compile('|'.join(f'(?P<{name}>{regex})' for name, regex in TOKENS.items()))

def debug(msg):
    print(f'[DEBUG] {msg}')


def tokenize(input_string):
    tokens = []
    for line in input_string.split('\n'):
        line = line.rstrip()
        if not line:
            continue
        matches = token_pattern.finditer(line)
        for match in matches:
            token_type = match.lastgroup
            token_value = match.group()

            tokens.append((token_type, token_value))
        tokens.append(('newline', '\n'))
    return tokens


def _read_tokens(tokens, output, pos=0) -> int:
    while True:
        if pos >= len(tokens):
            return pos

        # return if control flow
        if tokens[pos][0] == 'def' or tokens[pos][0] == 'if' or tokens[pos][0] == 'newline':
            return pos
        if tokens[pos][0] == 'func_call':
            return pos

        if tokens[pos][0] == 'delimiter':
            output.append(tokens[pos][1])
        elif tokens[pos][0] == 'assign':
            output.append('=')
        elif tokens[pos][0] == 'equal':
            output.append('==')
        elif tokens[pos][0] == 'tab':
            output.append('\t')
        elif tokens[pos][0] == 'operator':
            op_dict = {'加': '+', '减': '-', '乘': '*', '除': '/'}
            output.append(op_dict[tokens[pos][1]])
        elif tokens[pos][0] == 'number':
            # TODO: handle numbers
            output.append(tokens[pos][1])
        elif tokens[pos][0] == 'return':
            output.append('return ')
        elif tokens[pos][0] == 'print':
            output.append('print')
            pos += 1
            output.append('(')
            assert tokens[pos][0] == 'variable'
            pos = _read_tokens(tokens, output, pos=pos)
            output.append(')')
            assert tokens[pos][0] == 'newline',tokens[pos][0]
            output.append('\n')
            return pos
        elif tokens[pos][0] == 'variable':
            output.append(tokens[pos][1])
        else:
            raise ValueError(f"Unknown token {tokens[pos][0]}")
        pos += 1


def transpile(program: str) -> str:
    tokens = tokenize(program)

    debug(tokens)
    output = []

    pos = 0
    while True:
        if pos >= len(tokens):
            break

        if tokens[pos][0] == 'def':
            output.append('def ')
            pos += 1
            assert tokens[pos][0] == 'variable'
            output.append(tokens[pos][1])
            output.append('(')
            pos += 1

            # read the function params
            while True:
                if tokens[pos][0] == 'param':
                    pos += 1
                    if tokens[pos][0] == 'variable':
                        output.append(tokens[pos][1])
                        output.append(', ')
                elif tokens[pos][1] == '\n':
                    output.append('):')
                    output.append('\n')
                    break
                else:
                    raise ValueError(f'Expected param or new line, getting {tokens[pos][1]}')
                pos += 1
        elif tokens[pos][0] == 'if':
            # read the if condition
            output.append('if ')
            pos += 1
            pos = _read_tokens(tokens, output, pos)
            output.append(':')
        elif tokens[pos][0] == 'func_call':
            # call function
            pos += 1
            assert tokens[pos][0] == 'variable'
            output.append(tokens[pos][1])
            pos += 1
            output.append('(')
            pos = _read_tokens(tokens, output, pos)
            output.append(')')
            assert tokens[pos][0] == 'newline'

            output.append('\n')
            pos += 1
        elif tokens[pos][0] == 'newline':
            output.append('\n')
            pos += 1
        else:
            pos = _read_tokens(tokens, output, pos)

    return ''.join(output)


program = '''
吾有一术曰,降龙十八掌,欲练此术,必先得,青龙
    白虎,设,1
	若,青龙,为1
		白虎,设,青龙,加1
	乃得白虎
白虎,设,施降龙十八掌,2
录得白虎'''

transpiled = transpile(program)
debug(transpiled)

exec(transpiled)
