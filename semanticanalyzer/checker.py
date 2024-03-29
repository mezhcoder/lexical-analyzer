import glob
from parser import *

from lexicalanalyzer.lexer import Lexer
from semanticanalyzer.semantic import get_result_semantic_analyzer
from syntaxanalyzer.parser import Parser, get_str_tree

tests = sorted([f for f in glob.glob("tests/*.in")])
success_test = 0
for test in tests:
    try:
        with open(test, 'r') as content:
            program = str(content.read())
            got_data = get_result_semantic_analyzer(program)
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
