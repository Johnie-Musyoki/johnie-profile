"""Submit the profile URL to search engines via the IndexNow protocol.

The old sitemap ping endpoints are gone: Google deprecated its in June 2023
(the endpoint now 404s) and Bing returns 410. IndexNow is the current
mechanism, and works with a shared key hosted on the site.

The key file must be served from the host root, which for a GitHub Pages
project site means the repository root, so the deployed path is
  <site>/<key>.txt
not <site>/johnie-profile/<key>.txt.

Usage:
    python _indexnow_submit.py <site-url> [key]
"""
import json
import sys
import urllib.request

SITE = (sys.argv[1] if len(sys.argv) > 1 else
        "https://johnie-musyoki.github.io/johnie-profile/").rstrip("/") + "/"

try:
    with open(r"C:\Users\John\AppData\Local\Temp\indexnow_key.txt", encoding="utf-8") as fh:
        key = fh.read().strip()
except OSError:
    key = (sys.argv[2] if len(sys.argv) > 2 else "").strip()

if not key:
    sys.exit("no IndexNow key: pass one as argv[2] or write indexnow_key.txt")

# Verify the key file is actually served, or every submission will 422.
key_url = f"https://johnie-musyoki.github.io/johnie-profile/{key}.txt"
try:
    with urllib.request.urlopen(key_url, timeout=30) as fh:
        served = fh.read().decode("utf-8", "replace").strip()
    if served != key:
        sys.exit(f"key file mismatch at {key_url}")
    print(f"key file verified: {key_url}")
except Exception as exc:
    sys.exit(f"key file not served yet ({exc}); commit and wait for the rebuild")

payload = json.dumps({"host": "johnie-musyoki.github.io",
                      "key": key,
                      "keyLocation": key_url,
                      "urlList": [SITE]}).encode()

ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://api.bing.com/indexnow",
    "https://yandex.com/indexnow",
]

for endpoint in ENDPOINTS:
    req = urllib.request.Request(
        endpoint, data=payload, method="POST",
        headers={"Content-Type": "application/json; charset=utf-8",
                 "User-Agent": "johnie-profile-indexnow/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as fh:
            print(f"  {endpoint:38s} -> HTTP {fh.status}")
    except urllib.error.HTTPError as exc:
        print(f"  {endpoint:38s} -> HTTP {exc.code} {exc.reason}")
    except Exception as exc:
        print(f"  {endpoint:38s} -> {exc}")

print(f"\nsubmitted: {SITE}")
