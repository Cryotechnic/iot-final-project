from paho.mqtt import client as mqtt_client
from init_script import *

topic = [("IoT/light",0), ("IoT/humidity",0), ("IoT/temperature",0), ("IoT/rfid",0)]
client_id = f'python-mqtt-{r.randint(0,100)}'
username = "user"
password = "user"
broker = '192.168.0.183' # FIXME: Maybe find a way to ask for user input?
port = 1883


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
        isMotorMailSent = False
        isLightMailSent = False
        # sentEmailCount = 0 # FIXME: Replaced by helper but may need to localize instead
        emailMessage = ""

        # Sorts based on topic type
        if (msg.topic == "IoT/light"):
            lightMsg = int(msg.payload.decode())
            helper.lightIntensity = lightMsg
            print(f"DBG --- Light intensity: {lightMsg}")

        if (msg.topic == "IoT/humidity"):
            humidityMsg = float(msg.payload.decode())
            helper.humidityThresh = humidityMsg
            print(f"DBG --- Humidity: {humidityMsg}")
            
        if (msg.topic == "IoT/temperature"):
            temperatureMsg = float(msg.payload.decode())
            print(f"DBG --- Temperature: {temperatureMsg}")
            helper.temperatureThresh = temperatureMsg
            if (temperatureMsg > 20 and isMotorMailSent != True and helper.sentEmailCount == 0):
                # sendMotorNotificationEmail()
                helper.sentEmailCount += 1
                isMotorMailSent = True
            else:
                helper.sentEmailCount = 0
                isMotorMailSent = False
    
        if (msg.topic == "IoT/rfid"):
            # sendProfileEmail()
            helper.userTag = msg.payload.decode()
            print(f"DBG --- User Tag: {helper.userTag}")
            for user in users:
                if(user[0].lower() == helper.userTag.lower().strip()):
                    helper.temperatureThresh = user[1]
                    helper.humidityThresh = user[2]
                    helper.lightThresh = user[3]  
        # else:
        #     print("DBG --- Unknown topic received.\n")
        if (isMotorMailSent == True and helper.sentEmailCount == 1):
            print("DBG --- Motor notification email sent.\n")
            # reply = receiveMail()
        if (str(lightMsg) < "400" and isLightMailSent == False):
            # print("-------------------------")
            # print("DBG -- subscribeTopic > LightMsg: " + str(lightMsg))
            # print("Email sending...")
            # print("-------------------------")
            isLightMailSent = True
            helper.isLightOn = 'Light ON'
            # GPIO.output(LED_PIN, GPIO.HIGH) # Turn on LED
            print("DBG --- Light is ON")
            # sendLEDNotificationEmail()

    client.subscribe(topic)
    client.on_message = on_message
    return helper.lightIntensity, helper.humidityThresh, helper.temperatureThresh, helper.isLightOn

# main() for testing
if __name__ == "__main__":
    client = connect_mqtt()
    subscribeTopic(client)
    client.loop_forever()