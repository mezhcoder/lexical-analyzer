from anytree import Node as AnyNode, RenderTree
from lexicalanalyzer.lexer import TokenType, Lexer


class Node:
    def __init__(self, type_, value=None, children=None):
        self.type = type_
        self.value = value
        self.children = children or []

    def to_dict(self):
        children = []
        for child in self.children:
            if child is not None:
                children.append(child.to_dict())
        return {'type': self.type, 'value': self.value, 'children': children}


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.root = None

    def error(self):
        raise Exception(f'Invalid syntax at position {self.current_token.position}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        program_node = Node('program')
        self.eat(TokenType.PROGRAM)
        program_node.children.append(Node('ID', self.current_token.value))
        self.eat(TokenType.ID)
        self.eat(TokenType.SEMI)
        program_node.children.append(self.declarations())
        program_node.children.append(self.subprogram_declarations())
        program_node.children.append(self.compound_statement())
        self.eat(TokenType.DOT)
        self.root = program_node
        return program_node

    def declarations(self):
        declarations_node = Node('declarations')
        if self.current_token.type == TokenType.VAR:
            self.eat(TokenType.VAR)
            while self.current_token.type == TokenType.ID:
                var_declaration_node = Node('var_declaration')
                var_declaration_node.children.append(Node('ID', self.current_token.value))
                self.eat(TokenType.ID)
                self.eat(TokenType.COLON)
                var_declaration_node.children.append(Node('TYPE', self.current_token.value))
                self.eat(TokenType.INTEGER)
                self.eat(TokenType.SEMI)
                declarations_node.children.append(var_declaration_node)
        return declarations_node

    def subprogram_declarations(self):
        pass

    def compound_statement(self):
        compound_statement_node = Node('compound_statement')
        self.eat(TokenType.BEGIN)
        while self.current_token.type != TokenType.END:
            compound_statement_node.children.append(self.statement())
            if self.current_token.type == TokenType.SEMI:
                self.eat(TokenType.SEMI)
        self.eat(TokenType.END)
        return compound_statement_node

    def statement(self):
        statement_node = Node('statement')
        if self.current_token.type == TokenType.ID:
            assign_node = Node('assign')
            assign_node.children.append(Node('ID', self.current_token.value))
            self.eat(TokenType.ID)
            self.eat(TokenType.ASSIGN)
            assign_node.children.append(self.expression())
            statement_node.children.append(assign_node)
        elif self.current_token.type == TokenType.BEGIN:
            statement_node.children.append(self.compound_statement())
        else:
            self.error()
        return statement_node

    def expression(self):
        node = Node('Expression')
        node.children.append(self.term())
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = Node(self.current_token.value)
            self.eat(self.current_token.type)
            node.children.append(op)
            node.children.append(self.term())
        return node

    def term(self):
        node = Node('Term')
        node.children.append(self.factor())
        while self.current_token.type in (TokenType.MUL, TokenType.FLOAT_DIV):
            op = Node(self.current_token.value)
            self.eat(self.current_token.type)
            node.children.append(op)
            node.children.append(self.factor())
        return node

    def factor(self):
        if self.current_token.type == TokenType.INTEGER:
            node = Node('INTEGER', self.current_token.value)
            self.eat(TokenType.INTEGER)
        elif self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
        elif self.current_token.type == TokenType.ID:
            node = Node('ID', self.current_token.value)
            self.eat(TokenType.ID)
        else:
            self.error()
        return node


def get_str_tree(program_data):
    def build_tree(data, parent=None):
        if data is None:
            return
        node = AnyNode(data['type'], parent=parent, value=data.get('value'))
        for child in data.get('children', []):
            build_tree(child, parent=node)
        return node

    root = build_tree(program_data)
    result = ""
    for pre, fill, node in RenderTree(root):
        result += ("%s%s" % (pre, node.name)) + "\n"
    return result.strip()


def cli():
    import sys

    lexer = Lexer()
    lexer.text = sys.argv[1]
    lexer.current_char = lexer.text[lexer.pos]

    parser = Parser(lexer)
    result = get_str_tree(parser.program().to_dict())
    print(result)


if __name__ == "__main__":
    cli()
