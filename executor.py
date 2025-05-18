from csv_utils import *
from parser import *

tables = {}
procedures = {} 

def eval_condition(row, cond):
    val = row[cond.column]
    if isinstance(cond.value, (int, float)):
        try:
            val = float(val)
        except ValueError:
            pass 
    if cond.operator == '=':
        return val == cond.value
    if cond.operator == '>':
        return val > cond.value
    if cond.operator == '<':
        return val < cond.value
    return False

def join_tables(table1, table2, column):
    result = []
    for row1 in table1:
        for row2 in table2:
            if row1[column] == row2[column]:
                joined_row = {**row1, **row2}
                result.append(joined_row)
    return result

def execute(cmd):
    if isinstance(cmd, Select):
        if cmd.table not in tables:
            print(f"Tabela '{cmd.table}' não encontrada.")
            return
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
        tables[cmd.table_name] = load_csv(cmd.file_path)
        print(f"Tabela {cmd.table_name} importada de {cmd.file_path}")

    elif isinstance(cmd, ExportTable):
        if cmd.table_name not in tables:
            print(f"Tabela '{cmd.table_name}' não encontrada.")
            return
        save_csv(cmd.file_path, tables[cmd.table_name])
        print(f"Tabela {cmd.table_name} exportada para {cmd.file_path}")

    elif isinstance(cmd, CreateTable):
        if cmd.table_1 not in tables or cmd.table_2 not in tables:
            print("Tabela(s) para junção não encontrada(s).")
            return
        table1 = tables[cmd.table_1]
        table2 = tables[cmd.table_2]
        joined_table = join_tables(table1, table2, cmd.column)
        tables[cmd.new_table] = joined_table
        print(f"Tabela {cmd.new_table} criada a partir de {cmd.table_1} e {cmd.table_2}")

    elif cmd.__class__.__name__ == "CreateTableAsSelect":
        result_rows = []
        select_cmd = cmd.select_query
        if select_cmd.table not in tables:
            print(f"Tabela '{select_cmd.table}' não encontrada.")
            return
        rows = tables[select_cmd.table]
        if select_cmd.where:
            rows = [r for r in rows if eval_condition(r, select_cmd.where)]
        if select_cmd.columns != ['*']:
            rows = [{c: r[c] for c in select_cmd.columns} for r in rows]
        if select_cmd.limit:
            rows = rows[:select_cmd.limit]
        result_rows = rows
        tables[cmd.new_table] = result_rows
        print(f"Tabela '{cmd.new_table}' criada com sucesso a partir da consulta SELECT.")

    elif isinstance(cmd, DiscardTable):
        if cmd.table_name in tables:
            del tables[cmd.table_name]
            print(f"Tabela {cmd.table_name} descartada.")
        else:
            print(f"Tabela {cmd.table_name} não encontrada.")

    elif isinstance(cmd, RenameTable):
        if cmd.old_name in tables:
            tables[cmd.new_name] = tables.pop(cmd.old_name)
            print(f"Tabela {cmd.old_name} renomeada para {cmd.new_name}.")
        else:
            print(f"Tabela {cmd.old_name} não encontrada.")

    elif isinstance(cmd, PrintTable):
        if cmd.table_name in tables:
            for row in tables[cmd.table_name]:
                print(row)
        else:
            print(f"Tabela {cmd.table_name} não encontrada.")

    elif isinstance(cmd, Procedure):
        procedures[cmd.name] = cmd.commands
        print(f"Procedimento '{cmd.name}' armazenado com {len(cmd.commands)} comando(s).")

    elif isinstance(cmd, Call):
        if cmd.name not in procedures:
            print(f"Erro: procedimento '{cmd.name}' não encontrado.")
            return
        for sub_cmd in procedures[cmd.name]:
            execute(sub_cmd)

    else:
        print("Comando desconhecido.")

