#!pip install paho-mqtt
import pandas as pd
import sqlite3
from datetime import datetime
import os

# O caminho para o banco de dados.
DB_PATH = 'Database/agro.db'

def criar_tabela():
    """
    Cria a tabela 'Dados_Lavoura' com a estrutura da Fase 4, se ela não existir.
    """
    conn = None
    try:
        # Garante que a pasta 'Database' exista
        if not os.path.exists('Database'):
            os.makedirs('Database')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dados_Lavoura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            umidade REAL NOT NULL,
            temperatura REAL NOT NULL,
            ph REAL,
            presenca_fosforo INTEGER,
            presenca_potassio INTEGER,
            bomba_ligada INTEGER,
            previsao_irrigar REAL
        );
        ''')
        
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela: {e}")
    finally:
        if conn:
            conn.close()

def inserir_dados(umidade, temperatura, ph, presenca_fosforo, presenca_potassio, bomba_ligada):
    """
    Insere um novo registro completo na tabela, com todos os dados vindos do ESP32.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        timestamp_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute(
            '''
            INSERT INTO Dados_Lavoura 
            (timestamp, umidade, temperatura, ph, presenca_fosforo, presenca_potassio, bomba_ligada) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (timestamp_atual, umidade, temperatura, ph, int(presenca_fosforo), int(presenca_potassio), int(bomba_ligada))
        )
        conn.commit()
        return cursor.lastrowid
        
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")
        return None
    finally:
        if conn:
            conn.close()

def consultar_dados():
    """Consulta e retorna todos os dados da lavoura."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Dados_Lavoura ORDER BY id DESC')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar dados: {e}")
        return []
    finally:
        if conn:
            conn.close()



def get_dados_df():
    """Retorna os dados da lavoura como DataFrame ordenado."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM Dados_Lavoura ORDER BY id DESC", conn)
        return df
    except sqlite3.Error as e:
        print(f"Erro ao ler dados como DataFrame: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()


            
def atualizar_previsao(id, previsao):
    """
    Atualiza um registro existente com a probabilidade de irrigação gerada pelo modelo de ML.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE Dados_Lavoura SET previsao_irrigar = ? WHERE id = ?', (previsao, id))
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"Erro ao atualizar previsão: {e}")
        return 0
    finally:
        if conn:
            conn.close()
