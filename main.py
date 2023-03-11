import cv2
from cvzone.HandTrackingModule import HandDetector
import streamlit as st

html='''   
  <h2 style='background-color:tomato; text-align:center'>Virtual KeyBoard </h2>
'''
st.markdown(html,unsafe_allow_html=True)
if (st.button("Click")):
     
    cap=cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    detector=HandDetector(detectionCon=0.8,maxHands=2)
    keys=[["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]
        ]
    def drawALL(img,buttonList):
            for button in buttonList:
                x,y=button.pos
                w,h=button.size
                cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
                cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
            return img
    class Button():
        def __init__(self,pos,text,size=[85,85]):
            self.pos=pos
            self.text=text
            self.size=size
        
    buttonList=[]
    for i in range(len(keys)):
        for j,key in enumerate(keys[i]):
            buttonList.append(Button([100*j +50,100*i+50],key))
    finalText=""
    while True:
        success,img=cap.read()
        hands,img=detector.findHands(img)
        img=drawALL(img,buttonList)
        if hands:
        
            hand1=hands[0]
        
            lmList1=hand1['lmList']
            bbox1=hand1['bbox']
            # print(lmList1)
            for button in buttonList:
                x,y=button.pos
                w,h=button.size
                if ((lmList1[8][0]>x and lmList1[8][0]<x+w) and (lmList1[8][1]>y and lmList1[8][1]<y+h)):
                
                    cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED)
                    cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    l,_,_=detector.findDistance(lmList1[8][0:2],lmList1[12][0:2],img)
                    if l<30:
                        cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                        cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                        finalText+=button.text
                        
        cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
        cv2.putText(img,finalText,(60,425),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
        
        cv2.imshow("Image",img)
        cv2.waitKey(10)

        