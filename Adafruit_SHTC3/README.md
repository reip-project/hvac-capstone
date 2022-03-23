# Adafruit SHTC3 Temperature and Humidity Sensor Library [![Documentation](https://github.com/adafruit/ci-arduino/blob/master/assets/doxygen_badge.svg)](http://adafruit.github.io/Adafruit_SHTC3/html/index.html)

<a href="https://www.adafruit.com/product/4636"><img src="https://cdn-shop.adafruit.com/970x728/4636-03.jpg" width="500px"></a>

This is a library for the SHTC3 Digital Temp & Humidity sensor.

It is designed specifically to work with the SHTC3 Digital in the Adafruit shop:

* https://www.adafruit.com/products/4636

These sensors use **I2C** to communicate. 2 pins are required to interface: PB_2 (SCL) and PB_3 (SDA) for Tiva C (TM4C123GH6PM) microcontroller (port 0).

Written by Limor Fried/Ladyada for Adafruit Industries. Adapted by Yurii Piadyk for Energia and Tiva C (TM4C123GH6PM) MCU.
BSD license, all text above must be included in any redistribution

Check out the link below for the tutorials and wiring diagrams:

* https://learn.adafruit.com/adafruit-sensirion-shtc3-temperature-humidity-sensor

## Installation

Zip Adafruit_SHTC3 folder into Adafruit_SHTC3.zip. Then open [Energia IDE](https://energia.nu) and navigate to Sketch => Include Library => Add ZIP Library...
Choose Adafruit_SHTC3.zip archive and it will get copied into corresponding installation directory.

Navigate to File => Examples => Adafruit SHTC3 => SHTC3_Demo for an example of how to use the library.
The demo was designed to work with Tiva C [LaunchPad](https://www.ti.com/tool/EK-TM4C123GXL) and SHTC3 sensor [connected](https://learn.adafruit.com/adafruit-sensirion-shtc3-temperature-humidity-sensor/arduino) to I2C port #0:

<a href="https://www.ti.com/tool/EK-TM4C123GXL"><img src="https://energia.nu/pinmaps/img/EK-TM4C123GXL.jpg" width="1200px"></a>
