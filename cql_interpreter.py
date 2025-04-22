import ply.lex as lex
import ply.yacc as yacc
import csv

# Definição do Lexer
class CQLLexer:
    def __init__(self):
        self.tokens = [
            'SELECT', 'FROM', 'WHERE', 'LIMIT', 'STAR', 'COMMA', 'ID', 'STRING', 'NUMBER', 'EQUAL', 'NOTEQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL'
        ]
        self.t_SELECT = r'SELECT'
        self.t_FROM = r'FROM'
        self.t_WHERE = r'WHERE'
        self.t_LIMIT = r'LIMIT'
        self.t_STAR = r'\*'
        self.t_COMMA = r','
        self.t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
        self.t_STRING = r'"([^"\\]|\\.)*"'
        self.t_NUMBER = r'\d+(\.\d*)?'
        self.t_EQUAL = r'='
        self.t_NOTEQUAL = r'<>'
        self.t_GREATER = r'>'
        self.t_LESS = r'<'
        self.t_GREATER_EQUAL = r'>='
        self.t_LESS_EQUAL = r'<='

    def t_error(self, t):
        print(f"Invalid character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self):
        return lex.lex(module=self)

# Definição do Parser
class CQLParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self)

    def p_statement_select(self, p):
        '''statement : SELECT columns FROM ID WHERE condition'''
        print(f"SELECT {p[2]} FROM {p[4]} WHERE {p[6]}")

    def p_columns(self, p):
        '''columns : STAR
                   | column_list'''
        p[0] = p[1]

    def p_column_list(self, p):
        '''column_list : ID
                       | column_list COMMA ID'''
        p[0] = p[1] if len(p) == 2 else p[1] + ', ' + p[3]

    def p_condition(self, p):
        '''condition : ID EQUAL value
                     | ID NOTEQUAL value
                     | ID GREATER value
                     | ID LESS value
                     | ID GREATER_EQUAL value
                     | ID LESS_EQUAL value'''
        p[0] = f"{p[1]} {p[2]} {p[3]}"

    def p_value(self, p):
        '''value : STRING
                 | NUMBER'''
        p[0] = p[1]

    def p_error(self, p):
        print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOF")

    def parse(self, data):
        return self.parser.parse(data)

# Função para executar comandos CQL
def execute(command):
    lexer = CQLLexer().build()
    parser = CQLParser(lexer)
    parser.parse(command)

if __name__ == "__main__":
    # Testar o código com um comando de exemplo
    execute('SELECT * FROM estacoes WHERE Local = "Olhao, EPPO"')
