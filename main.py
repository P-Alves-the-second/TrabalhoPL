import sys
from lexer import lexer
from parser import parser
from executor import execute, tables
from csv_utils import load_csv

def process_commands(text):
    results = parser.parse(text, lexer=lexer)
    if results:
        for command in results:
            execute(command)

def repl():
    while True:
        try:
            cmd = input('cql> ')
            if cmd.strip().lower() == 'exit':
                break
            process_commands(cmd)
        except KeyboardInterrupt:
            print("\nInterrupção pelo utilizador. A sair...")
            break
        except Exception as e:
            print("Erro:", e)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                print(f"\nA processar comandos de '{file_path}'\n")
                process_commands(file_content)
        except FileNotFoundError:
            print(f"Erro: Ficheiro '{file_path}' não encontrado.")
        except Exception as e:
            print(f"Erro ao processar o ficheiro: {e}")
    else:
        repl()
