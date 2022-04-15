/*************************************************** 
  This is a demo for the SHTC3 Temp & Humidity Sensor

  Designed specifically to work with the SHTC3 sensor from Adafruit
  ----> https://www.adafruit.com/products/4636

  These sensors use I2C to communicate. 2 pins are required to
  interface: PB_2 (SCL) and PB_3 (SDA) for Tiva C (TM4C123GH6PM) MCU
 ****************************************************/

#include "Adafruit_SHTC3.h"

Adafruit_SHTC3 shtc3 = Adafruit_SHTC3();
int inByte = 0;

void setup() {
    // Initialize digital pins as outputs:
    pinMode(RED_LED, OUTPUT);  // LOW by default (LED off)
    pinMode(GREEN_LED, OUTPUT);

    Serial.begin(115200); // Use faster serial communication
    Wire.setModule(0);    // Tiva C microcontrollers have multiple I2C ports

    while (!Serial)
        delay(10);  // Should pause until serial console opens

    //Serial.println("\nSHTC3 Demo:");

    if (!shtc3.begin()) {
        digitalWrite(RED_LED, HIGH);  // Turn red LED on to indicate error
        Serial.println("Couldn't find SHTC3 sensor!");
        while (1) delay(1);
    }
   // Serial.println("Found SHTC3 sensor...");
}


void loop() {
    
    checkCommands();
}

void checkCommands()
{
    if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.read();
    // read first analog input, divide by 4 to make the range 0-255:
    //firstSensor = analogRead(A0)/4;
    // delay 10ms to let the ADC recover:
    //delay(10);
    // read second analog input, divide by 4 to make the range 0-255:
    //secondSensor = analogRead(A1)/4;
    // read switch, map it to 0 or 255L
    //thirdSensor = map(digitalRead(1), 0, 1, 0, 255); 
    // send sensor values:
    //Serial.write(firstSensor);
    //Serial.write(secondSensor);
    //Serial.write(thirdSensor); 
    if (inByte == 'm')
    {
     sensors_event_t humidity, temp;   // Data structures for storing sensor data

    digitalWrite(GREEN_LED, HIGH);    // Turn green LED on to ind
    
    shtc3.getEvent(&humidity, &temp); // Populate temp and humidity objects with fresh data
    digitalWrite(GREEN_LED, LOW);     // Turn green LED off after measurement is complete

    // Transmit aquired values:
    //Serial.print("Temp & Humidity: ");  
    Serial.print(temp.temperature); 
    Serial.print(",");
    Serial.println(humidity.relative_humidity); //Serial.println(" %, rH");
   
    }
   
  }
}
