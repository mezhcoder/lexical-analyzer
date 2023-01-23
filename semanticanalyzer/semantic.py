from syntaxanalyzer.parser import Parser, get_str_tree
from lexicalanalyzer.lexer import Lexer
from tabulate import tabulate
import pandas as pd


class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}
        self.current_scope = None
        self.type_table = {}
        self.current_expression_type = None

    def analyze(self):
        self.visit(self.ast)
        result_analyze = ""
        result_analyze += "Symbol Table\n"
        symbol_table_df = pd.DataFrame(columns=['Type', 'Scope'])
        for var, value in self.symbol_table.items():
            symbol_table_df = pd.concat(
                [symbol_table_df, pd.DataFrame({'Type': value['type'], 'Scope': value['scope']}, index=[var])])
        result_analyze += tabulate(symbol_table_df, headers='keys', tablefmt='pipe', showindex=False)
        result_analyze += "\n"
        result_analyze += "Type Table\n"
        type_table_df = pd.DataFrame.from_dict(self.type_table, orient='index', columns=['Type'])
        result_analyze += tabulate(type_table_df, headers='keys', tablefmt='pipe', showindex=True)
        return result_analyze

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
        if var_type not in self.type_table:
            self.type_table[var_type] = []
        self.type_table[var_type].append(var_name)

    def visit_compound_statement(self, node):
        for child in node.children:
            self.visit(child)

    def visit_statement(self, node):
        self.visit(node.children[0])

    def visit_assign(self, node):
        var_name = node.children[0].value
        if var_name not in self.symbol_table:
            raise NameError(f"Variable {var_name} not declared in scope {self.current_scope}.")
        self.visit(node.children[1])
        var_type = self.symbol_table[var_name]['type']
        if var_type != self.current_expression_type and self.current_expression_type is not None:
            raise TypeError(
                f"Type mismatch for variable {var_name} in scope {self.current_scope}. Expected {var_type} but got {self.current_expression_type}.")
        self.current_expression_type = None

    def visit_expression(self, node):
        self.visit(node.children[0])
        if len(node.children) > 1:
            self.visit(node.children[1])
            self.visit(node.children[2])
            if self.current_expression_type != 'integer':
                raise TypeError(f"Expression type must be integer but got {self.current_expression_type}")

    def visit_term(self, node):
        self.visit(node.children[0])
        if len(node.children) > 1:
            self.visit(node.children[1])
            self.visit(node.children[2])
            if self.current_expression_type != 'integer':
                raise TypeError(f"Term type must be integer but got {self.current_expression_type}")

    def visit_factor(self, node):
        if node.children[0].type == 'ID':
            var_name = node.children[0].value
            if var_name in self.symbol_table:
                self.current_expression_type = self.symbol_table[var_name]['type']
            else:
                raise NameError(f"Variable {var_name} not declared in scope {self.current_scope}.")
        elif node.children[0].type == 'NUM':
            self.current_expression_type = 'integer'


    def visit_type(self, node):
        self.current_expression_type = node.value


def get_result_semantic_analyzer(program : str):
    result_semantic_analyzer = ''
    # Lexer
    lexer = Lexer()
    lexer.text = program
    lexer.current_char = lexer.text[lexer.pos]

    # Parser
    parser = Parser(lexer)
    ast = parser.program()

    ast_result = get_str_tree(ast.to_dict())
    result_semantic_analyzer += ast_result
    result_semantic_analyzer += '\n'

    semantic_analyzer = SemanticAnalyzer(ast=ast)
    result_semantic_analyzer += semantic_analyzer.analyze()
    return result_semantic_analyzer

