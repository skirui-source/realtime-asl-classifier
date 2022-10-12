from flask import Flask, render_template, Response
import tensorflow as tf
import keras
import cv2
import numpy as np


app=Flask(__name__)

digits= ["0", "1" , "2", "3", "4", "5", "6", "7", "8", "9"]
mobilenet = keras.models.load_model("mobilenet")

camera = cv2.VideoCapture(0)

width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

def generate_frames():
    while True:
        # Grab a single frame of video
        success, frame = camera.read()
        
        if not success:
            break
        else:
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


            ret, buffer = cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=='__main__':
    app.run()


