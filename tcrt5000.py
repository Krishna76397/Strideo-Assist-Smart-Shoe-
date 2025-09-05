# TCRT5000 wrapper (surface reflectivity) with ADS1x15 analog read support
try:
    import board, busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    HW = True
except Exception:
    HW = False

import random

class TCRTWrapper:
    def __init__(self, channel=0, simulate=False):
        self.simulate = simulate or (not HW)
        if not self.simulate:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.ads = ADS.ADS1115(i2c)
            self.chan = AnalogIn(self.ads, ADS.P0 + channel)
        else:
            print("TCRT: simulation mode")

    def read_raw(self):
        if self.simulate:
            return random.randint(1000, 32000)
        return self.chan.value

    def get_surface_type(self):
        v = self.read_raw()
        # simple thresholds (you can calibrate)
        if v < 8000:
            return "dark_surface"   # e.g., black mat
        elif v < 20000:
            return "normal"         # concrete, typical
        else:
            return "reflective"     # tile or shiny
