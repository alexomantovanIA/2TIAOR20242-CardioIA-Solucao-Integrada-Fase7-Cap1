from machine import Pin
from time import sleep, time
import random

try:
    import network
    import urequests
except ImportError:
    network = None
    urequests = None


WIFI_SSID = ""
WIFI_PASSWORD = ""
API_URL = ""  # Exemplo: "http://192.168.0.10:5000/api/iot/ingest"
DEVICE_ID = "wokwi-esp32-cardioia"

LED_RED = Pin(25, Pin.OUT)
LED_GREEN = Pin(26, Pin.OUT)
LED_BLUE = Pin(27, Pin.OUT)


def set_rgb(red, green, blue):
    LED_RED.value(1 if red else 0)
    LED_GREEN.value(1 if green else 0)
    LED_BLUE.value(1 if blue else 0)


def classify_status(heart_rate, temperature, spo2):
    if heart_rate < 45 or heart_rate > 130 or spo2 < 90 or temperature >= 38.5:
        return "critico"
    if heart_rate < 55 or heart_rate > 100 or spo2 < 95 or temperature >= 37.8:
        return "atencao"
    return "normal"


def show_status(status):
    if status == "critico":
        set_rgb(1, 0, 0)
    elif status == "atencao":
        set_rgb(1, 1, 0)
    else:
        set_rgb(0, 1, 0)


def simulated_vitals():
    scenario = random.randint(0, 10)
    if scenario >= 9:
        heart_rate = random.randint(132, 155)
        temperature = round(random.uniform(38.5, 39.2), 1)
        spo2 = random.randint(86, 91)
    elif scenario >= 6:
        heart_rate = random.randint(101, 124)
        temperature = round(random.uniform(37.8, 38.3), 1)
        spo2 = random.randint(92, 95)
    else:
        heart_rate = random.randint(64, 92)
        temperature = round(random.uniform(36.2, 37.4), 1)
        spo2 = random.randint(96, 99)
    return heart_rate, temperature, spo2


def connect_wifi():
    if not network or not WIFI_SSID:
        print("Wi-Fi desativado; simulacao local.")
        return False

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando ao Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        for _ in range(20):
            if wlan.isconnected():
                break
            sleep(0.5)

    if wlan.isconnected():
        print("Wi-Fi conectado:", wlan.ifconfig()[0])
        return True

    print("Falha ao conectar Wi-Fi.")
    return False


def post_reading(payload):
    if not API_URL or not urequests:
        return
    try:
        response = urequests.post(API_URL, json=payload)
        print("POST backend:", response.status_code)
        response.close()
    except Exception as exc:
        print("Falha ao enviar leitura:", exc)


wifi_ready = connect_wifi()

while True:
    heart_rate, temperature, spo2 = simulated_vitals()
    status = classify_status(heart_rate, temperature, spo2)
    show_status(status)

    payload = {
        "device_id": DEVICE_ID,
        "heart_rate": heart_rate,
        "temperature": temperature,
        "spo2": spo2,
        "timestamp": str(time()),
    }

    print(
        "CardioIA IoT | FC:",
        heart_rate,
        "bpm | Temp:",
        temperature,
        "C | SpO2:",
        spo2,
        "% | Status:",
        status,
    )

    if wifi_ready:
        post_reading(payload)

    sleep(5)
