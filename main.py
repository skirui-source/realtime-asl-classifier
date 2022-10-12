import tensorflow as tf
import keras
import cv2
import numpy as np


digits= ["0", "1" , "2", "3", "4", "5", "6", "7", "8", "9"]
mobilenet = keras.models.load_model("mobilenet")

video_capture = cv2.VideoCapture(0)

width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    if ret is False:
        print("warning: image could not be loaded")

    # ROI coordinates
    left = int(0.5*width)
    top = int(0.5*height)
    right = left+250
    bottom =  top+250
    
    # print((left, top), (right, bottom))
    
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255,0), 2)
    roi = frame[top:bottom, left:right]
    
    # cv2.imshow("roi", roi)
    
    # Only process and predict the region of interest
    image = cv2.resize(roi, (224, 224)) 
    image_np = np.array(image)

    img_array_scaled = keras.applications.mobilenet.preprocess_input(image_np)
    img_array_expanded_dims = np.expand_dims(img_array_scaled, axis=0)
    
    proba = mobilenet.predict(img_array_expanded_dims)
    idx = np.argmax(proba)
    
    pred = digits[idx]

    # Display the results and draw label above the gesture
    font=cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, pred, (left+50, top-40), font, 3, (0,0,255), 2)
    
    # Display the resulting image
    cv2.imshow('full picture', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
