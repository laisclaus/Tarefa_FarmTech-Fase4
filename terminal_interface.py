from Database.db_actions import conectar, inserir_dado, consultar_dados, atualizar_umidade, remover_dado

MENU_OPTIONS = {
    "1": "Ver todos os dados",
    "2": "Inserir novo dado",
    "3": "Atualizar umidade",
    "4": "Remover dado",
    "0": "Sair"
}

def menu():
    print("\n=== Sistema de Gerenciamento de Dados da Lavoura ===")
    for key, value in MENU_OPTIONS.items():
        print(f"{key} - {value}")

def input_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Valor inválido. Digite um número.")

def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")

def ver_dados(cursor):
    dados = consultar_dados(cursor)
    print("\nID | LDR (pH) | Umidade | Temperatura")
    print("--------------------------------------")
    for row in dados:
        print(f"{row[0]:2} | {row[1]:7} | {row[2]:7.2f} | {row[3]:11.2f}")

def inserir_dado_menu(cursor, conn):
    while True:
        try:
            ldr = input_float("Digite o valor do LDR (pH): ")
            umidade = input_float("Digite o valor da umidade: ")
            temperatura = input_float("Digite o valor da temperatura: ")
            inserir_dado(cursor, conn, ldr, umidade, temperatura)
            print("Dado inserido com sucesso!")
            break
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
            print("Por favor, insira os dados novamente.\n")

def atualizar_umidade_menu(cursor, conn):
    while True:
        try:
            id = input_int("Digite o ID do registro a atualizar: ")
            nova_umidade = input_float("Digite o novo valor de umidade: ")
            if atualizar_umidade(cursor, conn, id, nova_umidade) == 0:
                print("ID não encontrado. Tente novamente.\n")
                continue
            print("Umidade atualizada com sucesso!")
            break
        except Exception as e:
            print(f"Erro ao atualizar umidade: {e}")
            print("Por favor, insira os dados novamente.\n")

def remover_dado_menu(cursor, conn):
    while True:
        try:
            id = input_int("Digite o ID do registro a remover: ")
            if remover_dado(cursor, conn, id) == 0:
                print("ID não encontrado. Tente novamente.\n")
                continue
            print("Dado removido com sucesso!")
            break
        except Exception as e:
            print(f"Erro ao remover dado: {e}")
            print("Por favor, tente novamente.\n")

def main():
    conn, cursor = conectar()
    actions = {
        "1": lambda: ver_dados(cursor),
        "2": lambda: inserir_dado_menu(cursor, conn),
        "3": lambda: atualizar_umidade_menu(cursor, conn),
        "4": lambda: remover_dado_menu(cursor, conn)
    }
    while True:
        menu()
        opcao = input("Escolha uma opção: ")
        if opcao == "0":
            break
        action = actions.get(opcao)
        if action:
            action()
        else:
            print("Opção inválida. Tente novamente.")
    conn.close()

if __name__ == "__main__":
    main()