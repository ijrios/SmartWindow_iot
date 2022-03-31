boolean reverse = false;
boolean lastState = false;
int enablePin = 11; // PWM 
int in1Pin = 10; // Control del motor
int in2Pin = 9; // Control del motor
int switchPin = 7; // Boton de encendido - se cambiará por una fotoresistencia
int switchPin2 = 2; // Fin de carrera ventana abierta
int switchPin3 = 3; // Fin de carrera ventana cerrada
int pinLDR = 0; // Pin analogico de entrada para el LDR
int valorLDR = 0; // Variable donde se almacena el valor del LDR


void setup()
{
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(enablePin, OUTPUT);
  pinMode(switchPin, INPUT_PULLUP);
  pinMode(switchPin2, INPUT_PULLUP);
  pinMode(switchPin3, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchPin2), blink, FALLING);
  attachInterrupt(digitalPinToInterrupt(switchPin3), blink, FALLING);
}

void loop()
{
  int estado =0;
  int speed = 255; // Velocidad
  valorLDR= analogRead(pinLDR); // Guardamos el valor leido del ADC en una variable
  Serial.println(valorLDR); // Imprimimos el valor leido 
 //-------------------------------------------------------------------------------------
  // Caso 1 - Botón
  if(digitalRead(switchPin) == LOW && digitalRead(switchPin) != lastState) // mirando para ver si el estado del botón es LOW y no es igual al último estado.
{ 
  reverse = !reverse; // solo cambiará cuando el estado del botón sea BAJO
  lastState = digitalRead(switchPin);
  setMotor(speed, reverse);
}
 //-------------------------------------------------------------------------------------
   // Caso 2 - Sensor LDR con poca luz
 if(valorLDR > 256)
  {reverse = !reverse; // solo cambiará cuando el estado del botón sea BAJO
  lastState = digitalRead(switchPin);
  setMotor(speed, reverse);
  }
  //-------------------------------------------------------------------------------------
   // Caso 3 - Sensor LDR con mucha luz
  if(valorLDR < 256)
  {
  reverse = !reverse; // solo cambiará cuando el estado del botón sea BAJO
  lastState = digitalRead(switchPin);
  setMotor(speed, reverse);
  } 
  //-------------------------------------------------------------------------------------
   // Caso 4 - sensor de lluvia

}

 //---------------------------------------------------------------------------------------
void setMotor(int speed, boolean reverse)
{
  analogWrite(enablePin, speed);
  digitalWrite(in1Pin, ! reverse);
  digitalWrite(in2Pin, reverse);
}

void blink() {
  analogWrite(enablePin, 0);
  reverse = !reverse; // solo cambiará cuando el estado del botón sea LOW
}
