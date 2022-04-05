int Pins[] = {11,10,9}; //Un pin para PWM, dos pines para la dirección del motor
int switchPin[] = {2,3} // Fin de carreraFin de carrera
int leds[] = {12,13} // Leds puerta abierta y cerada
int SensorPin = 0;  //Pin analógico para sensores
int sensorUmbral = 0;  //Debe tener tanta luz en un sensor para moverse
int apagar = 7; // Boton de apagado
boolean reversa = false;
boolean estadoant = false;


void setup()
{
  for(int i=1; i < 3; i++)
  {
    pinMode(Pins[i], OUTPUT);
  } 
   for(int j=1; j < 2; i++)
  {
    pinMode(switchPin[j], INPUT_PULLUP);
  }

  for(int h=1; h < 2; i++)
  {
    pinMode(leds[h], OUTPUT);
  }
  Serial.begin(9600); //Inicializamos monitor serie para visualizar los valores de LDR. 
  pinMode(apagar, INPUT_PULLUP); //Se asigna boton de apagado como entrada
  attachInterrupt(digitalPinToInterrupt(switchPin2), blink, CHANGE); //Se convierte los fines de carrera en interruptor
  attachInterrupt(digitalPinToInterrupt(switchPin3), blink, FALLING); //Se convierte los fines de carrera en interruptor
}

void loop()
{
    int Val = analogRead(SensorPin);
    Serial.println(Val); //Imprimimos dicho valor, comprendido entre 0 y 1023. 

    if(sensorUmbral == 0)
      sensorUmbral = (Val)/2;

    if(Val < sensorUmbral)
    {
        lookAround();
        digitalWrite(leds[1],HIGH); 
        digitalWrite(leds[2],LOW);   
    }

     if(Val > sensorUmbral)
    {
        lookAround2();
        digitalWrite(leds[1],HIGH); 
        digitalWrite(leds[2],LOW);   
    }
    
    
 if(digitalRead(apagar) == LOW && digitalRead(apagar) != estadoant) // mirando para ver si el estado del botón es LOW y no es igual al último estado.
    { 
       setSpeed(Pins, 0);
       digitalWrite(ledpin,LOW);
       digitalWrite(ledpin,LOW);
    }
   
}
void lookAround()
{
  //Girar a la izquierda 
  setSpeed(Pins, -127);
  
}
void lookAround2()
{
  //Girar a la derecha
  setSpeed(Pins, 127);
  
}

void setSpeed(int pins[], int speed)
{
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

//Metodo para apagar motor, manjeado como interrupcion para ignorar el estado del puerto
void blink() {
   // Se apaga el motor al llegar al fin de carrera
  analogWrite(Pins[0], 0);
  digitalWrite(leds[1],LOW);
  digitalWrite(leds[2],LOW);
  
}
