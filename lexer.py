import ply.lex as lex

# Palavras-Chave

keywords = {
    'import': 'IMPORT',
    'table': 'TABLE',
    'from': 'FROM',
    'select': 'SELECT',
    'where': 'WHERE',
    'limit': 'LIMIT',
    'export': 'EXPORT',
    'create': 'CREATE',
    'as': 'AS',
    'join': 'JOIN',
    'procedure': 'PROCEDURE',
    'do': 'DO',
    'end': 'END',
    'call': 'CALL',
    'using': 'USING',        
    'discard': 'DISCARD',    
    'rename': 'RENAME',      
    'print': 'PRINT'
}

# Tokens
tokens = list(keywords.values()) + [
    'ID', 'NUMBER', 'STRING',
    'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE',
    'COMMA', 'SEMI', 'STAR'
]

# Regras
t_EQ = r'='
t_NEQ = r'<>'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_COMMA = r','
t_SEMI = r';'
t_STAR = r'\*'
t_ignore = ' \t'


def t_COMMENT(t):
    r'--.*'
    pass

def t_BLOCK_COMMENT(t):
    r'{-[\s\S]*?-}'
    pass

def t_STRING(t):
    r'"([^\\"]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = keywords.get(t.value.lower(), 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()