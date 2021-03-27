#include <LiquidCrystal.h>

// creating the LED variables and other supplies
const byte sPower = 53;
const byte BLUE = 2;  
const byte GREEN = 3;
const byte RED = 4;
const byte FAN = 5;
String status;
int TIMER = 10; // amount of time in seconds (change to debug or whatnot)
int cycle;

// instantiating the LCD screen
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
    digitalWrite(sPower, LOW); // turn soil sensor off to begin with
    cycle = TIMER - 1; // start the countdown
    lcd.begin(16, 2); // 16 columns and 2 rows
    Serial.begin(9600);
    }  

void loop()  
{  
    lcd.clear();
  	int mMoisture = 400;
    digitalWrite(sPower, HIGH); // turn soil sensor on
    delay(10); // turn the sensor on and wait a second
    if(cycle <=0) {
      // if the moisture value is greater than or equal to 400, turn on the red light
      if(mMoisture >= 400) {
      digitalWrite(GREEN, LOW);
      digitalWrite(BLUE, LOW);
      digitalWrite(RED, HIGH);
      analogWrite(FAN, 0); // set the fan to 0% duty cycle (off)
      status = "DRY"; // create a message for the LCD screen
    }
    // if the moisture is "just right", turn on the green LED and the fan on 70%
    else if (mMoisture >= 300 && mMoisture < 400) {
      digitalWrite(GREEN, HIGH);
      digitalWrite(BLUE, LOW);
      digitalWrite(RED, LOW);
      analogWrite(FAN, 192); // set the fan to 70% duty cycle (middle setting)
      status = "STABLE"; 
    }
    // if moisture is less than 300, turn on the blue LED, turn the fan on 100%
    else if (mMoisture < 300) {
      digitalWrite(GREEN, LOW);
      digitalWrite(BLUE, HIGH);
      digitalWrite(RED, LOW);
      analogWrite(FAN, 255); // set the fan to 100% duty cycle (full power)
      status = "WET";
    }
    lcd.setCursor(0, 0); 
    lcd.print("Moisture Level"); // print on the first line of the LCD screen
    lcd.setCursor(0,1);
    lcd.print(status); // print the status message on the second line
    lcd.print(": ");
    lcd.print(mMoisture); // print the moisture level next to the status
    Serial.print(status);
    Serial.print(": ");
    Serial.println(mMoisture); // display the same information on the serial monitor
    digitalWrite(sPower, LOW); // turn off soil sensor
    delay(1000);
    cycle = TIMER - 1;  // continue countdown
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
