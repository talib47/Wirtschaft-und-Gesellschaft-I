/* Offline-Modus: Die App startet auch ohne Internet.
   Seiten der App: erst Netz (höchstens 3 Sekunden, damit gedrosseltes Datenvolumen nicht hängt), sonst die gespeicherte Kopie.
   GitHub-Abgleich (api.github.com) läuft nie über diesen Speicher. Der Lernstand liegt ohnehin im Gerät (localStorage). */
const CACHE = "wug-offline-v1";
const CORE = ["./", "./index.html", "./manifest.webmanifest?v=2", "./icon-192.png?v=2", "./apple-touch-icon.png?v=2"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

function timeout(ms){ return new Promise((_, rej) => setTimeout(() => rej(new Error("timeout")), ms)); }

self.addEventListener("fetch", e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== self.location.origin) return;
  if (url.pathname.endsWith("version.txt")) {   // Update-Check: nur aus dem Netz, offline einfach „keine Antwort“
    e.respondWith(fetch(req).catch(() => new Response("", {status: 503}))); return;
  }
  const isPage = req.mode === "navigate" || /\/(index\.html)?$/.test(url.pathname);
  const key = isPage ? "./index.html" : req;
  /* Auch wenn die 3 Sekunden ablaufen, lädt das Netz im Hintergrund weiter und aktualisiert die Kopie fürs nächste Mal. */
  const net = fetch(req).then(async res => { if (res && res.ok) { const c = await caches.open(CACHE); await c.put(key, res.clone()); } return res; });
  e.waitUntil(net.catch(() => {}));
  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    try {
      return await Promise.race([net, timeout(3000)]);
    } catch (err) {
      const hit = isPage ? await cache.match("./index.html") : await cache.match(req, {ignoreSearch: false}) || await cache.match(req, {ignoreSearch: true});
      if (hit) return hit;
      throw err;
    }
  })());
});
