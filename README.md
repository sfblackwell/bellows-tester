# Vintage-Camera Bellows Tester

## Simons @pimoroni Tiny2040 / BH1745 Based Vintage Camera Bellows Light Tighness Tester

##  Version 2 of the device has been created and the python code has had some clean up and minor changes, *key changes in italics*

### *** This is a work in progress, I am not a coder or programer, so please excuse the chaos ***

This is a small device for testing the light tighness of vintage cameras.

Vintage cameras often use cloth bellows and light seals. These wear over time and can start to allow light through which can spoil the film in the camera

This is a *version 2 prototype* of a device that can be placed inside the camera to detect any light leakage. 

*The code has been cleaned up a bit.*

- *Key settings*:
  - *REPL output is enabled by making*
    - *DEBUG = True*
  - *The delay before testing starts* 
    - *START_DELAY  = 20*
   - *Number of tests*
     -  *LOOPS = 10*
    
~~The device is about an 30mm * 30mm * 15 mm. The aim is to have a second version that is about 20mm * 25 * 10mm so it can be built in to a film canister~~

*Version 2 is now 25mm * 28mm * 15mm and while not quite as small as hoped, but is of much better and secure construction*

To operate, the device is switched on it is place inside the camera the rear cover is closed. After a delay the device will make a series of light readings over a period of time and will store them in a file with *a name based on the time and date the test was carried out*. This file can then be viewed on a computer.

- *At the end of the test run*:
  - *The LED's on the BH1745 are set ON for light detected (Fail) or OFF for light not detected (Pass)*
  - *The LED's on the Tiny2040 are set to RED for light detected (Fail) or Green for light not detected (Pass)* 
    - *The Tiny2040 LED's can be viewed thru the side of the case*

### Key parameters towards start of code used to control functionality

DEBUG  = True		#	True = Very vebose REPL debug messages oe execution progress messages

or

DEBUG  = False	#	False = No REPL debug messages or progress messages

LED_SLEEP    = 0.5	# startup LED flash delay 
FLASH_LOOPS  = 5		# startup LED flash count

START_DELAY  = 20 	#	delay after LEDS flash before readings start to be taken
LOOPS        = 10		#	number of reading to be taken
LOOPS_LIGHTS = 2		#	number of readings at start and end taken with bh1745 sensor LED on (test readings)

READING_WAIT = 0.5	#	delay before readings taken in loop
LOOP_WAIT    = 2		#	delay at end of oop before next loop

estTime = START_DELAY + (LOOPS * (LOOP_WAIT + READING_WAIT + READING_WAIT))		#	etimated total test time in seconds

Any questions, feel free to ask

### Items Used:

- Processor   [Tiny2040 RP2040 development board](https://shop.pimoroni.com/products/tiny-2040?variant=39560012234835)
- I2C Sensor  [BH1745 Luminance and Colour Sensor Breakout](https://shop.pimoroni.com/products/bh1745-luminance-and-colour-sensor-breakout)
- Battery     [Adafruit 20mm Coin Cell Breakout w/On-Off](https://shop.pimoroni.com/products/adafruit-20mm-coin-cell-breakout-w-on-off-switch-cr2032?variant=821160901)
- Micropython [pimoroni-tiny2040-v1.19.16-micropython](https://github.com/pimoroni/pimoroni-pico/releases/download/v1.19.17/pimoroni-tiny2040-v1.19.17-micropython.uf2)
- Case        [Adapted 3d Printed Case ](https://www.printables.com/model/166430-case-for-adafruit-qt-py-rp2040-and-seeed-xiao-rp20)

A few pictures:

*Device Version 2 Pictures:*

![20230516_143148196_iOS](https://github.com/sfblackwell/vintage-camera-bellows-tester/assets/122044826/ca48cf91-c169-4742-95db-acd7dbe44c35)
![20230516_143148326_iOS](https://github.com/sfblackwell/vintage-camera-bellows-tester/assets/122044826/bf388567-c57f-487d-9acd-1e682c306d6a)
![20230516_143148528_iOS](https://github.com/sfblackwell/vintage-camera-bellows-tester/assets/122044826/0862030b-aeca-4779-8c04-7b448d23d465)

Device Version 1 Pictures: 

![sfb20230324_135119125_iOS](https://user-images.githubusercontent.com/122044826/227643167-04a63aa0-db60-46e2-8a91-41ccb641a7ea.jpg)
![sfb20230324_135301384_iOS](https://user-images.githubusercontent.com/122044826/227643170-cc44c6c6-4bff-41bc-ab28-e98cc89ba21e.jpg)
![sfb20230324_135310196_iOS](https://user-images.githubusercontent.com/122044826/227643171-db75a86b-7d8e-4d85-8a21-47e790c1387a.jpg)

