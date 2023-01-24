from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    KEYWORD = 'KEYWORD'
    ID = 'ID'
    INTEGER = 'INTEGER'
    DOUBLE = 'DOUBLE'
    CHAR = 'CHAR'
    STRING = 'STRING'
    OPERATOR = 'OPERATOR'
    SEPERATOR = 'SEPERATOR'
    COMMENT = 'COMMENT'
    EOF = 'EOF'


class Lexeme(Enum):
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
    #KEYWORD

    KEYWORD = 'KEYWORD'
    PROGRAM = 'program'
    VAR = 'var'
    BEGIN = 'begin'
    END = 'end'
    ASSIGN = ':='
    DOT = '.'
    PROCEDURE = 'procedure'
    FUNCTION = 'function'

    @classmethod
    def is_keyword(cls, value: str) -> bool:
        start_keyword = Lexeme.KEYWORD.name
        end_keyword = Lexeme.FUNCTION.name
        members = cls.__members__
        keys = list(members.keys())
        keywords = keys[keys.index(start_keyword) : keys.index(end_keyword) + 1]
        return any(
            members[e].value == value
            for e in keywords
        )


@dataclass
class Token:
    type: TokenType
    lexeme: Lexeme
    value: str
    position: tuple

    def __repr__(self):
        return f"{self.position[0]}\t{self.position[1] + 1}\t{self.type.value}\t{self.value}\t{self.value}".strip()


class Lexer:
    def __init__(self):
        self.text = None
        self.pos = 0
        self.current_char = None
        self.line_number = 1
        self.symbol_number = 0
        self.lexeme_map = {
            ';': Lexeme.SEMI,
            ':': Lexeme.COLON,
            ',': Lexeme.COMMA,
            '+': Lexeme.PLUS,
            '-': Lexeme.MINUS,
            '*': Lexeme.MUL,
            '/': Lexeme.FLOAT_DIV,
            '(': Lexeme.LPAREN,
            ')': Lexeme.RPAREN,
            ':=': Lexeme.ASSIGN,
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
        self.symbol_number += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace() and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.line_number += 1
            self.symbol_number = -1
            self.advance()

    def integer(self):
        start_pos = self.symbol_number
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(type=TokenType.INTEGER,
                     lexeme=Lexeme.INTEGER,
                     value=int(result),
                     position=(self.line_number, start_pos))

    def _id(self):
        start_pos = self.symbol_number
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        if Lexeme.is_keyword(result):
            return Token(type=TokenType.KEYWORD, lexeme=Lexeme(result), value=result, position=(self.line_number, start_pos))
        else:
            return Token(type=TokenType.ID, lexeme=Lexeme.ID, value=result, position=(self.line_number, start_pos))

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
                start_pos = self.symbol_number
                self.advance()
                self.advance()
                return Token(type=TokenType.OPERATOR, lexeme=Lexeme.ASSIGN, value=':=', position=(self.line_number, start_pos))

            if self.current_char in self.lexeme_map:
                lexeme_type = self.lexeme_map[self.current_char]
                start_pos = self.symbol_number
                self.advance()
                return Token(type=TokenType.OPERATOR, lexeme=lexeme_type, value=lexeme_type.value, position=(self.line_number, start_pos))

            if self.current_char == '.':
                start_pos = self.symbol_number
                self.advance()
                return Token(type=TokenType.OPERATOR, lexeme=Lexeme.DOT, value='.', position=(self.line_number, start_pos))

            self.error()

    def tokenize(self, text):
        self.text = text
        self.pos = 0
        self.symbol_number = 0
        self.current_char = self.text[self.pos] if self.text else None
        tokens = []
        while self.current_char is not None:
            token = self.get_next_token()
            tokens.append(token)
        return tokens
