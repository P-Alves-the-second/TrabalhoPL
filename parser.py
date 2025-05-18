import ply.yacc as yacc
from lexer import tokens
from abstract_syntax_tree import *

start = 'commands'

def p_commands_multiple(p):
    'commands : command commands'
    p[0] = [p[1]] + p[2]

def p_commands_single(p):
    'commands : command'
    p[0] = [p[1]]

def p_command_select(p):
    'command : SELECT column_list FROM ID where_opt limit_opt SEMI'
    p[0] = Select(p[2], p[4], p[5], p[6])

def p_column_list_all(p):
    'column_list : STAR'
    p[0] = ['*']

def p_column_list(p):
    'column_list : ID COMMA column_list'
    p[0] = [p[1]] + p[3]

def p_column_list_one(p):
    'column_list : ID'
    p[0] = [p[1]]

def p_where_opt(p):
    'where_opt : WHERE condition'
    p[0] = p[2]

def p_where_opt_empty(p):
    'where_opt : '
    p[0] = None

def p_limit_opt(p):
    'limit_opt : LIMIT NUMBER'
    p[0] = p[2]

def p_limit_opt_empty(p):
    'limit_opt : '
    p[0] = None

def p_condition_single(p):
    '''condition : ID EQ value
                 | ID GT value
                 | ID LT value'''
    p[0] = Condition(p[1], p[2], p[3])

def p_condition_binary(p):
    'condition : condition AND condition'
    p[0] = AndCondition(p[1], p[3])


def p_value(p):
    '''value : NUMBER
             | STRING'''
    p[0] = p[1]

def p_command_import(p):
    'command : IMPORT TABLE ID FROM STRING SEMI'
    p[0] = ImportTable(p[3], p[5])

def p_command_export(p):
    'command : EXPORT TABLE ID AS STRING SEMI'
    p[0] = ExportTable(p[3], p[5])

def p_command_create_join_paren(p):
    'command : CREATE TABLE ID FROM ID JOIN ID USING LPAREN ID RPAREN SEMI'
    p[0] = CreateTable(p[3], p[5], p[7], p[10])

def p_command_create_join(p):
    'command : CREATE TABLE ID FROM ID JOIN ID USING ID SEMI'
    p[0] = CreateTable(p[3], p[5], p[7], p[9])

def p_command_create_as_select(p):
    'command : CREATE TABLE ID SELECT column_list FROM ID where_opt limit_opt SEMI'
    select_obj = Select(p[5], p[7], p[8], p[9])
    p[0] = CreateTableAsSelect(p[3], select_obj)

def p_command_discard(p):
    'command : DISCARD TABLE ID SEMI'
    p[0] = DiscardTable(p[3])

def p_command_rename(p):
    'command : RENAME TABLE ID ID SEMI'
    p[0] = RenameTable(p[3], p[4])

def p_command_print(p):
    'command : PRINT TABLE ID SEMI'
    p[0] = PrintTable(p[3])

def p_command_procedure(p):
    'command : PROCEDURE ID DO commands END'
    p[0] = Procedure(p[2], p[4])

def p_command_call(p):
    'command : CALL ID SEMI'
    p[0] = Call(p[2])

def p_error(p):
    print("Erro de sintaxe!")

parser = yacc.yacc()
