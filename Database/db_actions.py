# def inserir_dado(ldr, umidade, temperatura):
#     cursor.execute(
#         'INSERT INTO Dados_Lavoura (ldr, umidade, temperatura) VALUES (?, ?, ?)',
#         (ldr, umidade, temperatura)
#     )
#     conn.commit()

# def consultar_dados():
#     cursor.execute('SELECT * FROM Dados_Lavoura')
#     for row in cursor.fetchall():
#         print(row)

# def atualizar_umidade(id, nova_umidade):
#     cursor.execute('UPDATE Dados_Lavoura SET umidade = ? WHERE id = ?', (nova_umidade, id))
#     conn.commit()

# def remover_dado(id):
#     cursor.execute('DELETE FROM Dados_Lavoura WHERE id = ?', (id,))
#     conn.commit()
