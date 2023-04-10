#Modules importari
from firebase import firebase
import pymysql as MySQLdb
from machine import Pin
import datetime
import time, os
import _thread
import random
import sys

def edge_detected_rigth(pin_1):
    global sensor_value_pluvia
    global sensor_value_temp
    global sensor_value_light
    if sensor_value_pluvia >1000:
        print("[INFO] Derecha!")
        apagado()
        look_around()
    if sensor_value_temp >22:
        print("[INFO] Derecha!")
        apagado()
        look_around()
    if sensor_value_light >250:
        print("[INFO] Derecha!")
        apagado()
        look_around()
    if sensor_value_light >250 and sensor_value_temp >22:
        print("[INFO] Izquierda!")
        apagado()
        look_around2()

def edge_detected_left(pin_2):
    global sensor_value_pluvia
    global sensor_value_temp
    global sensor_value_light
    if sensor_value_pluvia <1000:
        print("[INFO] Derecha!")
        apagado()
        look_around2()
    if sensor_value_temp <22:
        print("[INFO] Derecha!")
        apagado()
        look_around2()
    if sensor_value_light <250:
        print("[INFO] Derecha!")
        apagado()
        look_around2()   

def read_shutdown(shutdown):
    print("[INFO] Cerrando ventana!")
    apagado()
        
def read_sensor_temp():
    global sensor_value_temp
    while True:
        sensor_value = random.random()
        print("[INFO] Sensor temp: {}".format(sensor_value_temp))
        time.sleep(1)
        
def read_sensor_luz():
    global sensor_value_light
    while True:
        sensor_value = random.random()
        print("[INFO] Sensor light: {}".format(sensor_value_light))
        time.sleep(1)

def set_speed(pins, speed):
  # Metodo para cambiar direccion del motor e innicializar su paso
  if speed < 0:
    Pin(pins[1], Pin.OUT).on()
    Pin(pins[2], Pin.OUT).off()
    speed = -speed
  else:
    Pin(pins[1], Pin.OUT).off()
    Pin(pins[2], Pin.OUT).on()
    
  PWM(Pin(pins[0]), freq=1000, duty=speed)
  
def look_around():
  # Girar a la izquierda
  set_speed(pins, -255)

def look_around2():
  # Girar a la derecha
  set_speed(pins, 255)

def apagado():
  # Metodo que apaga el motor
  set_speed(pins, 0)
  
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

if __name__ == "__main__":
    #Definimos las entradas
    switch_pin_1 = 14 # Fin de carrera 1
    switch_pin_2 = 12 # Fin de carrera 2
    shut = 13 # Cerrado manual
    auto = 11 # Automatic mode
    pin_1 = Pin(switch_pin_1, Pin.IN, Pin.PULL_UP)
    pin_2 = Pin(switch_pin_1, Pin.IN, Pin.PULL_UP)
    shutdown = Pin(shut, Pin.IN, Pin.PULL_UP)
    #Configuramos las interrupciones
    pin_1.irq(handler = edge_detected_rigth, trigger = Pin.IRQ_FALLING)
    pin_2.irq(handler = edge_detected_left, trigger = Pin.IRQ_FALLING)
    shutdown.irq(handler = edge_detected_left, trigger = Pin.IRQ_FALLING)
    #Configuramos los hilos para tomar valores de los sesnores
    _thread.start_new_thread(read_sensor_pluvia,())
    _thread.start_new_thread(read_sensor_temp,())
    _thread.start_new_thread(read_sensor_light,())
    
    while True:
        pass
    
    