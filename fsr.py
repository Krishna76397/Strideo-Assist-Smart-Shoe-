# FSR wrapper using ADS1115 for analog readings; simple step counter
import time, random
try:
    import board, busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    HW = True
except Exception:
    HW = False

class FSRWrapper:
    def __init__(self, channel=1, threshold=10000, simulate=False):
        self.simulate = simulate or (not HW)
        self.threshold = threshold
        self.steps = 0
        self.last_state = False
        if not self.simulate:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.ads = ADS.ADS1115(i2c)
            self.chan = AnalogIn(self.ads, ADS.P0 + channel)
        else:
            print("FSR: simulation mode")

    def read_raw(self):
        if self.simulate:
            # simulate step events occasionally
            if random.random() < 0.1:
                return self.threshold + 2000
            return random.randint(1000, self.threshold - 1)
        return self.chan.value

    def update(self):
        val = self.read_raw()
        pressed = val > self.threshold
        if pressed and not self.last_state:
            self.steps += 1
        self.last_state = pressed
        return self.steps

    def get_steps(self):
        # call update before get_steps in a loop for real counting
        self.update()
        return self.steps

    def estimate_calories(self, weight_kg=60):
        # rough estimate: calories per step ~ 0.05 kcal
        return round(self.steps * 0.05 * (weight_kg/60),2)
