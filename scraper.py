import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore, messaging
import base64
import uuid

# 1. Initialize Firebase (Using GitHub Secrets)
def init_firebase():
    firebase_creds = os.environ.get('FIREBASE_CREDENTIALS')
    if not firebase_creds:
        print("⚠️ No Firebase credentials found in environment. Skipping Push Notifications.")
        return None
    
    cred_dict = json.loads(firebase_creds)
    cred = credentials.Certificate(cred_dict)
    
    # Prevent initializing multiple times
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
        
    return firestore.client()

# 2. The Deep Dive Function
def get_rich_notice_data(notice_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(notice_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    main_window = soup.find('div', class_='col-md-9')
    if not main_window:
        return {"text": "Content could not be extracted.", "date": "Unknown Date", "pdfs": [], "images": []}

    card_body = main_window.find('div', class_='card-body')
    card_footer = main_window.find('div', class_='card-footer')

    extracted_data = {"text": "", "date": "Unknown Date", "pdfs": [], "images": []}

    if card_body:
        extracted_data["text"] = card_body.get_text(separator='<br><br>', strip=True)
        for a_tag in card_body.find_all('a'):
            href = a_tag.get('href')
            if href and '.pdf' in href.lower():
                if href.startswith('/'):
                    href = "https://kmc.du.ac.in" + href
                extracted_data["pdfs"].append(href)

       for img in card_body.find_all('img'):

            src = img.get('src')
        
            if not src:
                continue
        
            # convert base64 image to real file and store locally
            if src.startswith('data:image'):
                header, encoded = src.split(',', 1)
                image_data = base64.b64decode(encoded)
        
                os.makedirs("images", exist_ok=True)
        
                filename = f"images/{uuid.uuid4()}.jpg"
        
                with open(filename, "wb") as f:
                    f.write(image_data)
        
                extracted_data["images"].append(filename)
                continue
        
            # convert relative path to full url
            if src.startswith('/'):
                src = "https://kmc.du.ac.in" + src
        
            if src not in extracted_data["images"]:
                extracted_data["images"].append(src)

    if card_footer:
        fonts = card_footer.find_all('font')
        for font in fonts:
            if font.find('i', class_='fa-calendar'):
                extracted_data["date"] = font.text.strip()
                break

    return extracted_data

# 3. The Firebase Push Function
def send_push_notifications(db, new_notices):
    if not db or not new_notices: return

    # Get all subscriber tokens from Firestore
    tokens = []
    docs = db.collection('tokens').stream()
    for doc in docs:
        token_data = doc.to_dict()
        if 'token' in token_data:
            tokens.append(token_data['token'])
            
    if not tokens:
        print("No subscribers found in database.")
        return
    
    # Format the notification text

    if len(new_notices) == 1:
        title = "📢 New KMC Notice"
        notice_body = new_notices[0]['title']
    else:
        title = f"📢 {len(new_notices)} New KMC Notices"
        notice_body = "Tap to view the latest updates on the notice board."

    # Build a DATA-ONLY push message
    message = messaging.MulticastMessage(
            data={
                'title': title,
                'body': notice_body,
                'url': 'https://designswithharshit.github.io/KMC-Notifier/',
                'notice_link': new_notices[0]['link'] if len(new_notices) == 1 else ''
            },
            tokens=tokens
    )
    
    # Blast it out
    try:
        response = messaging.send_each_for_multicast(message)

        print(f"Successfully sent {response.success_count} push notifications!")
        print(f"Failed to send {response.failure_count} notifications.")
        
        # Remove invalid tokens automatically
        for idx, resp in enumerate(response.responses):
            if not resp.success:
                bad_token = tokens[idx]
                print(f"Removing invalid token: {bad_token}")
                db.collection('tokens').document(bad_token).delete()
    except Exception as e:
        print(f"Error sending notifications: {e}")

# 4. The Main Scraper Function
def get_and_filter_notices():
    db = init_firebase()
    
    url = "https://kmc.du.ac.in/kmcouter/collnews/NA/8888/All/All"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Changed to notices.json so your index.html can read it directly
    db_file = "notices.json" 
    
    if os.path.exists(db_file):
        with open(db_file, "r", encoding="utf-8") as f:
            notices_db = json.load(f)
    else:
        notices_db = {}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    sidebar = soup.find('div', class_='sidebar-box-inner')

    current_time = datetime.now()
    seven_days_ago = current_time - timedelta(days=30)
    
    notices = sidebar.find_all('li')
    new_notices_list = [] 

    print("Checking KMC Notices...")

    for notice in notices:
        link_tag = notice.find('a')
        if not link_tag: continue
            
        title = link_tag.text.strip()
        link = link_tag.get('href')
        
        if "Back to Home" in title: continue

        if link not in notices_db:
            # We fetch the rich data IMMEDIATELY so it's saved in the JSON for the website
            rich_data = get_rich_notice_data(link)
            
            notices_db[link] = {
                "title": title,
                "link": link,
                "date": rich_data['date'],
                "text": rich_data['text'],
                "pdfs": rich_data['pdfs'],
                "images": rich_data['images'],
                "discovered_on": current_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            new_notices_list.append(notices_db[link])
            print(f"New Notice Found & Processed: {title}")

    # Clean up notices older than 7 days to keep the website fast
    keys_to_delete = [link for link, data in notices_db.items() if datetime.strptime(data["discovered_on"], "%Y-%m-%d %H:%M:%S") < thirty_days_ago]
    for key in keys_to_delete:
        del notices_db[key]

    sorted_notices = dict(
    sorted(
        notices_db.items(),
        key=lambda item: item[1]["discovered_on"],
        reverse=True
        )
    )
    
    with open(db_file, "w", encoding="utf-8") as f:
        json.dump(sorted_notices, f, indent=4)

    if new_notices_list:
        print("Triggering Firebase Push Notifications...")
        send_push_notifications(db, new_notices_list)
    else:
        print("No new notices found.")

if __name__ == "__main__":

    get_and_filter_notices()











