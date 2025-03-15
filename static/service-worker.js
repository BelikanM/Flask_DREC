const CACHE_NAME = 'drecouvrement-cache-v1';
const FILES_TO_CACHE = [
    '/',
    '/index.html',
    '/static/app.js',
    '/static/styles.css',
    '/static/2uLgjGtq4u4Uh7PTbKG30AvJFaQ.svg',
    '/static/2uLj3r1phyUxfMGyQyicurrdVpk.svg',
    '/static/icons',
    '/static/manifest.json',
    '/static/vectorizer.pkl',
    '/static/model.pkl'
];

// Installation du service worker et mise en cache des fichiers
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                return cache.addAll(FILES_TO_CACHE);
            })
    );
});

// Activation du service worker
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Gestion des requêtes en utilisant le cache
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;  // Si le fichier est dans le cache, le renvoyer
            }
            return fetch(event.request);  // Sinon, faire une requête réseau
        })
    );
});
