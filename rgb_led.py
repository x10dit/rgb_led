from machine import Pin, PWM
import utime

led_colours_low = {
    "off":(1, 1, 1),
    "blue":(1, 1, 0),
    "green":(1, 0, 1),
    "cyan":(1, 0, 0),
    "red":(0, 1, 1),
    "pink":(0, 1, 0),
    "yellow":(0, 0, 1),
    "white":(0, 0, 0),
    }

led_colours_high = {
    "off":(0, 0, 0),
    "blue":(0, 0, 1),
    "green":(0, 1, 0),
    "cyan":(0, 1, 1),
    "red":(1, 0, 0),
    "pink":(1, 0, 1),
    "yellow":(1, 1, 0),
    "white":(1, 1, 1),
    }


class RGBLED:

    def __init__(self,
                 rd_led=None, # GPIO Pin.OUT or PWM Object
                 gn_led=None, # GPIO Pin.OUT or PWM Object
                 bl_led=None, # GPIO Pin.OUT or PWM Object
                 on_polarity="low", # high or low (default)
                 pwm_freq=1000,
                 **kwargs):
        """
        Args:
        rd_led : A GPIO Pin and/or PWM
        gn_led : A GPIO Pin and/or PWM
        bl_led : A GPIO Pin and/or PWM
        on_polarity : Usually set low for common anode LED or high for common cathode LED
        pwm_freq : Set desired PWM frequency
        """

        if type(rd_led) is Pin:
            if type(gn_led) is not Pin or type(bl_led) is not Pin:
                raise ValueError("All led objects must be the same type Pin.OUT or PWM")
            else:
                self.led_type = "pin"
        elif type(rd_led) is PWM:
            if type(gn_led) is not PWM or type(bl_led) is not PWM:
                raise ValueError("All led objects must be the same type Pin.OUT or PWM")
            else:
                self.led_type = "pwm"
        else:
            raise ValueError("All led objects must be eithe Pin.OUT or PWM")
        
        self.rd_led = rd_led
        self.gn_led = gn_led
        self.bl_led = bl_led

        if on_polarity == "low":
            self.led_colours = led_colours_low
        else:
            self.led_colours = led_colours_high
            
        if self.led_type == "pwm":
            self.rd_led.freq(pwm_freq)
            self.gn_led.freq(pwm_freq)
            self.bl_led.freq(pwm_freq)
            self.rd_led.duty_u16(65535)
            self.gn_led.duty_u16(65535)
            self.bl_led.duty_u16(65535)
        else:
            self.led_colour("off")
            
        
    def set_led_colour(self, led_colour=None):
        set_rd, set_gn, set_bl = led_colour
        self.rd_led.value(set_rd)
        self.gn_led.value(set_gn)
        self.bl_led.value(set_bl)

    def led_colour(self, colour=None, red=None, green=None, blue=None):
        if self.led_type == "pin":
            if colour in self.led_colours:
                self.set_led_colour(self.led_colours[colour])
            else:
                raise ValueError("Colour value is not a valid colour")
        else:
            if red >= 0 and red <= 65535 and green >= 0 and green <= 65535 and blue >= 0 and blue <= 65535:
                self.rd_led.duty_u16((red - 65535) * -1)
                self.gn_led.duty_u16((green - 65535) * -1)
                self.bl_led.duty_u16((blue - 65535) * -1)
            else:
                raise ValueError("RGB colour values must be between 0 and 65535")


def rgb_led_test():
    rd_led = machine.Pin(18, Pin.OUT)
    gn_led = machine.Pin(17, Pin.OUT)
    bl_led = machine.Pin(16, Pin.OUT)
    status_led = RGBLED(rd_led, gn_led, bl_led, on_lvl="low")
    status_led.led_colour("blue")
    utime.sleep(1)
    status_led.led_colour("green")
    utime.sleep(1)
    status_led.led_colour("cyan")
    utime.sleep(1)
    status_led.led_colour("red")
    utime.sleep(1)
    status_led.led_colour("pink")
    utime.sleep(1)
    status_led.led_colour("yellow")
    utime.sleep(1)
    status_led.led_colour("white")
    utime.sleep(1)
    status_led.led_colour("off")

    rd_led = machine.PWM(Pin(18))
    gn_led = machine.PWM(Pin(17))
    bl_led = machine.PWM(Pin(16))
    status_led = RGBLED(rd_led, gn_led, bl_led, on_lvl="low")
    # Fade the LED in and out a few times.
    duty = 0
    direction = 1
    for _ in range(2048):
        duty += direction
        if duty > 255:
            duty = 255
            direction = -1
        elif duty < 0:
            duty = 0
            direction = 1
        if _ >= 0 and _ < 683:
            status_led.led_colour(red=duty * 257, green=0, blue=0)
        elif _ >= 683 and _ < 1366:
            status_led.led_colour(red=0, green=duty * 257, blue=0)
        else:
            status_led.led_colour(red=0, green=0, blue=duty * 257)
        utime.sleep(0.005)
        
if __name__ == "__main__":
    rgb_led_test()
