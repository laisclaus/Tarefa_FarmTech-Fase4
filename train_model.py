
import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Caminho do banco
DB_PATH = 'Database/agro.db'

# Conecta e carrega os dados
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM Dados_Lavoura", conn)
conn.close()

# Cria a variável alvo: irrigar se umidade < 40
df['irrigar'] = (df['umidade'] < 40).astype(int)

# Cria proxy para LDR com fósforo + potássio
# Garante que as colunas existem
if 'presenca_fosforo' in df.columns and 'presenca_potassio' in df.columns:
    df['ldr'] = df['presenca_fosforo'].fillna(0) + df['presenca_potassio'].fillna(0)
else:
    df['ldr'] = 0  # fallback para evitar erro


# Features e target
X = df[['umidade', 'temperatura', 'ldr']]
y = df['irrigar']

# Split e treino
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Salva o modelo
joblib.dump(model, 'modelo_irrigacao.pkl')
print("✅ Modelo treinado e salvo como modelo_irrigacao.pkl")
