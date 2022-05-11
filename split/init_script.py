import random as r

# Initialization

# DHT Sensor Initialization
pin = 17
# dht = DHT.DHT(pin)

# LED Initialization
LED_PIN = 6
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(LED_PIN, GPIO.OUT)
# GPIO.output(LED_PIN, GPIO.LOW)
# state = 5 # TODO: What does this do?

# Email Initialization
# isMotorMailSent = False
# isLightMailSent = False
# sentEmailCount = 0 
# emailMessage = ""


# Motor Initialization
isMotorOn = False
motorStatus = "Motor is OFF"
Motor1A = 24
Motor1B = 23
Motor1E = 25
# GPIO.setup(Motor1A, GPIO.OUT)
# GPIO.setup(Motor1B, GPIO.OUT)
# GPIO.setup(Motor1E, GPIO.OUT)
# GPIO.output(Motor1E, GPIO.LOW)

# MQTT Initialization
# tempMsg = ""
# humidityMsg = ""
topic = [("IoT/light",0), ("IoT/humidity",0), ("IoT/temperature",0), ("IoT/rfid",0)]
client_id = f'python-mqtt-{r.randint(0,100)}'
username = "user"
password = "user"
broker = '192.168.113.208' # FIXME: Maybe find a way to ask for user input?
port = 1883

# Icon initialization
motorIconStatus = False
lightIconStatus = False
# profileIcons = [
#     # person icons
#     html.Img(src="assets/person.png", height=128, width=128),
#     html.Img(src="assets/person2.png", height=128, width=128),
# ]

# Profiles
users = [
    [
        'B3 72 85 0D',
        23,
        40,
        200
    ],
    [
        'E3 17 ED 15',
        24,
        50,
        300
    ]
]

# Helper Class with default values
class helper:
    lightIntensity = 0 # NOTE: Displays light value from 0-1000 (0-100%)
    humidityThresh = 60 # NOTE: Displays humidity threshold value from 20-80
    temperature = 0
    humidity = 0
    temperatureThresh = 80 # NOTE: Displays temperature threshold value from 20-100
    lightThresh = 800 # NOTE: Displays light threshold value from 0-1000 (0-100%)
    isLightOn = 'Light is OFF' # NOTE: checks
    motorStatusMsg = 'Light is ON' # NOTE: Displays motor status
    sentEmailCount = 0 # NOTE: Displays number of emails sent
    userTag = '' # NOTE: Displays user tag
    username = '' # NOTE: Displays username