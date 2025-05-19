import sqlite3

def conectar():
    conn = sqlite3.connect('Database/agro.db')
    return conn, conn.cursor()

def inserir_dado(cursor, conn, ldr, umidade, temperatura):
    cursor.execute(
        'INSERT INTO Dados_Lavoura (ldr, umidade, temperatura) VALUES (?, ?, ?)',
        (ldr, umidade, temperatura)
    )
    conn.commit()

def consultar_dados(cursor):
    cursor.execute('SELECT * FROM Dados_Lavoura')
    return cursor.fetchall()

def atualizar_umidade(cursor, conn, id, nova_umidade):
    cursor.execute('UPDATE Dados_Lavoura SET umidade = ? WHERE id = ?', (nova_umidade, id))
    conn.commit()
    return cursor.rowcount

def remover_dado(cursor, conn, id):
    cursor.execute('DELETE FROM Dados_Lavoura WHERE id = ?', (id,))
    conn.commit()
    return cursor.rowcount
