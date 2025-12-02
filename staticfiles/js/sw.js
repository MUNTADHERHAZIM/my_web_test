// Service Worker for Muntazir Portfolio
// Provides offline caching and performance improvements

const CACHE_NAME = 'muntazir-portfolio-v1';
const STATIC_CACHE = 'static-v1';
const DYNAMIC_CACHE = 'dynamic-v1';

// Assets to cache immediately
const STATIC_ASSETS = [
    '/',
    '/static/css/responsive.css',
    '/static/css/home-fixes.css',
    '/static/css/rtl-support.css',
    '/static/js/performance-optimizations.js',
    '/static/images/default-avatar.svg',
    '/static/images/apple-touch-icon.png'
];

// Install event - cache static assets
self.addEventListener('install', event => {
    console.log('Service Worker installing...');
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service Worker activating...');
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                            console.log('Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => self.clients.claim())
    );
});

// Fetch event - serve from cache with network fallback
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip admin and API requests
    if (url.pathname.startsWith('/admin/') || 
        url.pathname.startsWith('/api/') ||
        url.pathname.includes('ckeditor')) {
        return;
    }

    event.respondWith(
        cacheFirst(request)
    );
});

// Cache-first strategy for static assets
async function cacheFirst(request) {
    const url = new URL(request.url);
    
    // For static assets, use cache-first
    if (url.pathname.startsWith('/static/')) {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        try {
            const networkResponse = await fetch(request);
            if (networkResponse.ok) {
                const cache = await caches.open(STATIC_CACHE);
                cache.put(request, networkResponse.clone());
            }
            return networkResponse;
        } catch (error) {
            console.log('Network failed for static asset:', request.url);
            return new Response('Asset not available offline', { status: 503 });
        }
    }
    
    // For HTML pages, use network-first with cache fallback
    return networkFirst(request);
}

// Network-first strategy for HTML pages
async function networkFirst(request) {
    try {
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.log('Network failed, trying cache:', request.url);
        
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Return offline page if available
        const offlinePage = await caches.match('/offline/');
        if (offlinePage) {
            return offlinePage;
        }
        
        return new Response('Page not available offline', {
            status: 503,
            headers: { 'Content-Type': 'text/html' }
        });
    }
}

// Background sync for form submissions
self.addEventListener('sync', event => {
    if (event.tag === 'contact-form') {
        event.waitUntil(syncContactForm());
    }
});

// Sync contact form when online
async function syncContactForm() {
    try {
        // Get pending form data from IndexedDB
        const pendingForms = await getPendingForms();
        
        for (const formData of pendingForms) {
            try {
                const response = await fetch('/contact/', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    await removePendingForm(formData.id);
                }
            } catch (error) {
                console.log('Failed to sync form:', error);
            }
        }
    } catch (error) {
        console.log('Background sync failed:', error);
    }
}

// IndexedDB helpers (simplified)
async function getPendingForms() {
    // Implementation would use IndexedDB to store/retrieve pending forms
    return [];
}

async function removePendingForm(id) {
    // Implementation would remove form from IndexedDB
    console.log('Form synced:', id);
}

// Push notification handling
self.addEventListener('push', event => {
    if (!event.data) return;
    
    const data = event.data.json();
    const options = {
        body: data.body,
        icon: '/static/images/apple-touch-icon.png',
        badge: '/static/images/apple-touch-icon.png',
        vibrate: [200, 100, 200],
        data: {
            url: data.url || '/'
        },
        actions: [
            {
                action: 'view',
                title: 'View',
                icon: '/static/images/apple-touch-icon.png'
            },
            {
                action: 'close',
                title: 'Close'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    if (event.action === 'view') {
        const url = event.notification.data.url || '/';
        event.waitUntil(
            clients.openWindow(url)
        );
    }
});

// Periodic background sync for cache updates
self.addEventListener('periodicsync', event => {
    if (event.tag === 'cache-update') {
        event.waitUntil(updateCache());
    }
});

// Update cache in background
async function updateCache() {
    try {
        const cache = await caches.open(STATIC_CACHE);
        const requests = await cache.keys();
        
        for (const request of requests) {
            try {
                const response = await fetch(request);
                if (response.ok) {
                    await cache.put(request, response);
                }
            } catch (error) {
                console.log('Failed to update cache for:', request.url);
            }
        }
    } catch (error) {
        console.log('Cache update failed:', error);
    }
}

console.log('Service Worker loaded');