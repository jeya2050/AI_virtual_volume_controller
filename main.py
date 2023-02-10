import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np

# for control audio
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
vol=volume.GetVolumeRange()
volmin=vol[0]
volmax=vol[1]
print(volmin,volmax)
#volume.SetMasterVolumeLevel(-20.0, None)



video=cv2.VideoCapture(0)
video.set(3,1080)
video.set(4,720)

detector=HandDetector(detectionCon=0.8)
vol_1=100
vol_2=0
while True:
    _,frame=video.read() 
    lmlist,_=detector.findHands(frame)
    #print(lmlist)
    if len(lmlist) != 0:
        #print(lmlist[0]["lmList"])
        for id ,i in enumerate((lmlist[0]["lmList"])):
            if id == 4:  
                x1,y1=i[0],i[1]
                cv2.circle(frame,(x1,y1),15,(255,0,0),-1)
            if id == 8:
                x2,y2=i[0],i[1]
                cv2.circle(frame,(x2,y2),15,(255,0,0),-1)
        cx=(x1+x2)//2
        cy=(y1+y2)//2
        cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),5)
        cv2.circle(frame,(cx,cy),15,(255,0,0),-1)
        length=math.hypot((x2-x1),(y2-y1))
        #print(length)
        #we need -74-0
        #we have 160-15
        vol=np.interp(length,[15,160],[-74,0])
        vol_1=np.interp(vol,[-74,0],[400,100])
        vol_2=np.interp(vol,[-74,0],[0,100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length<25:
            cv2.circle(frame,(cx,cy),15,(0,255,0),-1)
    cv2.rectangle(frame,(100,100),(130,400),(0,255,255),1)
    cv2.rectangle(frame,(100,int(vol_1)),(130,400),(0,255,0),-1)
    cv2.putText(frame,"{} %".format(str(int(vol_2))),(90,450),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,255,255),3)
    cv2.imshow("video",frame)
    k=cv2.waitKey(1)
    if k == ord("q"):
        break