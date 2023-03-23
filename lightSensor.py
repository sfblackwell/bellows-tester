import time
import utime
import os
import uos
import pimoroni_i2c
import breakout_bh1745
import machine 

CONSOLE  = True

START_LEDS	 = False
START_DELAY  = 5
LOOPS        = 10
LOOPS_LIGHTS = 2
LED_ON_LOW   = LOOPS_LIGHTS
LED_ON_HIGH  = (LOOPS - LOOPS_LIGHTS) - 1

LOOP_WAIT    = 2
FLASH_LOOPS  = 4

DELIMITER0 = "*******************************"
DELIMITER1 = "==============================="

try:
    LIGHTSENSOR = {"sda": 0, "scl": 1}
    I2C = pimoroni_i2c.PimoroniI2C(**LIGHTSENSOR)
    bh1745 = breakout_bh1745.BreakoutBH1745(I2C)
    bh1745.leds(False)
except:
    print("===> No sensor found") 

def sensorRead():  
    
    rgbc_raw = bh1745.rgbc_raw()
    rgb_clamped = bh1745.rgbc_clamped()
    brightness=rgbc_raw[3]
    
    if rgbc_raw[0] > 0 or rgbc_raw[1] > 0 or rgbc_raw[2] > 0 or rgbc_raw[3] > 0 or rgb_clamped[0] > 0 or rgb_clamped[1] > 0 or rgb_clamped[2] > 0 or rgb_clamped[3] > 0:
        anythingSeen = True
    else:
        anythingSeen = False

    return rgbc_raw, rgb_clamped, brightness, anythingSeen

def writeLineResult(loopy, ts, raw, clamped, bright, led, anyLightText, delimit):
    
    f = open("result.txt", "a")
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
    
def writeFinalResult(anyLightText, delimit):
    
    f = open("result.txt", "a") 
    f.write(anyLightText + "\n")
    f.write(delimit + "\n")
    f.close()

#	setup and flash leds at startup

r = machine.Pin(18, machine.Pin.OUT)
g = machine.Pin(19, machine.Pin.OUT)
b = machine.Pin(20, machine.Pin.OUT)

if START_LEDS:
    for i in range(FLASH_LOOPS):
        r.value(False)
        g.value(False)
        b.value(False)
        bh1745.leds(False)
        time.sleep(0.5)
        r.value(True)
        g.value(True)
        b.value(True)
        bh1745.leds(True)
        time.sleep(0.5)
    bh1745.leds(False)
else:
    bh1745.leds(False)
    r.value(True)
    g.value(True)
    b.value(True)

if CONSOLE:
    print("Startup wait: ", START_DELAY)
    for i in range(START_DELAY):
        print("Wait: ", i)
        time.sleep(1)

anyLightAtAll = False

for loop in range(0,LOOPS):
    
    if loop == 0:
        loopy =         DELIMITER0 + "\n"
        loopy = loopy + "Start of test\n"
        loopy = loopy + DELIMITER0 + "\n"
    else:
        loopy = ""
    
    loopy = loopy + "Loop:       {}".format(loop)
    ts 	  = "TS:         {}".format(utime.time())  
    
    if loop < LED_ON_LOW or loop > LED_ON_HIGH:
        bh1745.leds(True)
        led = "LED:        On"
        ledOn = True
    else:
        bh1745.leds(False)
        led = "LED:        Off"
        ledOn = False
    
    time.sleep(.5)  
    rgbc_raw, rgb_clamped, brightness, anylight = sensorRead()
    time.sleep(.5)
    bh1745.leds(False)

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
    
    writeLineResult(loopy, ts, raw, clamped, bright, led, anyLightText, delimit)
    
    if CONSOLE:
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

bh1745.leds(False)

#	print final result to file, console and display result on back of case  

if anyLightAtAll:
    anyLightText = "Light Detected"
    r.value(False)
    g.value(True)
    b.value(True)
else:
    anyLightText = "Light NOT Detected"
    r.value(True)
    g.value(False)
    b.value(True)

if CONSOLE:
    print(anyLightText)
    writeFinalResult(anyLightText, delimit)
