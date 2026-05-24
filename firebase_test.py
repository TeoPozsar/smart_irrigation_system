import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("smart-irrigation-fd7ae-firebase-adminsdk-fbsvc-adbe6d3445.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection("test").document("sample")
doc_ref.set({
    "message": "Hello from Raspberry Pi",
    "status": "working"
})

print("Data sent to Firebase!")
