# Theme "Kala Kari - SEO Fixes 4 (H1)"

Unpublished copy of the live theme "Kala Kari - SEO Fixes 3", made after a
Seobility homepage scan. One change:

- `sections/kk-slideshow.liquid`: adds the homepage's only `<h1>`, visually
  hidden (like Shopify's Dawn theme does on its homepage), from a new section
  setting "Homepage H1". Default text:
  "Kala Kari Creations – Handcrafted Chikankari, Jaipuri Hand-Block Print and Ajrakh Ethnic Wear".
  Slide titles stay `<h2>`. Previously the homepage had no H1 at all.

Not changed (already correct in the live theme): the homepage `<title>` and meta
description come from Online Store → Preferences, which are set.

## Follow-up: "Kala Kari - SEO Fixes 5 (button)"

"SEO Fixes 4 (H1)" was published on 1 Nov 2026. A further copy, "SEO Fixes 5
(button)", renames the "Compare & save" section button on the homepage from
"Shop now" to "Shop all handcrafted ethnic wear" (Seobility flagged "Shop now" as
trivial anchor text). `templates/index.json` here is that version.
