import cv2, time

first_frame=None
status_list=[]

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

    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_delta=cv2.threshold(delta_frame, 10, 255, cv2.THRESH_BINARY)[1]
    thresh_delta=cv2.dilate(thresh_delta,None,iterations=2)

    (_,cnts,_)=cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        status=1

        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),3)

    status_list.append(status)
    cv2.imshow("gray",gray)
    cv2.imshow("first",first_frame)
    cv2.imshow("delta",delta_frame)
    cv2.imshow("thresh", thresh_delta)
    cv2.imshow("Color Frame",frame)

    key=cv2.waitKey(1)
    temps=temps+200
    if key==ord('q'):
        break

print(temps)
print(temp)

video.release()
cv2.destroyAllWindows
