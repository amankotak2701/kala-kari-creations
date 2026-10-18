# Instagram reels: tunics & shrug

Four 16-second 1080×1920 reels, one per product. Each one has a hook on the full look,
two slow close-ups on the craft details, the product name, and a maroon end card with the logo,
"DM us to order", the Call / WhatsApp number and "Video call appointments available".

Each reel has its own soft background track (tanpura drone, warm pad and bell melody). The
tracks were composed in `music.py` and use no samples or third-party recordings, so there is no copyright
claim to worry about. When you post, you can still swap in a track from Instagram's audio library
if you prefer.

Before posting, check the names and details against your Shopify listings and correct any that
differ (fabric, sizes, price).

Posting tips: pick a cover frame from the first 2 seconds (the full look with the hook text).
Turn on "Also share to feed". Keep the phone number in the caption so people can copy it.

---

## 1. Patchwork Block Print Long Shrug
File: `kalakari-reel-shrug-patchwork.mp4`

> Every patch tells a story ✨
> Our long shrug is pieced together from hand block-printed patchwork: indigo, rust, mustard and
> deep maroon prints in one flowing silhouette. Throw it over a black dress, a kurta or jeans and
> you're done.
>
> 💬 DM us to order
> 📞 Call / WhatsApp: +91 94081 14592
> 🎥 Video call appointments available
> 📦 Pan-India delivery
>
> #KalaKariCreations #BlockPrint #PatchworkShrug #HandBlockPrint #EthnicWear #IndianFashion
> #Handcrafted #SlowFashion #SustainableFashion #ShrugStyle #IndoWestern #VocalForLocal
> #MadeInIndia #EthnicLayering

## 2. Olive Smocked Yoke Tunic
File: `kalakari-reel-tunic-olive-smocked.mp4`

> Quiet colour, loud craft 🌿
> An olive tunic with a hand-smocked yoke, little mirror accents and white paisley thread work on
> the sleeves. It's easy enough for every day and special enough to be noticed.
>
> 💬 DM us to order
> 📞 Call / WhatsApp: +91 94081 14592
> 🎥 Video call appointments available
> 📦 Pan-India delivery
>
> #KalaKariCreations #ShortKurti #Tunic #Smocking #ThreadWork #MirrorWork #EthnicWear
> #OfficeWearIndia #EverydayEthnic #Handcrafted #IndianFashion #VocalForLocal #MadeInIndia

## 3. Ivory Leaf Appliqué Tunic
File: `kalakari-reel-tunic-ivory-leaf.mp4`

> Nature, stitched by hand 🍂
> Soft ivory with hand-cut brown appliqué leaves, finished with delicate running stitches. Wear
> it with wide-leg pants on slow mornings and long days alike.
>
> 💬 DM us to order
> 📞 Call / WhatsApp: +91 94081 14592
> 🎥 Video call appointments available
> 📦 Pan-India delivery
>
> #KalaKariCreations #Applique #AppliqueWork #IvoryTunic #MinimalEthnic #Handcrafted
> #SlowFashion #NeutralStyle #EthnicWear #IndianFashion #CoOrdSet #VocalForLocal #MadeInIndia

## 4. Ivory Lotus Appliqué Tunic
File: `kalakari-reel-tunic-ivory-lotus.mp4`

> Bloom in black & ivory 🪷
> A border of lace lotus appliqué, a striped V-neck and tiny silver ghungroos that chime as you
> move. It's a modern classic rooted in craft.
>
> 💬 DM us to order
> 📞 Call / WhatsApp: +91 94081 14592
> 🎥 Video call appointments available
> 📦 Pan-India delivery
>
> #KalaKariCreations #LotusMotif #Applique #BlackAndWhite #ShortKurti #Tunic #EthnicWear
> #Handcrafted #IndianFashion #EthnicChic #FestiveWear #VocalForLocal #MadeInIndia

---

## Re-rendering

Edit the text and shots in the `REELS` dict in `make_reels.py`, then run:

    npm pack @fontsource/cinzel @fontsource/cormorant-garamond   # extract to <fonts>/fontsource-cinzel etc.
    python3 make_reels.py <photos_dir> <fonts_dir> . [reel_id ...]

`<photos_dir>` holds the four product photos as `1.webp` (shrug), `2.webp` (olive), `3.webp` (leaf)
and `4.webp` (lotus).

---

## Navratri greeting reel
File: `kalakari-reel-navratri-greeting.mp4` (24 s, 1080×1920, original garba-style music: soft dhol, flute and tanpura)

Scenes: शुभ नवरात्रि / Happy Navratri with diyas and a marigold toran → Jaipuri, Chikankari and Kutchi
collections → Navratri offer (10% off above ₹3,000, code NAV10, valid till 19 Oct) → shop at
www.kalakaricreations.com, follow @kalakaricreations27, Call / WhatsApp +91 94081 14592.

> शुभ नवरात्रि! 🪔✨ Wishing you and your family nine nights of colour, devotion and dance.
>
> 🎁 Navratri Offer: 10% OFF on orders above ₹3,000
> 🏷️ Use code NAV10 · valid till 19 October
>
> Shop our Jaipuri, Chikankari, Kutchi & more collections at 🌐 www.kalakaricreations.com (link in bio)
> 📞 Call / WhatsApp: +91 94081 14592
> 🎥 Video call shopping available · 📦 Pan-India delivery
> ✨ Follow @kalakaricreations27 for new drops
>
> #Navratri #NavratriOutfits #Chikankari #EthnicWear #KalaKariCreations

---

## Kutchi patchwork shrug: fast-cut reel
File: `kalakari-reel-shrug-fastcut.mp4` (11 s, 1080×1920, original soft Kutchi folk music)

Hook "Every patch tells a story" → patchwork yoke → print panels → flowing hem → ₹1,500 (L · XL · 2XL)
→ Navratri NAV10 offer → "Comment SHRUG for the link".

> Every patch tells a story 🧵 Hand block-printed Kutchi patchwork, one long shrug. Throw it over a
> black dress, a kurta or jeans.
>
> ₹1,500 · Sizes L, XL, 2XL
> 🪔 Navratri: 10% OFF above ₹3,000 with NAV10 · ends 19 Oct
>
> 💬 Comment "SHRUG" and we'll DM you the link
>
> #Shrug #KutchiWork #BlockPrint #NavratriOutfits #KalaKariCreations

---

## Off-white chanderi 3-piece: fast-cut reel
File: `kalakari-reel-chanderi-3pc-fastcut.mp4` (11 s, 1080×1920, soft tanpura/pad/bell music)

Hook "Pure chanderi. Under ₹2,500." → block-printed yoke → paisley dupatta → borders → ₹2,200 (M–3XL)
→ NAV10 "last chance" offer → "Comment CHANDERI for the link".

> Pure chanderi. Under ₹2,500. 🤍
> Off-white chanderi kurta with a hand block-printed yoke, matching pants and a paisley dupatta.
>
> ₹2,200 · Sizes M to 3XL
> 🪔 Last chance: 10% OFF above ₹3,000 with NAV10 · ends 19 Oct
>
> 💬 Comment "CHANDERI" and we'll DM you the link
>
> #Chanderi #ChanderiSuit #SuitSet #NavratriOutfits #KalaKariCreations

Alternative hooks to test in later reels (swap the first scene text):
1. "3 pieces. 1 price. ₹2,200."
2. "The suit your mom will ask to borrow"
3. "Office to Navratri in one chanderi set"
