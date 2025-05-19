import sqlite3 as sql
import re

conn = sql.connect('agro.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dados_Lavoura (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ldr REAL,
        umidade REAL,
        temperatura REAL
    )
''')

with open('modelagem.txt', 'r') as arquivo:
    for linha in arquivo:
        partes = linha.strip().split(',')
        if len(partes) == 3:
            # Extrai o número (float) de cada parte
            ldr = float(re.search(r'[-+]?\d*\.\d+|\d+', partes[0]).group())
            umidade = float(re.search(r'[-+]?\d*\.\d+|\d+', partes[1]).group())
            temperatura = float(re.search(r'[-+]?\d*\.\d+|\d+', partes[2]).group())
            cursor.execute(
                'INSERT INTO Dados_Lavoura (ldr, umidade, temperatura) VALUES (?, ?, ?)', 
                (ldr, umidade, temperatura)
            )

for row in cursor.execute('SELECT * FROM Dados_Lavoura'):
    print(row)

conn.commit()
conn.close()

