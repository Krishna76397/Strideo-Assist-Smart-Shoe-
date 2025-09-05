# VL53L0X wrapper with simulation fallback
try:
    import board, busio
    import adafruit_vl53l0x
    HW = True
except Exception:
    HW = False
import random, time

class VL53Wrapper:
    def __init__(self, simulate=False):
        self.simulate = simulate or (not HW)
        if not self.simulate:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_vl53l0x.VL53L0X(i2c)
        else:
            print("VL53: running in simulation mode")

    def get_distance(self):
        if self.simulate:
            # simulate values between 20cm and 200cm
            return random.randint(20,200)
        else:
            return self.sensor.range
