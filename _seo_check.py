"""Validate the SEO layer: JSON-LD parses, meta tags agree, links resolve.

Run against the live URL so it checks what crawlers actually receive.
"""
import json
import re
import sys
import os
import urllib.request

URL = sys.argv[1] if len(sys.argv) > 1 else \
    "http://127.0.0.1:8094/"

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (seo-verify)"})
with urllib.request.urlopen(req, timeout=30) as fh:
    html = fh.read().decode("utf-8", "replace")

fails, warns = [], []


def check(cond, label, warn=False):
    tag = "WARN" if warn else "FAIL"
    if cond:
        print(f"  OK   {label}")
    else:
        print(f"  {tag} {label}")
        (warns if warn else fails).append(label)


print("=== title and description ===")
title = re.search(r"<title>(.*?)</title>", html, re.S)
desc = re.search(r'name="description" content="(.*?)"', html, re.S)
check(bool(title), "title present")
check(bool(desc), "meta description present")
if title:
    t = title.group(1).strip()
    print(f"       title = {t!r} ({len(t)} chars)")
    check(len(t) <= 60, f"title within 60 chars ({len(t)})", warn=True)
if desc:
    d = desc.group(1).strip()
    print(f"       desc  = {len(d)} chars")
    check(100 <= len(d) <= 160, f"description 100-160 chars ({len(d)})", warn=True)
    check("Nairobi" in d, "description names the location")

print("\n=== canonical and indexability ===")
canon = re.search(r'rel="canonical" href="([^"]+)"', html)
check(bool(canon), "canonical link present")
if canon:
    print(f"       canonical = {canon.group(1)}")
robots = re.search(r'name="robots" content="([^"]+)"', html)
check(bool(robots), "robots meta present")
if robots:
    check("index" in robots.group(1) and "follow" in robots.group(1),
          "robots allows index and follow")

print("\n=== open graph and twitter ===")
for prop in ("og:type", "og:title", "og:description", "og:url",
             "og:image", "og:image:width", "og:image:height", "og:locale"):
    m = re.search(rf'property="{prop}" content="([^"]*)"', html)
    check(bool(m and m.group(1)), f"{prop} present")
for nm in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
    m = re.search(rf'name="{nm}" content="([^"]*)"', html)
    check(bool(m and m.group(1)), f"{nm} present")

og_url = re.search(r'property="og:url" content="([^"]+)"', html)
og_canon = canon.group(1) if canon else None
if og_url and og_canon:
    check(og_url.group(1).rstrip("/") == og_canon.rstrip("/"),
          "og:url matches canonical")

og_img = re.search(r'property="og:image" content="([^"]+)"', html)
if og_img:
    u = og_img.group(1)
    name = u.rsplit("/", 1)[-1]
    # Local preview: absolute production URL has no local counterpart, so
    # verify the file on disk; live: fetch the URL itself.
    if URL.startswith("http://127.0.0.1"):
        local = os.path.join("assets", "img", name)
        ok = os.path.exists(local) and os.path.getsize(local) > 0
        check(ok, f"og:image file present ({local})")
    else:
        try:
            with urllib.request.urlopen(u, timeout=30) as im:
                check(im.status == 200, f"og:image resolves ({name})")
        except Exception as exc:
            check(False, f"og:image resolves ({exc})")

print("\n=== structured data ===")
blocks = re.findall(
    r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
check(len(blocks) >= 2, f"JSON-LD blocks found ({len(blocks)})")
types = []
for b in blocks:
    try:
        data = json.loads(b)
    except json.JSONDecodeError as exc:
        check(False, f"JSON-LD parses ({exc})")
        continue
    t = data.get("@type")
    types.append(t)
    print(f"       parsed @type = {t}")
check("Person" in types, "Person schema present")
check("FAQPage" in types, "FAQPage schema present")

person = next((json.loads(b) for b in blocks if '"Person"' in b), {})
faq = next((json.loads(b) for b in blocks if '"FAQPage"' in b), {})

# FAQ answers must appear in the visible page, or the markup is misleading.
body = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
body = re.sub(r"<[^>]+>", " ", body)
body = re.sub(r"\s+", " ", body)
for qa in faq.get("mainEntity", []):
    q, a = qa["name"], qa["acceptedAnswer"]["text"]
    check(q[:40] in body, f"FAQ question visible: {q[:40]!r}")
    check(a[:40] in body, f"FAQ answer visible: {a[:40]!r}")

print("\n=== headings and content ===")
h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)
h1s = [re.sub(r"<[^>]+>", "", x).strip() for x in h1s]
check(len(h1s) == 1, f"exactly one h1 ({len(h1s)})")
if h1s:
    print(f"       h1 = {h1s[0]!r}")
order = re.findall(r"<h([1-3])", html)
print(f"       heading sequence = {''.join(order)}")
check(order[0] == "1", "first heading is h1")
check("John Musyoki" in h1s[0] if h1s else False, "h1 contains the name")

imgs = re.findall(r"<img[^>]*>", html)
missing_alt = [i for i in imgs if "alt=" not in i or 'alt=""' in i]
check(not missing_alt, f"all images have alt text ({len(imgs)} images)")

print("\n=== crawl files ===")
base = URL if URL.endswith("/") else URL + "/"
for f in ("robots.txt", "sitemap.xml", "site.webmanifest"):
    try:
        with urllib.request.urlopen(base + f, timeout=20) as fh:
            body_f = fh.read().decode("utf-8", "replace")
        check(fh.status == 200, f"{f} served")
        if f == "robots.txt":
            check("Sitemap:" in body_f, "robots.txt points at a sitemap")
        if f == "sitemap.xml":
            check("sitemaps.org" in body_f, "sitemap uses the correct namespace")
    except Exception as exc:
        check(False, f"{f} served ({exc})")

print("\n=== links ===")
for href in re.findall(r'href="(https?://[^"]+)"', html):
    if "johnie-musyoki.github.io" in href:
        continue
    print(f"       external: {href}")

print(f"\n{'=' * 46}")
print(f"failures: {len(fails)}   warnings: {len(warns)}")
if fails:
    for f in fails:
        print(f"  FAIL {f}")
sys.exit(1 if fails else 0)
