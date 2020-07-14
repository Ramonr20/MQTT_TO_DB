from time import gmtime, strftime
import paho.mqtt.client as mqtt
import json
import sqlite3

from DB.dbConnection import DBConnection as db

broker = "test.mosquitto.org"
topic_node_2 = "habitaciones/1/nodos/2"
port = 1883

data = ['']*6

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_node_2)
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    theTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    payload = msg.payload
    my_json = payload.decode('utf8')
    sensorData = json.loads(my_json)

    print(msg.topic + ":\t" + 'voltaje: ' + str(sensorData['voltaje']) + 
    ', corriente: ' + str(sensorData['corriente']) +
    ', fac_de_pot: ' + str(sensorData['fac_de_pot']) +
    ', pot_activa: ' + str(sensorData['pot_activa']) +
    ', pot_real: ' + str(sensorData['pot_real']) +
    ', pot_aparente: ' + str(sensorData['pot_aparente'])
    )
    
    data[0] = sensorData['voltaje']
    data[1] = sensorData['corriente']
    data[2] = sensorData['fac_de_pot']
    data[3] = sensorData['pot_activa']
    data[4] = sensorData['pot_real']
    data[5] = sensorData['pot_aparente']

    if (msg.topic == topic_node_2):
        if ('' not in data):
            writeToDb(data[0], data[1], data[2],data[3], data[4], data[5], theTime, 2)
    return

def writeToDb(voltaje, corriente, fac_de_pot, pot_activa, pot_real, pot_aparente, theTime, room_node):
    print("Writing to db...")
    db.execute_query("INSERT INTO entrena_reg_node VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (None, voltaje, corriente, fac_de_pot, pot_activa, pot_real, pot_aparente, True, theTime, room_node))                    
    db.connection.commit()

    print("Successful")

    data = [''*6]

def main():
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(broker, port, 60)

        print("Esperando mensaje")
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
        print("Exit status successful")

if __name__ == "__main__":
    main()