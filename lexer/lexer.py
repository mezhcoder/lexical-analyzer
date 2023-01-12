class Lexer:
    def __init__(self):
        self.text = None
        self.pos = 0
        self.current_char = None

    def error(self):
        raise Exception(f'Invalid character at position {self.pos}')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        start_pos = self.pos
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return {'type': 'INTEGER', 'value': int(result), 'position': (start_pos, self.pos)}

    def _id(self):
        start_pos = self.pos
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        if result in ['program', 'var', 'integer', 'begin', 'end']:
            return {'type': result, 'value': result, 'position': (start_pos, self.pos)}
        else:
            return {'type': 'ID', 'value': result, 'position': (start_pos, self.pos)}

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
                return {'type': ':=', 'value': ':=', 'position': (start_pos, self.pos)}

            if self.current_char == ';':
                start_pos = self.pos
                self.advance()
                return {'type': ';', 'value': ';', 'position': (start_pos, self.pos)}

            if self.current_char == ':':
                start_pos = self.pos
                self.advance()
                return {'type': ':', 'value': ':', 'position': (start_pos, self.pos)}

            if self.current_char == ',':
                start_pos = self.pos
                self.advance()
                return {'type': ',', 'value': ',', 'position': (start_pos, self.pos)}

            if self.current_char == '+':
                start_pos = self.pos
                self.advance()
                return {'type': '+', 'value': '+', 'position': (start_pos, self.pos)}

            if self.current_char == '-':
                start_pos = self.pos
                self.advance()
                return {'type': '-', 'value': '-', 'position': (start_pos, self.pos)}

            if self.current_char == '*':
                start_pos = self.pos
                self.advance()
                return {'type': '*', 'value': '*', 'position': (start_pos, self.pos)}

            if self.current_char == '/':
                start_pos = self.pos
                self.advance()
                return {'type': '/', 'value': '/', 'position': (start_pos, self.pos)}

            if self.current_char == '(':
                start_pos = self.pos
                self.advance()
                return {'type': '(', 'value': '(', 'position': (start_pos, self.pos)}

            if self.current_char == ')':
                start_pos = self.pos
                self.advance()
                return {'type': ')', 'value': ')', 'position': (start_pos, self.pos)}

            if self.current_char == '.':
                start_pos = self.pos
                self.advance()
                return {'type': '.', 'value': '.', 'position': (start_pos, self.pos)}

            self.error()

        return {'type': 'EOF', 'value': 'EOF', 'position': (self.pos, self.pos)}

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def test_lex(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(
                f"{token['position'][0]}      "
                f"{token['position'][1]}      "
                f"{token['type']}      "
                f"{token['value']}      "
                f"{token['value']}"
            )
            if token['type'] == 'EOF':
                break
        return '\n'.join(tokens)
