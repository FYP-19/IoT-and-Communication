import firebase_admin
from firebase_admin import credentials, firestore
import datetime;
import sys

# Initialize Firebase Admin SDK with your service account key
cred = credentials.Certificate("/home/fyp/fyp-19/scripts/credentials/fyp-app-643cb-firebase-adminsdk-rk1mo-459231c0ff.json")
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()

# Access the collection where you want to add the data

collection_ref_after = db.collection('trapStatus').document('0kuCvsdhGU45zwz2Lsas')


# Add data to the collection

data2 = {
    'cageId':'12',
    'status': 0
}

try:
    collection_ref_after.update(data2)
    print("Cage Reset Completed!")
except Exception as e:
    print("Data base update failed!")