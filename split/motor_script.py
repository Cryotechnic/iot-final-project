import init_script as init
import Rpi.GPIO as GPIO

isMotorOn = False
motorStatus = "Motor is OFF"
Motor1A = 24
Motor1B = 23
Motor1E = 25
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.output(Motor1E, GPIO.LOW)

def spinMotor():
    init.helper.motorStatusMsg = "Motor is ON"
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)



# main for testing
if __name__ == "__main__":
    print("Motor is ON")
    spinMotor()
    print("Motor is OFF")
    GPIO.output(Motor1E, GPIO.LOW)
    GPIO.cleanup()

