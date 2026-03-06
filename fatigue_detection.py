import cv2
import time

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

eye_counter = 0
blink_count = 0
start_time = time.time()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.3,5)

    status = "ACTIVE"

    for (x,y,w,h) in faces:

        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        roi_gray = gray[y:y+h,x:x+w]
        roi_color = frame[y:y+h,x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray,1.1,5)

        if len(eyes)==0:
            eye_counter +=1
        else:
            if eye_counter > 2:
                blink_count +=1
            eye_counter = 0

        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

    if eye_counter > 35:

        status = "DROWSY"

        cv2.putText(frame,
                    "DROWSINESS ALERT!",
                    (100,100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    3)

    attention_score = max(0,100 - (blink_count*2) - eye_counter)

    with open("driver_status.txt", "w") as f:
      f.write(status)
      f.flush()

    cv2.putText(frame,"Driver Status: "+status,(50,50),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)

    cv2.putText(frame,"Blink Count: "+str(blink_count),(50,100),
                cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)

    cv2.putText(frame,"Attention Score: "+str(attention_score),
                (50,150),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

    cv2.imshow("SafeDrive AI Camera",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()