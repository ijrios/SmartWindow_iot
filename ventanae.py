from umqtt.simple import MQTTClient
from machine import Pin
import time, os
import _thread
import network
import random
import sys
import pyrebase

##################################################################################

#Configurare machinas in global environment
pin_6 = Pin(33, Pin.OUT)
pin_7 = Pin(32, Pin.OUT)

#Database configuramus
config = {              
  "authDomain": "controlventana-33",
  "databaseURL": "https://controlventana-33-default-rtdb.firebaseio.com/",
  "storageBucket": "project-509531904366"
}
#Database nos initialize
firebase = pyrebase.initialize_app(config)
database = firebase.database()
ProjectBucket = database.child("project-509531904366") 

##################################################################################

#MQTT configuratione
MQTT_BROKER    = "broker.hivemq.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_CLIENT_ID = "clientId-Q7kiVUm3JHq"
MQTT_TOPIC     = "udemedellin/motus"
MQTT_TOPIC_2   = "udemedellin/declinemus"
MQTT_TOPIC_2   = "udemedellin/pretium"
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

#DUXERIT NUNTIUM CONFIG
def message_arrived(topic, msg):
    print("[INFO] {}{}".format(topic,msg))
    if (topic == 'udemedellin/motus'):
        if (msg == b'1'):
            print("[INFO] ad dextram")
            value="ad dextram"
            look_around()
            client.publish(b"udemedellin/pretium",value)
        if (msg == b'0'):
            value="ad sinistram"
            look_around2()
            print("[INFO] ad sinistram")
            client.publish(b"udemedellin/pretium",value)
    if (topic == 'udemedellin/declinemus'):
        if (msg == b'1'):
            print("[INFO] ut declinemus")
            value="ut declinemus"
            apagado()
            client.publish(b"udemedellin/pretium",value)

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
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC))
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC_2))
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC_3))
    return client

################################################################################
def edge_detected_rigth(pin_1):
    #Fin de carrera apagado
    print("Apagado fin 1")
    apagado()
    #look_around()

def edge_detected_left(pin_2):
    #Fin de carrera apagado
    print("Apagado fin 2")
    apagado()
    #look_around()
    
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
    
def read_apagado():
    global estado1
    estado1 = ProjectBucket.child("apa").get().val()
    #Off
    if estado1 == 1:
        print("Declinamus")
        print(estado1)
        apagado()
    
def read_derecha():
    global estado2
    estado2 = ProjectBucket.child("der").get().val()
    #Dexteram
    if estado2 == 1:
        print("Dexteram")
        print(estado2)
        look_around2()
    
def read_izquierda():
    global estado3
    estado3 = ProjectBucket.child("izq").get().val()
    #Sinistram
    if estado3 == 1:
        print("Sinistram")
        print(estado3)
        look_around()

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
    pin_6.value(0)
    pin_7.value(1)

def look_around2():
    pin_6.value(1)
    pin_7.value(0)

def apagado():
    pin_6.value(0)
    pin_7.value(0)
    
################################################################################

#PROGRAMMA PRÆVIUM  
if __name__ == "__main__":
    #Definimus initibus
    switch_pin_1 = 14 #Finis currere 1
    switch_pin_2 = 12 #Finis currere 2
    derecha = 25
    izquierda = 26
    apaga = 27
    pin_1 = Pin(switch_pin_1, Pin.IN, Pin.PULL_UP)
    pin_2 = Pin(switch_pin_2, Pin.IN, Pin.PULL_UP)
    pin_3 = Pin(derecha, Pin.IN, Pin.PULL_UP)
    pin_4 = Pin(izquierda, Pin.IN, Pin.PULL_UP)
    pin_5 = Pin(apaga, Pin.IN, Pin.PULL_UP)
    #Configuramus interpellationes
    pin_1.irq(handler = edge_detected_rigth, trigger = Pin.IRQ_FALLING)
    pin_2.irq(handler = edge_detected_left, trigger = Pin.IRQ_FALLING)
    pin_3.irq(handler = left, trigger = Pin.IRQ_FALLING)
    pin_4.irq(handler = rigth, trigger = Pin.IRQ_FALLING)
    pin_5.irq(handler = down, trigger = Pin.IRQ_FALLING)
    #Configuramus stamina ad valores e datorum accipiendos
    _thread.start_new_thread(read_apagado,())
    _thread.start_new_thread(read_derecha,())
    _thread.start_new_thread(read_izquierda,())
    
    #MQTT
    wifi_connect()
    client = subscribe()

    while True:
        #client.wait_msg()
        client.check_msg()
    #time.sleep(0.5)      # BLINK LED