int Pins[] = {11,10,9}; //Un pin para PWM, dos pines para la dirección del motor
int SensorPin = 0;  //Pin analógico para sensores
int sensorUmbral = 0;  //Debe tener tanta luz en un sensor para moverse
int switchPin = 7; // Boton de apagado
int switchPin2 = 2; // Fin de carrera ventana abierta
int switchPin3 = 3; // Fin de carrera ventana cerrada
boolean reversa = false;
boolean estadoant = false;
int ledpin = 12; // Led puerta abierta
int ledpin2 = 13; // Led puerta cerrada


void setup()
{
  for(int i=1; i < 3; i++)
  {
    pinMode(Pins[i], OUTPUT);
  }  
  Serial.begin(9600); //Inicializamos monitor serie para visualizar los valores de LDR. 
  pinMode(switchPin, INPUT_PULLUP);
  pinMode(switchPin2, INPUT_PULLUP);
  pinMode(switchPin3, INPUT_PULLUP);
  pinMode(ledpin, OUTPUT);
  pinMode(ledpin2, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(switchPin2), blink, FALLING);
  attachInterrupt(digitalPinToInterrupt(switchPin3), blink, FALLING);
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
        digitalWrite(ledpin,HIGH); 
        digitalWrite(ledpin2,LOW);   
    }

     if(Val > sensorUmbral)
    {
        lookAround2();
        digitalWrite(ledpin,HIGH); 
        digitalWrite(ledpin2,LOW);   
    }
    
    
 if(digitalRead(switchPin) == LOW && digitalRead(switchPin) != estadoant) // mirando para ver si el estado del botón es LOW y no es igual al último estado.
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
  //Girar a la izquierda 
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
  digitalWrite(ledpin,LOW);
  digitalWrite(ledpin2,LOW);
  
}
