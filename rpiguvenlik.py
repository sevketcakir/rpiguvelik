import RPi.GPIO as GPIO
import time
import picamera
import datetime
import os
import subprocess as sp

def get_file_name():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")

sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False
recording = False

cam = picamera.PiCamera()
start_time=time.time()

while True:
    time.sleep(0.1)
    previous_state = current_state
    current_state = GPIO.input(sensor)
    if current_state:
        start_time=time.time()
    #print("Son hareketten bu yana %s s" % (int(time.time()-start_time)))
    if current_state and not recording:
        fileName = get_file_name()
        #cam.start_preview()
        cam.start_recording(fileName)
        print "Recording started"
        recording=True
    elif not current_state and recording and int(time.time()-start_time)>5:
        #cam.stop_preview()
        cam.stop_recording()
        print "Recording stopped"
        recording=False
        sp.call("cd /opt/python3.3.2/bin && sudo ./youtube-upload --title="+fileName+" --client-secret=CLIENT_SECRETS /home/pi/"+fileName+" && cd",shell=True)
        os.environ['file']=fileName
        os.system('echo $file | mail -s $file mstfyldrm358@gmail.com')
        sp.call("/bin/rm -f /home/pi/"+fileName,shell=True)
