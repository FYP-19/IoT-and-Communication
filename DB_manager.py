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
collection_ref_before = db.collection('results')
collection_ref_after = db.collection('trapStatus').document('0kuCvsdhGU45zwz2Lsas')

cage_id = sys.argv[1]
accuracy = sys.argv[2]
animal_type = sys.argv[3]


# Add data to the collection
data1 = {
    'accuracy': int(accuracy),
    'cageId': cage_id,
    'type':animal_type,
    'date': datetime.datetime.now()
    # Add more fields as needed
}

data2 = {
    'cageId':cage_id,
    'status': 1
}

try:
    collection_ref_before.add(data1)
    collection_ref_after.update(data2)
    print("Databse Sucessfully Updated!")
    print(f"============================================================== \n")
except Exception as e:
    print("Data base update failed!")