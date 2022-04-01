int leftPins[] = {11,10,9}; //one pin for PWm, two pins for motor direction

int leftSensorPin = 0;  //analog pin for sensors

int sensorThreshold = 0;  //must have this much light on a sensor to move
int looks = 0;  //the number of attempts to turn and find light

void setup()
{
  for(int i=1; i < 3; i++)
  {
    pinMode(leftPins[i], OUTPUT);
  }  
  Serial.begin(9600); //Inicializamos monitor serie para visualizar los valores de LDR. 
}

void loop()
{
    int leftVal = analogRead(leftSensorPin);
    Serial.println(leftVal); //Imprimimos dicho valor, comprendido entre 0 y 1023. 
    if(sensorThreshold == 0)
      sensorThreshold = (leftVal)/2;

    if(leftVal < sensorThreshold)
    {
      if(looks < 4) //limit the number of consecutive looks
      {
        lookAround();
        looks = looks + 1;  
      }  
    }
    else 
    {
      //if there is adequate ligth to move ahead
      setSpeed(leftPins, map(leftVal,0,1023,0,255));
      looks = 0;  
    }
    
}
void lookAround()
{
  //rotate left or half a second
  setSpeed(leftPins, -127);
  
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
