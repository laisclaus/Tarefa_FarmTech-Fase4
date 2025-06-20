from Database.db_actions import consultar_dados
from data_processing import carregar_dados, escalar_dados
from clustering import aplicar_kmeans

def main():
    # 1. Consultar dados do banco
    dados_brutos = consultar_dados()

    # 2. Transformar em DataFrame
    df = carregar_dados(dados_brutos)

    # 3. Escalar colunas de interesse
    colunas_para_escalar = ["umidade", "temperatura"]
    dados_escalados = escalar_dados(df, colunas_para_escalar)

    # 4. Aplicar KMeans
    labels, centros = aplicar_kmeans(dados_escalados)

    # 5. Exibir resultados (ou salvar, etc.)
    print("Labels dos clusters:", labels)
    print("Centros dos clusters:", centros)

if __name__ == "__main__":
    main()
