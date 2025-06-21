# Projeto FarmTech Solutions - Fase 4
# 1. Introdução

O projeto FarmTech Solutions - Fase 4 representa a evolução de um sistema de agricultura de precisão, elevando o monitoramento e automação da irrigação a um novo patamar. Esta fase integra hardware simulado, armazenamento de dados em nuvem, visualização interativa e, crucialmente, inteligência artificial. A solução utiliza um microcontrolador ESP32 para coletar dados de umidade do solo, que são enviados para um banco de dados remoto. Uma aplicação em Python, construída com Streamlit, não apenas exibe esses dados em tempo real e históricos, mas também emprega um modelo de Machine Learning (Scikit-learn) para prever a necessidade futura de irrigação, oferecendo uma ferramenta poderosa e inteligente para a gestão agrícola.

# 2. Objetivo

O objetivo principal do projeto é desenvolver um sistema de irrigação inteligente e automatizado que:

Monitore continuamente a umidade do solo usando um sensor conectado a um ESP32.
Exiba os dados críticos (umidade e status da irrigação) localmente em um display LCD.
Armazene de forma persistente todo o histórico de leituras em um banco de dados SQL.
Preveja a necessidade de irrigação futura com base nos dados históricos, utilizando um modelo de classificação treinado com Scikit-learn.
Apresente todas as informações em um dashboard web interativo e de fácil compreensão, permitindo a visualização de dados em tempo real, análises históricas e insights preditivos.

# 3. Componentes da Solução

A solução é composta por uma combinação de hardware (simulado), software e serviços em nuvem:

Hardware (Simulado no Wokwi):

Microcontrolador ESP32 DevKit V1
Sensor de Umidade do Solo Capacitivo
Display LCD 16x2 com interface I2C
LED (para simular a ativação da bomba de água/válvula solenoide)
Resistor
Software e Plataformas:

Wokwi: Plataforma online para simulação do circuito eletrônico e do ESP32.
Arduino IDE / C++: Para a programação do firmware do ESP32.
Python: Linguagem principal para o backend e o dashboard.
Streamlit: Biblioteca Python para a criação do dashboard web interativo.
Scikit-learn: Biblioteca Python para a implementação do modelo de Machine Learning preditivo.
Pandas: Para manipulação e análise dos dados.
MySQL: Sistema de gerenciamento de banco de dados para armazenar os dados dos sensores.

# 4. Arquitetura da Solução

A arquitetura do projeto segue um fluxo de dados lógico e distribuído:

Coleta de Dados: O Sensor de Umidade do Solo lê o nível de umidade e envia o valor analógico para o ESP32.
Processamento Local: O ESP32 processa o valor bruto, converte-o para uma porcentagem, exibe no Display LCD e decide, com base em um limiar, se a irrigação (LED) deve ser ativada.
Comunicação e Armazenamento: O ESP32 conecta-se à rede Wi-Fi e envia os dados de umidade e o status da irrigação, via requisição HTTP POST, para uma API que os insere no Banco de Dados MySQL.
Análise e Predição: A Aplicação Python/Streamlit conecta-se ao Banco de Dados MySQL para buscar os dados.
Visualização: O Dashboard Streamlit exibe os dados mais recentes em métricas, plota gráficos históricos da umidade e utiliza um modelo pré-treinado do Scikit-learn para prever a necessidade de irrigação, mostrando a sugestão na interface do usuário.

# 5. Circuitos e Montagem

O circuito é projetado para ser simples e funcional, interligando o sensor e os atuadores ao ESP32.

Sensor de Umidade do Solo: O pino de sinal (A0) é conectado a uma porta analógica do ESP32 (como GPIO34) para leitura dos níveis de umidade.
Display LCD I2C: É conectado utilizando os pinos de comunicação I2C do ESP32.
SDA do LCD -> GPIO21 do ESP32
SCL do LCD -> GPIO22 do ESP32
LED (Simulador de Irrigação): O anodo do LED é conectado a uma porta digital do ESP32 (como GPIO12) através de um resistor, e o catodo ao GND.

# 6. Montagem do Circuito no Wokwi
A montagem no simulador Wokwi replica o circuito físico, permitindo o desenvolvimento e teste do firmware sem a necessidade do hardware real. As conexões seguem a descrição acima, arrastando os componentes para a área de trabalho e ligando os pinos virtuais.

   # 6.1 Lógica de Funcionamento
   O sistema opera em um ciclo contínuo:
  
   Inicialização: O ESP32 é ligado, inicializa a comunicação serial, conecta-se à rede Wi-Fi configurada e inicializa o display LCD.
   Leitura do Sensor: A cada iteração do loop principal, o ESP32 realiza uma leitura analógica da porta onde o sensor de umidade está conectado.
   Conversão de Dados: O valor bruto lido (0-4095) é mapeado para uma escala percentual (0-100%) para facilitar a interpretação.
   Atuação e Display:
   A umidade e o status da irrigação são exibidos no LCD.
   Se a umidade estiver abaixo de um limiar pré-definido (ex: 60%), o ESP32 ativa o pino do LED (simulando o início da irrigação) e define o status como "ON". Caso contrário o    LED é desligado e o status é "OFF".
   Envio de Dados: O ESP32 formata os dados (umidade e status) em uma string e os envia via HTTP POST para a API responsável por persistir as informações no banco de dados.
   Intervalo: O sistema aguarda um tempo determinado (delay) antes de iniciar o próximo ciclo de leitura.

   # 6.2 Imagem do funcionamento do Wokwi
   ![image](https://github.com/user-attachments/assets/6ddc289d-d22d-487a-835c-3b0a01a168a6)

   # Link de acesso ao Wokwi: 
   https://wokwi.com/projects/434117279482199041
   
# 7. Código do ESP32
O firmware (.ino) desenvolvido em C/C++ para o ESP32 é responsável por toda a lógica embarcada. Suas principais seções são:

Inclusão de Bibliotecas: WiFi.h para conectividade de rede, HTTPClient.h para realizar requisições web, e LiquidCrystal_I2C.h para controlar o display.
Configurações: Definição dos pinos do sensor e do LED, além das credenciais de Wi-Fi e do endereço do servidor/API.
setup(): Função que executa uma única vez para inicializar os componentes (Serial, WiFi, LCD).
loop(): Função principal que executa em ciclo contínuo, implementando a "Lógica de Funcionamento" descrita no item anterior. Contém a lógica para ler, processar, exibir e enviar os dados.

# 8. Armazenamento dos Dados em Banco de Dados SQL
Os dados coletados são armazenados em um banco de dados MySQL chamado farmtech. A estrutura é definida pelo script Script_Banco.sql e contém uma tabela principal:

Tabela sensor_data:
id: INT, Chave Primária, Auto Incremento.
umidade: FLOAT, armazena o valor percentual da umidade do solo.
status_irrigacao: VARCHAR, armazena o estado da irrigação ("ON" ou "OFF").
data_hora: TIMESTAMP, registra o momento exato da leitura, com o valor padrão sendo a data e hora atuais.
Esta tabela serve como fonte de dados única tanto para a exibição de informações em tempo real quanto para o treinamento e uso do modelo de Machine Learning.

# 9. Python
O código em Python (Dashboard_Python/app.py) é o cérebro da interface com o usuário.

Streamlit: É a base para construir a página web. Comandos como st.title, st.metric, st.line_chart e st.info são usados para criar uma interface rica e interativa.
MySQL Connector/Pandas: O script se conecta ao banco de dados MySQL, executa uma query para buscar todos os dados da tabela sensor_data e os carrega em um DataFrame do Pandas.
Joblib/Scikit-learn: A biblioteca joblib é usada para carregar o modelo de Machine Learning (modelo_irrigacao.pkl) que foi previamente treinado. O script pega o dado mais recente de umidade, o alimenta no modelo (model.predict()) e exibe a predição resultante (se deve ou não irrigar) no dashboard.

# 10. Instruções de como rodar o Projeto
Para executar a solução completa, siga os passos abaixo:

Pré-requisitos:

Instale um servidor MySQL (XAMPP, WampServer ou Docker).
Instale o Python 3.8 ou superior.
Instale o Arduino IDE com o suporte para a placa ESP32 configurado.
Configuração do Banco de Dados:

Inicie o serviço MySQL.
Use um cliente de banco de dados (como HeidiSQL ou DBeaver) para criar um novo banco de dados chamado farmtech.
Execute o conteúdo do arquivo BancoDeDados/Script_Banco.sql para criar a tabela sensor_data.
Configuração do Firmware do ESP32:

Abra o arquivo Codigo_ESP32/Codigo_ESP32.ino no Arduino IDE.
Altere as variáveis ssid, password com as credenciais da sua rede Wi-Fi.
Nota: O código atual envia dados para um endpoint web. Você precisará de uma API intermediária para receber o POST do ESP32 e inserir no banco de dados.
Compile e envie o código para sua placa ESP32 ou inicie a simulação no Wokwi.
Execução do Dashboard Python:

Navegue até a pasta Dashboard_Python via terminal.
Instale as dependências: pip install -r requirements.txt.
Abra o arquivo app.py em um editor de texto e atualize os detalhes da conexão com o banco de dados na função get_db_connection (host, user, password, database).
Execute o dashboard com o comando: streamlit run app.py.
Visualização:

Abra o seu navegador web e acesse o endereço fornecido pelo Streamlit (geralmente http://localhost:8501).
Observe os dados sendo atualizados no dashboard conforme o ESP32 envia novas leituras.
