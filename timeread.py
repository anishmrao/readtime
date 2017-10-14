import numpy as np
import cv2
from math import sqrt
from math import atan
from math import floor
import os

def ret_val(angle,quad,chk):
  angle=angle*180/3.1415
  angle=abs(angle)
  if(chk):
    if(quad == 1):
      return int(floor(15-angle*15/90))
    elif(quad==2):
      return int(floor(45+angle*15/90))
    elif(quad==3):
      return int(floor(45-angle*15/90))
    else:
      return int(floor(15+angle*15/90))
  else:
    if(quad == 1):
      hr = int(floor(3-angle/30))
      if(hr == 0):
        return 12
      else:
        return hr
    elif(quad==2):
      return int(floor(9+angle/30))
    elif(quad==3):
      return int(floor(9-angle/30))
    else:
      return int(floor(3+angle/30))
    
def det_time(x1,y1,x2,y2):
  d2 = sqrt(pow((320 - x2), 2) + pow((240 - y2), 2))
  d1 = sqrt(pow((320 - x1), 2) + pow((240 - y1), 2))
  a1=atan(float(y1-240)/float(x1-320))
  a2=atan(float(y2-240)/float(x2-320))
  if(d1<d2):
    hpos= True
  else:
    hpos= False
    
  if(x1>320 and y1<240):
    quad1=1
  elif(x1<320 and y1<240):
    quad1=2
  elif(x1<320 and y1>240):
    quad1=3
  else:
    quad1=4
  if(x2>320 and y2<240):
    quad2=1
  elif(x2<320 and y2<240):
    quad2=2
  elif(x2<320 and y2>240):
    quad2=3
  else:
    quad2=4
    
  if(hpos):
    hours=ret_val(a1,quad1,0)
    minutes=ret_val(a2,quad2,1)
  else:
    hours=ret_val(a2,quad2,0)
    minutes=ret_val(a1,quad1,1)

  #print d1,quad1,a1
  #print d2,quad2,a2
  if(0<=minutes<=9):
    return str(hours)+":0"+str(minutes)
  else:
    return str(hours)+":"+str(minutes)
  
    
    

def on_mouse(event,x,y,flag,param):
  if(event==cv2.EVENT_LBUTTONDOWN):
    #print("In on_mouse")
    image = cv2.imread("capture.png")
    pixel = image[y, x] # Note y index "row" of matrix and x index "col".
    tolerance = 30
    #print image.shape
    # Ensure your bounds are within 0 and 255.
    lower = map(lambda x: max(0, x - tolerance), pixel)
    upper = map(lambda x: min(255, x + tolerance), pixel)
    lower = np.asarray(lower)
    upper = np.asarray(upper)
    m = cv2.inRange(image, lower, upper)
    
    
    non_zero = cv2.findNonZero(m)
    #print type(non_zero)
    maxx=maxy=0
    minx=320
    miny=240

    for i in non_zero:
      if(i[0][1]>maxy):
        p2=i[0]
        maxy=i[0][1]
      elif(i[0][1]<miny):
        p1=i[0]
        miny=i[0][1]
    if(abs(miny-240)<=5 or abs(maxy-240)<=5):
      for i in non_zero:
        if(i[0][0]>maxx):
          p1=i[0]
          maxx=i[0][0]
        elif(i[0][0]<minx):
          p2=i[0]
          minx=i[0][0]
    if(abs(p1[0]-320)<=5 and abs(p1[1]-240)<=5):
      p1=p2
    elif(abs(p2[0]-320)<=5 and abs(p2[1]-240)<=5):
      p2=p1
    #print p1,p2,x,y
    result = det_time(p1[0], p1[1], p2[0], p2[1])
    print result
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(m,result,(250,400), font, 2,(255,255,255),2)
    cv2.imshow("Res", m)

    
retval = True
r=True

while retval:
    vc = cv2.VideoCapture(0)
    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False
    while rval:
        rval, frame = vc.read()
        height,width,depth = frame.shape
        cv2.circle(frame,(width/2,height/2), 1, (255, 0, 0), thickness = 1)
        circle_img = np.zeros((height,width), np.uint8)
        cv2.circle(circle_img,(width/2,height/2),100,1,thickness=-1)
        masked_data = cv2.bitwise_and(frame, frame, mask=circle_img)
        cv2.imshow("masked", masked_data)
        key = cv2.waitKey(20)
        if key == 32:
            r=True
            cv2.imwrite("capture.png", masked_data)
            break
        if key == 27:
            r = False
            break
    
    vc.release()
    
    if(r):
        cv2.setMouseCallback("masked", on_mouse)
        while(True):
            key = cv2.waitKey(20)
            if key == 32:
              break
            if key == 27:
                r = False
                break
        cv2.destroyAllWindows()
        os.remove("capture.png")
    if not r:
        cv2.destroyAllWindows()
        retval=False

    
   
