import paho.mqtt.client as mqtt
import json




def on_connect(mqttc, obj, flags, rc):
    mqttc.subscribe('home')
    print("rc: "+str(rc))


def on_message(mqttc, obj, msg):
    returnDataFromMqttBroker(msg.payload)


def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))



def on_disconnect(mqttc,obj,rc):
    print("discoonected reconnecting")
    print(obj)
    print(rc)
    mqttc.connect('192.168.159.56', 1883, 6)


mqttc = mqtt.Client("database")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect
# mqttc.connect('mosquitto-docker', 9001, 60)
mqttc.connect('192.168.159.56', 1883, 60)
print(f'trying to connect.....')





def returnDataFromMqttBroker(data):
    print(data)

def send_data(toggle):
    mqttc.publish("home",toggle)




