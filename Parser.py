from collections import deque
from parsetable import create_parse_table
from Scanner import scanner, SYM_TAB
from Rules import production_rules

TERMINALS = {
    'Z0': 0,
    '[id]': 1,
    '[Constant]': 2,
    'package': 3,
    'import': 4,
    'abstract': 5,
    'final': 6,
    'sealed': 7,
    'private': 8,
    'protected': 9,
    'class': 10,
    'object': 11,
    'val': 12,
    'def': 13,
    '<=': 14,
    'if': 15,
    'else': 16,
    'while': 17,
    'case': 18,
    '=>': 19,
    'in': 20,
    'print': 21,
    'return': 22,
    'not': 23,
    'true': 24,
    'false': 25,
    'and': 26,
    'or': 27,
    'int': 28,
    'real': 29,
    'bool': 30,
    ';': 31,
    '{': 32,
    '}': 33,
    '(': 34,
    ')': 35,
    ':': 36,
    ',': 37,
    '=': 38,
    '+': 39,
    '*': 40,
    '@': 41,
}

NON_TERMINALS = {
    '<scala>': 42,
    '<packages>': 43,
    '<imports>': 44,
    '<scala-body>': 45,
    '<subbody>': 46,
    '<modifier>': 47,
    '<subbody-tail>': 48,
    '<tail-type>': 49,
    '<block>': 50,
    '<stmts>': 51,
    '<stmt>': 52,
    '<dcl>': 53,
    '<dcl-tail>': 54,
    '<ids>': 55,
    '<more-ids>': 56,
    '<type>': 57,
    '<asmt>': 58,
    '<if>': 59,
    '<while>': 60,
    '<case>': 61,
    '<in>': 62,
    '<out>': 63,
    '<return>': 64,
    '<expr>': 65,
    '<arith-expr>': 66,
    '<arith>': 67,
    '<bool-expr>': 68,
    '<bool>': 69,
    '"': 70
}


def get_value(key_to_find):
    d = {**TERMINALS, **NON_TERMINALS}
    for key, value in d.items():
        if key == key_to_find:
            return value


def get_key(value_to_find):
    d = {**TERMINALS, **NON_TERMINALS}
    for key, value in d.items():
        if value == value_to_find:
            return key


def find_rule(df, current_stack_top, parse_look_ahead):
    return df.loc[current_stack_top][parse_look_ahead]


def Parser():
    step = 1
    parse_look_ahead = ''
    df = create_parse_table()
    program_stack = deque()

    # push Z0 onto stack initially
    program_stack.append(get_value('Z0'))
    print('-' * 123)
    print('|     {0:15}     |    {1:20}    |     {2:20}   |     {3}      |'.format(step, get_key(
        program_stack[-1]) + '  ' + str(program_stack[-1]), parse_look_ahead, 'Push start symbol to stack'))

    program_stack.append(get_value('<scala>'))  # push start symbol to stack

    token_from_scanner = scanner()  # call scanner to get the initial
    if token_from_scanner:
        tokentype,parse_look_ahead,_ = token_from_scanner
    else:
        parse_look_ahead = None

    while len(program_stack)!=0:
        current_stack_top = program_stack[-1]

        if current_stack_top in TERMINALS.values():
            if get_key(current_stack_top) == parse_look_ahead or get_key(current_stack_top) in ['[id]', '[Constant]']:
                step += 1
                print('-' * 123)
                if get_key(current_stack_top) in ['[id]', '[Constant]']:
                    print('|     {0:15}     |    {1:20}    |     {2:20}   |      {3:<26}     |'.format(step, get_key(
                    current_stack_top) + '  ' + str(current_stack_top), parse_look_ahead+'  ' + str(current_stack_top), 'Match'))
                else:
                    print('|     {0:15}     |    {1:20}    |     {2:20}   |      {3:<26}     |'.format(step, get_key(
                    current_stack_top) + '  ' + str(current_stack_top), parse_look_ahead+'  ' + str(get_value(parse_look_ahead)), 'Match'))
                program_stack.pop()
                token_from_scanner = scanner()
                if token_from_scanner:
                    tokentype,parse_look_ahead,_ = token_from_scanner
                else:
                    parse_look_ahead = None
            elif current_stack_top == 0 and parse_look_ahead == None:  # Accept when stack_top is Z0 and there is no token from scanner.
                step += 1
                print('-' * 123)
                print('|     {0:15}     |    {1:20}    |     {2:20}   |      {3:<26}     |'.format(step, get_key(
                    current_stack_top) + '  ' + str(current_stack_top),'  ', 'Accept'))
                program_stack.pop()
            else:
                print('parser errror')
        elif current_stack_top == get_value('"'):
            program_stack.pop()
        elif current_stack_top in NON_TERMINALS.values():
            if parse_look_ahead != None:
                if tokentype == 'id' or tokentype == 'Constant':
                    rule_no = find_rule(df, get_key(current_stack_top), tokentype)
                else:
                    rule_no = find_rule(df, get_key(current_stack_top), parse_look_ahead)
                rule_to_use = production_rules[str(rule_no)]
                lhs, rhs = rule_to_use.split('->')
                step += 1
                program_stack.pop()
                print('-' * 123)
                if tokentype == 'id' or tokentype == 'Constant':
                    print('|     {0:15}     |    {1:20}    |     {2:20}   |     {3:<26}      |'.format(step, get_key(
                        current_stack_top) + '  ' + str(current_stack_top), parse_look_ahead + '  ' + str(
                        get_value(f'[{tokentype}]')), f'Use Rule {rule_no}'))
                else:
                    print('|     {0:15}     |    {1:20}    |     {2:20}   |     {3:<26}      |'.format(step, get_key(
                        current_stack_top) + '  ' + str(current_stack_top), parse_look_ahead + '  ' + str(
                        get_value(parse_look_ahead)), f'Use Rule {rule_no}'))
                for i in rhs.split(' ')[::-1]:
                    program_stack.append(get_value(i))
            else:
                rule_no = find_rule(df, get_key(current_stack_top),'"')
                rule_to_use = production_rules[str(rule_no)]
                lhs, rhs = rule_to_use.split('->')
                step += 1
                program_stack.pop()
                print('-' * 123)
                print('|     {0:15}     |    {1:20}    |     {2:20}   |     {3:26}      |'.format(step, get_key(current_stack_top) + '  ' + str(current_stack_top), ' ',f'Use Rule {rule_no}'))
                for i in rhs.split(' ')[::-1]:
                    program_stack.append(get_value(i))


def main():
    # read the file name from command line and print contents of the file to std output
    print('--------------------- Source Program -----------------------')
    with open('sample.scala', encoding='utf-8') as source_file:
        source_code_as_string = source_file.read()
        print(source_code_as_string)

    # parser output
    print('-' * 123)
    print('|     {0:15}     |    {1:20}    |     {2:20}   |     {3:26}      |'.format('Steps', 'Stack_Top', 'Look_ahead','Action'))

    # call parser to parse the source code
    Parser()
    print('-' * 123)

    # Print the contents of the symbol table
    print('--------------------- Symbol Table -----------------------')
    for tokenkey, tokenvalue in SYM_TAB.items():
        print("|{0:15}   |  {1:>15}   |".format(tokenkey, tokenvalue))

    source_file.close()


if __name__ == '__main__':
    main()
