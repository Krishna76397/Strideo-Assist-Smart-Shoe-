"""
Strideo-Assist main orchestrator (simulation-friendly)

Run with --simulate to use fake sensor data.
"""
import argparse
import time
import threading
from modules import vl53, ultrasonic_servo, gps_telegram, tcrt5000, fsr, raindrop, image_recognition, tts_alert, utils

def periodic_status(controller, interval=10):
    while True:
        loc = controller['gps'].get_location()
        steps = controller['fsr'].get_steps()
        surface = controller['tcrt'].get_surface_type()
        print(f"[STATUS] Location: {loc} | Steps: {steps} | Surface: {surface}")
        time.sleep(interval)

def main(simulate=False):
    # initialize modules
    vl = vl53.VL53Wrapper(simulate=simulate)
    us = ultrasonic_servo.UltrasonicServo(simulate=simulate)
    gps = gps_telegram.GPSWrapper(simulate=simulate)
    tcrt = tcrt5000.TCRTWrapper(simulate=simulate)
    fsr_sensor = fsr.FSRWrapper(simulate=simulate)
    rain = raindrop.RainWrapper(simulate=simulate)
    tts = tts_alert.TTSWrapper(simulate=simulate)

    controller = {'vl53': vl, 'us': us, 'gps': gps, 'tcrt': tcrt, 'fsr': fsr_sensor, 'rain': rain, 'tts': tts}

    # start ultrasonic sweep in background
    threading.Thread(target=us.start_sweep, args=(controller,), daemon=True).start()

    # start periodic status print
    threading.Thread(target=periodic_status, args=(controller,10), daemon=True).start()

    try:
        while True:
            # check emergency button (simulated via gps module method)
            if gps.check_emergency():
                msg = f"EMERGENCY! Location: {gps.get_location(link=True)}"
                print("[ALERT]", msg)
                gps.send_telegram_alert(msg)
                tts.speak("Emergency detected. Help is on the way.")
            # raindrop/wet detection
            if rain.is_wet():
                print("[ALERT] Wet surface detected")
                tts.speak("Caution. Wet surface detected")
            # surface type
            surface = tcrt.get_surface_type()
            if surface != "normal":
                print(f"[INFO] Surface: {surface}")
                tts.speak(f"Surface detected: {surface}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--simulate', action='store_true', help='Run in simulation mode (no hardware required)')
    args = parser.parse_args()
    main(simulate=args.simulate)
