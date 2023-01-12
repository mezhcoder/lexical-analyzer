import sys


class AST:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def fill_arr_str_tree(self, is_last=True, level=0, arr_str_tree=None):
        if level != 0:
            prefix = "    " * (level - 1) + ("└── " if is_last else "├── ")
            arr_str_tree.append(prefix + self.operator)
        else:
            arr_str_tree.append(self.operator)
        if self.left:
            self.left.fill_arr_str_tree(False, level + 1, arr_str_tree)
        if self.right:
            self.right.fill_arr_str_tree(True, level + 1, arr_str_tree)

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
            raise ValueError(f'Invalid token at position {self.index + 1}: {token}')


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


def cli():
    expression = sys.argv[1]
    tokens = lexer(expression)
    parser = Parser(tokens)
    ast = parser.parse()

    arr_str_tree = []
    ast.fill_arr_str_tree(arr_str_tree=arr_str_tree)
    print('\n'.join(arr_str_tree))


if __name__ == "__main__":
    cli()
