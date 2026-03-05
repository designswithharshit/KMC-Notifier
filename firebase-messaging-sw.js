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

// 1. Catch the hidden data from Python and show the notification
messaging.onBackgroundMessage(function(payload) {
  const notificationTitle = payload.data.title;
  const notificationOptions = {
    body: payload.data.body,
    icon: 'https://kmc.du.ac.in/home/officelogo/colllogo_new.fw.png',
    data: {
        url: payload.data.url // Save the URL so the click function can find it
    }
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});

// 2. Handle what happens when the user clicks the notification
self.addEventListener('notificationclick', function(event) {
  event.notification.close(); // Close the pop-up
  event.waitUntil(
    clients.openWindow(event.notification.data.url) // Open the website
  );
});
