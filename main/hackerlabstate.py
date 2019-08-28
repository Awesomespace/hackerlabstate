import esp, network, urequests
from . import credentials
from machine import Pin
from time import sleep, sleep_ms
from umqtt.robust import MQTTClient

node_id = "hackerlabstate"

mqtt_host = "statsdingen.ass"
mqtt_topic = "ass/hackerlabstate"

button_pin = 5

class HackerLabState:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

        ap = network.WLAN(network.AP_IF)
        ap.active(False)

        self.mqtt = MQTTClient(node_id, mqtt_host)

        self.do_connect()

        pin = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.state_changed)

        while True:
            pass

    def do_connect(self):
        if not self.wlan.isconnected():
            print("Connecting to wifi...")
            self.wlan.connect(credentials.wifi_ssid, credentials.wifi_password)
            while not self.wlan.isconnected():
                pass
            print("Network config: ", self.wlan.ifconfig())

            print("Connecting to MQTT...")
            if not self.mqtt.connect():
                print("Connected")
            else:
                print("Could not connect")

    def state_changed(self, pin):
        pin_value = pin.value()
        active = 0
        while active < 100:
            if pin.value() != pin_value:
                active += 1
            else:
                active = 0
            sleep_ms(1)

        print("State ", pin_value)
        self.mqtt.publish(mqtt_topic, b"1" if pin_value == 1 else b"0")

        if pin_value == 1:
            state = "OPEN"
        else:
            state = "CLOSED"
        urequests.get("https://slack.com/api/chat.postMessage?token=%s&channel=hackerlab&text=Hackerlab%%20is%%20%s" % ( credentials.slack_token, state ) )
