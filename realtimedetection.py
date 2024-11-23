import cv2
from keras.models import model_from_json
from keras.models import Sequential
import numpy as np
import pywhatkit
import time
import firebase_admin
from firebase_admin import credentials, db
import easygui
import re

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\Admin\project\face_emotion\chat-fa5cf-firebase-adminsdk-7qtt1-4dc17c8473.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chat-fa5cf-default-rtdb.firebaseio.com/'  # Replace with your Firebase Realtime Database URL
})

# Function to validate email format
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email)

# Function to update visitors count in Firebase Realtime Database
def update_visitors_count():
    ref = db.reference('visitors')
    count = ref.get()  # Get current count
    if count is None:
        count = 1
    elif isinstance(count, dict):
        count = len(count) + 1  # Increment count considering it's a dictionary
    else:
        count = int(count) + 1  # Convert to integer and increment count
    ref.set(count)  # Update count

# Function to store user data in Firebase Realtime Database
def store_user_data(email, password):
    ref = db.reference('users')
    ref.push({
        'email': email,
        'password': password
    })

# Function to detect facial emotions and perform actions accordingly
def detect_emotions():
    # Load the facial emotion model
    json_file = open("facialemotionmodel.json", "r")
    model_json = json_file.read()
    json_file.close()
    model = model_from_json(model_json)
    model.load_weights("facialemotionmodel.h5")

    # Load the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Map emotions to YouTube links
    emotion_links = {
        'angry': "https://www.youtube.com/results?search_query=angry+songs+in+kannada",
        'disgust': "https://www.youtube.com/results?search_query=disgust+songs+",
        'fear': "https://www.youtube.com/results?search_query=bakhti+songs+kannada",
        'happy': "https://www.youtube.com/results?search_query=happy+songs+english",
        'sad': "https://www.youtube.com/results?search_query=sad+songs+kannada",
        'surprise': "https://www.youtube.com/results?search_query=surprise+songs+kannada"
    }

    # Define emotion labels
    labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

    # State variable to track if a link has been opened for each face
    links_opened = {}

    # Initialize webcam
    webcam = cv2.VideoCapture(0)

    while True:
        try:
            # Read frame from webcam
            ret, frame = webcam.read()
            if not ret:
                break

            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                # Extract face region
                face_image = gray[y:y + h, x:x + w]
                face_image = cv2.resize(face_image, (48, 48))
                face_feature = np.array(face_image).reshape(1, 48, 48, 1) / 255.0

                # Predict emotion
                face_pred = model.predict(face_feature)
                face_prediction_label = labels[face_pred.argmax()]

                # Skip processing for neutral emotion
                if face_prediction_label.lower() == 'neutral':
                    continue

                # Play a YouTube video based on the detected emotion for each face
                if face_prediction_label.lower() in emotion_links:
                    youtube_link = emotion_links[face_prediction_label.lower()]
                    if (x, y) not in links_opened or not links_opened[(x, y)]:
                        pywhatkit.playonyt(youtube_link)
                        links_opened[(x, y)] = True  # Set the state to indicate that a link has been opened for this face
                        time.sleep(5)  # Add a delay to give the user time with the link
                    else:
                        links_opened[(x, y)] = False  # Reset the state if the user closes the link

                # Draw rectangle around the face and put label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, '%s' % (face_prediction_label), (x - 10, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,
                            (0, 0, 255))

            # Display the frame
            cv2.imshow("Emotion Detection", frame)

            # Exit if 'Esc' key is pressed
            key = cv2.waitKey(1)
            if key == 27:
                break
        except cv2.error:
            pass

    # Release the webcam and close all OpenCV windows
    webcam.release()
    cv2.destroyAllWindows()

# Get user's email and password through easygui
email = easygui.enterbox("Enter your email:")
# Validate email format
if not validate_email(email):
    print("Invalid email format. Please enter a valid Gmail address.")
else:
    password = easygui.passwordbox("Enter your password:")

    # Update visitors count, store user data, and start facial emotion detection
    update_visitors_count()  # Update visitors count
    store_user_data(email, password)  # Store user data
    detect_emotions()  # Start facial emotion detection
