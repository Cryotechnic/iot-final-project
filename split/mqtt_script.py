from paho.mqtt import client as mqtt_client
from init_script import *
import time
import mail_script
# import motor_script

topic = [("IoT/light",0), ("IoT/humidity",0), ("IoT/temperature",0), ("IoT/rfid",0)]
client_id = f'python-mqtt-{r.randint(0,100)}'
username = "user"
password = "user"
broker = '192.168.0.183' # FIXME: Maybe find a way to ask for user input?
port = 1883
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

        # Sorts based on topic type
        if (msg.topic == "IoT/light"):
            lightMsg = int(msg.payload.decode())
            helper.lightIntensity = lightMsg
            if (str(lightMsg) < "400" and mailStatus.isLightMailSent == False):
                # print("-------------------------")
            # print("DBG -- subscribeTopic > LightMsg: " + str(lightMsg))
            # print("Email sending...")
            # print("-------------------------")
                mailStatus.isLightMailSent = True
                helper.isLightOn = 'Light is ON'
            # GPIO.output(LED_PIN, GPIO.HIGH) # Turn on LED
                mail_script.sendLEDNotificationEmail()

        if (msg.topic == "IoT/humidity"):
            humidityMsg = float(msg.payload.decode())
            helper.humidityThresh = humidityMsg
            
        if (msg.topic == "IoT/temperature"):
            temperatureMsg = float(msg.payload.decode())
            helper.temperatureThresh = temperatureMsg
            if (temperatureMsg > 20 and mailStatus.isMotorMailSent != True and helper.sentEmailCount == 0):
                # motor_script.spinMotor()
                mail_script.sendMotorNotificationEmail()
                helper.sentEmailCount += 1
                mailStatus.isMotorMailSent = True
            else:
                helper.sentEmailCount = 0
                mailStatus.isMotorMailSent = False
    
        if (msg.topic == "IoT/rfid"):
            helper.userTag = msg.payload.decode()
            mail_script.sendProfileEmail()
            for user in users:
                if(user[0].lower() == helper.userTag.lower().strip()):
                    helper.temperatureThresh = user[1]
                    helper.humidityThresh = user[2]
                    helper.lightThresh = user[3]  
        # else:
        #     print("DBG --- Unknown topic received.\n")
        if (mailStatus.isMotorMailSent == True and helper.sentEmailCount == 1):
            reply = mail_script.receiveMail()
            if (mail_script.receiveMail()):
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
    print(f"DBG --- Light intensity: {helper.lightIntensity}")
    print(f"DBG --- Humidity Thresh: {helper.humidityThresh}")
    print(f"DBG --- Temperature Thresh: {helper.temperatureThresh}")
    print(f"DBG --- Temperature: {helper.temperature}")
    print(f"DBG --- Humidity: {helper.humidity}")
    print(f"DBG --- Light Thresh: {helper.lightThresh}")
    print(f"DBG --- Light: {helper.isLightOn}")
    print(f"DBG --- User Tag: {helper.userTag}")
    print(f"DBG --- Motor status: {helper.motorStatusMsg}")
    return helper.lightIntensity, helper.humidityThresh, helper.temperatureThresh, helper.temperature, helper.humidity, helper.lightThresh, helper.isLightOn, helper.userTag, helper.motorStatusMsg

# main() for testing
if __name__ == "__main__":
    
    client = connect_mqtt()
    subscribeTopic(client)
    client.loop_forever()
    
