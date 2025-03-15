const cacheName = 'my-pwa-cache-v1';
const resourcesToCache = [
    '/',
    '/index.html',
    '/static/app.js',
    '/static/styles.css',
    '/static/2uLgjGtq4u4Uh7PTbKG30AvJFaQ.svg', // tes images SVG
    '/static/2uLj3r1phyUxfMGyQyicurrdVpk.svg',
    '/static/icons', // si tu veux aussi mettre en cache ton dossier icons
    '/static/manifest.json',
    '/static/vectorizer.pkl',
    '/static/model.pkl',
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(cacheName)
            .then((cache) => {
                return cache.addAll(resourcesToCache);
            })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((cachedResponse) => {
                if (cachedResponse) {
                    return cachedResponse;
                }
                return fetch(event.request);
            })
    );
});
