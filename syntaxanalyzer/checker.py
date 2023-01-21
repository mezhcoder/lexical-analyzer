import glob
from parser import *

from lexicalanalyzer.lexer import Lexer
from syntaxanalyzer.parser import Parser, get_str_tree

tests = [f for f in glob.glob("tests/*.in")]
success_test = 0
for test in tests:
    try:
        with open(test, 'r') as content:
            lexer = Lexer()
            lexer.text = str(content.read())
            lexer.current_char = lexer.text[lexer.pos]

            parser = Parser(lexer)
            got_data = get_str_tree(parser.program().to_dict())
        with open(test.replace('.in', '.out'), 'r') as expected_file:
            expected_data = expected_file.read()
        if got_data == expected_data:
            print(f"🟢 Test: {test.replace('tests/', '')}")
            success_test += 1
        else:
            print(f"🔴 Error test: {test.replace('tests/', '')}")
    except Exception as e:
        print(f"🔴 Error test: {test.replace('tests/', '')}\nMessage: {str(e)}")

print(f"Total: {success_test}/{len(tests)}")
