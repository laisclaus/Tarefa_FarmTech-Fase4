import sqlite3
conn = sqlite3.connect('agro.db')

def limpar_tabela():
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Dados_Lavoura')
    conn.commit()
    cursor.close()
    print("Tabela limpa com sucesso.")
    
limpar_tabela()