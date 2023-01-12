import glob
from parser.lexer import Lexer

tests = [f for f in glob.glob("tests/*.in")]
success_test = 0
for test in tests:
    lexer = Lexer()
    with open(test, 'r') as content:
        got_lexeme = lexer.test_lex(str(content.read()))
    with open(test.replace('.in', '.out'), 'r') as excepted_file:
        excepted_lexeme = excepted_file.read()
    if got_lexeme == excepted_lexeme:
        print(f"🟢 Test: {test.replace('tests/', '')}")
        success_test += 1
    else:
        print(f"🔴 Error test: {test.replace('tests/', '')}")
print(f"Total: {success_test}/{len(tests)}")
