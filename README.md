# johnie.dev

Personal profile site for **John Musyoki** — Cyber Security Analyst, Nairobi, Kenya.

A static site: plain HTML, CSS and JavaScript. No build step, no framework, no
runtime dependencies. It is the successor to the previous profile at
`johnie.epizy.com`, rebuilt around current roles and work rather than a
hobbyist summary.

## What changed from the old profile

- Title changed from Cyber Security Analyst to **Cyber Security Consultant**
- Removed the projects section
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
assets/fontawesome/css/all.min.css    Font Awesome 5.15.4 (vendored)
assets/fontawesome/webfonts/*.woff2    solid + brands subsets only
```

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
