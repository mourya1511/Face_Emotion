import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\Admin\project\face_emotion\chat-fa5cf-firebase-adminsdk-7qtt1-4dc17c8473.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chat-fa5cf-default-rtdb.firebaseio.com/'  # Replace with your Firebase Realtime Database URL
})

# Function to store data in Firebase Realtime Database
def store_data(data):
    ref = db.reference('visitors/to/data')
    ref.push(data)

# Example usage
data = {'name': 'John', 'age': 30}
store_data(data)
