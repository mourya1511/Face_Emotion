# Face_Emotion

Overview
This project implements a facial emotion detection system that integrates with Firebase Realtime Database for user data management. It uses a trained convolutional neural network model for emotion detection from facial expressions captured through a webcam. Based on the detected emotion, the program plays a related YouTube video. Additionally, it validates user email, updates visitor counts, and stores user data in Firebase.

Features
Facial Emotion Detection: Detects seven types of emotions (angry, disgust, fear, happy, neutral, sad, surprise) from webcam input using a pre-trained Keras model.
Real-time Video Analysis: Processes video frames in real-time using OpenCV to detect faces and predict emotions.
YouTube Video Playback: Plays YouTube videos related to the detected emotion using PyWhatKit.
Firebase Integration: Stores user data and tracks the number of visitors using Firebase Realtime Database.
User Input: Collects user email and password using EasyGUI.
Setup and Installation
Prerequisites
Python 3.x

Required Libraries: Install the necessary Python packages using pip:

bash
Copy code
pip install opencv-python keras numpy pywhatkit firebase-admin easygui
Firebase Setup:

Create a Firebase project and enable Realtime Database.
Download the Firebase Admin SDK service account key as a .json file and update the path in the code:
python
Copy code
cred = credentials.Certificate(r"C:\path\to\your\firebase-adminsdk-key.json")
Files and Resources
Model files: The emotion detection model (facialemotionmodel.json and facialemotionmodel.h5) should be in the project directory.
Haar Cascade: The OpenCV Haar Cascade file for face detection is automatically loaded from the OpenCV library.
Code Explanation
1. Firebase Initialization
python
Copy code
cred = credentials.Certificate(r"C:\path\to\your\firebase-adminsdk-key.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://your-database-url.firebaseio.com/'})
Initializes Firebase Admin SDK with credentials and connects to the Realtime Database.

2. Email Validation
python
Copy code
def validate_email(email):[Uploading train-checkpoint.ipynb…]()

    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email)
Validates that the user's email follows the Gmail format.

3. Updating Visitor Count
python
Copy code
def update_visitors_count():
    ref = db.reference('visitors')
    count = ref.get() or 0
    ref.set(count + 1)
Updates the count of visitors in Firebase.

4. Storing User Data
python
Copy code
def store_user_data(email, password):
    ref = db.reference('users')
    ref.push({'email': email, 'password': password})
Stores the user's email and password in the Firebase Realtime Database.

5. Emotion Detection and YouTube Video Playback
python
Copy code
def detect_emotions():
    ...
    labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
    emotion_links = {
        'angry': "https://www.youtube.com/results?search_query=angry+songs+in+kannada",
        'disgust': "https://www.youtube.com/results?search_query=disgust+songs+",
        ...
    }
    ...
Uses a Keras model to predict emotions and map them to corresponding YouTube links. When a non-neutral emotion is detected, a YouTube video is played using PyWhatKit.

6. Face Detection
python
Copy code
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
Detects faces in the webcam video stream using OpenCV's Haar Cascade.

7. Emotion Prediction and Video Playback
python
Copy code
face_pred = model.predict(face_feature)
face_prediction_label = labels[face_pred.argmax()]
Predicts the emotion from the detected face and plays a YouTube video based on the prediction.

How to Run
Ensure that your Firebase Realtime Database is set up and the necessary credentials file is in place.
Run the Python script. It will:
Prompt the user for their email and password.
Update the visitor count and store user data in Firebase.
Launch the webcam to start real-time facial emotion detection and play YouTube videos based on the detected emotions.
Future Improvements
Enhance the emotion detection model by training on a larger dataset.
Implement better security for storing user passwords, such as hashing.
Add more emotions and refine the YouTube video recommendations.
