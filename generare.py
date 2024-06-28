import random
import time
import paho.mqtt.client as mqtt
import json
import sys
import signal

BROKER = "localhost"
PORT = 1883
TOPIC = "device/ChiritescuAndrei"
CLIENT_ID = "Andrew"

def signal_handler(sig,frame):
    print("Stopping the generation of data")
    client.loop_stop()
    client.disconnect()
    print("Client disconnected")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def on_connect(client, userdata, flags,rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Failed to connect, return code {rc}")


def on_publish(client, userdata, mid):
    print("Message published")

client = mqtt.Client(CLIENT_ID)
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the broker
client.connect(BROKER, PORT, 60)

def generare():
    while True:
        random_heart_rate = round(random.uniform(60, 100), 2)  # Ritm cardiac între 60 și 100 bpm
        random_oxygen_saturation = round(random.uniform(90, 100), 2)  # Saturația oxigenului între 90 și 100%
       
        data = {
           "ritm_cardiac": random_heart_rate,
           "saturatie_oxigen": random_oxygen_saturation
       }
        
        json_data = json.dumps(data)

        result = client.publish(TOPIC, json_data)
       
        status = result.rc
        if status == 0:
            print(f"Sent `{json_data}` to topic `{TOPIC}`")
        else:
            print(f"Failed to send message to topic {TOPIC}")
        
        time.sleep(3)


client.loop_start()


generare()


client.loop_stop()
client.disconnect()
print("Client disconnected")
