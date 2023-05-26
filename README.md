# Sistema IoT Retrofit de control domotizado para ventanas deslizantes (sensor de lluvia, temperatura y luz analógicos) - Arduino y microPython. 

## OBJETIVOS 

•	Aplicar las definiciones y conceptos de las asignaturas vistas para implementar un sistema de control de ventanas con motores impulsados por Arduino.

•	Crear y probar sensores para manejar el abrir y cerrar de la ventana

•	Realizar el acondicionamiento de señales respectivo al sistema, para la correcta adquisición y manipulación de los datos en el proceso 

•	Llevar a cabo la puesta en funcionamiento del prototipo utilizando tecnología de tiempo real

## PROBLEMA

• El problema al tener una venta común y corriente es que al momento de no estar en el sitio ya sea casa, oficina, salón de universidad, etc. Cuando llueve y salimos del lugar sin percatarnos de si dejamos abierta o cerrada la ventana, tendríamos un inconveniente ya que podemos tener cosas al pendiente cerca a la ventana y se pueden dañar con la lluvia, además, si nos encontramos en el sitio esta brindará confort, pues se adapta a las condiciones climaticas del momento mientras esté en el modo automatico.

## DESCRIPCIÓN TECNOLÓGICA Y ESTADOS 

• El software consta de dos modos de operación que permiten la comunicación de los sensores acoplados en el hardware con el sistema electrónico que acciona la operación de la tecnología. Los modos son automático y manual, en las cuales las condiciones en modo automático se ejecutan de forma autónoma reaccionando a la información obtenida a partir de los sensores. En modo manual, el usuario activa los motores que direccionan la apertura y el cerrado de la ventana a través de una serie de botones acoplados a la tecnología. 

Los sensores que controlan los motores que permiten la apertura y el cerrado de la ventana, y, que, a su vez, son controlados por el software con:

•	Sensor de temperatura
•	Sensor de lluvia
•	Sensor de fin de carrera
•	Sensor de iluminación

A continuación, se presenta una descripción de la secuencia de operación del software en modo automático y en modo manual.

# microPython SP32


Los siguientes algoritmos fueron diseñados e integrados al software para el control de la ventana inteligente:

Algoritmo de la lectura de sensore:
```
  def legere_sensor_temperatus():
    global sensorem_pretium_temp
    sensorem_pretium_temp = dht.DHT11(pin_temperatus)
    while True:
        try:
            sensorem_pretium_temp.measure()
            temperatus = sensorem_pretium_temp.temperature()
            humiditas = sensorem_pretium_temp.humidity()
            print("[INFO] Sensor temp: {}°C".format(sensorem_pretium_temp))
            print("[INFO] Sensor temp: {}%".format(humiditas))
        except OSError as e:
            print("Error al leer el sensor DHT11:", e)
        time.sleep(1)
        
def legere_sensorem_lux():
    # Leer el valor analógico de la luz
    global sensorem_pretium_lux
    while True:
        sensorem_pretium_lux = pin_lux.read()
        print("[INFO] Sensor light: {}".format(sensorem_pretium_lux))
        time.sleep(1)
        
def legere_sensorem_pluvia():
    global sensorem_pretium_pluvia
    while True:
        sensorem_pretium_pluvia = pin_pluvia.value()
        print("[INFO] Sensor light: {}".format(sensorem_pretium_pluvia))
        time.sleep(1)
```

```
#Configuramus stamina ad valores e datorum accipiendos (main)
    _thread.start_new_thread(legere_sensorem_lux,())
    _thread.start_new_thread(legere_sensorem_temperatus,())
    _thread.start_new_thread(legere_sensorem_pluvia,())

```

Algoritmo de la lectura de las interrupciones:

```
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
```

```
 #Configuramus interpellationes (main)
    pin_1.irq(handler = edge_detected_rigth, trigger = Pin.IRQ_FALLING)
    pin_2.irq(handler = edge_detected_left, trigger = Pin.IRQ_FALLING)
    pin_3.irq(handler = left, trigger = Pin.IRQ_FALLING)
    pin_4.irq(handler = rigth, trigger = Pin.IRQ_FALLING)
    pin_5.irq(handler = down, trigger = Pin.IRQ_FALLING)

```

Algoritmo de la lectura de la base de datos MYSQL:

```
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
```

Algoritmo de la lectura de la conexión a Wi-Fi:

```
#CONNECT WI-FI 
def wifi_connect():
    print("[INFO] Connectens", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    try:
        sta_if.connect('MARIO S10', 'unodos12')
    except:
        machine.reset()
```

Algoritmo de la lectura del MQTT:

```
 

#MQTT configuratione
MQTT_BROKER    = "broker.hivemq.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_CLIENT_ID = "clientId-YWyGsNoiWf"
MQTT_TOPIC     = "udemedellin/sinistram"
MQTT_TOPIC_2   = "udemedellin/declinemus"
MQTT_TOPIC_3   = "udemedellin/pretium"
MQTT_TOPIC_4   = "udemedellin/dexteram"
MQTT_PORT = 1883

    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)
    
    print(" [INFO] Wi-FI connexa!")

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
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC))
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC_2))
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC_3))
    print("Connected on %s, topic subscribed: %s " % (MQTT_BROKER, MQTT_TOPIC_4))
    return client
```

Algoritmo de la rutina 1
```
   if (sensorem_pretium_pluvia == 0 and legere_sensorem_temperatus > 25 and legere_sensorem_lux <= 400):
            look_around2()
            print("Ventana abre")
```
En el algoritmo de la rutina 1, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar la apertura de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Alta); 
- Sensor de temperatura (Estado: Temperatura: alta >22°C);  
- Sensor de lluvia (Estado: con lluvia)
- Rutina de operación: Abrir ventana

Nota 1: Cuando la ventana llega hasta el final de su desplazamiento, un sensor de fin carrera ubicado en dicha posición es accionado. Esto conlleva a enviar una señal al computador de placa reducida, que, a su vez, es procesada por el software para detener el motor que genera el desplazamiento lateral.

Algoritmo de la rutina 2
```
if (sensorem_pretium_pluvia == 1 and legere_sensorem_temperatus < 18 and legere_sensorem_lux > 400):
            look_around()
            print("Ventana cierra")
```
En el algoritmo de la rutina 2, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar el cerrado de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Baja); 
- Sensor de temperatura (Estado: Temperatura: Baja <18°C);  
- Sensor de lluvia (Estado: Con lluvia)
- Rutina de operación: Cerrar ventana

Nota: Se aplica lo descrito en la Nota 1

Algoritmo de la rutina 3
```
if (sensorem_pretium_pluvia == 0 and legere_sensorem_temperatus < 18 and legere_sensorem_lux > 400):
            look_around()
            print("Ventana cierra")
```
En el algoritmo de la rutina 3, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar la apertura de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Baja); 
- Sensor de temperatura (Estado: Temperatura: Baja <18°C);  
- Sensor de lluvia (Estado: Sin lluvia)
- Rutina de operación: Cerrar ventana

Nota: Se aplica lo descrito en la Nota 1

Algoritmo de la rutina 4
```
if (sensorem_pretium_pluvia == 0 and legere_sensorem_temperatus > 22 and legere_sensorem_lux > 400):
            look_around2()
            print("Ventana abre")
```
En el algoritmo de la rutina 4, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar el cerrado de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Baja); 
- Sensor de temperatura (Estado: Temperatura: Alta >22°C);  
- Sensor de lluvia (Estado: Sin lluvia)
- Rutina de operación: Abrir ventana

Nota: Se aplica lo descrito en la Nota 1

Algoritmo de la rutina 5
```
if (sensorem_pretium_pluvia == 1 and legere_sensorem_temperatus > 22 and legere_sensorem_lux > 400):
            look_around()
            print("Ventana cierra")
```
En el algoritmo de la rutina 5, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar el cerrado de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Baja); 
- Sensor de temperatura (Estado: Temperatura: Alta >22°C);  
- Sensor de lluvia (Estado: Con lluvia)
- Rutina de operación: Cerrar ventana

Nota: Se aplica lo descrito en la Nota 1

Algoritmo de la rutina 6
```
if (sensorem_pretium_pluvia == 1 and legere_sensorem_temperatus > 22 and legere_sensorem_lux <= 400):
            look_around()
            print("Ventana cierra") 
```
En el algoritmo de la rutina 6, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar el cerrado de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Alta); 
- Sensor de temperatura (Estado: Temperatura: Alta >22°C);  
- Sensor de lluvia (Estado: Con lluvia)
- Rutina de operación: Cerrar ventana

Nota: Se aplica lo descrito en la Nota 1

Algoritmo de la rutina 7
```
if (sensorem_pretium_pluvia == 1 and legere_sensorem_temperatus < 18 and legere_sensorem_lux <= 400):
            look_around()
            print("Ventana cierra")
```
En el algoritmo de la rutina 7, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar el cerrado de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Alta); 
- Sensor de temperatura (Estado: Temperatura: Baja <18°C);  
- Sensor de lluvia (Estado: Con lluvia)
- Rutina de operación: Cerrar ventana

Algoritmo de la rutina 8

```
if (sensorem_pretium_pluvia == 1 and legere_sensorem_temperatus < 18 and legere_sensorem_lux <= 400):
            look_around()
            print("Ventana cierra")
```
En el algoritmo de la rutina 7, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar el cerrado de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Alta); 
- Sensor de temperatura (Estado: Temperatura: Baja <18°C);  
- Sensor de lluvia (Estado: Con lluvia)
- Rutina de operación: Cerrar ventana

# Arduino

MODO AUTOMÁTICO

Los siguientes algoritmos fueron diseñados e integrados al software para el control de la ventana inteligente:

Algoritmo de la rutina 1
```
    if(Val_luz <= 400 && Val_temp > 22 && Val_lluvia > 780  && digitalRead(automatico)  == HIGH)
    {
        lookAround();
        digitalWrite(leds[0],LOW); 
        digitalWrite(leds[1],HIGH);  
    }  
```
En el algoritmo de la rutina 1, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar la apertura de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Alta); 
- Sensor de temperatura (Estado: Temperatura: Alta >22°C);  
- Sensor de lluvia (Estado: Sin lluvia)
- Rutina de operación: Abrir ventana

Nota 1: Cuando la ventana llega hasta el final de su desplazamiento, un sensor de fin carrera ubicado en dicha posición es accionado. Esto conlleva a enviar una señal al computador de placa reducida, que, a su vez, es procesada por el software para detener el motor que genera el desplazamiento lateral.

Algoritmo de la rutina 2
```
   if(Val_luz <= 400 && Val_temp < 15 && Val_lluvia > 780 && digitalRead(automatico)  == HIGH)
    {
        lookAround2();
        digitalWrite(leds[1],LOW); 
        digitalWrite(leds[0],HIGH);   
    }
```
En el algoritmo de la rutina 2, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar el cerrado de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Alta); 
- Sensor de temperatura (Estado: Temperatura: Baja <22°C);  
- Sensor de lluvia (Estado: Sin lluvia)
- Rutina de operación: Cerrar ventana

Nota: Se aplica lo descrito en la Nota 1

Algoritmo de la rutina 3
```
if(Val_luz > 400 && Val_temp > 22 && Val_lluvia > 780  && digitalRead(automatico)  == HIGH)
    {
        lookAround();
        digitalWrite(leds[0],HIGH); 
        digitalWrite(leds[1],LOW);   
    }
```
En el algoritmo de la rutina 3, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar la apertura de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Baja); 
- Sensor de temperatura (Estado: Temperatura: Alta >22°C);  
- Sensor de lluvia (Estado: Sin lluvia)
- Rutina de operación: Abrir ventana

Nota: Se aplica lo descrito en la Nota 1

Algoritmo de la rutina 4
```
if(Val_luz > 400 && Val_temp < 15 && Val_lluvia > 780 && digitalRead(automatico)  == HIGH)
    {
        lookAround2();
        digitalWrite(leds[1],HIGH); 
        digitalWrite(leds[0],LOW);   
    }
```
En el algoritmo de la rutina 4, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar el cerrado de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Baja); 
- Sensor de temperatura (Estado: Temperatura: Baja <22°C);  
- Sensor de lluvia (Estado: Con lluvia)
- Rutina de operación: Cerrar ventana

Nota: Se aplica lo descrito en la Nota 1

Algoritmo de la rutina 5
```
if(Val_luz > 400 && Val_temp > 22 && Val_lluvia <= 780 && digitalRead(automatico)  == HIGH)
    {
        lookAround2();
        digitalWrite(leds[1],HIGH); 
        digitalWrite(leds[0],LOW);   
    }
```
En el algoritmo de la rutina 5, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar el cerrado de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Baja); 
- Sensor de temperatura (Estado: Temperatura: Alta >22°C);  
- Sensor de lluvia (Estado: Con lluvia)
- Rutina de operación: Cerrar ventana

Nota: Se aplica lo descrito en la Nota 1

Algoritmo de la rutina 6
```
if(Val_luz <= 400 && Val_temp > 22 && Val_lluvia <= 780 && digitalRead(automatico)  == HIGH)
    {
        lookAround2();
        digitalWrite(leds[1],LOW); 
        digitalWrite(leds[0],HIGH);  
    }  
```
En el algoritmo de la rutina 6, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar el cerrado de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Alta); 
- Sensor de temperatura (Estado: Temperatura: Alta >22°C);  
- Sensor de lluvia (Estado: Con lluvia)
- Rutina de operación: Cerrar ventana

Nota: Se aplica lo descrito en la Nota 1

Algoritmo de la rutina 7
```
if(Val_luz <= 400 && Val_temp < 15 && Val_lluvia <= 780  && digitalRead(automatico)  == HIGH)
    {
        lookAround2();
        digitalWrite(leds[1],LOW); 
        digitalWrite(leds[0],HIGH);   
    }  
```
En el algoritmo de la rutina 7, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para gestionar el cerrado de la ventana de la siguiente forma. 

- Sensor de iluminación (Estado: Iluminación Alta); 
- Sensor de temperatura (Estado: Temperatura: Baja <22°C);  
- Sensor de lluvia (Estado: Con lluvia)
- Rutina de operación: Cerrar ventana

Nota: Se aplica lo descrito en la Nota 1

Nota 2: El software de control de la ventana inteligente tiene una fuerte dependencia en su algoritmo con respecto a la información enviada por el sensor de lluvia. Por lo tanto, cuando el sensor detecta presencia de lluvia, la ventana se cerrará ignorando cualquier otra condición. 

ESTADO MANUAL

La rutina establecida para el modo manual consiste en la operación por parte del usuario a partir de la obturación de una serie de pulsadores que direccionan al software a activar y/o desactivar los motores para generar el desplazamiento de la ventana. Cuando el hardware es puesto en modo manual, las rutinas establecidas en el modo automático dejan de funcionar. 

Configuración de los pulsadores:

- Pulsador 1: Activa el motor para generar el cierre de la ventana
- Pulsador 2: Activa el motor para generar la apertura de la ventana
- Pulsador 3: Detiene el motor

En el algoritmo manual, al pulsar el botón 1, los datos obtenidos de los sensores de iluminación, temperatura y lluvia se correlacionan para la gestionar el cerrado de la ventana de la siguiente forma.

En el modo manual, el usuario controla la ventana desde pulsadores y desde una aplicación móvil, en este estado las condiciones descritas anteriormente se ignoran; si está lloviendo la ventana no se cerrará, el usuario se hace responsable al ingresar al modo manual.

