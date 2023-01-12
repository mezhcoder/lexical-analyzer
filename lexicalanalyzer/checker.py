import glob
from lexer import Lexer

tests = [f for f in glob.glob("tests/*.in")]
success_test = 0
for test in tests:
    lexer = Lexer()
    try:
        with open(test, 'r') as content:
            got_lexeme = lexer.test_lex(str(content.read()))
        with open(test.replace('.in', '.out'), 'r') as expected_file:
            expected_lexeme = expected_file.read()
        if got_lexeme == expected_lexeme:
            print(f"🟢 Test: {test.replace('tests/', '')}")
            success_test += 1
        else:
            print(f"🔴 Error test: {test.replace('tests/', '')}")
    except Exception as e:
        print(f"🔴 Error test: {test.replace('tests/', '')}\nMessage: {str(e)}")

print(f"Total: {success_test}/{len(tests)}")
