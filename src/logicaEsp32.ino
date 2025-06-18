// =================================================================
// ==           FARMTECH SOLUTIONS - CÓDIGO FASE 4              ==
// ==                  VERSÃO COMPLETA E CORRIGIDA                ==
// =================================================================

// --- 1. Inclusão de Bibliotecas ---
#include <DHT.h>
#include <math.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <PubSubClient.h>

// --- 2. Definições de Pinos e Constantes (Otimizadas) ---
const uint8_t pinoDHT = 23;
const uint8_t relePin = 12;
const uint8_t ledPhosphorus = 13;
const uint8_t ledPotassium = 21;

#define modeloDHT DHT22

// --- 3. Configurações de Rede e MQTT ---
const char* ssid = "Wokwi-GUEST"; // Para Wokwi, use "Wokwi-GUEST"
const char* password = "";        // Para Wokwi, a senha é vazia
const char* mqtt_server = "broker.hivemq.com";
const char* mqtt_topic = "farmtech/fase4/dados";

// --- 4. Criação dos Objetos ---
DHT dht(pinoDHT, modeloDHT);
LiquidCrystal_I2C lcd(0x27, 16, 2);
WiFiClient espClient;
PubSubClient client(espClient);

// --- 5. Declaração de Variáveis Globais ---
long lastMsg = 0;
bool statusBomba = false;

// --- 6. Função de Setup (Executa uma vez) ---
void setup() {
    Serial.begin(115200);
    
    pinMode(relePin, OUTPUT);
    pinMode(ledPhosphorus, OUTPUT);
    pinMode(ledPotassium, OUTPUT);
    digitalWrite(relePin, LOW);

    dht.begin();
    lcd.init();
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print("FarmTech v4.0");
    
    setup_wifi();
    client.setServer(mqtt_server, 1883);
}

// --- 7. Funções de Ajuda ---
void setup_wifi() {
    delay(10);
    Serial.println("Conectando ao WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi conectado!");
}

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

// --- 8. Loop Principal (Executa repetidamente) ---
void loop() {
    if (!client.connected()) {
        reconnect_mqtt();
    }
    client.loop();

    long now = millis();
    if (now - lastMsg > 2000) {
        lastMsg = now;

        bool simularFosforo = millis() % 8000 < 4000;
        bool simularPotassio = millis() % 12000 < 6000;

        delay(10); // Pausa para estabilizar a leitura do DHT
        
        float umidade = dht.readHumidity();
        float temperatura = dht.readTemperature();
        float ph = 7.0 + 2.0 * sin(millis() / 5000.0);

        if (isnan(umidade) || isnan(temperatura)) {
            Serial.println("Falha ao ler do sensor DHT!");
            lcd.clear();
            lcd.setCursor(0,0);
            lcd.print("ERRO NO SENSOR");
            lcd.setCursor(0,1);
            lcd.print("Verifique DHT22");
            return;
        }

        bool umidadeBaixa = (umidade < 40.0);
        statusBomba = umidadeBaixa;
        digitalWrite(relePin, statusBomba ? HIGH : LOW);
        
        digitalWrite(ledPhosphorus, simularFosforo ? HIGH : LOW);
        digitalWrite(ledPotassium, simularPotassio ? HIGH : LOW);

        String jsonPayload = "{";
        jsonPayload += "\"umidade\":" + String(umidade, 1) + ",";
        jsonPayload += "\"temperatura\":" + String(temperatura, 1) + ",";
        jsonPayload += "\"ph\":" + String(ph, 2) + ",";
        jsonPayload += "\"presenca_fosforo\":" + String(simularFosforo) + ",";
        jsonPayload += "\"presenca_potassio\":" + String(simularPotassio) + ",";
        jsonPayload += "\"bomba_ligada\":" + String(statusBomba);
        jsonPayload += "}";

        Serial.println("Enviando payload: " + jsonPayload);
        client.publish(mqtt_topic, jsonPayload.c_str());

        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Umidade: " + String(umidade, 1) + "%");
        lcd.setCursor(0, 1);
        lcd.print("Bomba: " + String(statusBomba ? "LIGADA" : "DESLIGADA"));
    }
}
