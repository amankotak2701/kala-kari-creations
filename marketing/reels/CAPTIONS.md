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

Hook "Pure chanderi." → block-printed yoke → paisley dupatta → borders → ₹2,200 (M–3XL)
→ NAV10 "last chance" offer → "Comment CHANDERI for the link".

> Pure chanderi. 🤍
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

---

## Happy Dussehra reel
File: `kalakari-reel-happy-dussehra.mp4` (18 s, 1080×1920, original soft bansuri in raag Yaman, tabla and tanpura)

शुभ दशहरा / Happy Dussehra with a gold bow & arrow, fireworks, diyas and a marigold toran → Classic Black
Jaipuri 3-piece, Sky Blue chikankari suit, Kutchi block-print shirt → www.kalakaricreations.com, @kalakaricreations27, Call / WhatsApp.

> शुभ दशहरा! 🏹✨ May goodness always win, and may this Vijayadashami bring you joy, courage and new beginnings.
>
> From our family to yours, Happy Dussehra 🙏
>
> Shop Jaipuri, Chikankari & Kutchi pieces at 🌐 www.kalakaricreations.com
> 📞 WhatsApp +91 94081 14592 · 📦 Pan-India delivery
>
> #HappyDussehra #Dussehra2026 #Vijayadashami #EthnicWear #KalaKariCreations

---

## Brand reel (after Navratri, for ads)
File: `kalakari-brand-reel-9x16.mp4` (15 s, 1080×1920, same music as the Navratri brand reel). Script: `brand_reel.py`.

No offer. Maroon Lucknowi chikankari kurti (₹1,500) → Navy blue Jaipuri 3-piece (₹1,300) → Ajrakh kali flair
kurti (₹1,600) → tunics → mul cotton pants → mother & son story → end card with kalakaricreations.com and Call / WhatsApp.

> Handcrafted. Not mass-made. ✨ Lucknowi chikankari, Jaipuri hand-block prints and Kutchi Ajrakh, made in
> small batches from our Ahmedabad home by a mother & son.
>
> 🌐 Shop at www.kalakaricreations.com
> 📞 Call / WhatsApp: +91 94081 14592 · 📦 Pan-India delivery · Easy size exchange
>
> #Chikankari #JaipuriPrint #Ajrakh #EthnicWear #KalaKariCreations

---

## "Which one is your pick?" clock reel
File: `kalakari-reel-pick-your-favourite.mp4` (16 s, 1080×1920, original light, fun music: pizzicato melody,
offbeat strums, dholak, claps and a clock tick). Script: `clock_reel.py` (product cut-outs in `cutouts/`).

A maroon clock hand ticks round the screen, one word per tick, and a product pops in where it points:
"Which one is your pick? Chikankari, Jaipuri or Ajrakh?" → number badges 1–8 with "Comment the number below!"
→ end card: kalakaricreations.com, Call / WhatsApp, @kalakaricreations27.

1 Rani Pink chikankari suit · 2 Yellow Jaipuri 3-piece · 3 Sky Blue chikankari suit · 4 Parrot Green Jaipuri 3-piece
· 5 Classic Black Jaipuri 3-piece · 6 Maroon Lucknowi chikankari kurti · 7 Navy Blue Jaipuri 3-piece · 8 Ajrakh kali flair kurti

> Which one is your pick? 👀✨ Comment the number 1–8 below 👇
>
> Chikankari, Jaipuri hand-block prints & Kutchi Ajrakh, handcrafted in small batches.
> 🌐 Shop at www.kalakaricreations.com
> 📞 Call / WhatsApp: +91 94081 14592 · 📦 Pan-India delivery
>
> #Chikankari #JaipuriPrint #Ajrakh #EthnicWear #KalaKariCreations

Reply to each comment with that product's link: it lifts the reel's reach and starts DMs.

---

## Cartoon story reel: Riya & Priya
File: `kalakari-reel-story-riya-priya.mp4` (32.6 s, 1080×1920, soft, light original background music: warm
electric-piano chords, a low pad and gentle bass, no high or bright sounds; light soft pops on every speech
bubble, a soft whoosh, thump and pop when each parcel arrives). Script: `story_reel.py`.
`kalakari-reel-story-riya-priya-no-music.mp4` is the same reel with sound effects only, to add a song from
Instagram's music library when posting (`python3 story_reel.py remusic <in> <out> sfx`).

Riya & Priya → a big fashion store (₹4,999, machine-made "chikankari") → a famous shopping app (faded after one
wash, wrong size, no exchange) → sad → they find Kala Kari Creations on Instagram → order on kalakaricreations.com
(size help on WhatsApp / video call) → the parcel: real chikankari & Jaipuri → "Now Kala Kari Creations is their
fashion destination" → end card. The store and app are fictional and unnamed.

> POV: You finally found real chikankari that's worth every rupee 😍💛
>
> Real hand chikankari, Jaipuri hand-block prints & Ajrakh, handcrafted in small batches.
> ✅ Easy size exchange · 🎥 Video call shopping · 📦 Pan-India delivery
> 🌐 www.kalakaricreations.com · 📞 WhatsApp +91 94081 14592
>
> Tag your shopping bestie 👭
>
> #Chikankari #JaipuriKurti #HandmadeFashion #EthnicWear #KalaKariCreations

---

## "I know I should sleep… but the voices in my head go" trend reel
File: `kalakari-reel-voices-in-my-head.mp4` (6.5 s, ends with the sound, 1080×1920). Script: `voices_reel.py`.

Same format and timing as the reference trend reel, with our own maroon velvet arch and gold lotus artwork:
typed "I know I should sleep" → BUT / THE / VOICES / IN / MY / HEAD / GO → fast cuts of Kala Kari chikankari,
Jaipuri and Ajrakh pieces on the beat (12 cuts) → end card with kalakaricreations.com, Call / WhatsApp, @kalakaricreations27.
Uses the reference's sound, ending where it ends; a website band shows on every product cut. For extra reach, pick the same trending sound in
Instagram's audio library when posting.

> Me at 2 AM: "just one more scroll" 🌙🛍️
> The voices in my head: chikankari, Jaipuri, Ajrakh… ADD TO CART 😅
>
> 🌐 www.kalakaricreations.com · 📞 WhatsApp +91 94081 14592
>
> #Chikankari #JaipuriKurti #EthnicWear #KurtiLove #KalaKariCreations

### Version 2 (new products)
File: `kalakari-reel-voices-in-my-head-v2.mp4` (6.5 s). Same reel, with 12 product shots not used in any earlier reel:
Pink Jaipuri, Maroon & Striped Jaipuri, Maroon & Olive Green Jaipuri 3-piece dresses, Rich Brown Bandhani Anarkali · Rich Red Hand-Embroidered Chanderi Shirt
(full look + close-up) · Mushroo Grey Silk Kutchi kurti · Pure Mul Cotton Relaxed Pants (maroon, black, white).
(`KK_VOICES=v2 python3 voices_reel.py x <audio.wav> <out.mp4>`)

### Version 3 (tunics, co-ords, sets)
File: `kalakari-reel-voices-in-my-head-v3.mp4` (6.5 s). 12 cuts: Sky Blue Lucknowi chikankari 2-piece · Folk-Art Mustard
co-ord · Olive Green tunic · Classic Black Jaipuri 3-piece · Black and White co-ord (lace trim) · Off-White and Brown tunic ·
Olive Green Jaipuri Print 2-piece (tassels) · Ivory Sleeveless kurta set · Off-White and Black (lotus) tunic ·
Pink rayon 2-piece · Olive Green Leheriya 3-piece · Black Collared 2-piece. Photos in `../product-photos/reel-uploads/`.
(`KK_VOICES=v3 python3 voices_reel.py x <audio.wav> <out.mp4>`)

---

## Diwali Dhamaka offer reel: FLAT 20% OFF till 9 Nov
File: `kalakari-reel-diwali-dhamaka-20-off.mp4` (9.8 s, 1080×1920). Script: `diwali_offer_reel.py`.

Timed like the reference trend reel, with its music: tilt down from the dusk sky to a lit palace avenue as a rocket
climbs → burst → Diwali Dhamaka Sale badge (Diwali → DHAMAKA → SALE) → FLAT 20% OFF · ON ALL PRODUCTS with fireworks
→ everything clears → OFFER VALID TILL ribbon + 9 NOV zooms in → logo + "Shop now at kalakaricreations.com".
Lettering: Rozha One (Diwali), Alfa Slab One marquee gold with twinkling bulbs (DHAMAKA, SALE, 20%, 9 NOV), Poppins ribbons.

> 🪔 DIWALI DHAMAKA SALE IS LIVE 🎆
> FLAT 20% OFF on ALL products: chikankari, Jaipuri, Ajrakh, co-ords, tunics & more ✨
>
> ⏳ Offer valid till 9th November
> 🌐 Shop now at www.kalakaricreations.com (link in bio)
> 📞 WhatsApp +91 94081 14592 · 📦 Pan-India delivery
>
> #DiwaliSale #DiwaliDhamaka #Chikankari #EthnicWear #KalaKariCreations

---

## Brand reel with the Diwali offer
File: `kalakari-brand-reel-diwali-9x16.mp4` (15 s, 1080×1920, same music as the brand reel). Script: `brand_reel_diwali.py`.

The current brand reel (maroon chikankari, navy Jaipuri, Ajrakh kali, off-white tunic, pants, mother & son) plus a
Diwali Dhamaka offer scene (FLAT 20% OFF on all products · valid till 9 November, toran and flickering diyas) and the
offer line on the end card.

> Handcrafted. Not mass-made. ✨ This Diwali, get FLAT 20% OFF on all products 🪔
> Lucknowi chikankari, Jaipuri hand-block prints, Kutchi Ajrakh, tunics & more, made in small batches from our
> Ahmedabad home by a mother & son.
>
> ⏳ Offer valid till 9th November
> 🌐 www.kalakaricreations.com · 📞 WhatsApp +91 94081 14592 · 📦 Pan-India delivery
>
> #DiwaliSale #Chikankari #JaipuriPrint #EthnicWear #KalaKariCreations

---

## "New festive arrivals · Coming soon" sparkler teaser
Files: `kalakari-reel-new-festive-arrivals-4x5.mp4` (feed, same 4:5 frame as the reference) and
`kalakari-reel-new-festive-arrivals-9x16.mp4` (Reels/Stories). 9 s, reference music. Script: `sparkler_reel.py`.

Kala Kari logo on deep maroon; the hand with a gold ring and kada (from the reference reel) holds a sparkler that lights at
0.35 s and burns towards the fingers; "New" (1.1 s) → "festive" (2.7 s) → "arrivals" (5.0 s) fade in word by word,
then "COMING SOON · STAY TUNED" (5.8 s).

> Something new is sparkling at Kala Kari ✨🪔
> New festive arrivals are on their way: handcrafted chikankari, Jaipuri & more.
>
> Coming soon… stay tuned! 👀
> 🔔 Turn on post notifications so you're the first to shop
>
> #NewArrivals #FestiveWear #Chikankari #EthnicWear #KalaKariCreations

---

## "HEY HEY HEY · STOP · LOOK AT · THIS" new arrivals reel
File: `kalakari-reel-new-arrivals.mp4` (8.75 s, 1080×1920, reference audio). Script: `new_arrivals_reel.py`.
Photos (in order) in `../product-photos/new-arrivals-ai/`: blush pink mul 3-piece, denim floral top, mustard mul
chanderi 3-piece, indigo Dabu 3-piece, pink Jaipuri top, indigo denim dress, Jamdani silk 3-piece → hero: ivory silk
embroidered 3-piece, with "New arrivals at kalakaricreations.com".

> New arrivals just dropped 💕 Which one is your favourite? Comment 1–8 👇
> Handcrafted chikankari, Jamdani, Dabu, mul chanderi & more, now on our website.
>
> 🌐 www.kalakaricreations.com · 📞 WhatsApp +91 94081 14592 · 📦 Pan-India delivery
>
> #NewArrivals #EthnicWear #Chikankari #IndianFashion #KalaKariCreations

---

## "The invite says wedding season. Dress code: unforgettable." new edit reel
File: `kalakari-reel-new-edit.mp4` (19.9 s, 1080×1920). Scripts: `edit_story_reel.py` (video) and
`edit_story_voiceover.py` (narration: open-source Kokoro TTS voice "am_michael", in the reference's timing, with
phoneme spellings for Sangeet "sung-geet", Puja "poojaa", Haldi "hul-dee", over a soft original music bed): "The invite
says… wedding season. The dress code says… unforgettable. Sangeet night. Puja morning. Haldi day. Roka evening. Every
piece, hand-embroidered in Jaipur. Shop at Kala Kari Creations."
Photos in `../product-photos/new-edit-ai/` (p1–p4, a = main, b = second): 01 Sangeet night, champagne mul chanderi ·
02 Puja morning, Jamdani silk (deer) · 03 Haldi day, mustard mul mirror-work · 04 Roka evening, dusty pink mul chanderi.

> The invite says wedding season. The dress code says unforgettable. ✨
> 01 Sangeet night · 02 Puja morning · 03 Haldi day · 04 Roka evening
> Which look is yours? Comment 1, 2, 3 or 4 👇
>
> Shop the New Edit at 🌐 www.kalakaricreations.com · 📞 WhatsApp +91 94081 14592
>
> #WeddingSeason #NewArrivals #EthnicWear #IndianWedding #KalaKariCreations
