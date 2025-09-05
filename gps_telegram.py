# GPS (Neo6M) + Telegram alert wrapper
import time, threading
try:
    import serial, pynmea2
    HW = True
except Exception:
    HW = False
import requests

class GPSWrapper:
    def __init__(self, port="/dev/ttyS0", baud=9600, simulate=False, telegram_token=None, chat_id=None):
        self.simulate = simulate or (not HW)
        self.port = port
        self.baud = baud
        self.telegram_token = telegram_token or ""
        self.chat_id = chat_id or ""
        self.latest = {"lat": None, "lon": None}
        if not self.simulate:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
            threading.Thread(target=self._reader, daemon=True).start()
        else:
            print("GPS: simulation mode")

    def _reader(self):
        while True:
            line = self.ser.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                try:
                    msg = pynmea2.parse(line)
                    if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                        self.latest['lat'] = msg.latitude
                        self.latest['lon'] = msg.longitude
                except Exception:
                    pass

    def get_location(self, link=False):
        if self.simulate:
            return "12.9716,77.5946" if not link else "https://maps.google.com/?q=12.9716,77.5946"
        if self.latest['lat'] and self.latest['lon']:
            if link:
                return f"https://maps.google.com/?q={self.latest['lat']},{self.latest['lon']}"
            return f\"{self.latest['lat']},{self.latest['lon']}\"
        return "Unknown"

    def check_emergency(self):
        # placeholder for button press; in simulation returns False
        return False

    def send_telegram_alert(self, message):
        if not self.telegram_token or not self.chat_id:
            print("[Telegram] Token/Chat ID not configured. Alert:", message)
            return False
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message}
        try:
            r = requests.post(url, data=data, timeout=5)
            return r.ok
        except Exception as e:
            print("Telegram send error:", e)
            return False
