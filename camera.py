import cv2
import time
import numpy as np
import speech_recognition as sr
import pyttsx3
from twilio.rest import Client

# Twilio setup
TWILIO_SID = "ACed2910aec66d1f6142eacb5d33905f88"
TWILIO_AUTH_TOKEN = "32ccfb78c9d32c41e4a706ebc432c59c"
TWILIO_PHONE_NUMBER = " " # registered twilio phone number
EMERGENCY_CONTACTS = [
    'your phone number',  # Emergency contact 1
]

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_response(timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for response...")
        try:
            audio = recognizer.listen(source, timeout=timeout)
            response = recognizer.recognize_google(audio).lower()
            print("User response:", response)
            return response
        except sr.UnknownValueError:
            print("Could not understand response.")
        except sr.WaitTimeoutError:
            print("No response detected.")
    return None

def send_emergency_message():
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for contact in EMERGENCY_CONTACTS:
        try:
            message = client.messages.create(
                body="Emergency! hey your friend is in danger, please check on them.",
                from_=TWILIO_PHONE_NUMBER,
                to=contact  # Send the message to each contact individually
            )
            print(f"Emergency message sent to {contact}!")
        except Exception as e:
            print(f"Failed to send message to {contact}. Error: {str(e)}")


# Load OpenCV face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

cap = cv2.VideoCapture(0)
eyes_closed_time = 0
EYES_CLOSED_THRESHOLD = 5  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    eyes_detected = False
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) > 0:
            eyes_detected = True
    
    if not eyes_detected:
        if eyes_closed_time == 0:
            eyes_closed_time = time.time()
        elif time.time() - eyes_closed_time > EYES_CLOSED_THRESHOLD:
            print("Eyes closed for too long! Checking if the driver is okay...")
            speak("Are you okay?")
            response = listen_for_response()
            
            if response and ("okay" in response or "yes" in response):
                print("User confirmed they are okay. No action needed.")
            else:
                speak("I will ask one more time. Are you okay?")
                response = listen_for_response()
                if response and ("okay" in response or "yes" in response):
                    print("User confirmed they are okay. No action needed.")
                else:
                    send_emergency_message()
            
            eyes_closed_time = 0  # Reset the timer
    else:
        eyes_closed_time = 0  # Reset the timer if eyes are detected
    
    cv2.imshow("Driver Monitoring", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
