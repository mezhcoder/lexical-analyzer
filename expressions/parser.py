class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0

    def parse(self):
        return self.expression()

    def expression(self):
        left = self.term()
        while self.tokens[self.current_token][0] in ('+', '-'):
            op = self.tokens[self.current_token][0]
            self.current_token += 1
            right = self.term()
            left = (op, left, right)
        return left

    def term(self):
        left = self.factor()
        while self.tokens[self.current_token][0] in ('*', '/'):
            op = self.tokens[self.current_token][0]
            self.current_token += 1
            right = self.factor()
            left = (op, left, right)
        return left

    def factor(self):
        if self.tokens[self.current_token][0] in ('number', 'identifier'):
            return self.tokens[self.current_token][1]
        elif self.tokens[self.current_token][0] == '(':
            self.current_token += 1
            result = self.expression()
            if self.tokens[self.current_token][0] != ')':
                raise Exception('Expected )')
            self.current_token += 1
            return result
        else:
            raise Exception(f"Unexpected token: {self.tokens[self.current_token]}")

tokens = [('number', 2), ('*', '*'), ('number', 3), ('+', '+'), ('number', 4), ('/', '/'), ('number', 5)]
parser = Parser(tokens)
print(parser.parse())
