# Ultrasonic + Servo sweeping object detection (simulation-friendly)
import time, random
try:
    import RPi.GPIO as GPIO
    HW = True
except Exception:
    HW = False

class UltrasonicServo:
    def __init__(self, trigger_pin=23, echo_pin=24, servo_pin=18, simulate=False):
        self.simulate = simulate or (not HW)
        self.trigger = trigger_pin
        self.echo = echo_pin
        self.servo = servo_pin
        if not self.simulate:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.trigger, GPIO.OUT)
            GPIO.setup(self.echo, GPIO.IN)
            GPIO.setup(self.servo, GPIO.OUT)
            self.pwm = GPIO.PWM(self.servo, 50)
            self.pwm.start(7.5)
        else:
            print("UltrasonicServo: simulation mode")

    def measure_distance(self):
        if self.simulate:
            return random.randint(10,300)
        # real measurement
        GPIO.output(self.trigger, False)
        time.sleep(0.0002)
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
        pulse_start = time.time()
        timeout = pulse_start + 0.04
        while GPIO.input(self.echo)==0 and time.time() < timeout:
            pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.echo)==1 and time.time() < timeout:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        return round(distance,2)

    def sweep_once(self):
        # rotate servo across a sweep and read ultrasonic distances
        readings = []
        for angle in range(30,150,15):
            if not self.simulate:
                duty = 2 + (angle/18.0)
                self.pwm.ChangeDutyCycle(duty)
                time.sleep(0.2)
            distance = self.measure_distance()
            readings.append((angle, distance))
        return readings

    def start_sweep(self, controller=None):
        while True:
            readings = self.sweep_once()
            # look for close objects
            close = [r for r in readings if r[1] < 100]
            if close:
                print("[UltrasonicServo] Close objects:", close)
                if controller and 'tts' in controller:
                    controller['tts'].speak("Object ahead, please take caution")
            time.sleep(0.5)
