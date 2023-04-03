from machine import Pin
import _thread
import random
import time
import sys

def edge_detected_rigth(pin_1):
    global sensor_value_pluvia
    global sensor_value_temp
    global sensor_value_light
    if sensor_value_pluvia >1000:
        print("[INFO] Derecha!")
    if sensor_value_temp >22:
        print("[INFO] Derecha!")
    if sensor_value_light >250:
        print("[INFO] Derecha!")

def edge_detected_left(pin_1):
    global sensor_value_pluvia
    global sensor_value_temp
    global sensor_value_light
    if sensor_value_pluvia <1000:
        print("[INFO] Derecha!")
    if sensor_value_temp <22:
        print("[INFO] Derecha!")
    if sensor_value_light <250:
        print("[INFO] Derecha!")
        
def edge_detected_left(pin_2):
    global sensor_value_pluvia
    global sensor_value_temp
    global sensor_value_light
    if sensor_value_pluvia <1000:
        print("[INFO] Derecha!")
    if sensor_value_temp <22:
        print("[INFO] Derecha!")
    if sensor_value_light <250:
        print("[INFO] Derecha!")
    
def read_shutdown(shutdown):
    print("[INFO] Cerrando ventana!")
        
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

if __name__ == "__main__":
    switch_pin_1 = 14 # Fin de carrera 1
    switch_pin_2 = 12 # Fin de carrera 2
    shut = 13 # Cerrado manual
    auto = 11 # Automatic mode
    pin_1 = Pin(switch_pin_1, Pin.IN, Pin.PULL_UP)
    pin_2 = Pin(switch_pin_1, Pin.IN, Pin.PULL_UP)
    shutdown = Pin(shut, Pin.IN, Pin.PULL_UP)
    pin_1.irq(handler = edge_detected_rigth, trigger = Pin.IRQ_FALLING)
    pin_2.irq(handler = edge_detected_left, trigger = Pin.IRQ_FALLING)
    shutdown.irq(handler = edge_detected_left, trigger = Pin.IRQ_FALLING)
    _thread.start_new_thread(read_sensor_pluvia,())
    _thread.start_new_thread(read_sensor_temp,())
    _thread.start_new_thread(read_sensor_light,())
    
    while True:
        pass
    
    