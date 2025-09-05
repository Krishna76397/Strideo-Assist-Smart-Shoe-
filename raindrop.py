# Raindrop/wet floor detector (digital input)
try:
    import RPi.GPIO as GPIO
    HW = True
except Exception:
    HW = False
import random

class RainWrapper:
    def __init__(self, pin=17, simulate=False):
        self.simulate = simulate or (not HW)
        self.pin = pin
        if not self.simulate:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN)
        else:
            print("Rain: simulation mode")

    def is_wet(self):
        if self.simulate:
            return random.random() < 0.05
        return GPIO.input(self.pin) == GPIO.HIGH
