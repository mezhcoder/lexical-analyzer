from syntaxanalyzer.parser import Parser
from lexicalanalyzer.lexer import Lexer
import pandas as pd


class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}
        self.current_scope = None

    def analyze(self):
        self.visit(self.ast)
        print("Symbol Table:")
        symbol_table_df = pd.DataFrame(columns=['Type', 'Scope'])
        for var, value in self.symbol_table.items():
            symbol_table_df = pd.concat([symbol_table_df, pd.DataFrame({'Type': value['type'], 'Scope': value['scope']}, index=[var])])
        print(symbol_table_df.to_string())

    def visit(self, node):
        method_name = 'visit_' + node.type
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_program(self, node):
        self.current_scope = node.children[0].value
        self.visit(node.children[1])
        self.visit(node.children[2])
        self.visit(node.children[3])

    def visit_declarations(self, node):
        for child in node.children:
            self.visit(child)

    def visit_var_declaration(self, node):
        var_name = node.children[0].value
        var_type = node.children[1].value
        if var_name in self.symbol_table:
            raise NameError(f"Variable {var_name} already declared in scope {self.current_scope}.")
        self.symbol_table[var_name] = {'type': var_type, 'scope': self.current_scope}

    def visit_compound_statement(self, node):
        for child in node.children:
            self.visit(child)

    def visit_statement(self, node):
        self.visit(node.children[0])

    def visit_assign(self, node):
        var_name = node.children[0].value
        if var_name not in self.symbol_table:
            raise NameError(f"Variable {var_name} not declared in scope {self.current_scope}.")
        var_type = self.symbol_table[var_name]['type']
        self.visit(node.children[1])
        if var_type != 'integer':
            raise TypeError(f"Type mismatch for variable {var_name} in scope {self.current_scope}.")

    def visit_expression(self, node):
        self.visit(node.children[0])
        if len(node.children) > 1:
            self.visit(node.children[2])

    def visit_term(self, node):
        self.visit(node.children[0])
        if len(node.children) > 1:
            self.visit(node.children[2])

    def visit_factor(self, node):
        if node.children[0].type == 'ID':
            var_name = node.children[0].value
            if var_name not in self.symbol_table:
                raise NameError(f"Variable {var_name} not declared in scope {self.current_scope}.")
            self.symbol_table[var_name]['Scope'] = self.current_scope
        self.visit(node.children[0])

# Input program
program = "program Test; var x: integer; begin x := 2 + 3 * 4; end."

# Lexer
lexer = Lexer()
lexer.text = program
lexer.current_char = lexer.text[lexer.pos]

# Parser
parser = Parser(lexer)
ast = parser.program()

# Semantic Analyzer
semantic_analyzer = SemanticAnalyzer(ast=ast)
semantic_analyzer.analyze()

# Output
print("Semantic analysis complete - no errors found.")

