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
            results = parser.parse(cmd, lexer=lexer)
            if results:
                for command in results:
                    execute(command)
        except KeyboardInterrupt:
            print("\nInterrupção. A sair...")
            break 
        except Exception as e:
            print("Erro:", e)

if __name__ == '__main__':
    tables['estacoes'] = load_csv("estacoes.csv")
    tables['observacoes'] = load_csv("observacoes.csv")
    repl()
