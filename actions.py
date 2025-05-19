import sqlite3

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
    cursor.execute('SELECT * FROM Dados_Lavoura')
    dados = cursor.fetchall()
    print("\nID | LDR (pH) | Umidade | Temperatura")
    print("--------------------------------------")
    for row in dados:
        print(f"{row[0]:2} | {row[1]:7} | {row[2]:7.2f} | {row[3]:11.2f}")

def inserir_dado(cursor, conn):
    while True:
        try:
            ldr = input_int("Digite o valor do LDR (pH): ")
            umidade = input_float("Digite o valor da umidade: ")
            temperatura = input_float("Digite o valor da temperatura: ")
            cursor.execute(
                'INSERT INTO Dados_Lavoura (ldr, umidade, temperatura) VALUES (?, ?, ?)',
                (ldr, umidade, temperatura)
            )
            conn.commit()
            print("Dado inserido com sucesso!")
            break
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
            print("Por favor, insira os dados novamente.\n")

def atualizar_umidade(cursor, conn):
    while True:
        try:
            id = input_int("Digite o ID do registro a atualizar: ")
            nova_umidade = input_float("Digite o novo valor de umidade: ")
            cursor.execute('UPDATE Dados_Lavoura SET umidade = ? WHERE id = ?', (nova_umidade, id))
            if cursor.rowcount == 0:
                print("ID não encontrado. Tente novamente.\n")
                continue
            conn.commit()
            print("Umidade atualizada com sucesso!")
            break
        except Exception as e:
            print(f"Erro ao atualizar umidade: {e}")
            print("Por favor, insira os dados novamente.\n")

def remover_dado(cursor, conn):
    while True:
        try:
            id = input_int("Digite o ID do registro a remover: ")
            cursor.execute('DELETE FROM Dados_Lavoura WHERE id = ?', (id,))
            if cursor.rowcount == 0:
                print("ID não encontrado. Tente novamente.\n")
                continue
            conn.commit()
            print("Dado removido com sucesso!")
            break
        except Exception as e:
            print(f"Erro ao remover dado: {e}")
            print("Por favor, tente novamente.\n")

def main():
    conn = sqlite3.connect('Database/agro.db')
    cursor = conn.cursor()
    actions = {
        "1": lambda: ver_dados(cursor),
        "2": lambda: inserir_dado(cursor, conn),
        "3": lambda: atualizar_umidade(cursor, conn),
        "4": lambda: remover_dado(cursor, conn)
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