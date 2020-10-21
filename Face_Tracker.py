import cv2
import serial
from time import sleep

#Create the serial connection on the specified com port
s=serial.Serial('COM3',115200)
#Serial Port Test

# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1) #Create a video capture point (0 is for a integrated webcam and 1 is for an external one)
faces = [] #Create an empty tuple to start so the code doesn't erro if a face is not detected
#These are your cameras max width and height
width = 640
height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


#This loop will look for faces and once a face is found, then it will continue with the rest of the code. Otherwise it will be stuck here.
#The gimbal will not track
while not len(faces): #While no face has been detected
    ret, frame = cap.read() #Get an image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Turn the image to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.1, 4) #Detect any faces




#This loop will detect faces and create a bounding box around them (it can be turned off)
while True:
    #Capture any faces, if none are found, it will continue with the last image
    ret, frame = cap.read() #Get an image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Turn the image to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.1, 4) #Detect any faces

    #detect the largest box which will be the face
    Largest_Area = 0 #Assume there is no largest box to begin   

    for (_x, _y, _w, _h) in faces: # Check all the faces for the biggest one
            if _w*_h > Largest_Area: #Once a new largest area has been found, update the largest bounding box to match
                x = _x
                y = _y
                w = _w
                h = _h
                Largest_Area = w*h

    #Now we have the largest box which contains the face to be tracked (all others will be ignored unless another persons face is bigger)
    center_X = int((2*x+w)/2) #Calculate the X center of the box
    center_Y = int((2*y+h)/2) #Calculate the Y center of the box
    cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.circle(gray, (center_X, center_Y), 10, (0,0,255))
    cv2.imshow('frame',gray) #Show the image on the screen

    #Calculate position error. Used to detemine direction of travel for the servo
    error_X = int(width/2)-center_X
    error_Y = int(height/2) - center_Y
    print(str(error_X) + " " + str(error_Y))
    pos = str(error_X)+","+str(error_Y)+'\n'
    s.write(bytes(pos, 'ascii'))
    s.flushOutput()

    #Test if the arduino is getting the right information
    #val = s.readline()
    #s.flushInput()
    #print(val) # Read the newest output from the Arduino

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#Serial Port Testing Code
#counter = 32
#print(str(counter))
#while True:
#     counter +=1
#     s.write(bytes(str(counter), 'ascii')) # Convert the decimal number to ASCII then send it to the Arduino
#     val = s.readline(s.inWaiting())
#     print(val) # Read the newest output from the Arduino
#     sleep(.1) # Delay for one tenth of a second
#     if counter == 255:
#        counter = 32