importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js');

const firebaseConfig = {
  apiKey: "AIzaSyCoPs4FCINqAhX4EQ1k-kOzDCPLxHnFQNQ",
  authDomain: "kmc-notifier.firebaseapp.com",
  projectId: "kmc-notifier",
  storageBucket: "kmc-notifier.firebasestorage.app",
  messagingSenderId: "662736328747",
  appId: "1:662736328747:web:2bc93b40ae57971c85326e"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

// 1. Catch the hidden data from Python (When app is CLOSED)
messaging.onBackgroundMessage(function(payload) {
  const notificationOptions = {
    body: payload.data.body,
    icon: 'https://kmc.du.ac.in/home/officelogo/colllogo_new.fw.png',
    data: { url: payload.data.url } 
  };

  // The 'return' stops Android from killing the script early!
  return self.registration.showNotification(payload.data.title, notificationOptions);
});

// 2. Handle the Click Action
self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true })
    .then((clientList) => {
    
    for (const client of clientList) {
        if (client.url === event.notification.data.url && "focus" in client) {
            return client.focus();
        }
    }
    
    if (clients.openWindow) {
        return clients.openWindow(event.notification.data.url);
    }
    });
  );
});

