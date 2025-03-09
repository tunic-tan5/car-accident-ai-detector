CAR ACCIDENT AI DETECTOR
An AI-based system using OpenCV, Twilio, and Speech Recognition to detect driver drowsiness or accidents and send emergency alerts.

📌 Features
✅ Detects if a driver's eyes remain closed for too long
✅ Uses voice recognition to check if the driver is okay
✅ If no response, sends an emergency SMS via Twilio
✅ Uses OpenCV for face and eye detection
✅ Works with camera-based monitoring & voice detection

🛠️ Tech Stack
Python 🐍
OpenCV (for face & eye detection)
Twilio API (for emergency SMS alerts)
SpeechRecognition & Pyttsx3 (for voice interaction)
NumPy

 ->Run the script

 Set up Twilio
Create a Twilio account and get:
Account SID
Auth Token
Twilio Phone Number
add these details in script then run.
 
python camera.py
python voice.py

📌 How It Works

Monitors the driver’s face & eyes using OpenCV
If eyes remain closed for too long, it asks: "Are you okay?"
If no response or negative response, it sends an emergency SMS
Stops monitoring when the user confirms "I'm okay"
 
