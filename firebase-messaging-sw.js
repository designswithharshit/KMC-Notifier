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

// 1. Catch hidden data (App Closed)
messaging.onBackgroundMessage(function(payload) {
  const notificationOptions = {
    body: payload.data.body,
    icon: 'https://kmc.du.ac.in/home/officelogo/colllogo_new.fw.png',
    data: payload.data.url // Storing the URL directly
  };
  return self.registration.showNotification(payload.data.title, notificationOptions);
});

// 2. Bulletproof Click Handler
self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  
  // Fallback to your site URL just in case data gets lost
  const targetUrl = event.notification.data || 'https://designswithharshit.github.io/KMC-Notifier/';
  
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function(clientList) {
      // If website is already open in background, focus it
      for (let i = 0; i < clientList.length; i++) {
        let client = clientList[i];
        if (client.url === targetUrl && 'focus' in client) {
          return client.focus();
        }
      }
      // Otherwise, open a brand new tab
      if (clients.openWindow) {
        return clients.openWindow(targetUrl);
      }
    })
  );
});
