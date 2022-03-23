/*************************************************** 
  This is a demo for the SHTC3 Temp & Humidity Sensor

  Designed specifically to work with the SHTC3 sensor from Adafruit
  ----> https://www.adafruit.com/products/4636

  These sensors use I2C to communicate. 2 pins are required to
  interface: PB_2 (SCL) and PB_3 (SDA) for Tiva C (TM4C123GH6PM) MCU
 ****************************************************/

#include "Adafruit_SHTC3.h"

Adafruit_SHTC3 shtc3 = Adafruit_SHTC3();

void setup() {
    // Initialize digital pins as outputs:
    pinMode(RED_LED, OUTPUT);  // LOW by default (LED off)
    pinMode(GREEN_LED, OUTPUT);

    Serial.begin(115200); // Use faster serial communication
    Wire.setModule(0);    // Tiva C microcontrollers have multiple I2C ports

    while (!Serial)
        delay(10);  // Should pause until serial console opens

    Serial.println("\nSHTC3 Demo:");

    if (!shtc3.begin()) {
        digitalWrite(RED_LED, HIGH);  // Turn red LED on to indicate error
        Serial.println("Couldn't find SHTC3 sensor!");
        while (1) delay(1);
    }
    Serial.println("Found SHTC3 sensor...");
}


void loop() {
    sensors_event_t humidity, temp;   // Data structures for storing sensor data

    digitalWrite(GREEN_LED, HIGH);    // Turn green LED on to indicate measurement
    shtc3.getEvent(&humidity, &temp); // Populate temp and humidity objects with fresh data
    digitalWrite(GREEN_LED, LOW);     // Turn green LED off after measurement is complete

    // Transmit aquired values:
    Serial.print("Temp & Humidity: ");  Serial.print(temp.temperature); Serial.print(" °C, ");
    Serial.print(humidity.relative_humidity); Serial.println(" %, rH");
    delay(1000); // Repeat every second
}