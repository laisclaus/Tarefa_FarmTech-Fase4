
import streamlit as st
import pandas as pd
from predict import prever_irrigacao
from Database.db_actions import get_dados_df, atualizar_previsao

st.set_page_config(page_title="FarmTech Dashboard", layout="wide")
st.title("🌾 Monitoramento Inteligente da Lavoura")

df = get_dados_df()

if df.empty:
    st.warning("Nenhum dado disponível no momento.")
else:
    st.subheader("📈 Umidade do Solo")
    st.line_chart(df.set_index('id')['umidade'])

    st.subheader("🌡️ Temperatura")
    st.line_chart(df.set_index('id')['temperatura'])

    #st.subheader("💡 Presença de Fósforo e Potássio")
    #st.bar_chart(df[['presenca_fosforo', 'presenca_potassio']].tail(10))

    # Previsão com Scikit-learn
    st.subheader("🤖 Previsão de Irrigação com IA")

    ultimo = df.iloc[0]
    umidade = ultimo['umidade']
    temperatura = ultimo['temperatura']
    ldr = (ultimo.get('presenca_fosforo', 0) or 0) + (ultimo.get('presenca_potassio', 0) or 0)

    previsao = prever_irrigacao(umidade, temperatura, ldr)

    # Atualiza o banco
    atualizar_previsao(id=ultimo['id'], previsao=float(previsao))

    if previsao:
        st.success("✅ O modelo recomenda irrigação agora.")
    else:
        st.info("💧 O modelo indica que não é necessário irrigar.")
