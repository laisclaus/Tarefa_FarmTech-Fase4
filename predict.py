
import joblib
import numpy as np

# Carrega o modelo salvo no mesmo diretório
model = joblib.load("modelo_irrigacao.pkl")

def prever_irrigacao(umidade, temperatura, ldr):
    entrada = np.array([[umidade, temperatura, ldr]])
    previsao = model.predict(entrada)
    return bool(previsao[0])
