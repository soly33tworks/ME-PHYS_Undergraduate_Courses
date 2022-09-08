/*
  Temperature, pressure and humidity DAQ together with load cell readings.
  Was developed and used as an educational tool for mass metrology.
  Check github for wiring. Run with the python GUI code for visualization
  and calibration.
*/

#include <LiquidCrystal_I2C.h>
#include <HX711_ADC.h>
#include <SFE_BMP180.h>
#include <Wire.h>
#include "DHT.h"

#define DHTPIN 7 // DHT22 SGN pin
#define DHTTYPE DHT22

HX711_ADC LoadCell(3, 2);
SFE_BMP180 pressure;
DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27,16,2);

byte degree[8]={
  B01110,
  B01010,
  B01110,
  B00000,
  B00000,
  B00000,
  B00000,
};

unsigned long previousMillis1 = 0;
unsigned long previousMillis2 = 0;
const long interval1 = 2000;
const long interval2 = 5000;

void setup()
{
  Serial.begin(9600);
  LoadCell.begin();
  LoadCell.start(2000);
  LoadCell.setCalFactor(1940.0);
  
  lcd.begin();
  lcd.backlight();
  lcd.createChar(0, degree);

  pressure.begin();
  dht.begin();

}

void loop()
{
  LoadCell.update();
  float i = LoadCell.getData();
  Serial.print(i);
  Serial.println();
  delay(100); 
  
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis1 >= interval1) {
    previousMillis1 = currentMillis;

    float h = dht.readHumidity();
    float t = dht.readTemperature();
    if (isnan(h) || isnan(t)) {
      return;
    }  
    
    lcd.setCursor(0,0);         
    lcd.print("T=");
    lcd.print(t,1);
    lcd.write(byte(0)); 
    lcd.print("C");
    lcd.print(" ");
  
    lcd.setCursor(9,0);
    lcd.print("RH=");
    lcd.print(h,1);
    lcd.print(" ");
    }

   if (currentMillis - previousMillis2 >= interval2) {
    previousMillis2 = currentMillis;

    char status;
    double T,P;
  
    status = pressure.startTemperature();
    if (status != 0)
    {
      delay(status);

      status = pressure.getTemperature(T);
      if (status != 0)
      {
        status = pressure.startPressure(3);
        if (status != 0)
        {
          delay(status);

          status = pressure.getPressure(P,T);
          if (status != 0)
          {
          }
          else return;
        }
        else return;
      }
      else return;
    }
    else return;
    
    lcd.setCursor(0,1);         
    lcd.print("P=");
    lcd.print(P, 2);
    lcd.print("mbar");
    lcd.print(" ");
    }
}
