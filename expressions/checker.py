import glob
from parser import *

tests = sorted([f for f in glob.glob("tests/*.in")])
success_test = 0
for test in tests:
    try:
        with open(test, 'r') as content:
            tokens = lexer(str(content.read()))
            parser = Parser(tokens)
            ast = parser.parse()
            arr_str_tree = []
            ast.fill_arr_str_tree(arr_str_tree=arr_str_tree)
            got_data = '\n'.join(arr_str_tree)
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
