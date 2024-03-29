from lexicalanalyzer.lexer import Lexer
from syntaxanalyzer.parser import Parser, get_str_tree


def cli():
    import sys

    lexer = Lexer()
    lexer.text = 'program Test; var x: integer; begin x := 2 + 3 * 4; end.'
    lexer.current_char = lexer.text[lexer.pos]

    parser = Parser(lexer)
    result = get_str_tree(parser.program().to_dict())
    print(result)


if __name__ == "__main__":
    cli()