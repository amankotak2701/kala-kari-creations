# Theme "Kala Kari - SEO Fixes 6 (speed + H1)"

Unpublished copy of the live theme "Kala Kari - SEO Fixes 4" (theme 139032821968,
which moved `<meta charset>` to the top of `<head>`). That live theme was copied from
the older "SEO Fixes 3", so it did not have the H1 / button fixes from
"SEO Fixes 4 (H1)" and "SEO Fixes 5 (button)". This copy keeps its change and adds:

## Speed
- `sections/kk-slideshow.liquid`
  - Slides 2–5 no longer download with the page. Their `<img>` keeps `src`/`srcset`
    in `data-src`/`data-srcset`; `hydrate()` fills them in for the next slide after
    page load and whenever a slide is shown. (`loading="lazy"` didn't help: the
    hidden slides sit inside the viewport, so browsers loaded them all.)
  - Split-layout slides ask for a half-width image on desktop
    (`sizes="(max-width: 800px) 100vw, 50vw"` instead of `100vw`).
- `sections/kk-new-in.liquid` (the three "New in" story reels)
  - Only each reel's first piece has a real image; later pieces load (via
    `hydrate()`) just before they're shown, plus one ahead. Previously every piece's
    two photos (~46 images at up to 900px) downloaded as soon as the section neared
    the screen. Video posters for later pieces are deferred the same way.
  - The first piece's photo is now `loading="lazy"` instead of `eager`, so it no
    longer competes with the slideshow banner for bandwidth.

## SEO (re-applied)
- Hidden homepage `<h1>` in the slideshow, with a "Homepage H1" section setting.
- "Compare & save" button: "Shop now" → "Shop all handcrafted ethnic wear"
  (`templates/index.json`, identical to the "SEO Fixes 5 (button)" version).
