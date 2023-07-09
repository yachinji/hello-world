import RPi.GPIO as GPIO
import dht11
import time
import paho.mqtt.client as mqtt_client

broker="mqtt-dashboard.com"
port=1883
client_id="joypi"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print("Sent `{}` to topic `{}`".format(msg, topic))
    else:
        print("Failed to send message to topic {}".format(topic))

def run():
    client = connect_mqtt()
    client.loop_start()

    while True:
        humidity, temperature = dht11.read(dht11.DHT11, 4)
        print("Temp: {0:0.1f} C  Humidity: {1:0.1f} %".format(temperature, humidity))
        publish(client, "t/sensor/temperature", temperature)
        publish(client, "t/sensor/humidity", humidity)

        sleep(60)

if __name__ == "__main__":
    while True:
        try:
            run()
        except:
            print("Exception, retrying in 5 min")
            sleep(300)
            continue
