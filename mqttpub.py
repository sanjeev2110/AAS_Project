import json
import random
import time
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "aas/updates"
client_id = f'publish-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id, protocol=mqtt_client.MQTTv5)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        time.sleep(5)
        good_parts_value = random.randint(0, 200)
        msg = {"idShort": "GoodParts", "value": good_parts_value}
        result = client.publish(topic, json.dumps(msg))
        status = result[0]
        if status == 0:
            print(f"Sent `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()
