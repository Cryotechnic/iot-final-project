# PythonDash for DHT11 sensor, including mailing functions as well as various
# other init.helper functions
# TODO: Test the entire code and make sure it works
# TODO: Test the new styling stuff for motor & LED
# TODO: Check if variables are being updated correctly
# TODO: Check if some vars need to be global or local
# TODO: Update init.helper class if necessary
# FIXME: Check if the email is being sent correctly
# FIXME: Check if MQTT is properly handling responses to email requests
# FIXME: Some other stuff that I didn't take into account


# Importing modules
import random as r
import dash
import dash.dependencies
import dash_daq as daq
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from paho.mqtt import client as mqtt_client
import random
# import RPi.GPIO as GPIO
import mail_script as mail
import init_script as init
import mqtt_script as mqtt

#################################################################################################################
#                                  MQTT STUFF                                                                   #
#################################################################################################################
# from init_script import *
# import random as r
import time
# import mail_script
# import motor_script

topic = [("IoT/light",0), ("IoT/humidity",0), ("IoT/temperature",0), ("IoT/rfid",0)]
client_id = f'python-mqtt-{r.randint(0,100)}'
username = "user"
password = "user"
broker = 'localhost' # FIXME: Maybe find a way to ask for user input?
port = 1883
global lightIntensity
global isLightOn
global humidityThresh
global temperatureThresh
global lightThresh
global sentEmailCount
global userTag
global temperature
global humidity
global motorStatusMsg


class mailStatus:
    isLightMailSent = False
    isMotorMailSent = False


def connect_mqtt() -> mqtt_client:
    print("Connecting to MQTT broker...")
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker!\n")
        else:
            print("Failed to connect to broker, returned code: " + str(rc) + "\n")
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribeTopic(client: mqtt_client):
    def on_message(client, userdata, msg):
        lightMsg = ""
        humidityMsg = ""
        temperatureMsg = ""
        lightIntensity = 0
        humidity = 0
        temperature = 0
        motorStatusMsg = "Motor is OFF"
        userTag = ""
        isLightOn = "Light is OFF"

        # Sorts based on topic type
        if (msg.topic == "IoT/light"):
            lightMsg = int(msg.payload.decode())
            lightIntensity = lightMsg
            if (str(lightMsg) < "400" and mailStatus.isLightMailSent == False):
                # print("-------------------------")
            # print("DBG -- subscribeTopic > LightMsg: " + str(lightMsg))
            # print("Email sending...")
            # print("-------------------------")
                mailStatus.isLightMailSent = True
                isLightOn = 'Light is ON'
            # GPIO.output(LED_PIN, GPIO.HIGH) # Turn on LED
                mail.sendLEDNotificationEmail()

        if (msg.topic == "IoT/humidity"):
            humidityMsg = float(msg.payload.decode())
            humidityThresh = humidityMsg
            
        if (msg.topic == "IoT/temperature"):
            temperatureMsg = float(msg.payload.decode())
            temperatureThresh = temperatureMsg
            if (temperatureMsg > 20 and mailStatus.isMotorMailSent != True and sentEmailCount == 0):
                # motor_script.spinMotor()
                mail.sendMotorNotificationEmail()
                sentEmailCount += 1
                mailStatus.isMotorMailSent = True
            else:
                sentEmailCount = 0
                mailStatus.isMotorMailSent = False
    
        if (msg.topic == "IoT/rfid"):
            userTag = msg.payload.decode()
            mail.sendProfileEmail()
            for user in init.users:
                if(user[0].lower() == userTag.lower().strip()):
                    temperatureThresh = user[1]
                    humidityThresh = user[2]
                    lightThresh = user[3]  
        # else:
        #     print("DBG --- Unknown topic received.\n")
        if (mailStatus.isMotorMailSent == True and sentEmailCount == 1):
            reply = mail.receiveMail()
            if (mail.receiveMail()):
                print("DBG --- Email received.\n")
                # motor_script.spinMotor()

    client.subscribe(topic)
    client.on_message = on_message

    # Test data
    client.publish("IoT/light", "400")
    client.publish("IoT/humidity", "50")
    client.publish("IoT/temperature", "20")
    client.publish("IoT/rfid", "B3 72 85 0D")

    print("All info:")
    print(f"DBG --- Light intensity: " + str(lightIntensity))
    print(f"DBG --- Humidity Thresh: {humidityThresh}")
    print(f"DBG --- Temperature Thresh: {temperatureThresh}")
    print(f"DBG --- Temperature: {temperature}")
    print(f"DBG --- Humidity: {humidity}")
    print(f"DBG --- Light Thresh: {lightThresh}")
    print(f"DBG --- Light: {isLightOn}")
    print(f"DBG --- User Tag: {userTag}")
    print(f"DBG --- Motor status: {motorStatusMsg}")
    return lightIntensity, humidityThresh, temperatureThresh, temperature, humidity, lightThresh, isLightOn, userTag, motorStatusMsg


#################################################################################################################
#                                  MQTT STUFF END                                                               #
#################################################################################################################

def updateThresholds(var_name: str, var_value: int):
    if (var_name == "lightThresh"):
        lightThresh = var_value
    elif (var_name == "humidityThresh"):
        humidityThresh = var_value
    elif (var_name == "temperatureThresh"):
        temperatureThresh = var_value
    elif (var_name == "username"):
        username = var_value
    else:
        print("DBG -- updateThresholds > Unknown variable name.")

def checkProfile():
        if (userTag == "B3 72 85 0D"):
            return 'person.png'
        elif (userTag == "E3 17 ED 15"):
            return 'person2.png'
        else:
            return 'person.png'

def checkLight():
    if (lightIntensity >= lightThresh):
        return 'lightOn.png'
    else:
        return 'lightOff.png'

def checkMotor():
    if (motorStatusMsg == "Motor is ON"):
        return 'motorOn.png'
    else:
        return 'motorOff.png'

def createDash():
    # temperature = init.helper.temperature
    # humidity = init.helper.humidity 
    # lightIntensity = init.helper.lightIntensity
    # isLightOn = init.helper.isLightOn
    # motorStatusMsg = init.helper.motorStatusMsg
    # userTag = init.helper.userTag
    # userTag = "B3 72 85 0D"
    # userTag = "E3 17 ED 15"
    # init.helper.userTag = "B3 72 85 0D"
    # init.helper.userTag = "E3 17 ED 15"
    # userTag = init.helper.userTag
    print ("DBG -- createDash > userTag: " + userTag)
    # init.helper.lightIntensity = random.randint(0, 1000)
    # init.helper.isLightOn = 'Light OFF'
    # init.helper.motorStatusMsg = "Motor is OFF"
    # init.helper.userTag = random.randint(10000000000000, 99999999999999)
    # init.helper.userTag = "E3 17 ED 15"

    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(17, GPIO.IN)

    app = dash.Dash(meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/main.css'])
    if (init.helper.userTag == "B3 72 85 0D" or init.helper.userTag == "E3 17 ED 15"):
        app.layout = html.Div(children=[
            html.H1(children='IoT Dashboard', style={'textAlign': 'center'}),
            html.Div(children='''IoT Dashboard is a web application that displays the current status of IoT devices connected to it.
            ''', id='description', style={'textAlign': 'center'}),
            # Create box displaying user tag, temperature threshold, and humidity threshold
            html.Div(id='user-tag-box', children=[
                html.Img(src=app.get_asset_url(checkProfile()), id='profile-logo', style={'margin-left': 'auto', 'margin-right': 'auto', 'margin-top': '1%', 'display': 'block', 'width': '100px', 'height': '100px'}),
                html.H3(children='User Tag', style={'text-align': 'center'}),
                html.P(children=userTag, style={'text-align': 'center'}, id='userTag'),
                html.H3(children='Temperature Threshold', style={'text-align': 'center'}),
                html.P(children=temperatureThresh, style={'text-align': 'center'}, id='tempThres'),
                html.H3(children='Humidity Threshold', style={'text-align': 'center'}),
                html.P(children=humidityThresh, style={'text-align': 'center'}, id='humidityThresh'),
                html.H3(children='Light Threshold', style={'text-align': 'center'}),
                html.P(children=lightThresh, style={'text-align': 'center'}, id='lightThresh'),
            ]),
            # Images for LED on, off, motor on and off
            html.Div(id='led-box', children=[
                html.H1(children=isLightOn, style={'text-align': 'center'}),
                html.Img(src=app.get_asset_url(checkLight()), id='light-status', style={'width': '100px', 'height': '100px', 'margin-left': 'auto', 'margin-right': 'auto', 'display': 'block'}),
                daq.LEDDisplay(
                    id='light-display',
                    value=lightIntensity,
                    style={'margin-top': '20px', 'text-align': 'center', 'display': 'block'},
                ),
            ]),
            html.Div(id='motor-box', children=[
                html.H1(children=motorStatusMsg, style={'text-align': 'center'}),
                html.Img(src=app.get_asset_url(checkMotor()), id='motor-status', style={'width': '100px', 'height': '100px', 'margin-left': 'auto', 'margin-right': 'auto', 'display': 'block'}),
            ]),
            daq.Gauge(
                id='temperature-gauge',
                value=temperature,
                label={'label':'Temperature', 'style':{'font-size': '40px', 'color': '#abe2fb'}},
                max=80,
                min=20,
                size=400,
                units='Celsius',
                showCurrentValue=True,
                color={"gradient":True,"ranges":{"aqua":[20, 40],"teal":[40,55],"blue":[55,65],"navy":[65,80]}},
                style={'margin-right': '70%', 'display': 'block','margin-top': '-40%', 'padding-left': '20%'},
            ),
            daq.Gauge(
                id='humidity-gauge',
                value= humidity,
                label={'label':'Humidity', 'style':{'font-size': '40px', 'color': '#abe2fb'}},
                max=80,
                min=20,
                size=400,
                units="Humidity (%)",
                showCurrentValue=True,
                color={"gradient":True,"ranges":{"aqua":[20, 40],"teal":[40,60],"#7338B3":[60,80]}},
                style={'margin-right': '50%', 'display': 'block','margin-top': '-29%', 'margin-left': '75%'},
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
        ])
    else:
        app.layout = html.Div(children=[
            html.H1(children="Please scan your RFID Tag to load profile values", style={'text-align':'center'})
        ])

    # Refresh page every 2 seconds
    @app.callback(dash.dependencies.Output('user-tag-box', 'children'),
    [dash.dependencies.Input('temperature-component', 'n_intervals')])
    def update_user_tag(n):
        return userTag, temperatureThresh, humidityThresh, isLightOn, motorStatusMsg
    @app.callback(
        dash.dependencies.Output('humidity-gauge', 'value'),
        [dash.dependencies.Input('humidity-interval', 'n_intervals')]
    )
    def update_output(n):
        # humidity = init.helper.humidity
        return humidity
    @app.callback(
        dash.dependencies.Output('temperature-gauge', 'value'),
        [dash.dependencies.Input('temperature-interval', 'n_intervals')]
    )
    def update_output2(n):
        # temperature = init.helper.temperature
        return temperature
    @app.callback(
        dash.dependencies.Output('light-display', 'value'),
        [dash.dependencies.Input('light-interval', 'n_intervals')]
    )
    def update_output3(n):
        # lightIntensity = init.helper.lightIntensity
        return lightIntensity

    @app.callback(dash.dependencies.Output('userTag', 'children'),
        [dash.dependencies.Input('humidity-interval', 'n_intervals')])    
    def update_user_tag(n):
        return userTag  

    @app.callback(dash.dependencies.Output('tempThres', 'children'),
        [dash.dependencies.Input('temperature-interval', 'n_intervals')])    
    def update_user_temperature(n):
        return temperatureThresh

    @app.callback(dash.dependencies.Output('humidityThresh', 'children'),
        [dash.dependencies.Input('humidity-interval', 'n_intervals')])    
    def update_user_humidity(n):
        return humidityThresh

    @app.callback(dash.dependencies.Output('lightThresh', 'children'),
        [dash.dependencies.Input('light-interval', 'n_intervals')])    
    def update_user_temperature(n):
        return lightThresh  
           
    return app
    
if __name__ == "__main__":
    client = connect_mqtt()
    subscribeTopic(client)
    client.loop_start()
    app = createDash().run_server(debug=True, host='localhost', port=8000)