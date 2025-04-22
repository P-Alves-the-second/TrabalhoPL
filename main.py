from lexer import lexer
from parser import parser
from executor import execute, tables
from csv_utils import load_csv

def repl():
    while True:
        try:
            cmd = input('cql> ')
            if cmd.strip().lower() == 'exit':
                break
            result = parser.parse(cmd, lexer=lexer)
            if result:
                execute(result)
        except Exception as e:
            print("Erro:", e)

if __name__ == '__main__':
    # Exemplo: importar manualmente uma tabela antes do SELECT
    tables['observacoes'] = load_csv("estacoes.csv")
    repl()
