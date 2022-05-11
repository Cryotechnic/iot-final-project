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
import random
# import RPi.GPIO as GPIO
import mail_script as mail
import init_script as init
import mqtt_script as mqtt

def updateThresholds(var_name: str, var_value: int):
    if (var_name == "lightThresh"):
        init.helper.lightThresh = var_value
    elif (var_name == "humidityThresh"):
        init.helper.humidityThresh = var_value
    elif (var_name == "temperatureThresh"):
        init.helper.temperatureThresh = var_value
    elif (var_name == "username"):
        init.helper.username = var_value
    else:
        print("DBG -- updateThresholds > Unknown variable name.")

def checkProfile():
        if (init.helper.userTag == "B3 72 85 0D"):
            return 'person.png'
        elif (init.helper.userTag == "E3 17 ED 15"):
            return 'person2.png'
        else:
            return 'person.png'

def checkLight():
    if (init.helper.lightIntensity >= init.helper.lightThresh):
        return 'lightOn.png'
    else:
        return 'lightOff.png'

def checkMotor():
    if (init.helper.motorStatusMsg == "Motor is ON"):
        return 'motorOn.png'
    else:
        return 'motorOff.png'

def createDash():
    temperature = init.helper.temperature
    humidity = init.helper.humidity 
    lightIntensity = init.helper.lightIntensity
    isLightOn = init.helper.isLightOn
    motorStatusMsg = init.helper.motorStatusMsg
    # userTag = init.helper.userTag
    # userTag = "B3 72 85 0D"
    # userTag = "E3 17 ED 15"
    init.helper.userTag = "B3 72 85 0D"
    # init.helper.userTag = "E3 17 ED 15"
    userTag = init.helper.userTag
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
                html.P(children=init.helper.userTag, style={'text-align': 'center'}, id='userTag'),
                html.H3(children='Temperature Threshold', style={'text-align': 'center'}),
                html.P(children=init.helper.temperatureThresh, style={'text-align': 'center'}, id='tempThres'),
                html.H3(children='Humidity Threshold', style={'text-align': 'center'}),
                html.P(children=init.helper.humidityThresh, style={'text-align': 'center'}, id='humidityThresh'),
                html.H3(children='Light Threshold', style={'text-align': 'center'}),
                html.P(children=init.helper.lightThresh, style={'text-align': 'center'}, id='lightThresh'),
            ]),
            # Images for LED on, off, motor on and off
            html.Div(id='led-box', children=[
                html.H1(children=init.helper.isLightOn, style={'text-align': 'center'}),
                html.Img(src=app.get_asset_url(checkLight()), id='light-status', style={'width': '100px', 'height': '100px', 'margin-left': 'auto', 'margin-right': 'auto', 'display': 'block'}),
                daq.LEDDisplay(
                    id='light-display',
                    value=init.helper.lightIntensity,
                    style={'margin-top': '20px', 'text-align': 'center', 'display': 'block'},
                ),
            ]),
            html.Div(id='motor-box', children=[
                html.H1(children=init.helper.motorStatusMsg, style={'text-align': 'center'}),
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
        return init.helper.userTag, init.helper.temperatureThresh, init.helper.humidityThresh, init.helper.isLightOn, init.helper.motorStatusMsg
    @app.callback(
        dash.dependencies.Output('humidity-gauge', 'value'),
        [dash.dependencies.Input('humidity-interval', 'n_intervals')]
    )
    def update_output(n):
        humidity = init.helper.humidity
        return humidity
    @app.callback(
        dash.dependencies.Output('temperature-gauge', 'value'),
        [dash.dependencies.Input('temperature-interval', 'n_intervals')]
    )
    def update_output2(n):
        temperature = init.helper.temperature
        return temperature
    @app.callback(
        dash.dependencies.Output('light-display', 'value'),
        [dash.dependencies.Input('light-interval', 'n_intervals')]
    )
    def update_output3(n):
        lightIntensity = init.helper.lightIntensity
        return lightIntensity

    @app.callback(dash.dependencies.Output('userTag', 'children'),
        [dash.dependencies.Input('humidity-interval', 'n_intervals')])    
    def update_user_tag(n):
        return init.helper.userTag  

    @app.callback(dash.dependencies.Output('tempThres', 'children'),
        [dash.dependencies.Input('temperature-interval', 'n_intervals')])    
    def update_user_temperature(n):
        return init.helper.temperatureThresh

    @app.callback(dash.dependencies.Output('humidityThresh', 'children'),
        [dash.dependencies.Input('humidity-interval', 'n_intervals')])    
    def update_user_humidity(n):
        return init.helper.humidityThresh

    @app.callback(dash.dependencies.Output('lightThresh', 'children'),
        [dash.dependencies.Input('light-interval', 'n_intervals')])    
    def update_user_temperature(n):
        return init.helper.lightThresh  
           
    return app
    
if __name__ == "__main__":
    client = mqtt.connect_mqtt()
    mqtt.subscribeTopic(client)
    client.loop_start()
    app = createDash().run_server(debug=True, host='localhost', port=8000)