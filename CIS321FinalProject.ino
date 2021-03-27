#include <LiquidCrystal.h>
  
const byte sPower = 53;
const byte BLUE = 2;  
const byte GREEN = 3;
const byte RED = 4;
const byte FAN = 5;
String status;
int TIMER = 10; // amount of time in seconds (change to debug or whatnot)
int cycle;

const int rs = 8, en = 9, d4 = 10, d5 = 11, d6 = 12, d7= 13;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup()  
{  
    pinMode(BLUE, OUTPUT);  
    pinMode(RED,OUTPUT);
    pinMode(GREEN, OUTPUT);
    pinMode(A1, INPUT);
    pinMode(sPower, OUTPUT);
    pinMode(FAN, OUTPUT);
    digitalWrite(sPower, LOW);
    cycle = TIMER - 1;
    lcd.begin(16, 2); // 16 columns and 2 rows
    //print a message to LCD
    Serial.begin(9600);
    }  

void loop()  
{  
    lcd.clear();
    // read the input on analog pin 0:
    // String test = Serial.readStringUntil("\n"); // test different values
    //int mMoisture = analogRead(A0); // manure moisture
  	int mMoisture = 400;
    // delay(1500);        // delay in between reads for stability
    digitalWrite(sPower, HIGH);
    delay(10); // turn the sensor on and wait a second
    if(cycle <=0) {
      // if the moisture value is greater than or equal to 400, turn on the red light
      if(mMoisture >= 400) {
      digitalWrite(GREEN, LOW);
      digitalWrite(BLUE, LOW);
      digitalWrite(RED, HIGH);
      analogWrite(FAN, 0);// 0% duty cycle
      status = "DRY";
    }
    // if the moisture is "just right", turn on the green LED and the fan on 70%
    else if (mMoisture >= 300 && mMoisture < 400) {
      digitalWrite(GREEN, HIGH);
      digitalWrite(BLUE, LOW);
      digitalWrite(RED, LOW);
      analogWrite(FAN, 192); // 70% duty cycle
      status = "STABLE";
      
    }
    // if moisture is less than 300, turn on the blue LED, turn the fan on 100%
    else if (mMoisture < 300) {
      digitalWrite(GREEN, LOW);
      digitalWrite(BLUE, HIGH);
      digitalWrite(RED, LOW);
      analogWrite(FAN, 255); // 100% duty cycle
      status = "WET";
      lcd.print(status);
    }
    lcd.setCursor(0, 0);
    lcd.print("Moisture Level");
    lcd.setCursor(0,1);
    lcd.print(status);
    lcd.print(": ");
    lcd.print(mMoisture);
    Serial.print(status);
    Serial.print(": ");
    Serial.println(mMoisture);
    digitalWrite(sPower, LOW);
    delay(1000);
    cycle = TIMER - 1;  
  }
  else {
    // if cycle hasn't finished, wait 10 seconds and turn off LEDs
    delay(10);
    digitalWrite(GREEN, LOW);
    digitalWrite(BLUE, LOW);
    digitalWrite(RED, LOW);
  }
  Serial.println(cycle); // debugging cycle
  cycle--;
  delay(990); // decrement cycle and wait a second (1 minute - 10 sec for reading)
} 
