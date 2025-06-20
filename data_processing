import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def carregar_dados(dados_brutos):
    """Converte lista de tuplas em DataFrame com colunas nomeadas."""
    column_names = ["timestamp", "umidade", "temperatura", "ph", "presenca_fosforo", "presenca_potassio", "bomba_ligada"]
    return pd.DataFrame(dados_brutos, columns=column_names)

def escalar_dados(df, colunas_para_escalar):
    """Aplica MinMaxScaler nas colunas selecionadas."""
    scaler = MinMaxScaler()
    dados_escalados = scaler.fit_transform(df[colunas_para_escalar])
    return dados_escalados
