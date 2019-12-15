import cv2
from hyperlpr import *
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(40,GPIO.IN)
pan = GPIO.PWM(22,50)
pan.start(0)
pan.ChangeDutyCycle(2)#初始化杆位子

def carCome():
    if GPIO.input(40):
        return False
    else:
        return True

def getCar():
    if carCome(): #检测到车，低电平
        cap = cv2.VideoCapture(0)
        ret,frame = cap.read()
        cv2.imshow("capture", frame)
        #cv2.waitKey(1)
        cv2.imwrite("/home/pi/capturedPlate.jpg", frame)
        image = cv2.imread("/home/pi/capturedPlate.jpg")
        recoResult = HyperLPR_PlateRecogntion(image)
        cap.release()
        cv2.destroyAllWindows()
        if len(recoResult):#识别到车牌
            print(recoResult[0][0])#输出车牌信息
            pan.ChangeDutyCycle(6)#--抬杆
            while carCome(): i=0
            pan.ChangeDutyCycle(2)#--
        else:
            print("识别错误")
            
            

#cv2.destroyAllWindows()
        
        
while True :
    getCar()
    
