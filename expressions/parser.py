class AST:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def print_tree(self, is_last=True, level=0):
        if level != 0:
            prefix = "    " * (level - 1) + ("└── " if is_last else "├── ")
            print(prefix + self.operator)
        else:
            print(self.operator)
        if self.left:
            self.left.print_tree(False, level + 1)
        if self.right:
            self.right.print_tree(True, level + 1)

    def __str__(self):
        return f"({self.operator} {self.left} {self.right})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        return self.expression()

    def expression(self):
        left = self.term()
        while self.index < len(self.tokens) and self.tokens[self.index] in ['+', '-']:
            operator = self.tokens[self.index]
            self.index += 1
            right = self.term()
            left = AST(operator, left, right)
        return left

    def term(self):
        left = self.factor()
        while self.index < len(self.tokens) and self.tokens[self.index] in ['*', '/']:
            operator = self.tokens[self.index]
            self.index += 1
            right = self.factor()
            left = AST(operator, left, right)
        return left

    def factor(self):
        token = self.tokens[self.index]
        if token.isnumeric():
            self.index += 1
            return AST(token, None, None)
        elif token.isalpha():
            self.index += 1
            return AST(token, None, None)
        elif token == '(':
            self.index += 1
            expression = self.expression()
            self.index += 1  # skip ')'
            return expression
        else:
            raise ValueError(f'Invalid token: {token}')


def lexer(expression):
    tokens = []
    current_token = ""
    for char in expression:
        if char in ["+", "-", "*", "/", "(", ")"]:
            if current_token:
                tokens.append(current_token)
            current_token = ""
            tokens.append(char)
        elif char.isspace():
            if current_token:
                tokens.append(current_token)
            current_token = ""
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)
    return tokens


def main():
    expression = "3 * (5 + a)"
    tokens = lexer(expression)
    parser = Parser(tokens)
    ast = parser.parse()
    ast.print_tree()


if __name__ == "__main__":
    main()
