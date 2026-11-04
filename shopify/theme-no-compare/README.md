# Theme update: remove "Compare & Save" from the homepage

Removes the `kk_price_video` section ("Compare & save — Handcrafted. Authentic.
Pocket-friendly.", with the leading-brands price comparison and the honest-pricing
video) from `templates/index.json`. All other homepage sections are unchanged.

That section only appeared on the homepage; no other template used it.
The `sections/kk-price-video.liquid` file stays in the theme but isn't used, so it
can be added back from the theme editor if needed.

Applied to the unpublished theme **"Kala Kari - No Compare & Save"**, a copy of the
live theme "Kala Kari - SEO Fixes 6 (speed + H1)". Preview it, then publish it from
Shopify admin → Online Store → Themes.
