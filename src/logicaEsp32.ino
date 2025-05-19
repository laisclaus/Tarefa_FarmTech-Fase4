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
