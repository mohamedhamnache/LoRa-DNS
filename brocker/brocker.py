import paho.mqtt.client as mqttClient
import time


def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("Connected to broker")

        global Connected  # Use global variable
        Connected = True  # Signal connection

    else:

        print("Connection failed")


def on_message(client, userdata, message):
    print("Message received: " + message.payload)
    with open(
        "/home/mhamnache/learning-dev/python/LoRa-DNS/brocker/test.txt", "a+"
    ) as f:
        f.write("Message received: " + message.payload + "\n")


Connected = False  # global variable for the state of the connection

broker_address = "127.0.0.1"  # Broker address
port = 1883  # Broker port
# user = "me"                    #Connection username
# password = "abcdef"            #Connection password

client = mqttClient.Client("Python")  # create new instance
# client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback
client.connect(broker_address, port, 60)  # connect
client.subscribe("application/5/device/70b3d549967ceb93")  # subscribe
client.loop_forever()  # then keep listening forever
