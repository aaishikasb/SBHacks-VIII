#include <string.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

Servo pointer;

LiquidCrystal_I2C lcd(0x27, 16, 2);
int sensorValue = 0;
int val;

void setup() {
  // Initialize LEDs
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(13, OUTPUT);//Red
  pinMode(12, OUTPUT);//Green

  // Initialize Servo
  pointer.attach(9);

  Serial.begin(9600);

}

void loop() {
  // Initialize LCD
  lcd.init();
  lcd.backlight();
  lcd.clear();

  // Receive Potentiometer Data
  sensorValue = analogRead(A0);
  Serial.println(sensorValue);

  // Operate Pointer
  val = analogRead(A0);
  val = map(val, 0, 700, 0, 180);
  pointer.write(val);
  delay(0);

  // LEDs
  if (sensorValue < 350){
    digitalWrite(13, HIGH);
    digitalWrite(12, LOW);
  }

  else if (sensorValue > 350){
    digitalWrite(13, LOW);
    digitalWrite(12, HIGH);
  }

  
    lcd.setCursor(0,0);
    lcd.print("Sensor Value:");
    lcd.setCursor(0,1);
    lcd.print(sensorValue);
}
