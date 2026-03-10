import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, messaging

# 1. Reuse your exact setup to keep it secure
def init_firebase():
    firebase_creds = os.environ.get('FIREBASE_CREDENTIALS')
    if not firebase_creds:
        print("⚠️ No Firebase credentials found. Exiting.")
        return None
    
    cred_dict = json.loads(firebase_creds)
    cred = credentials.Certificate(cred_dict)
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
        
    return firestore.client()

def send_global_announcement():
    db = init_firebase()
    if not db: return

    tokens = []
    docs = db.collection('tokens').stream()
    for doc in docs:
        token_data = doc.to_dict()
        if 'token' in token_data:
            tokens.append(token_data['token'])
            
    if not tokens:
        print("No users found.")
        return

    # 2. Customize your message
    message = messaging.MulticastMessage(
        data={
            'title': "📢 KMC Notifier Update!",
            'body': "KMC Notifier is now simplified with a faster version. Tap to see the changes!",
            'url': "https://designswithharshit.github.io/KMC-Notifier/" 
        },
        tokens=tokens
    )
    
    try:
        response = messaging.send_each_for_multicast(message)
        print(f"Success! Sent {response.success_count} notifications.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_global_announcement()
