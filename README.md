# Strideo-Assist — E-Shoe for the Visually Impaired

This repository contains software for the **Strideo-Assist** smart shoe described in the project PDF.
It includes Python modules for:
- VL53L0X ToF sensors (topography)
- Ultrasonic + servo sweeping object detection
- Neo-6M GPS + reverse-geocoding (Geopy)
- Emergency Telegram alerts
- TCRT5000 surface analysis
- FSR-based step counting & calorie estimate
- Raindrop (wet floor) detection
- Image recognition (VGG16 example)
- TTS alerts (espeak) and buzzer control

Files are written to be **Raspberry Pi friendly** but include simulation fallbacks so you can run on a regular PC for testing.

## Structure
```
Strideo-Assist/
├─ README.md
├─ requirements.txt
├─ main.py
├─ modules/
│  ├─ vl53.py
│  ├─ ultrasonic_servo.py
│  ├─ gps_telegram.py
│  ├─ tcrt5000.py
│  ├─ fsr.py
│  ├─ raindrop.py
│  ├─ image_recognition.py
│  ├─ tts_alert.py
│  └─ utils.py
```

## How to run (simulation)
1. Create virtualenv & install requirements:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the main orchestrator (simulation mode):
   ```bash
   python3 main.py --simulate
   ```

## Hardware notes
- Follow the pin comments in each module for wiring on Raspberry Pi.
- Install the required hardware libraries on the Pi (Adafruit CircuitPython libraries, RPi.GPIO, pyserial, etc.).

---
