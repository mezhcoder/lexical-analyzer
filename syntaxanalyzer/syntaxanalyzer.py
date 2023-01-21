from lexicalanalyzer.lexer import Lexer, TokenType


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception(f'Invalid syntax at position {self.current_token.position}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            print(self.current_token.type, token_type)
            self.error()

    def program(self):
        print("program")
        self.eat(TokenType.PROGRAM)
        print(" ", self.current_token.value)
        self.eat(TokenType.ID)
        self.eat(TokenType.SEMI)
        print("  declarations")
        self.declarations()
        print("  subprogram_declarations")
        self.subprogram_declarations()
        print("  compound_statement")
        self.compound_statement()
        self.eat(TokenType.DOT)

    def declarations(self):
        if self.current_token.type == TokenType.VAR:
            self.eat(TokenType.VAR)
            while self.current_token.type == TokenType.ID:
                print("   ", self.current_token.value)
                self.eat(TokenType.ID)
                self.eat(TokenType.COLON)
                print("   ", self.current_token.value)
                self.eat(TokenType.INTEGER)
                self.eat(TokenType.SEMI)

    def subprogram_declarations(self):
        pass  # Implementation left as an exercise for the reader

    def compound_statement(self):
        self.eat(TokenType.BEGIN)
        while self.current_token.type != TokenType.END:
            print("   statement")
            self.statement()
            if self.current_token.type == TokenType.SEMI:
                self.eat(TokenType.SEMI)
        self.eat(TokenType.END)


    def statement(self):
        if self.current_token.type == TokenType.ID:
            print("    ", self.current_token.value)
            self.eat(TokenType.ID)
            self.eat(TokenType.ASSIGN)
            self.expression()
        elif self.current_token.type == TokenType.BEGIN:
            self.compound_statement()
        else:
            self.error()

    def expression(self):
        print("    term")
        self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            print("    ", self.current_token.value)
            self.eat(self.current_token.type)
            self.term()

    def term(self):
        print("    factor")
        self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.FLOAT_DIV):
            print("    ", self.current_token.value)
            self.eat(self.current_token.type)
            self.factor()

    def factor(self):
        if self.current_token.type == TokenType.INTEGER:
            print("    ", self.current_token.value)
            self.eat(TokenType.INTEGER)
        elif self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            self.expression()
            self.eat(TokenType.RPAREN)
        elif self.current_token.type == TokenType.ID:
            print("    ", self.current_token.value)
            self.eat(TokenType.ID)
        else:
            self.error()

# Example usage
lexer = Lexer()
lexer.text = 'program Test; var x: integer; begin x := 2 + 3 * 4; end.'
lexer.current_char = lexer.text[lexer.pos]

parser = Parser(lexer)
parser.program()
