#DEBUG  = True		#	True = Very vebose REPL debug messages
DEBUG  = False		#	False = No REPL debug messages

if DEBUG: print("\n===> Starting Bellows Light Sensor Code\n")

import time
import utime
import os
import uos
import pimoroni_i2c
import breakout_bh1745
import machine 

LED_SLEEP    = 0.5		# 	startup LED flash delay 
FLASH_LOOPS  = 5		# 	startup LED flash count

START_DELAY  = 20 		#	delay after LEDS flash before readings start to be taken
LOOPS        = 10		#	number of reading to be taken
LOOPS_LIGHTS = 2		#	number of readings at start and end taken with bh1745 sensor LED on (test readings)

LED_ON_LOW   = LOOPS_LIGHTS
LED_ON_HIGH  = (LOOPS - LOOPS_LIGHTS) - 1

READING_WAIT = 0.5		#	delay before readings taken in loop
LOOP_WAIT    = 2		#	delay at end of oop before next loop

estTime = START_DELAY + (LOOPS * (LOOP_WAIT + READING_WAIT + READING_WAIT))		#	etimated total test time in seconds

if DEBUG: print("===> Estimated test duration once sensor LED's stop flashing", estTime)

DELIMITER0 = "*******************************"
DELIMITER1 = "==============================="

try:
    LIGHTSENSOR = {"sda": 0, "scl": 1}
    I2C = pimoroni_i2c.PimoroniI2C(**LIGHTSENSOR)
    bh1745 = breakout_bh1745.BreakoutBH1745(I2C)
    bh1745.leds(False)
    if DEBUG: print("===> BH1745 Sensor found")
except:
    print("===> No sensor found")
    sys.exit("No sensor found, Cannot continue")

def sensorRead():  
    
    rgbc_raw = bh1745.rgbc_raw()
    rgb_clamped = bh1745.rgbc_clamped()
    brightness=rgbc_raw[3]
    
    if rgbc_raw[0] > 0 or rgbc_raw[1] > 0 or rgbc_raw[2] > 0 or rgbc_raw[3] > 0 or rgb_clamped[0] > 0 or rgb_clamped[1] > 0 or rgb_clamped[2] > 0 or rgb_clamped[3] > 0:
        anythingSeen = True
    else:
        anythingSeen = False

    return rgbc_raw, rgb_clamped, brightness, anythingSeen

def writeLineResult(resultsFile, loopy, ts, raw, clamped, bright, led, anyLightText, delimit):
    
    f = open(resultsFile, "a")
    f.write(loopy + "\n")
    f.write(ts + "\n")
    f.write(led + "\n")
    f.write(raw + "\n")
    f.write(clamped + "\n")
    f.write(bright + "\n")
    if anyLightText != "":
        f.write(anyLightText + "\n")
    f.write(delimit + "\n")
    f.close()
    
def writeFinalResult(resultsFile, anyLightText, delimit):
    
    f = open(resultsFile, "a") 
    f.write(anyLightText + "\n")
    f.write(delimit + "\n")
    f.close()

#
#	setup and flash leds at startup to show unit is alive and kicking
#

r = machine.Pin(18, machine.Pin.OUT)
g = machine.Pin(19, machine.Pin.OUT)
b = machine.Pin(20, machine.Pin.OUT)

#	True is OFF

r.value(True)
g.value(True)
b.value(True)

#	Flash the sensor LED

for i in range(FLASH_LOOPS):
    bh1745.leds(True)
    time.sleep(LED_SLEEP)
    bh1745.leds(False)
    time.sleep(LED_SLEEP)

#
#	lets wait while user gets set up
#

if DEBUG: print("===> Startup wait: ", START_DELAY)
for i in range(START_DELAY):
    if DEBUG: print(".",end="")
    time.sleep(1)
if DEBUG: print("")
if DEBUG: print("\n")
#
#	setup for a date-time based file name
#

pyear, pmonth, pday, phour, pminute, psecond, pweekday, pyearday = time.localtime()
timeString  = "result-{:04}{:02}{:02}-{:02}{:02}{:02}.txt"
resultsFile = timeString.format(pyear, pmonth, pday, phour, pminute, psecond)
if DEBUG: print("Results file name: ", resultsFile)

#
#	into the main loop
#

anyLightAtAll = False

for loop in range(0,LOOPS):
    
    #
    #	header for each loop
    #

    if loop == 0:
        loopy =         DELIMITER0 + "\n"
        loopy = loopy + "Start of test\n"
        loopy = loopy + DELIMITER0 + "\n"
    else:
        loopy = ""
    
    loopy = loopy + "Loop:       {}".format(loop)
    
    pyear, pmonth, pday, phour, pminute, psecond, pweekday, pyearday = time.localtime()
    timeString = "TS:         {:02}:{:02}:{:02} {:04}/{:02}/{:02}"
    ts     = timeString.format(phour, pminute, psecond, pyear, pmonth, pday)
    
    if loop < LED_ON_LOW or loop > LED_ON_HIGH:
        #
        #	test bh1745 sensor is woking by doing a loop with LED on
        #        
        bh1745.leds(True)
        led = "LED:        On"
        ledOn = True
        if DEBUG: print("===> test loop with bh1745 sensor LED on")
    else:
        #
        #	actual reading with bh1745 sensor LED off
        #        
        bh1745.leds(False)
        led = "LED:        Off"
        ledOn = False
        if DEBUG: print("===> proper reading with bh1745 sensor LED off")
        
    #	get a light reading
 
    time.sleep(READING_WAIT)  
    rgbc_raw, rgb_clamped, brightness, anylight = sensorRead()
    time.sleep(READING_WAIT)
    bh1745.leds(False)

    #	set up results text
    
    if not ledOn and anylight:
        anyLightAtAll = True
        anyLightText = "Light Detected"
    elif not ledOn :
        anyLightText = "Light NOT Detected"
    else:
        anyLightText = ""
                
    raw 	= "Raw:        {}, {}, {}, {}".format(*rgbc_raw)
    clamped = "Clamped:    {}, {}, {}, {}".format(*rgb_clamped)
    bright  = "Brightness: {}".format(brightness)
    delimit = DELIMITER1
    
    writeLineResult(resultsFile, loopy, ts, raw, clamped, bright, led, anyLightText, delimit)
    
    #	console text if needed
    
    if DEBUG:
        print(loopy)
        print(ts)
        print(led)
        print(raw)
        print(clamped)
        print(bright)
        if anyLightText != "":
            print(anyLightText) 
        print(delimit)
        
    time.sleep(LOOP_WAIT)

#	all done, turn of led

bh1745.leds(False)

#	print final result to file, console and display result on back of case

#	ANY light detected = BH1745 sensor LED will be ON  & Tiny2040 LED will be RED

#	NO light detected  = BH1745 sensor LED will be OFF & Tiny2040 LED will be GREEN

if anyLightAtAll:
    anyLightText = "Light Detected"
    r.value(False)
    g.value(True)
    b.value(True)
    
    bh1745.leds(True)
else:
    anyLightText = "Light NOT Detected"
    r.value(True)
    g.value(False)
    b.value(True)
    
    bh1745.leds(False)

writeFinalResult(resultsFile, anyLightText, delimit)
if DEBUG: print("Final result: ", anyLightText)
if DEBUG: print(DELIMITER1)
