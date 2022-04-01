boolean reverse = false;
boolean lastState = false;
int enablePin = 11; // PWM 
int in1Pin = 10; // Control del motor
int in2Pin = 9; // Control del motor
int switchPin = 7; // Boton de encendido 
int switchPin2 = 2; // Fin de carrera ventana abierta
int switchPin3 = 3; // Fin de carrera ventana cerrada
int pinLDR = A0; // Pin analogico de entrada para el LDR
int valorLDR = 0; // Variable donde se almacena el valor del LDR
int ledpin = 12; // Led puerta abierta
int ledpin2 = 13; // Led puerta cerrada


void setup()
{
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
  pinMode(ledpin, OUTPUT);
  pinMode(ledpin2, OUTPUT);
  pinMode(enablePin, OUTPUT);
  pinMode(switchPin, INPUT_PULLUP);
  pinMode(switchPin2, INPUT_PULLUP);
  pinMode(switchPin3, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(switchPin2), blink, FALLING);
  attachInterrupt(digitalPinToInterrupt(switchPin3), blink, FALLING);
  Serial.begin(9600); //Inicializamos monitor serie para visualizar los valores de LDR. 
  
}

void loop()
{
  int estado =0;
  int speed = 255; // Velocidad
  valorLDR= analogRead(pinLDR); // Guardamos el valor leido del ADC en una variable
  Serial.println(valorLDR);      //Imprimimos dicho valor, comprendido entre 0 y 1023. 
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
  {
  //reverse = !reverse; // solo cambiará cuando el estado del botón sea BAJO
  //lastState = digitalRead(switchPin);
  //setMotor(speed, reverse);
  //digitalWrite(ledpin,HIGH);
  }

 //-------------------------------------------------------------------------------------
  
  // Caso 3 - Sensor LDR con mucha luz
   // FUCKKKK FUNCIONAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
   // MIERDA CONVIERTETE EN INTERRUCIÓN PLEASE
  if(valorLDR < 256 )
  {
  reverse = !reverse; // solo cambiará cuando el estado del botón sea BAJO
  lastState = digitalRead(switchPin);
  setMotor(speed, reverse);
  digitalWrite(ledpin2,HIGH);
  } 

  //-------------------------------------------------------------------------------------
   // Caso 4 - sensor de lluvia
   
  //-------------------------------------------------------------------------------------
}

 //---------------------------------------------------------------------------------------
void setMotor(int speed, boolean reverse)
{
  analogWrite(enablePin, speed);
  digitalWrite(in1Pin, ! reverse);
  digitalWrite(in2Pin, reverse);
}

//Metodo para apagar motor, manjeado como interrupcion para ignorar el estado del puerto
void blink() {
  analogWrite(enablePin, 0); // Se apaga el motor al llegar al fin de carrera
  reverse = !reverse; // solo cambiará cuando el estado del botón sea LOW
  digitalWrite(ledpin,LOW);
  digitalWrite(ledpin,LOW);
}
