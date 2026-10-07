/* =========================================================
   ARIVORA AI
   SERVICE WORKER
   OFFLINE LEARNING SUPPORT
========================================================= */


/* =========================================================
   CACHE CONFIGURATION
========================================================= */

const CACHE_NAME = "arivora-ai-v2.2";


const STATIC_FILES = [

    "./",

    "./index.html",

    "./style.css",

    "./script.js",

    "./service-worker.js",

    /* Bootstrap */

    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",

    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js",

    /* Bootstrap Icons */

    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"

];


/* =========================================================
   INSTALL EVENT
========================================================= */

self.addEventListener(
    "install",
    event => {

        console.log(
            "ARIVORA AI Service Worker installing..."
        );


        event.waitUntil(

            caches
                .open(CACHE_NAME)
                .then(cache => {

                    console.log(
                        "Caching ARIVORA AI files..."
                    );


                    /*
                        Cache files individually.

                        If an external CDN fails,
                        the remaining application
                        files can still be cached.
                    */

                    return Promise.all(

                        STATIC_FILES.map(
                            file => {

                                return cache
                                    .add(file)
                                    .catch(
                                        error => {

                                            console.log(
                                                "Unable to cache:",
                                                file
                                            );

                                        }
                                    );

                            }
                        )

                    );

                })

        );


        self.skipWaiting();

    }
);


/* =========================================================
   ACTIVATE EVENT
========================================================= */

self.addEventListener(
    "activate",
    event => {

        console.log(
            "ARIVORA AI Service Worker activated."
        );


        event.waitUntil(

            caches
                .keys()
                .then(cacheNames => {

                    return Promise.all(

                        cacheNames
                            .map(cacheName => {

                                if (
                                    cacheName !==
                                    CACHE_NAME
                                ) {

                                    console.log(
                                        "Deleting old cache:",
                                        cacheName
                                    );


                                    return caches
                                        .delete(
                                            cacheName
                                        );

                                }

                            })

                    );

                })

        );


        self.clients.claim();

    }
);


/* =========================================================
   FETCH EVENT
========================================================= */

self.addEventListener(
    "fetch",
    event => {

        /*
            Only handle GET requests.
        */

        if (event.request.method !== "GET") {
            return;
        }

        event.respondWith(
            fetch(event.request)
                .then(networkResponse => {
                    if (networkResponse && networkResponse.status === 200) {
                        const responseClone = networkResponse.clone();
                        caches.open(CACHE_NAME).then(cache => {
                            cache.put(event.request, responseClone);
                        });
                    }
                    return networkResponse;
                })
                .catch(() => {
                    return caches.match(event.request).then(cached => {
                        return cached || caches.match("./index.html");
                    });
                })
        );
    }
);


/* =========================================================
   MESSAGE EVENT
========================================================= */

self.addEventListener(
    "message",
    event => {

        if (
            !event.data
        ) {

            return;

        }


        /* -----------------------------------------
           SKIP WAITING
        ----------------------------------------- */

        if (
            event.data.type ===
            "SKIP_WAITING"
        ) {

            self.skipWaiting();

        }


        /* -----------------------------------------
           CLEAR CACHE
        ----------------------------------------- */

        if (
            event.data.type ===
            "CLEAR_CACHE"
        ) {

            caches
                .delete(
                    CACHE_NAME
                )
                .then(
                    () => {

                        console.log(
                            "ARIVORA AI cache cleared."
                        );

                    }
                );

        }

    }
);


/* =========================================================
   BACKGROUND SYNC
========================================================= */

self.addEventListener(
    "sync",
    event => {

        if (
            event.tag ===
            "arivora-study-sync"
        ) {

            event.waitUntil(
                syncStudyData()
            );

        }

    }
);


async function syncStudyData() {

    console.log(
        "ARIVORA AI study data sync started."
    );


    /*
        Future backend integration:

        - Sync quiz progress
        - Sync uploaded material metadata
        - Sync exam reminders
        - Sync study history
        - Sync voice notes

        when internet becomes available.
    */

}


/* =========================================================
   PUSH NOTIFICATIONS
========================================================= */

self.addEventListener(
    "push",
    event => {

        let data = {

            title:
                "ARIVORA AI",

            body:
                "Your daily study reminder is ready.",

            icon:
                "./icons/icon-192.png",

            badge:
                "./icons/icon-192.png"

        };


        if (
            event.data
        ) {

            try {

                data =
                    event.data.json();

            } catch {

                data.body =
                    event.data.text();

            }

        }


        event.waitUntil(

            self.registration
                .showNotification(
                    data.title,
                    {

                        body:
                            data.body,

                        icon:
                            data.icon,

                        badge:
                            data.badge,

                        vibrate:
                            [
                                100,
                                50,
                                100
                            ],

                        data:
                            {
                                url:
                                    "./index.html"
                            }

                    }
                )

        );

    }
);


/* =========================================================
   NOTIFICATION CLICK
========================================================= */

self.addEventListener(
    "notificationclick",
    event => {

        event.notification.close();


        event.waitUntil(

            clients
                .matchAll({
                    type: "window",
                    includeUncontrolled: true
                })
                .then(
                    clientList => {

                        for (
                            const client
                            of clientList
                        ) {

                            if (
                                "focus"
                                in client
                            ) {

                                return client
                                    .focus();

                            }

                        }


                        if (
                            clients.openWindow
                        ) {

                            return clients
                                .openWindow(
                                    "./index.html"
                                );

                        }

                    }
                )

        );

    }
);


/* =========================================================
   OFFLINE STATUS MESSAGE
========================================================= */

self.addEventListener(
    "message",
    event => {

        if (
            event.data?.type ===
            "CHECK_OFFLINE_STATUS"
        ) {

            event.source.postMessage({

                type:
                    "OFFLINE_STATUS",

                status:
                    "ARIVORA AI Offline Mode Ready"

            });

        }

    }
);


/* =========================================================
   SERVICE WORKER READY
========================================================= */

console.log(
    "%c ARIVORA AI OFFLINE ENGINE READY ",
    "font-weight:bold;font-size:16px;"
);
