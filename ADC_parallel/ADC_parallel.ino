int analogPin  = A0 ; //input pin (current measure)

int pin0 = 2; //output pins
int pin1 = 3;
int pin2 = 4;
int pin3 = 5;
int pin4 = 6;
int pin5 = 7;
int pin6 = 8;
int pin7 = 9;
int pin8 = 10;
int pin9 = 11;

bool DEBUG_MODE=true;

float offset = 2.455;
int val = 0 ;

void setup ()
{
  Serial.begin(9600); //check bitrate in function of desired measure frequency
  pinMode(pin0,OUTPUT);  
  pinMode(pin1,OUTPUT);
  pinMode(pin2,OUTPUT);
  pinMode(pin3,OUTPUT);
  pinMode(pin4,OUTPUT);
  pinMode(pin5,OUTPUT);
  pinMode(pin6,OUTPUT);
  pinMode(pin7,OUTPUT);
  pinMode(pin8,OUTPUT);
  pinMode(pin9,OUTPUT);
 
}

int i=0;
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (float)(x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min;
}

void loop ()
{
  Serial.println("");
  Serial.println("**********");
  val = analogRead(analogPin);
  Serial.println(String(val)+"  readed value 0-1023");
  float voltage= val * (5.0 / 1023.0);
  //val=mapfloat(val, 0, 1023, 0, 5);
  Serial.println(String(voltage)+" V");
  
  Serial.println(String(voltage-offset)+" V OffSetted");
  
  //Sensitivity of the sensor: 625 mV/Ipn. Ipn = 50A, so the slope is 12.5 mV/A
  float current = (voltage-offset)/0.0125;
  Serial.println(String(current)+"A");
  /*
  //Rescaled value inside range
  int minBattery=0;
  int maxBattery=100;
  int rescaledValue=mapfloat(val, minBattery, maxBattery, 0,1023);
  Serial.print("Value rescaled: " + String(rescaledValue));
  */
  digitalWrite(pin0,bitRead(val,0)) ; //write on parallel port
  digitalWrite(pin1,bitRead(val,1)) ;
  digitalWrite(pin2,bitRead(val,2)) ;
  digitalWrite(pin3,bitRead(val,3)) ;
  digitalWrite(pin4,bitRead(val,4)) ;
  digitalWrite(pin5,bitRead(val,5)) ;
  digitalWrite(pin6,bitRead(val,6)) ;
  digitalWrite(pin7,bitRead(val,7)) ;
  digitalWrite(pin8,bitRead(val,8)) ;
  digitalWrite(pin9,bitRead(val,9)) ;

  if(DEBUG_MODE)
  {
    Serial.println(bitRead(val,0));
    Serial.println(bitRead(val,1));
    Serial.println(bitRead(val,2));
    Serial.println(bitRead(val,3));
    Serial.println(bitRead(val,4));
    Serial.println(bitRead(val,5));
    Serial.println(bitRead(val,6));
    Serial.println(bitRead(val,7));
    Serial.println(bitRead(val,8));
    Serial.println(bitRead(val,9)); 
  }
  
  delay(50);
  i+=1;
  
}
