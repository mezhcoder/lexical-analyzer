#return f"{self.position[0]}\t{self.position[1]}\t{self.type.value}\t{self.value}\t{self.value}"
from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    INTEGER = 'INTEGER'
    ID = 'ID'
    SEMI = ';'
    COLON = ':'
    COMMA = ','
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    FLOAT_DIV = '/'
    LPAREN = '('
    RPAREN = ')'
    PROGRAM = 'program'
    VAR = 'var'
    BEGIN = 'begin'
    END = 'end'
    ASSIGN = ':='
    DOT = '.'
    PROCEDURE = 'procedure'
    FUNCTION = 'function'


@dataclass
class Token:
    type: TokenType
    value: str
    position: tuple

    def __repr__(self):
        return f"{self.position[0]}\t{self.position[1] + 1}\t{self.type.value}\t{self.value}\t{self.value}"


class Lexer:
    def __init__(self):
        self.text = None
        self.pos = 0
        self.current_char = None
        self.line_number = 1
        self.token_map = {
            ';': TokenType.SEMI,
            ':': TokenType.COLON,
            ',': TokenType.COMMA,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MUL,
            '/': TokenType.FLOAT_DIV,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            ':=': TokenType.ASSIGN,
        }

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def error(self):
        raise Exception(f'Invalid character at position {self.pos}')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace() and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.line_number += 1
            self.advance()

    def integer(self):
        start_pos = self.pos
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(type=TokenType.INTEGER, value=int(result), position=(self.line_number, start_pos))

    def _id(self):
        start_pos = self.pos
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        if result in ['program', 'var', 'integer', 'begin', 'end']:
            return Token(type=TokenType[result.upper()], value=result, position=(self.line_number, start_pos))
        else:
            return Token(type=TokenType.ID, value=result, position=(self.line_number, start_pos))

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.integer()

            if self.current_char == ':' and self.peek() == '=':
                start_pos = self.pos
                self.advance()
                self.advance()
                return Token(type=TokenType.ASSIGN, value=':=', position=(self.line_number, start_pos))

            if self.current_char in self.token_map:
                token_type = self.token_map[self.current_char]
                start_pos = self.pos
                self.advance()
                return Token(type=token_type, value=self.current_char, position=(self.line_number, start_pos))

            if self.current_char == '.':
                start_pos = self.pos
                self.advance()
                return Token(type=TokenType.DOT, value='.', position=(self.line_number, start_pos))

            self.error()

    def tokenize(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        tokens = []
        while self.current_char is not None:
            token = self.get_next_token()
            tokens.append(token)
        return tokens

