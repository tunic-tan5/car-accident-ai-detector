import speech_recognition as sr
import pyttsx3
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak out a message
def speak(message):
    engine.say(message)
    engine.runAndWait()

# Function to listen for voice input
def listen_for_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening for help...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing speech...")
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return ""

# Main function to check distress signal
def check_for_distress():
    # Ask the user if they're okay
    speak("Are you okay? Please respond.")
    time.sleep(2)
    
    # Listen to the response
    response = listen_for_audio()
    
    # Check for distress signals (e.g., "help" or "emergency")
    distress_keywords = ['help', 'emergency', 'distress', 'help me', 'save me']
    
    if any(keyword in response for keyword in distress_keywords):
        speak("Help is coming.")
    else:
        speak("Please respond if you're in danger. Are you okay?")

# Main loop to simulate the car monitoring system
def car_monitoring_system():
    while True:
        # Simulate continuous monitoring inside the car for distress
        print("Monitoring...")

        # Wait for any distress signals or specific keywords
        listen_for_audio()
        
        # Check if any distress signals are detected
        check_for_distress()

        time.sleep(5)  # Wait before checking again

if __name__ == "__main__":
    car_monitoring_system()

