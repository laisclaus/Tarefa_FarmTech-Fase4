# !pip install paho-mqtt
import paho.mqtt.client as mqtt
from Database.db_actions import inserir_dados

# MQTT settings
broker = "broker.hivemq.com"
port = 1883
topic = "farmtech/fase4/dados"

# Called when connected to broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker.")
        client.subscribe(topic)
    else:
        print(f"❌ Failed to connect. Return code={rc}")

# Called when a message is received
def on_message(client, userdata, msg):
    import json
    try:
        esp32_readings = json.loads(msg.payload.decode())
        inserir_dados(
            esp32_readings["umidade"],
            esp32_readings["temperatura"],
            esp32_readings["ph"],
            esp32_readings["presenca_fosforo"],
            esp32_readings["presenca_potassio"],
            esp32_readings["bomba_ligada"]
        )
        print(f"Dados inseridos: {esp32_readings}")
    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")

# Set up client and callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect and listen
client.connect(broker, port, keepalive=60)
client.loop_forever()
