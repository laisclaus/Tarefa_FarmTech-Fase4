#include <DHT.h>
#include <math.h>

#define ldrPin 34 // pino do Sensor LDR
#define pinoDHT 23 // pino do Sensor DHT22
#define modelo DHT22 // modelo do sensor DHT
#define relePin 12 // pino do relé
#define ledPhosphorus 13 // pino do LED de Fósforo
#define ledPosttasium 21 // pino do LED de Potássio

DHT dht(pinoDHT, modelo);

// Função principal que executa a lógica de irrigação e simulação de sensores
void setup() {
    pinMode(relePin, OUTPUT); // Configura o pino do relé como saída
    pinMode(ledPhosphorus, OUTPUT); // Configura o pino do LED de Fósforo como saída
    pinMode(ledPosttasium, OUTPUT); // Configura o pino do LED de Potássio como saída

    Serial.begin(9600); // Inicializa a comunicação serial
    dht.begin(); // Inicializa o sensor DHT22
}

void loop() {
    // Simular presença de Fósforo e Potássio alternando entre true/false
    bool simularFosforo = millis() % 4000 < 2000;   // alterna a cada 2 segundos
    bool simularPotassio = millis() % 6000 < 3000;  // alterna a cada 3 segundos

    digitalWrite(ledPhosphorus, simularFosforo ? HIGH : LOW); // Liga/Desliga o LED de Fósforo
    digitalWrite(ledPosttasium, simularPotassio ? HIGH : LOW); // Liga/Desliga o LED de Potássio

    // Simular valor de pH variando suavemente entre 5.0 e 9.0
    float ldrValue = 7.0 + 2.0 * sin(millis() / 2000.0);  // Varia entre 5.0 e 9.0

    // Ler umidade e temperatura do DHT22
    float h = random(30, 60); // Umidade aleatória de umidade entre 30% e 60%
    float t = random(20, 31); // Umidade aleatória de temperatura entre 20 a 31C

    if (isnan(h) || isnan(t)) {
        Serial.println("Falha ao ler do sensor DHT!"); // Verifica se a leitura falhou
    } else {
        // Exibi os valores lidos 
        String linha = "LDR: " + String(ldrValue) + ", Umidade: " + String(h) + ", Temperatura: " + String(t);
        Serial.println(linha);

        // Lógica para irrigação
        bool phIdeal = (ldrValue > 400 && ldrValue < 700); // Exemplo de faixa ideal
        bool umidadeBaixa = (h < 40.0); // Umidade abaixo de 40%

        if (simularFosforo && simularPotassio && phIdeal && umidadeBaixa) {
            digitalWrite(relePin, HIGH); // Liga irrigação
        } else {
            digitalWrite(relePin, LOW); // Desliga irrigação
        }
    }

    delay(2000); // Aguarda 2 segundos
}


// =================================================================
// ==           FARMTECH SOLUTIONS - CÓDIGO FASE 4              ==
// =================================================================

// --- Inclusão de Bibliotecas ---
#include <DHT.h>
#include <math.h>
// NOVO (Fase 4): Bibliotecas para LCD I2C e comunicação MQTT
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <PubSubClient.h>

// --- OTIMIZAÇÃO (Fase 4): Pinos definidos como 'const uint8_t' ---
// Isso economiza 75% de memória por variável (1 byte vs 4 bytes de um int)
// e garante que os valores não sejam alterados acidentalmente.
const uint8_t pinoDHT = 23;
const uint8_t relePin = 12;
const uint8_t ledPhosphorus = 13;
const uint8_t ledPotassium = 21; // Corrigido de "Posttasium" para "Potassium"

// --- Configurações dos Sensores e Dispositivos ---
#define modeloDHT DHT22

// --- NOVO (Fase 4): Configurações de Rede e MQTT ---
const char* ssid = "NOME_DA_SUA_REDE_WIFI";
const char* password = "SENHA_DA_SUA_REDE_WIFI";
const char* mqtt_server = "broker.hivemq.com"; // Usando um broker público para teste
const char* mqtt_topic = "farmtech/fase4/dados";

// --- Inicialização dos Objetos ---
DHT dht(pinoDHT, modeloDHT);
LiquidCrystal_I2C lcd(0x27, 16, 2); // (Endereço I2C, Colunas, Linhas)
WiFiClient espClient;
PubSubClient client(espClient);

// --- Variáveis de Controle ---
long lastMsg = 0; // Para o timer não bloqueante
bool statusBomba = false;

// --- Função de Setup ---
void setup() {
    Serial.begin(115200); // Aumentar a velocidade para comunicação mais rápida
    
    // Configuração dos pinos de saída
    pinMode(relePin, OUTPUT);
    pinMode(ledPhosphorus, OUTPUT);
    pinMode(ledPotassium, OUTPUT);
    digitalWrite(relePin, LOW); // Garantir que a bomba comece desligada

    // Inicialização dos periféricos
    dht.begin();
    lcd.init();
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print("FarmTech v4.0");
    
    // NOVO (Fase 4): Conexão WiFi e MQTT
    setup_wifi();
    client.setServer(mqtt_server, 1883); // Porta padrão do MQTT
}

// --- NOVO (Fase 4): Função para conectar ao WiFi ---
void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Conectando em ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi conectado!");
    Serial.print("Endereço IP: ");
    Serial.println(WiFi.localIP());
}

// --- NOVO (Fase 4): Função para reconectar ao MQTT ---
void reconnect_mqtt() {
    while (!client.connected()) {
        Serial.print("Tentando conexão MQTT...");
        if (client.connect("ESP32_FarmTechClient")) {
            Serial.println("conectado!");
        } else {
            Serial.print("falhou, rc=");
            Serial.print(client.state());
            Serial.println(" tentando novamente em 5 segundos");
            delay(5000);
        }
    }
}

// --- Loop Principal ---
void loop() {
    // NOVO (Fase 4): Mantém a conexão MQTT
    if (!client.connected()) {
        reconnect_mqtt();
    }
    client.loop();

    // NOVO (Fase 4): Timer não bloqueante, executa a cada 2 segundos
    long now = millis();
    if (now - lastMsg > 2000) {
        lastMsg = now;

        // --- Leitura e Simulação dos Sensores ---
        bool simularFosforo = millis() % 8000 < 4000;  // alterna a cada 4 segundos
        bool simularPotassio = millis() % 12000 < 6000; // alterna a cada 6 segundos

        // CORREÇÃO (Fase 4): Lendo os dados REAIS do sensor DHT22
        float umidade = dht.readHumidity();
        float temperatura = dht.readTemperature();

        // Simulação de pH (a mesma lógica suave, pois é uma boa simulação)
        float ph = 7.0 + 2.0 * sin(millis() / 5000.0);

        // Verificação de falha na leitura do DHT
        if (isnan(umidade) || isnan(temperatura)) {
            Serial.println("Falha ao ler do sensor DHT!");
            return;
        }

        // --- Lógica de Decisão ---
        // CORREÇÃO (Fase 4): Lógica de pH ajustada para a faixa correta de valores
        bool phIdeal = (ph > 6.0 && ph < 7.5);
        bool umidadeBaixa = (umidade < 40.0);

        // A lógica de irrigação agora depende apenas da umidade para simplificar
        if (umidadeBaixa) {
            statusBomba = true;
        } else {
            statusBomba = false;
        }
        digitalWrite(relePin, statusBomba ? HIGH : LOW);
        
        // Atualiza LEDs de nutrientes
        digitalWrite(ledPhosphorus, simularFosforo ? HIGH : LOW);
        digitalWrite(ledPotassium, simularPotassio ? HIGH : LOW);

        // --- NOVO (Fase 4): Preparando os dados em formato JSON ---
        String jsonPayload = "{";
        jsonPayload += "\"umidade\":" + String(umidade, 1) + ",";
        jsonPayload += "\"temperatura\":" + String(temperatura, 1) + ",";
        jsonPayload += "\"ph\":" + String(ph, 2) + ",";
        jsonPayload += "\"presenca_fosforo\":" + String(simularFosforo) + ",";
        jsonPayload += "\"presenca_potassio\":" + String(simularPotassio) + ",";
        jsonPayload += "\"bomba_ligada\":" + String(statusBomba);
        jsonPayload += "}";

        // --- Saídas e Comunicação ---
        
        // 1. Saída para o Monitor Serial (para debug)
        Serial.println("Enviando payload: " + jsonPayload);

        // 2. NOVO (Fase 4): Publicando os dados via MQTT
        client.publish(mqtt_topic, jsonPayload.c_str());

        // 3. NOVO (Fase 4): Atualizando o Display LCD
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Umidade: " + String(umidade, 1) + "%");
        lcd.setCursor(0, 1);
        lcd.print("Bomba: " + String(statusBomba ? "LIGADA" : "DESLIGADA"));

        // 4. NOVO (Fase 4): Saída para o Serial Plotter
        // Imprime apenas o valor numérico da umidade para ser plotado corretamente.
        // A linha de debug acima (com texto) deve ser comentada para usar o plotter.
        // Serial.println(umidade); 
    }
}
