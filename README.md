# SISTEMA DE CONTROL DE VENTANAS AUTOMATIZADO (sensor de lluvia, temperatura y luz analógicos) - IOT. 

## OBJETIVOS 

•	Aplicar las definiciones y conceptos de las asignaturas vistas para implementar un sistema de control de ventanas con motores impulsados por Arduino.

•	Crear y probar sensores para manejar el abrir y cerrar de la ventana

•	Realizar el acondicionamiento de señales respectivo al sistema, para la correcta adquisición y manipulación de los datos en el proceso 

•	Llevar a cabo la puesta en funcionamiento del prototipo utilizando tecnología de tiempo real

## PROBLEMA

• El problema al tener una venta común y corriente es que al momento de no estar en el sitio ya sea casa, oficina, salón de universidad, etc. Cuando llueve y salimos del lugar sin percatarnos de si dejamos abierta o cerrada la ventana, tendríamos un inconveniente ya que podemos tener cosas al pendiente cerca a la ventana y se pueden dañar con la lluvia, además, si nos encontramos en el sitio esta brindará confort, pues se adapta a las condiciones climaticas del momento mientras esté en el modo automatico.

## DESCRIPCIÓN TECNOLÓGICA

• Los sensores van a emitir una señal al microcontrolador programado, dependiendo de la condición (estados) que se cumpla se encenderá el motor que hará que cierre o abra la ventana dependiendo la situación climática, se podrá controlar la ventana de manera manual. 

## ESTADOS

• Caso 1: Cuando hay mucha luz y temperatura alta, la ventana abre.

• Caso 2: Cuando hay poca luz y temperatura baja, la ventana cierra.

• Caso 3: Cuando hay poca luz y temperatura alta, la ventana abre.

• Caso 4: Cuando hay poca luz y temperatura baja; está lloviendo ventana cierra.

• Caso 5: Cuando hay poca luz y temperatura alta; está lloviendo, la ventana cierra.

• Caso 6: Cuando hay mucha luz y temperatura alta; está lloviendo, la ventana cierra.

• Caso 7: Cuando hay mucha luz y temperatura baja; está lloviendo, la ventana cierra.

• Caso 7: Cuando hay mucha luz y temperatura baja, la ventana cierra.

• Caso 8: Modo manual, el usuario controla la ventana desde pulsadores y desde una aplicación móvil.


