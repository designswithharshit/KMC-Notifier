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

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

// Handles background notifications automatically
messaging.onBackgroundMessage(function(payload) {
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: 'https://kmc.du.ac.in/home/img/favicon.fw.png'
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});