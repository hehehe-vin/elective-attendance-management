# local Firestore client setup (ensure GOOGLE_APPLICATION_CREDENTIALS set for GCP auth)
from google.cloud import firestore
db = firestore.Client()
