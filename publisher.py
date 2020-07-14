import paho.mqtt.client as mqtt #mqtt library
import os
import json
import time
from datetime import datetime
import random

#host name is localhost because both broker and python are Running on same 
#machine/Computer.
broker="test.mosquitto.org" #host name , Replace with your IP address.
topic_node_2="habitaciones/1/nodos/2"

port=1883 #MQTT data listening port

def random_number(init, end):
  return random.randrange(init, end)

def on_publish(client, userdata, result): #create function for callback
  print("published data is : ")
  pass

def main():

  try:
    client1 = mqtt.Client("CETEVI") #create client object

    client1.on_publish = on_publish #assign function to callback
    client1.connect(broker, port, 60) #establishing connection

    #publishing after every 2 secs
    while True:

      payload = "{"
      payload += "\"voltaje\":" + str(random_number(120,125))
      payload += ","
      payload += "\"corriente\":" + str(random_number(20,23))
      payload += ","
      payload += "\"fac_de_pot\":" + str(random_number(0,2))
      payload += ","
      payload += "\"pot_activa\":" + str(random_number(123,125))
      payload += ","
      payload += "\"pot_real\":" + str(random_number(120,125))
      payload += ","
      payload += "\"pot_aparente\":" + str(random_number(120,123))
      payload += "}"

      ret = client1.publish(topic_node_2, payload) #sensor1

      print(payload)
      print("Please check data on your Subscriber Code \n")

      time.sleep(2)
  except KeyboardInterrupt:
    client1.disconnect()
    print("Exit status successful")
  
if __name__ == '__main__':
  main()