int Pins[] = {11,10,9}; //Un pin para PWM, dos pines para la dirección del motor
int switchPin = 6; // Fin de carreraFin de carrera
int switchPin2 = 7; // Fin de carreraFin de carrera
int leds[] = {12,13}; // Leds puerta abierta y cerada
int SensorPin_luz = 0;  //Pin analógico para sensor de luz
int SensorPin_temp = 1;  //Pin analógico para sensor de temperatura
int SensorPin_lluvia = 2;  //Pin analógico para sensor de lluvia 
int abrir_cerrar = 4; // Abrir y cerrar ventana manualmente
int apagar = 2; // Apagado manual de la ventana
int automatico = 5; // Cambiar el estado de automatico manual 


void setup()
{
  for(int i=1; i < 3; i++)
  {
    pinMode(Pins[i], OUTPUT); //Se asignan los controladores del motor como salida
  } 
  for(int h=1; h < 2; h++)
  {
    pinMode(leds[h], OUTPUT); //Se asignan leds como salida
  }
  Serial.begin(9600); //Inicializamos monitor serie para visualizar los valores de LDR. 
  pinMode(switchPin, INPUT_PULLUP); //Se asigna boton de fin de carrera como entrada
  pinMode(switchPin2, INPUT_PULLUP); //Se asigna boton de fin de carrera como entrada
  pinMode(abrir_cerrar, INPUT_PULLUP); //Se asigna boton manual para abrir y cerrar como entrada
  pinMode(automatico, INPUT_PULLUP); //Se asigna boton manueal de automatico como entrada
  pinMode(apagar, INPUT_PULLUP); //Se asigna boton manueal para apagar en cualquier estado como entrada
  attachInterrupt(digitalPinToInterrupt(apagar), blink, LOW); //Se convierte el boton manual en interruptor para apagarla en cualquier estado
}

void loop()
{
    int Val_luz = analogRead(SensorPin_luz); //Se lee el valor del sensor de luz
    int Val_temp = analogRead(SensorPin_temp); //Se lee el valor del sensor de temperatura
    int Val_lluvia = analogRead(SensorPin_lluvia); //Se lee el valor del sensor de lluvia
    Val_temp = (5.0 * Val_temp * 100.0)/1024.0; //Convertimos valor del sensor a temperatura en grados
    Serial.print("Sensor de luz: "); 
    Serial.println(Val_luz); //Imprimimos dicho valor, comprendido entre 0 y 1023. 
    Serial.print("Sensor de Temperatura en grados: ");
    Serial.println(Val_temp); //Imprimimos dicho valor, comprendido entre 0 y 100.
    Serial.print("Sensor de Lluvia: ");
    Serial.println(Val_lluvia); //Imprimimos dicho valor, comprendido entre 0 y 1023.


     // ---------------------------   MODO AUTOMATICO ----------------------------
     
     //Cuando hay poca luz y temperatura baja, está lloviendo ventana cierra
     if(Val_luz > 400 && Val_temp < 22 && Val_lluvia <= 780 && digitalRead(automatico)  == HIGH)
    {
        lookAround2();
        digitalWrite(leds[0],HIGH); 
        digitalWrite(leds[1],LOW);   
    }

     //Cuando hay poca luz y temperatura baja, ventana cierra
     if(Val_luz > 400 && Val_temp < 22 && Val_lluvia > 780 && digitalRead(automatico)  == HIGH)
    {
        lookAround2();
        digitalWrite(leds[1],HIGH); 
        digitalWrite(leds[0],LOW);   
    }


    //Cuando hay poca luz y temperatura alta, ventana abre
     if(Val_luz > 400 && Val_temp > 22 && Val_lluvia > 780  && digitalRead(automatico)  == HIGH)
    {
        lookAround();
        digitalWrite(leds[0],HIGH); 
        digitalWrite(leds[1],LOW);   
    }

    
       //Cuando hay mucha luz y temperatura alta, ventana abre
     if(Val_luz <= 400 && Val_temp > 22 && Val_lluvia > 780  && digitalRead(automatico)  == HIGH)
    {
        lookAround();
        digitalWrite(leds[0],LOW); 
        digitalWrite(leds[1],HIGH);  

    }  

     //Cuando hay poca luz y temperatura alta, está lloviendo ventana cierra
     if(Val_luz > 400 && Val_temp > 22 && Val_lluvia <= 780 && digitalRead(automatico)  == HIGH)
    {
        lookAround2();
        digitalWrite(leds[1],HIGH); 
        digitalWrite(leds[0],LOW);   
    }

    
       //Cuando hay mucha luz y temperatura alta, está lloviendo ventana cierra
     if(Val_luz <= 400 && Val_temp > 22 && Val_lluvia <= 780 && digitalRead(automatico)  == HIGH)
    {
        lookAround2();
        digitalWrite(leds[1],LOW); 
        digitalWrite(leds[0],HIGH);  

    }  

     //Cuando hay mucha luz y temperatura baja, está lloviendo ventana cierra
     if(Val_luz <= 400 && Val_temp < 22 && Val_lluvia <= 780  && digitalRead(automatico)  == HIGH)
    {
        lookAround2();
        digitalWrite(leds[1],LOW); 
        digitalWrite(leds[0],HIGH);   
    }  

    //Cuando hay mucha luz y temperatura baja, ventana cierra
     if(Val_luz <= 400 && Val_temp < 22 && Val_lluvia > 780 && digitalRead(automatico)  == HIGH)
    {
        lookAround2();
        digitalWrite(leds[1],LOW); 
        digitalWrite(leds[0],HIGH);   
    }  

      //Cuando llega al final de carrera apaga, y enciende solo cuando no hay luz 
   if(digitalRead(switchPin) == LOW && Val_luz > 400 && digitalRead(automatico)  == HIGH) 
   {
      apagado();
      digitalWrite(leds[0],LOW); 
      digitalWrite(leds[1],LOW);  
    }
    
    //Cuando llega al final de carrera apaga, y enciende solo cuando hay luz 
   if(digitalRead(switchPin) == LOW && Val_luz < 400 && digitalRead(automatico)  == HIGH) 
   {
      apagado();
      digitalWrite(leds[0],LOW); 
      digitalWrite(leds[1],LOW);  
    } 

     //Cuando llega al final de carrera apaga, y enciende solo cuando hay luz
   if(digitalRead(switchPin2) == LOW && Val_luz < 400 && digitalRead(automatico)  == HIGH && Val_lluvia > 780) 
    { 
      apagado();
      digitalWrite(leds[0],LOW); 
      digitalWrite(leds[1],LOW); 
    } 

    // ----------------------- MODO MANUAL ------------------

     //Boton manual ventana cierra
     if(digitalRead(abrir_cerrar) == LOW && digitalRead(automatico) == LOW)
    {
        lookAround2();
        digitalWrite(leds[1],LOW); 
        digitalWrite(leds[2],HIGH);  

    }  

       //Boton manual ventana abre
     if(digitalRead(abrir_cerrar) == HIGH && digitalRead(automatico) == LOW)
    {
        lookAround();
        digitalWrite(leds[0],LOW); 
        digitalWrite(leds[1],HIGH);  

    }  

      
     //Cuando llega al final de carrera apaga, y enciende solo cuando no hay luz 
   if(digitalRead(switchPin) == LOW && digitalRead(abrir_cerrar) == LOW && digitalRead(automatico) == LOW) 
   {
      apagado();
      digitalWrite(leds[0],LOW); 
      digitalWrite(leds[1],LOW);  
    }

   //Cuando llega al final de carrera apaga, y enciende solo cuando hay luz
   if(digitalRead(switchPin2) == LOW && digitalRead(abrir_cerrar) == HIGH && digitalRead(automatico) == LOW) 
    { 
      apagado();
      digitalWrite(leds[0],LOW); 
      digitalWrite(leds[1],LOW); 
    }  
   
}

void apagado()
{
  //Metodo que apaga el motor
  setSpeed(Pins, 0);
}

void lookAround()
{
  //Girar a la izquierda 
  setSpeed(Pins, -255);
  
}
void lookAround2()
{
  //Girar a la derecha
  setSpeed(Pins, 255);
  
}

void setSpeed(int pins[], int speed)
{
  //Metodo para cambiar direccion del motor e innicializar su paso
  if(speed < 0)
  {
    digitalWrite(pins[1], HIGH);
    digitalWrite(pins[2], LOW);
    speed = -speed;  
    
  }  
  else
  {
    digitalWrite(pins[1], LOW);
    digitalWrite(pins[2], HIGH);  
  }
  analogWrite(pins[0], speed);
}

//Metodo para apagar motor, manejado como interrupcion para ignorar el estado del puerto
void blink() {
  apagado();
  digitalWrite(leds[1],HIGH); 
  digitalWrite(leds[0],HIGH);  
}
