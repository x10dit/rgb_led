# rgb_led
A simple Python class to interface an RGB 4-lead Common Anode or Common Cathode LED with a Raspberry Pi Pico.  
You'll need 3 free GPIO pins to drive the LED.
You can either drive the output level of the pins directly or use a PWM.
You can use common cathode or common anode by initialising the appropriate "on_lvl" argument.
In PWM mode you can set the PWM frequency with the "pwm_freq" argument.

Copy rgb_led.py into your project

import rgb_led

# Driving the pin levels directly
#Initialise the led output pins

bl_led = machine.Pin(16, Pin.OUT)

gn_led = machine.Pin(17, Pin.OUT)

rd_led = machine.Pin(18, Pin.OUT)

#Initialise the tri-colour status led

status_led = rgb_led.RGBLED(rd_led, gn_led, bl_led, on_lvl="low")

# Set the (approximate) colour of the LED
#Colour can be any one of blue, green, cyan, red, pink, yellow, white, off

status_led.led_colour("colour")

# Driving the pin with a PWM
#Initialise the led output pins

rd_led = machine.PWM(Pin(18))

gn_led = machine.PWM(Pin(17))

bl_led = machine.PWM(Pin(16))

#Initialise the tri-colour status led

status_led = RGBLED(rd_led, gn_led, bl_led, on_lvl="low", pwm_freq=1000)

#Configure the PWM duty values for red, green and blue channel

status_led.led_colour(red=65535, green=0, blue=0) # Red

status_led.led_colour(red=0, green=65535, blue=0) # Green

status_led.led_colour(red=0, green=0, blue=65535) # Blue
