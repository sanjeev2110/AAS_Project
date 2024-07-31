import json
import requests
import random
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "aas/updates"
client_id = f'subscribe-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id, protocol=mqtt_client.MQTTv5)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"Received raw payload: {payload}")
        data = json.loads(payload)
        print(f"Received `{data}` from `{msg.topic}` topic")
        update_submodel(data)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON payload: {e}")

def update_submodel(payload):
    url = 'http://localhost:5005/submodel/element/GoodParts'
    response = requests.post(url, json={"value": payload['value']})
    if response.status_code == 200:
        print("Submodel updated successfully")
    else:
        print(f"Failed to update submodel: {response.text}")

def run():
    client = connect_mqtt()
    client.on_message = on_message
    client.loop_forever()

if __name__ == '__main__':
    run()
