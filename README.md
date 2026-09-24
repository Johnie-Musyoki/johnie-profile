# johnie.dev

Personal profile site for **John Musyoki** — Cyber Security Analyst, Nairobi, Kenya.

A static site: plain HTML, CSS and JavaScript. No build step, no framework, no
runtime dependencies. It is the successor to the previous profile at
`johnie.epizy.com`, rebuilt around current roles and work rather than a
hobbyist summary.

## What changed from the old profile

- Title changed from Cyber Security Analyst to **Cyber Security Consultant**
- Removed the projects section
- Removed the Engineering skill group
- Restored the portrait from the old site into the hero
- Adopted the previous site's visual language: purple gradient hero, fixed
  dotted-circle sidebar, spotlight cards with a pink gradient edge, Font Awesome
  icons, and the scroll-hint down arrow
- Added the three practice areas as spotlights: vulnerability assessment,
  security advisory, incident response
- Replaced the flat skills list with grouped offensive, defensive, engineering
  and practice skills
- Corrected "Content Writting" and other copy errors
- No employer named, at request

## Structure

```
index.html                             single page, five sections
assets/css/main.css                    layout, palette, responsive rules
assets/js/main.js                      smooth scroll, scroll-spy, reveal
assets/img/john.jpg                    portrait, carried over from the old site
assets/fontawesome/css/all.min.css    Font Awesome 5.15.4 (vendored)
assets/fontawesome/webfonts/*.woff2    solid + brands subsets only
assets/img/og.png                      1200x630 social share card
assets/img/favicon.svg                 shield mark
robots.txt, sitemap.xml                crawl directives
site.webmanifest                       installable metadata
_make_icons.py                         regenerates og.png and the icons
_seo_check.py                          validates the SEO layer
```

## Images

`assets/img/john.jpg` is the portrait from `johnie.epizy.com` (1280x960). The old
site also had `tech.jpg` and `work.jpg`; neither is used, so they were not
carried over. If you want a fresh headshot, replace that one file — the CSS
crops toward the top of the frame and the markup sets explicit dimensions, so
swap in any portrait-orientation image and the layout holds.

Font Awesome is vendored rather than loaded from a CDN. The CDN stylesheet was
being rejected by subresource-integrity checks, and self-hosting removes both
that fragility and the third-party request. Only the two font families actually
used are included, so the added weight is about 155 KB.

## Accessibility notes

- Content is visible by default. `main.js` adds a `js-reveal` class before
  hiding anything, so a scripting failure cannot leave sections invisible.
- All interactive targets are at least 44px; nav labels are screen-reader-only
  beside their icons.
- `prefers-reduced-motion` disables the reveal animation and the bouncing
  scroll hint.

## Local preview

```bash
# any static server works
python -m http.server 8080
# then open http://localhost:8080
```

Opening `index.html` directly from disk also works; there is no module loading
or fetch call.

## Contact details

Update these in `index.html` if any change:

- `jhnmusyoki@gmail.com`
- `linkedin.com/in/john-musyoki-4304a8193`
- `github.com/Johnie-Musyoki`
- `twitter.com/johnie_musyoki`

## Search visibility

The page is built to be indexable without relying on any external service.

**Crawl and index signals**

- `robots.txt` allows everything and points at `sitemap.xml`
- `sitemap.xml` with an image entry for the portrait
- `meta robots` set to `index, follow, max-image-preview:large`
- `rel="canonical"` on the single URL, matching `og:url`
- `lang="en-KE"` plus `geo.region` and `geo.placename` for Nairobi
- `rel="me"` links to the LinkedIn, GitHub and X profiles, which helps entity
  matching on name searches

**Metadata**

- Title at 55 characters and description at 150, both inside the range search
  results actually display
- Open Graph `profile` type with first and last name, and a Twitter
  `summary_large_image` card
- `assets/img/og.png` is a 1200x630 share card generated from the site palette,
  so a pasted link renders as a card rather than a bare URL
- `site.webmanifest` for the installable name and theme colour
- `favicon.svg` plus 180px and 32px rasters

**Structured data**

- `Person` schema: name, job title, location, email, portrait, `knowsAbout`
  terms, and `sameAs` profile links
- `FAQPage` schema over the five questions in the Common questions section.
  Google has deprecated FAQ rich results for most sites, so treat this as
  semantic clarity rather than a rich-result strategy; the visible section is
  what earns the impressions.

**Content structure**

One `h1`, no heading-level skips, every image carries alt text, and the
questions answer real search phrasing: "penetration testing services in Kenya",
"ISO 27001 compliance", "incident response engagement".

### Checking it

```
python _seo_check.py http://127.0.0.1:8000/
```

Validates title and description lengths, canonical, Open Graph and Twitter
tags, both JSON-LD blocks parse, every FAQ answer is visible page text (so the
markup cannot claim something the page does not say), heading order, alt text,
and that the crawl files are served. It runs against any URL, so the same check
works against production.

### Telling search engines about changes

The classic sitemap ping endpoints are dead: Google deprecated its in June 2023
and the endpoint now returns 404, and Bing returns 410. This site uses IndexNow
instead, which needs no account.

```
python _indexnow_submit.py https://johnie-musyoki.github.io/johnie-profile/
```

The key is committed at the repository root, because GitHub Pages serves a
project site from a `/johnie-profile/` prefix, so the key file has to be
reachable at the host root for verification to pass. The script checks the key
file is actually served before submitting, since a missing key makes every
request fail validation.

As of the last run, `api.indexnow.org` and Yandex both accepted the submission
with HTTP 202. Bing's own endpoint was returning HTTP 400 with "Our services
aren't available right now", which is a Bing-side outage rather than a
rejection of the request; Bing is a participant in the shared IndexNow
endpoint, so the submission is already covered.

Sitemaps still need submitting once through Search Console and Bing Webmaster
Tools, and those need an account. The ping route is only for changes after
that.

### What actually gets it indexed

The technical layer is necessary but not sufficient. The site will be picked up
by Google's sitemap submission, but ranking for terms like "cyber security
consultant Nairobi" depends on how long the page has existed, links pointing
at it, and competing pages. The highest-value next step is having the same
profile URL listed on LinkedIn, GitHub and the other profiles, which is what
the `sameAs` and `rel="me"` declarations point at.
