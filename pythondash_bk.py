# PythonDash for DHT11 sensor, including mailing functions as well as various
# other helper functions
# TODO: Test the entire code and make sure it works
# TODO: Test the new styling stuff for motor & LED
# TODO: Check if variables are being updated correctly
# TODO: Check if some vars need to be global or local
# TODO: Update Helper class if necessary
# FIXME: Check if the email is being sent correctly
# FIXME: Check if MQTT is properly handling responses to email requests
# FIXME: Some other stuff that I didn't take into account
# TODO: Phase 4 Implementation


# Importing modules
import time
from datetime import date
import random as r
# import Rpi.GPIO as GPIO # NOTE: This is for the Raspberry Pi, uncomment if using a Raspberry Pi
# import FreenoveDHT as DHT
import dash
import dash.dependencies
import dash_daq as daq
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
# from paho.mqtt import client as mqtt_client
import smtplib
import imaplib 
import email
import random
# import RPi.GPIO as GPIO

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
sourceAdd = 'pythonmailer9843098432@gmail.com'
destAdd = 'pythonmailer9843098432@gmail.com'
emailPassword = 'monkeyman123?'
imap_srv = 'imap.gmail.com'
imap_port = 993

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
profileIcons = [
    # person icons
    html.Img(src="assets/person.png", height=128, width=128),
    html.Img(src="assets/person2.png", height=128, width=128),
]

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
    lightIntensity = '' # NOTE: Displays light value from 0-1000 (0-100%)
    humidityThresh = 60 # NOTE: Displays humidity threshold value from 20-80
    temperatureThresh = 80 # NOTE: Displays temperature threshold value from 20-100
    lightThresh = 800 # NOTE: Displays light threshold value from 0-1000 (0-100%)
    isLightOn = '' # NOTE: checks
    motorStatusMsg = '' # NOTE: Displays motor status
    sentEmailCount = 0 # NOTE: Displays number of emails sent
    userTag = '' # NOTE: Displays user tag
    username = '' # NOTE: Displays username

# TODO: If need be, add more parameters to their respective categories as they come up

def get_temp_humidity():
    # dht = readDHT11()
    # temperature = dht.temperature
    # humidity = dht.humidity
    # if (temperature is not None) and (humidity is not None):
    #     return temperature, humidity
    # else:
        # return (0, 0) # TODO: Can also return (None, None) 
        return random.randint(0, 100), random.randint(0, 100), random.randint(200, 1000) # FIXME: Comment this line for production
# def connect_mqtt() -> mqtt_client:
#     print("Connecting to MQTT broker...")
#     def on_connect(client, userdata, flags, rc):
#         if rc == 0:
#             print("Connected to MQTT broker!\n")
#         else:
#             print("Failed to connect to broker, returned code: " + str(rc) + "\n")
#     client = mqtt_client.Client(client_id)
#     client.on_connect = on_connect
#     client.connect(broker, port)
#     return client

# def subscribeTopic(client: mqtt_client):
#     def on_message(client, userdata, msg):
#         lightMsg = ""
#         humidityMsg = ""
#         temperatureMsg = ""
#         isMotorMailSent = False
#         isLightMailSent = False
#         # sentEmailCount = 0 # FIXME: Replaced by helper but may need to localize instead
#         emailMessage = ""

#         # Debug message for receiving messages
#         # print(f"Received `{msg.payload.decode()}` on topic `{msg.topic}` from broker.\n")

#         # Sorts based on topic type
#         if (msg.topic == "IoT/light"):
#             lightMsg = int(msg.payload.decode())
#             helper.lightIntensity = lightMsg
#             # print(f"DBG --- Light intensity: {lightMsg}")
#         if (msg.topic == "IoT/humidity"):
#             humidityMsg = float(msg.payload.decode())
#             helper.humidityThresh = humidityMsg
#             # print(f"DBG --- Humidity: {humidityMsg}")
#         if (msg.topic == "IoT/temperature"):
#             temperatureMsg = float(msg.payload.decode())
#             # print(f"DBG --- Temperature: {temperatureMsg}")
#             helper.temperatureThresh = temperatureMsg
#             if (temperatureMsg > 20 and isMotorMailSent != True and helper.sentEmailCount == 0):
#                 # sendMotorNotificationEmail()
#                 helper.sentEmailCount += 1
#                 isMotorMailSent = True
#             else:
#                 helper.sentEmailCount = 0
#                 isMotorMailSent = False
    
#         if (msg.topic == "IoT/rfid"):
#             # sendProfileEmail()
#             helper.userTag = msg.payload.decode()
#             print(f"DBG --- User Tag: {helper.userTag}")
#             for user in users:
#                 if(user[0].lower() == helper.userTag.lower().strip()):
#                     helper.temperatureThresh = user[1]
#                     helper.humidityThresh = user[2]
#                     helper.lightThresh = user[3]  
#         # else:
#         #     print("DBG --- Unknown topic received.\n")
#         if (isMotorMailSent == True and helper.sentEmailCount == 1):
#             reply = receiveMail()
#         if (str(lightMsg) < "400" and isLightMailSent == False):
#             # print("-------------------------")
#             # print("DBG -- subscribeTopic > LightMsg: " + str(lightMsg))
#             # print("Email sending...")
#             # print("-------------------------")
#             isLightMailSent = True
#             helper.isLightOn = 'Light ON'
#             GPIO.output(LED_PIN, GPIO.HIGH) # Turn on LED
#             # sendLEDNotificationEmail()

#     client.subscribe(topic)
#     client.on_message = on_message
#     return helper.lightIntensity, helper.humidityThresh, helper.temperatureThresh, helper.isLightOn

def updateThresholds(var_name: str, var_value: int):
    if (var_name == "lightThresh"):
        helper.lightThresh = var_value
    elif (var_name == "humidityThresh"):
        helper.humidityThresh = var_value
    elif (var_name == "temperatureThresh"):
        helper.temperatureThresh = var_value
    elif (var_name == "username"):
        helper.username = var_value
    else:
        print("DBG -- updateThresholds > Unknown variable name.")

def sendProfileEmail():
    time = date.today()
    time = time.strftime("%d/%m/%Y")
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(sourceAdd, password)
    subject = "IoT Project - Profile"
    body = "User Tag: " + helper.userTag + " has logged in at " + time
    msg = f"Subject: {subject}\n\n{body}"

    s.sendmail(sourceAdd, destAdd, msg)
    s.quit()

def spinMotor():
    helper.motorStatusMsg = "Motor is ON"
    # GPIO.output(Motor1A, GPIO.HIGH)
    # GPIO.output(Motor1B, GPIO.LOW)
    # GPIO.output(Motor1E, GPIO.HIGH)

def sendLEDNotificationEmail():
    time = date.today()
    time = time.strftime("%d/%m/%Y")
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(sourceAdd, password)

    subject = "LED Status Notification"
    body = "The LED was set to ON at " + time
    msg = f"Subject: {subject}\n\n{body}"

    s.sendmail(sourceAdd, destAdd, msg)
    s.quit()

def sendMotorNotificationEmail():
    time = date.today()
    time = time.strftime("%d/%m/%Y")
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(sourceAdd, password)

    subject = "Motor Status Notification"
    body = "The motor was set to ON at " + time + " and is currently running. Would you like to ENABLE the fan?\n\n Type 'ENABLE' to enable the fan or 'DISABLE' to disable the fan."
    msg = f"Subject: {subject}\n\n{body}"

    s.sendmail(sourceAdd, destAdd, msg)
    s.quit()

def receiveMail():
    while True:
        print("Waiting for email...")
        conn = imaplib.IMAP4_SSL(imap_srv, imap_port)
        conn.login(sourceAdd, password)
        conn.select('INBOX')
        status, data = sourceAdd.search(None, 'FROM ' + destAdd + ' SUBJECT "LED Status Notification" UNSEEN')
        mail_ids = []
        for block in data:
            mail_ids += block.split()
        for i in mail_ids:
            status, data = sourceAdd.fetch(i, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1].decode('utf-8'))
                    email_from = msg['from']
                    email_subject = msg['subject']
                    print('From: ' + email_from + '\n')
                    print('Subject: ' + email_subject + '\n')
                    if msg.is_multipart():
                        mail_content = ''
                        for part in msg.get_payload():
                            if part.get_content_type() == 'text/plain':
                                mail_content = part.get_payload()
                                reply = f'Content: {mail_content}'
                                if ("YES" in reply):
                                    helper.sentEmailCount += 1
                                    spinMotor()
                                    helper.motorStatusMsg = "Motor is ON"
                                    return helper.motorStatusMsg
                    else:
                        mail_content = msg.get_payload()
                        return False
        time.sleep(10)

def checkProfile():
        if (helper.userTag == "B3 72 85 0D"):
            return 'person.png'
        elif (helper.userTag == "E3 17 ED 15"):
            return 'person2.png'
        else:
            return 'person.png'

def createDash():
    temperature = get_temp_humidity()[0]
    humidity = get_temp_humidity()[1]
    helper.lightIntensity = random.randint(0, 1000)
    helper.isLightOn = 'Light OFF'
    helper.motorStatusMsg = "Motor is OFF"
    # helper.userTag = random.randint(10000000000000, 99999999999999)
    helper.userTag = "E3 17 ED 15"

    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(17, GPIO.IN)

    # app = dash.Dash(__name__, external_stylesheets=external_stylesheets) # NOTE: Removed external_stylesheets
    app = dash.Dash(meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP])
    if (helper.userTag == "B3 72 85 0D" or helper.userTag == "E3 17 ED 15"):
        app.layout = html.Div(children=[
            html.H1(children='IoT Dashboard'),
            html.Div(children='''IoT Dashboard is a web application that displays the current status of IoT devices connected to it.
            ''', id='description'),
            # Create box displaying user tag, temperature threshold, and humidity threshold #FIXME: Need to test & make it look nice (?)
            html.Div(id='user-tag-box', children=[
                html.Img(src=app.get_asset_url(checkProfile()), id='iot-logo', style={'margin-left': 'auto', 'margin-right': 'auto', 'display': 'block', 'width': '100px', 'height': '100px'}),
                html.H3(children='User Tag', style={'text-align': 'center'}),
                html.P(children=helper.userTag, style={'text-align': 'center'}),
                html.H3(children='Temperature Threshold', style={'text-align': 'center'}),
                html.P(children=helper.temperatureThresh, style={'text-align': 'center'}),
                html.H3(children='Humidity Threshold', style={'text-align': 'center'}),
                html.P(children=helper.humidityThresh, style={'text-align': 'center'}),
            ]),
            # Images for LED on, off, motor on and off
            html.Div(id='led-box', children=[
                html.H1(children=helper.isLightOn, style={'text-align': 'center'}),
                # html.Img(id='led-image', src=helper.ledImage, style={'width': '100px', 'height': '100px'}),
                daq.LEDDisplay(
                    id='light-display',
                    value=helper.lightIntensity,
                    style={'margin-top': '20px', 'text-align': 'center', 'display': 'block'},
                ),
            ]),
            html.Div(id='motor-box', children=[
                html.H1(children=helper.motorStatusMsg, style={'text-align': 'center'}),
                # html.Img(id='motor-image', src=helper.motorImage, style={'width': '100px', 'height': '100px'}),
            ]),
            daq.Gauge(
                id='temperature-gauge',
                value=temperature,
                label='Temperature',
                max=80,
                min=20,
                units='Celsius',
                showCurrentValue=True,
                color={"gradient":True,"ranges":{"aqua":[20, 40],"teal":[40,55],"blue":[55,65],"navy":[65,80]}},
                style={'margin-right': '70%', 'display': 'block','margin-top': '-20%', 'padding-left': '20%'},
            ),
            daq.Gauge(
                id='humidity-gauge',
                value=humidity,
                label='Humidity',
                max=80,
                min=20,
                units='Humidity %',
                showCurrentValue=True,
                color={"gradient":True,"ranges":{"aqua":[20, 40],"teal":[40,55],"blue":[55,65],"navy":[65,80]}},
                style={'margin-right': '50%', 'display': 'block', 'margin-top': '-17%', 'margin-left': '75%'},
            ),

            dcc.Interval(
                id='temperature-interval',
                interval=2*1000,
                n_intervals=0
            ),
            dcc.Interval(
                id='humidity-interval',
                interval=2*1000,
                n_intervals=0
            ),
            dcc.Interval(
                id='light-interval',
                interval=2*1000,
                n_intervals=0
            ),
            # FIXME: Find proper assets for the icons.
            # FIXME: Test this code, probably will not work.
        ])
    else:
        app.layout = html.Div(children=[
            html.H1(children="Please scan your RFID Tag to load profile values", style={'text-align':'center'})
        ])

        # Refresh page every 2 seconds
        @app.callback(dash.dependencies.Output('user-tag-box', 'children'),
        [dash.dependencies.Input('temperature-component', 'n_intervals')])
        def update_user_tag(n):
            return helper.userTag, helper.temperatureThresh, helper.humidityThresh, helper.isLightOn, helper.motorStatusMsg

    def updateIcons():
        # Update the icons
        if (helper.motorStatusMsg == "Motor is ON"):
            motorIconStatus = True
        else:
            motorIconStatus = False
        if (helper.isLightOn == "Light ON"):
            lightIconStatus = True
        else:
            lightIconStatus = False
        return motorIconStatus, lightIconStatus
    @app.callback(
        dash.dependencies.Output('humidity-gauge', 'value'),
        [dash.dependencies.Input('humidity-interval', 'n_intervals')]
    )
    def update_output(n):
        humidity = get_temp_humidity()[1]
        return humidity
    @app.callback(
        dash.dependencies.Output('temperature-gauge', 'value'),
        [dash.dependencies.Input('temperature-interval', 'n_intervals')]
    )
    def update_output2(n):
        temperature = get_temp_humidity()[0]
        return temperature
    @app.callback(
        dash.dependencies.Output('light-display', 'value'),
        [dash.dependencies.Input('light-interval', 'n_intervals')]
    )
    def update_output3(n):
        lightIntensity = get_temp_humidity()[2]
        # lightIntensity = helper.lightIntensity FIXME: Uncomment this when you want to test production
        return lightIntensity
    
    return app

def main():
    # print("Starting MQTT connection...")
    # client = connect_mqtt()
    # print("Subscribed to MQTT topic...")
    # subscribeTopic(client)
    # print("Starting Dash app...")
    # client.loop_start()
    app = createDash()
    app.run_server(debug=True, host='localhost', port=8050)
    
main()