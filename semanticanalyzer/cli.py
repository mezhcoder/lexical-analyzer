from lexicalanalyzer.lexer import Lexer
from semanticanalyzer.semantic import get_result_semantic_analyzer
from syntaxanalyzer.parser import Parser, get_str_tree


def cli():
    import sys

    program = 'program Test; begin end.'
    print(get_result_semantic_analyzer(program))


if __name__ == "__main__":
    cli()