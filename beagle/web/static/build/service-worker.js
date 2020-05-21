/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("/workbox-v3.6.3/workbox-sw.js");
workbox.setConfig({modulePathPrefix: "/workbox-v3.6.3"});

importScripts(
<<<<<<< HEAD
  "/precache-manifest.a95933fa36e63b9c6aba0dad3cbb3ce3.js"
=======
  "/precache-manifest.de804af3b62b8e1166357be605626360.js"
>>>>>>> f3e4346e8979532d2b74fb053577974619e352bb
);

workbox.clientsClaim();

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.suppressWarnings();
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});

workbox.routing.registerNavigationRoute("/index.html", {
  
<<<<<<< HEAD
  blacklist: [/^\/_/,/\/[^/]+\.[^/]+$/],
=======
  blacklist: [/^\/_/,/\/[^\/]+\.[^\/]+$/],
>>>>>>> f3e4346e8979532d2b74fb053577974619e352bb
});
