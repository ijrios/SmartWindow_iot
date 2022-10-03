# Sistema IoT Retrofit de control domotizado para ventanas deslizantes (sensor de lluvia, temperatura y luz analógicos). 

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

