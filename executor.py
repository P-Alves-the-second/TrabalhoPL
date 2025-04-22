from csv_utils import *
from parser import *

tables = {}

def execute(cmd):
    if isinstance(cmd, Select):
        rows = tables[cmd.table]
        if cmd.where:
            rows = [r for r in rows if eval_condition(r, cmd.where)]
        if cmd.columns != ['*']:
            rows = [{c: r[c] for c in cmd.columns} for r in rows]
        if cmd.limit:
            rows = rows[:cmd.limit]
        for r in rows:
            print(r)

    elif isinstance(cmd, ImportTable):
        # Carregar o arquivo CSV para a tabela na memória
        tables[cmd.table_name] = load_csv(cmd.file_path)
        print(f"Tabela {cmd.table_name} importada de {cmd.file_path}")
    
    elif isinstance(cmd, ExportTable):
        # Exportar a tabela para um arquivo CSV
        save_csv(cmd.file_path, tables[cmd.table_name])
        print(f"Tabela {cmd.table_name} exportada para {cmd.file_path}")
    
    elif isinstance(cmd, CreateTable):
        # Criar uma nova tabela com uma junção
        table1 = tables[cmd.table_1]
        table2 = tables[cmd.table_2]
        joined_table = join_tables(table1, table2, cmd.column)
        tables[cmd.new_table] = joined_table
        print(f"Tabela {cmd.new_table} criada a partir de {cmd.table_1} e {cmd.table_2}")
    
    elif isinstance(cmd, DiscardTable):
        # Eliminar a tabela
        if cmd.table_name in tables:
            del tables[cmd.table_name]
            print(f"Tabela {cmd.table_name} descartada.")
        else:
            print(f"Tabela {cmd.table_name} não encontrada.")
    
    elif isinstance(cmd, RenameTable):
        # Renomear a tabela
        if cmd.old_name in tables:
            tables[cmd.new_name] = tables.pop(cmd.old_name)
            print(f"Tabela {cmd.old_name} renomeada para {cmd.new_name}.")
        else:
            print(f"Tabela {cmd.old_name} não encontrada.")
    
    elif isinstance(cmd, PrintTable):
        # Imprimir a tabela
        if cmd.table_name in tables:
            for row in tables[cmd.table_name]:
                print(row)

def eval_condition(row, cond):
    val = row[cond.column]
    if isinstance(cond.value, (int, float)):
        val = float(val)
    if cond.operator == '=': return val == cond.value
    if cond.operator == '>': return val > cond.value
    if cond.operator == '<': return val < cond.value

    
def join_tables(table1, table2, column):
    # Função simples para fazer o join das tabelas
    result = []
    for row1 in table1:
        for row2 in table2:
            if row1[column] == row2[column]:
                joined_row = {**row1, **row2}
                result.append(joined_row)
    return result

def eval_condition(row, cond):
    val = row[cond.column]
    if isinstance(cond.value, (int, float)):
        val = float(val)
    if cond.operator == '=': return val == cond.value
    if cond.operator == '>': return val > cond.value
    if cond.operator == '<': return val < cond.value
