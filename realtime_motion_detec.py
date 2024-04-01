import cv2, time, pandas
from datetime import datetime

first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=["Start","End"])

video=cv2.VideoCapture(0)
temp=0
temps=0

while True:

    check, frame = video.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if temps==temp:
        first_frame=gray
        temp=temp+1000
        continue

    # delta_frame=cv2.absdiff(first_frame,gray)
    # thresh_delta=cv2.threshold(delta_frame, 10, 255, cv2.THRESH_BINARY)[1]
    # thresh_delta=cv2.dilate(thresh_delta,None,iterations=2)

    # (_,cnts,_)=cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate absolute difference between frames
    delta_frame = cv2.absdiff(first_frame, gray)

    # Apply binary threshold to delta frame
    thresh_delta = cv2.threshold(delta_frame, 10, 255, cv2.THRESH_BINARY)[1]

    # Apply dilation to thresholded frame
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh_delta = cv2.dilate(thresh_delta, kernel, iterations=2)

    # Find contours in thresholded frame
    cnts, _ = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        status=1

        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),3)

    status_list.append(status)
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    
    # cv2.imshow("gray",gray)
    # cv2.imshow("first",first_frame)
    # cv2.imshow("delta",delta_frame)
    # cv2.imshow("thresh", thresh_delta)
    cv2.imshow("Color Frame",frame)

    key=cv2.waitKey(1)
    
    temps=temps+200

    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break

print(temps)
print(temp)

print(status_list)
print(times)

for i in range(0,len(times)-1,2):
    df=df._append({"Start":times[i],"End":times[i+1]},ignore_index=True)
    print(i)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows
