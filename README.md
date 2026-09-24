# johnie.dev

Personal profile site for **John Musyoki** — Cyber Security Analyst, Nairobi, Kenya.

A static site: plain HTML, CSS and JavaScript. No build step, no framework, no
runtime dependencies. It is the successor to the previous profile at
`johnie.epizy.com`, rebuilt around current roles and work rather than a
hobbyist summary.

## What changed from the old profile

- Recast around professional experience instead of a personal introduction
- Added the three practice areas: vulnerability assessment, security advisory,
  incident response
- Replaced the flat skills list with grouped offensive, defensive, engineering
  and practice skills
- Added a projects section covering the Go work
- Corrected "Content Writting" and other copy errors
- No employer named, at request
- Rebuilt on a static site with a responsive layout and accessible contrast

## Structure

```
index.html              single page, four sections
assets/css/main.css     design tokens and layout
assets/js/main.js       footer year, scroll-spy, anchor offset
```

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
