# 📢 College Notice Alert System

Never miss an important college notice again.

This project monitors the official college website for new notices and sends real-time browser notifications to subscribed users through a dedicated notification website.

---

## 🚀 Why This Project Exists

College notices are often published only on the official website, with no direct alert system. Students frequently miss important updates such as:

- Exam schedules  
- Seating plans  
- Fee deadlines  
- Academic announcements  
- Urgent administrative notices  

This system solves that problem by automatically detecting new notices and notifying students instantly.

---

## 🧠 How It Works

The system consists of three main parts:

### 1️⃣ Scraper (Python)

- Scrapes the official college website  
- Stores notice data in a JSON file  
- Detects newly published notices  
- Triggers push notifications when new content appears  

### 2️⃣ Notification Website (GitHub Pages)

- Displays latest notices  
- Allows users to subscribe to browser notifications  
- Works on both mobile and desktop  

### 3️⃣ Push Notification Service

- Uses Firebase Cloud Messaging (FCM)  
- Sends real-time browser notifications  
- No email, no login, no personal data collection  

---

## 🔔 How Users Receive Notifications

1. Visit the notification website  
2. Click **Subscribe**  
3. Allow browser notifications  

That’s it.

When a new notice is published, users receive:

📢 New Notice Published  
Tap to view details

Even if the website is closed.

---

## 🛠 Tech Stack

- Python (Requests + BeautifulSoup)
- JSON for notice tracking
- GitHub Actions (automation)
- GitHub Pages (frontend hosting)
- Firebase Cloud Messaging (push notifications)

---

## 📂 Project Structure

```
scraper/
├── scraper.py
├── notices.json
└── send_push.py

site/
├── index.html
├── firebase.js
├── sw.js
```


---

## 🔐 Privacy & Security

- No email collection  
- No personal data stored  
- Only anonymous device tokens are used for push delivery  
- Secrets are stored securely using environment variables  

---

## ⚙️ Deployment

- Scraper runs automatically via GitHub Actions  
- Notification website is hosted on GitHub Pages  
- Firebase handles message delivery  

---

## 📈 Future Improvements

- Department-specific notifications  
- Keyword-based filtering  
- Notice categorization  
- Official integration with college website  

---

## ⚠️ Disclaimer

This is an independent student-built project and is not officially affiliated with the college unless adopted by the institution.
