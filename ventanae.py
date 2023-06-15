from umqtt.simple import MQTTClient
#import pymysql as MySQLdb
from machine import Pin
import time, os
import machine
import _thread
import network
import random
import sys
import dht
#import pyrebase


##################################################################################

#Configurare machinas in global environment
pin_6 = Pin(33, Pin.OUT)
pin_7 = Pin(32, Pin.OUT)
pin_lux = machine.ADC(machine.Pin(34))
pin_pluvia = machine.Pin(12, machine.Pin.IN) 
pin_temperatus = machine.Pin(4, machine.Pin.IN)

################################################################################

#DUXERIT NUNTIUM CONFIG
def message_arrived(topic, msg):
    print("[INFO] {}{}".format(topic,msg))
    if (topic == b'udemedellin/dexteram'):
        if (msg == b'1'):
            print("[INFO] ad dextram")
            value="ad dextram"
            look_around()
            client.publish(b"udemedellin/pretium",value)
    if (topic == b'udemedellin/sinistram'):
        if (msg == b'1'):
            value="ad sinistram"
            look_around2()
            print("[INFO] ad sinistram")
            client.publish(b"udemedellin/pretium",value)
    if (topic == b'udemedellin/declinemus'):
        if (msg == b'1'):
            print("[INFO] ut declinemus")
            value="ut declinemus"
            apagado()
            client.publish(b"udemedellin/pretium",value)

##################################################################################

def legere_sensorem():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    client.set_callback(message_arrived)
    global sensorem_pretium_pluvia
    global sensorem_pretium_temp
    global sensorem_pretium_lux
    sensorem_pretium_temp = dht.DHT11(pin_temperatus)
    while True:
        try:
            sensorem_pretium_temp.measure() #sensorem temp
            sensorem_pretium_lux = pin_lux.read() #sensorem lux
            humiditas = sensorem_pretium_temp.humidity() #sensorem humiditas
            sensorem_pretium_pluvia = pin_pluvia.value() #sensorem pluvia
            temperatus = sensorem_pretium_temp.temperature() #sensorem temp
            
            print("[INFO] Sensor lux: {}".format(sensorem_pretium_lux))
            print("[INFO] Sensor temperatus: {}°C".format(sensorem_pretium_temp))
            print("[INFO] Sensor humeditas: {}%".format(humiditas))
            print("[INFO] Sensor pluvia: {}".format(sensorem_pretium_pluvia))
            client.publish(b"udemedellin/temp",sensorem_pretium_temp)
            client.publish(b"udemedellin/lux",sensorem_pretium_lux)
            client.publish(b"udemedellin/pluvia",sensorem_pretium_pluvia)            
            
            # Cuando llueve ventana cierra
            if (sensorem_pretium_pluvia == 0):
                edge_detected_left(pin_2)
                print("Hay lluvia, se cierra ventana")

            # Cuando hay mucha luz y temperatura alta, ventana abre
            if (sensorem_pretium_pluvia == 1  and sensorem_pretium_temp > 25 and sensorem_pretium_lux <= 400):
                look_around2()
                print("Ventana abre")

            # Cuando hay poca luz y temperatura baja, está lloviendo ventana cierra
            if (sensorem_pretium_pluvia == 0 and sensorem_pretium_temp < 18 and sensorem_pretium_lux > 400):
                look_around()
                print("Ventana cierra")

            # Cuando hay poca luz y temperatura baja, ventana cierra
            if (sensorem_pretium_pluvia == 1 and sensorem_pretium_temp < 18 and sensorem_pretium_lux > 400):
                look_around()
                print("Ventana cierra")

            # Cuando hay poca luz y temperatura alta, ventana abre
            if (sensorem_pretium_pluvia == 1 and sensorem_pretium_temp > 22 and sensorem_pretium_lux > 400):
                look_around2()
                print("Ventana abre")

            # Cuando hay poca luz y temperatura alta, está lloviendo ventana cierra
            if (sensorem_pretium_pluvia == 0 and sensorem_pretium_temp > 22 and sensorem_pretium_lux > 400):
                look_around()
                print("Ventana cierra")

            # Cuando hay mucha luz y temperatura alta, está lloviendo ventana cierra
            if (sensorem_pretium_pluvia == 0 and sensorem_pretium_temp > 22 and sensorem_pretium_lux <= 400):
                look_around()
                print("Ventana cierra")

            # Cuando hay mucha luz y temperatura baja, está lloviendo ventana cierra
            if (sensorem_pretium_pluvia == 0 and sensorem_pretium_temp < 18 and sensorem_pretium_lux <= 400):
                look_around()
                print("Ventana cierra")

            # Cuando hay mucha luz y temperatura baja, ventana cierra
            if (sensorem_pretium_pluvia == 1 and sensorem_pretium_temp < 18 and sensorem_pretium_lux <= 400):
                look_around()
                print("Ventana cierra")
            
        except OSError as e:
            print("Error al leer el sensor DHT11:", e)
        time.sleep(1)
        
        
##################################################################################

def database_connect():
    
    #MYSQL DATABASE - General Occasus
    #Optiones ad database nexu
    hostname = '127.0.0.1'
    username = 'pi'
    password = 'raspberry'
    database = 'pidata'

def scribe_MYSQL(identification,timestamp,level,rain):
    
    print("Scribere database")
    query = "INSERT INTO controlVentana (identification,timestamp,temp,lux,pluvia) " \
                "VALUES (%s,%s,%s,%s)"
    args = (identification,timestamp,temp,lux,pluvia)

    try:
        conn = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()

    except Exception as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
        
def legere_MYSQL():

    try:
        
        conn = MySQLdb.connect(host=hostname, user=username, passwd=password, db=database )
        cursor = conn.cursor()
        query = ("SELECT * FROM controlVentana ")
        cursor.execute(query)
        rows = cursor.fetchall()
        
        print('Total Row(s):', cursor.rowcount)
        numerare = []
        for row in rows:
           numerare.append(row[0])

    except ValueError as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return numerare

##################################################################################

def edge_detected_rigth(pin_1):
    #Fin de carrera apagado
    print("Apagado fin 1")
    apagado()
    #look_around()

def edge_detected_left(pin_2):
    #Fin de carrera apagado
    print("Apagado fin 2")
    apagado()
    #look_around2()

##################################################################################

#MQTT configuratione
MQTT_BROKER    = "broker.hivemq.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_CLIENT_ID = "clientId-mhlafO0g4J"
MQTT_TOPIC     = "udemedellin/sinistram"
MQTT_TOPIC_2   = "udemedellin/declinemus"
MQTT_TOPIC_3   = "udemedellin/pretium"
MQTT_TOPIC_4   = "udemedellin/dexteram"
MQTT_TOPIC_5   = "udemedellin/pluvia"
MQTT_TOPIC_6   = "udemedellin/temp"
MQTT_TOPIC_7   = "udemedellin/lux"
MQTT_PORT = 1883

################################################################################

#CONNECT WI-FI 
def wifi_connect():
    print("[INFO] Connectens", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    try:
        sta_if.connect('iPhone', 'andres158')
    except:
        machine.reset()

    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)
    
    print(" [INFO] Wi-FI connexa!")

################################################################################

#PECUNIAM DO
def subscribe():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    # Subscribed messages will be delivered to this callback
    client.set_callback(message_arrived)
    isconnected = False
    while not isconnected:
        try:
            client.connect()
            isconnected = True
        except Exception as e:
            print("[ERROR] {}".format(e))
            time.sleep(1)
    client.subscribe(MQTT_TOPIC)
    client.subscribe(MQTT_TOPIC_2)
    client.subscribe(MQTT_TOPIC_3)
    client.subscribe(MQTT_TOPIC_4)
    client.subscribe(MQTT_TOPIC_5)
    client.subscribe(MQTT_TOPIC_6)
    client.subscribe(MQTT_TOPIC_7)
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC))
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC_2))
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC_3))
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC_4))
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC_5))
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC_6))
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC_7))
    return client

################################################################################
    
def left(pin_3):
    #sinistram
    print("Izquierda")
    look_around()
    
def rigth(pin_4):
    #dextram
    print("Derecha")
    look_around2()
    
def down(pin_5):
    #Off
    print("Off")
    apagado()


def set_speed(pins, speed):
  #Modus mutandi directionem motoris et gradum initialize
  if speed < 0:
    Pin(pins[1], Pin.OUT).value(1)
    Pin(pins[2], Pin.OUT).value(0)
    speed = -speed
  else:
    Pin(pins[1], Pin.OUT).value(0)
    Pin(pins[2], Pin.OUT).value(1)
    
  PWM(Pin(pins[0]), freq=1000, duty=speed)
  
def look_around():
    #Derecha
    pin_6.value(0)
    pin_7.value(1)

def look_around2():
    #Izquierda
    pin_6.value(1)
    pin_7.value(0)

def apagado():
    pin_6.value(0)
    pin_7.value(0)
    
################################################################################

#PROGRAMMA PRÆVIUM  
if __name__ == "__main__":

    #Definimus initibus
    switch_pin_1 = 27 #Finis currere 1
    switch_pin_2 = 26 #Finis currere 2
    pin_1 = Pin(switch_pin_1, Pin.IN, Pin.PULL_UP)
    pin_2 = Pin(switch_pin_2, Pin.IN, Pin.PULL_UP)
    #pin_3 = Pin(derecha, Pin.IN, Pin.PULL_UP)
    #pin_4 = Pin(izquierda, Pin.IN, Pin.PULL_UP)
    #pin_5 = Pin(apaga, Pin.IN, Pin.PULL_UP)

    #Configuramus interpellationes
    pin_1.irq(handler = edge_detected_rigth, trigger = Pin.IRQ_FALLING)
    pin_2.irq(handler = edge_detected_left, trigger = Pin.IRQ_FALLING)
    #pin_3.irq(handler = left, trigger = Pin.IRQ_FALLING)
    #pin_4.irq(handler = rigth, trigger = Pin.IRQ_FALLING)
    #pin_5.irq(handler = down, trigger = Pin.IRQ_FALLING)
    wifi_connect()
    client = subscribe()
    
    #Configuramus stamina ad valores e datorum accipiendos
    _thread.start_new_thread(legere_sensorem,())
    
    #MQTT
    
    while True:
        client.check_msg()
        #client.wait_msg()