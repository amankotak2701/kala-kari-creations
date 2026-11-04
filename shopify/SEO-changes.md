# SEO changes — 31 Oct 2026

Applied directly to the live store (kalakaricreations.com) through the Shopify connection.

## 1. Collection SEO titles & meta descriptions (15 collections)

All 15 collections previously had no SEO title or meta description. Each now has a
keyword-focused title and a ~150-character description:

| Collection (handle) | SEO title |
|---|---|
| new-arrivals | New Arrivals – Handcrafted Ethnic Wear \| Kala Kari Creations |
| chikankari | Lucknowi Chikankari Kurtis & Suits \| Kala Kari Creations |
| jaipuri-prints | Jaipuri Hand Block Print Suits & Kurtis \| Kala Kari Creations |
| kutchi-work | Kutchi Work & Ajrakh Kurtis, Shrugs \| Kala Kari Creations |
| kurtis | Handcrafted Long Kurtis for Women \| Kala Kari Creations |
| 2-piece-sets | 2-Piece Kurta Pant Sets for Women \| Kala Kari Creations |
| 3-piece-dresses | 3-Piece Suit Sets with Dupatta \| Kala Kari Creations |
| tunics-shirts-shrugs | Tunics, Block Print Shirts & Shrugs \| Kala Kari Creations |
| featured | Featured Handcrafted Ethnic Wear \| Kala Kari Creations |
| pants | Mul Cotton Pants for Women – Wide Leg \| Kala Kari Creations |
| chanderi | Chanderi Shirts & Suit Sets \| Kala Kari Creations |
| mul-cotton | Mul Cotton Suits, Kurtis & Co-Ords \| Kala Kari Creations |
| co-ord-sets | Ethnic Co-Ord Sets for Women \| Kala Kari Creations |
| pair-with | Pants, Shirts & Tunics Under ₹1,000 \| Kala Kari Creations |
| diwali-sale | Diwali Sale – 20% Off Ethnic Wear \| Kala Kari Creations |

**After 9 Nov:** don't delete the Diwali Sale collection. Change its SEO title to something
like "Festive Sale – Handcrafted Ethnic Wear" so the URL keeps its search value.

## 2. Image alt text (51 media items)

Added descriptive alt text to 46 product images and 5 product videos that had none
(pattern: `<colour> <craft> <fabric> <garment> - Kala Kari Creations - view N`).
Every product image in the store now has alt text.

## 3. "3-Piece Dress" → "3-Piece Suit Set" (23 products + 1 collection)

People in India search "3 piece suit set", not "3 piece dress". Renamed the title and SEO
title of all 23 products that said "3-Piece Dress" / "3 Piece Dress", and renamed the
`3-piece-dresses` collection to **3-Piece Suit Sets**.

Product URLs (handles) were **not** changed, so no links, ads or Google results break.
Meta descriptions still mention "dress", so both search terms are covered.

If your header menu has a typed-in label "3-Piece Dresses", update it in
Online Store → Navigation.

## 4. TO DO BY HAND — homepage title & description

Shopify doesn't allow apps to change these. Go to
**Online Store → Preferences → Title and meta description** and paste:

**Homepage title**

```
Kala Kari Creations – Handcrafted Chikankari, Jaipuri & Ajrakh Ethnic Wear
```

**Homepage meta description**

```
Shop handcrafted kurtis, 2 & 3-piece suit sets and co-ords in Lucknowi Chikankari, Jaipuri hand-block print, Ajrakh and Kutchi work. Made in small batches in Ahmedabad, shipped across India.
```

---

# Round 2 — collection content & blog posts (31 Oct 2026)

## 5. Collection page content + FAQs (9 collections)

Chikankari, Jaipuri Prints, Kutchi Work, Kurtis, 2-Piece Sets, 3-Piece Suit Sets,
Co-Ord Sets, Mul Cotton and Chanderi now have, under their original intro line, a
collapsible **"Read more about …"** section (HTML `<details>`, so the product grid stays
near the top) with:

- 2 paragraphs of craft and fabric explanation, using the words people search for
- links to related collections, blog posts, Size Guide and policies
- 3–4 FAQs whose answers match the existing FAQ, shipping and exchange pages

To edit: Products → Collections → (collection) → Description.

## 6. New blog posts (The Kala Kari Journal)

| Post | URL | Target searches |
|---|---|---|
| Real vs Machine Chikankari: How to Spot Hand Embroidery | /blogs/journal/real-vs-machine-chikankari | real chikankari, hand vs machine chikankari |
| Leheriya and Bandhani: Rajasthan's Tie-Dye Traditions Explained | /blogs/journal/leheriya-and-bandhani-explained | what is leheriya, leheriya vs bandhani |
| Mul Cotton, Chanderi or Silk? Choosing the Right Fabric | /blogs/journal/mul-cotton-chanderi-silk-fabric-guide | mul cotton vs chanderi, best fabric for summer |
| How to Style a Co-Ord Set: 5 Easy Looks | /blogs/journal/how-to-style-a-co-ord-set | how to style co-ord set |

Each has an SEO title, meta description, featured image and links to specific products
and collections. The 3 older posts also got SEO titles and meta descriptions.

## Please check

- The Chikankari post says "Every Chikankari piece at Kala Kari Creations is hand
  embroidered." If any piece (e.g. the Wine short kurti) is not, edit that sentence.
- The Chanderi collection text mentions the red Chanderi shirt and the off-white Chanderi
  suit set. Update it if you add or remove Chanderi pieces.

---

# Round 3 — fixes from the homepage SEO check (31 Oct 2026)

| Checker warning | Fix | Where |
|---|---|---|
| Title too short ("Kala Kari Creations") / meta description missing | Set the homepage SEO title and meta description (shop metafields `global.title_tag` / `global.description_tag`, the same fields Online Store → Preferences edits) | Live now |
| Images without alt text | Added alt text to 17 library images (homepage craft tile, collection banner images, logo, maroon tunic copies) and to the 4 collection images (New Arrivals, Chikankari, Jaipuri Prints, Kutchi Work) | Live now |
| Duplicate heading texts | Product cards showed each product name as an `<h3>`. The homepage shows the same product in several tabs and in the new-arrivals grid, so the same heading repeated many times. Changed the name to a `<p>` with the same class, so it looks the same | Theme **"Kala Kari - SEO Fixes"** (unpublished) — `snippets/kk-card.liquid` |
| No Apple touch icon | Added `<link rel="apple-touch-icon">` using the favicon at 180×180 | Theme **"Kala Kari - SEO Fixes"** (unpublished) — `snippets/meta-tags.liquid` |

"Kala Kari - SEO Fixes" is a copy of the live theme "Kala Kari - ₹99 Shipping Note" with only
those two files changed. Preview it, then publish it from Online Store → Themes.
If you edit the live theme before publishing, make the same edits in the copy too.

Left alone: 14 library images without alt text that have AI-generated file names and do not
appear on the homepage or collection pages (they could not be viewed from this session, so no
alt text was guessed). The second "hover" image on product cards keeps `alt=""` on purpose;
it is decorative and the product name is already on the main image.

---

# Round 4 — second homepage SEO check (31 Oct 2026)

"Kala Kari - SEO Fixes" was published. New unpublished copy **"Kala Kari - SEO Fixes 2"**
adds the following (files saved in `theme-seo-fixes/`):

| Checker warning | Fix |
|---|---|
| 42 images have no alt attribute | The second "hover" photo on product cards and in the new-arrival reels had `alt=""`. Now `<product title> - alternate view` (`snippets/kk-card.liquid`, `sections/kk-new-in.liquid`). "Shop by style" tiles now fall back to the tile name as alt text (`sections/kk-styles.liquid`) |
| Internal links with dynamic parameters | The 3 "Shop by price" links (`?filter.v.price…`) now have `rel="nofollow"` (`sections/kk-styles.liquid`) |
| Duplicate headings / 60 headings | Mostly fixed by round 3 (product names no longer headings); rescan after publishing |

## TO DO BY HAND — H1 too short

The homepage H1 is a hidden heading in `sections/header.liquid` that prints only the shop name.
In **Online Store → Themes → (theme) → ⋯ → Edit code → sections/header.liquid**, find:

```
<h1 class="visually-hidden">{{ shop.name }}</h1>
```

and replace it with:

```
<h1 class="visually-hidden">{{ shop.name }} – Handcrafted Chikankari, Jaipuri & Kutchi Ethnic Wear</h1>
```

(Do it in "SEO Fixes 2" before publishing, or in the live theme after.)

## Not changed (and why)

- **Anchor texts used more than once / too long**: every product links from its photo and its
  name, and the same product appears in several homepage tabs. That is normal for a shop
  homepage and harmless.
- **2 trivial anchor texts**: likely the "Shop all" links under the new-arrival reels. Change
  them in the theme editor (Kala Kari new arrivals → each reel → Link text), e.g.
  "Shop all 3-piece suit sets".
- **Response time 0.77 s**: Shopify server time. The homepage builds 7 product tabs (up to
  12 products each) plus the new-arrivals reels and grid on every visit; cutting the tabs to
  3–4 would make it lighter.
- **Backlinks**: only fixable off-site (see chat notes).

## Round 4b — homepage speed and link text (also in "SEO Fixes 2")

`templates/index.json`:

- **Product tabs cut from 7 to 4**: Featured, Kurtis, 2-Piece Sets, 3-Piece Suit Sets.
  Removed Tunics & Shirts, Pants and Chanderi tabs (still reachable from the "Shop by style"
  tiles and the menu). The homepage now builds at most 48 tab products instead of 84.
- **Reel link texts** (were all "Shop all"): "Shop all 3-piece suit sets",
  "Shop all new arrivals", "Shop all tunics & tops".
- **"3-Piece Dresses" → "3-Piece Suit Sets"** in visible homepage text: slideshow slides 1 and 4
  (text and buttons), new-arrival reel title, Shop-by-style tile, product tab.
  Collection links (`/collections/3-piece-dresses`) and the reel's product-type filter
  (`3-Piece Dresses`) are unchanged on purpose, so nothing breaks.

---

# Round 5 — full-site audit (31 Oct 2026)

## Fixed directly in the store (live now)

- **Restored 23 product meta descriptions.** The round-1 rename of "3-Piece Dress" products
  sent only a new SEO title, which cleared their meta descriptions. All 23 now have one again.
- **8 more products tidied**: SEO titles over 70 characters shortened, descriptions over
  160 characters shortened, brand added where missing.
- **Pages**: SEO titles + meta descriptions for Contact, Return & Exchange, Shipping, Terms,
  Our Story, Size Guide and FAQs. The Size Exchange form page is now hidden from Google
  (`seo.hidden`) because it is a utility form, not a landing page.
- **Blog**: SEO title + description for The Kala Kari Journal.
- **Image file names**: 147 product images renamed from `Gemini_Generated_Image_….png` /
  `Code_Generated_Image….png` to descriptive names (e.g.
  `indigo-dabu-block-print-cotton-3-piece-dress-with-patchwork-1-kala-kari.png`). Full list:
  `image-renames.csv`. Skipped: the 6 images the homepage theme points to by file name, and
  14 images with no alt text.

## Theme copy "Kala Kari - SEO Fixes 3" (unpublished — preview, then publish)

Files saved in `theme-seo-fixes/`:

- `sections/kk-collection.liquid` — **bug fix**: the italic intro under each collection title
  was built from the whole description, so on the 9 collections with a "Read more" section it
  ran into that text. It now shows only the intro, and the box under the products shows only
  the "Read more" section (no repeated paragraph).
- `snippets/meta-tags.liquid` —
  - Default share image (og:image, 1200 px) for pages without their own image, e.g. the
    homepage, so WhatsApp / Facebook / Pinterest previews show a photo.
  - `og:image:alt`.
  - Structured data: **OnlineStore** (business name, logo, email, phone, Ahmedabad,
    Instagram), **WebSite** (helps Google show "Kala Kari Creations" as the site name) and
    **BreadcrumbList** on product, collection, blog, article and page URLs.
- `sections/header.liquid` (prepared but **not uploaded** — too large to send safely through
  the connection): longer hidden H1 and removal of the old Organization block whose `url`
  pointed at the wrong page. See "TO DO BY HAND" below.

## TO DO BY HAND in "SEO Fixes 3" → Edit code → `sections/header.liquid`

1. Find `<h1 class="visually-hidden">{{ shop.name }}</h1>` and replace with
   `<h1 class="visually-hidden">{{ shop.name }} – Handcrafted Chikankari, Jaipuri &amp; Kutchi Ethnic Wear</h1>`
2. Delete the block that starts `<script type="application/ld+json">` and contains
   `"@type": "Organization"` (about 11 lines, just above `<header-component`).
   The new, complete version is in `snippets/meta-tags.liquid`.

---

# Round 6 — product openings, unused images, Diwali Sale (1 Nov 2026)

## Unique product description openings (44 products, live now)

44 product descriptions opened with the same template ("Crafted from ultra-soft, breathable
mul cotton, this gorgeous ensemble…", "Step into effortless elegance with our signature…").
Each opening paragraph is now unique and plain, built only from facts already in that
product's description (fabric, craft, colour, details, what's included). Size charts and
everything else are unchanged. All 44 were read back from Shopify and match exactly.
New openings: `product-openings.csv`.

The 11 newest products (denim, tunics, Jamdani, Mul Chanderi, Dabu…) already had unique text
and were not touched. The Handblock Ajrakh Kali kurti was also left as it was.

## The 14 images without alt text

None of them is used anywhere: not on any product, collection, page, blog post or the
homepage. They are unused uploads in Content → Files (file names
`Gemini_Generated_Image_e9aeij…`, `x83pb2…`, `nfph8e…`, `7lmqci…` ×2, `j1o1tm…`, `mn9gl4…`,
`1ztz8g…`, `13ykut…`, `92f6zl…`, `gzjc9a…`, `pjm6f8…`, `vbbyco…`, `79jq6i…`).
Google never sees them, so they have no SEO effect. They were left in place; delete them in
Content → Files if they are not needed.

## Diwali Sale collection

A one-time scheduled task fires at **12:35 AM IST on 10 Nov 2026** (just after the sale ends)
to change the collection's Google title/description to:

- Title: Festive Sale – Handcrafted Ethnic Wear | Kala Kari Creations
- Description: Shop handcrafted kurtis, suit sets and co-ords from our festive sales:
  Lucknowi Chikankari, Jaipuri hand-block print and Ajrakh, shipped across India.

It checks first and changes nothing if the owner has already edited it. The visible collection
text, the automatic 20% discount and the homepage banner are left for the owner.

## Round 6b — fuller product descriptions (44 products, live now)

The same 44 products now also have, between the opening paragraph and the size chart:
**Key Features** (bullets), **Fabric & Care** (fabric, colour, care), **Includes** (what's
in the set) and **Occasions**, plus the standard colour-variation note. This matches the
layout of the 11 newest products.

- Every feature, fabric and colour comes from that product's existing description; nothing
  new was claimed.
- Care text follows the FAQ/care guide by fabric: Chikankari, printed cotton/mul, embroidered
  cotton, rayon, silk, Chanderi, plain pants. Mentions of mirror work, tassels, beads or
  appliqué only appear where the product has them.
- Read back from Shopify: all 44 match (Shopify only adds line breaks inside list items).
- Full text: `product-sections.md`.

---

# Round 7 — re-check after publishing "SEO Fixes 3" (1 Nov 2026)

Verified live:
- "Kala Kari - SEO Fixes 3" is the published theme; collection-intro fix, schema,
  breadcrumbs and share image are in it (files unchanged since upload).
- Owner's header edit is correct: longer hidden H1, old Organization block removed (no duplicate).
- All 61 products: SEO title ≤70, meta description ≤160, no duplicates, every image has alt text.
- All collections, pages (except the hidden size-exchange form) and blog posts have SEO titles
  and descriptions.

Fixed now:
- Homepage meta description shortened from 186 to 156 characters so Google doesn't cut it off.
- Handblock Ajrakh Cotton Kali Flair Long Kurti rewritten to the same format as the other
  products (unique opening + Key Features, Fabric & Care, Includes, Occasions). Wording keeps
  "Ajrakh-inspired" as in the original.
- "Read more" text + FAQs added to the Tunics, Shirts & Shrugs and Pants collections.

Needs the owner (cannot be done from here):
- 11 products have only one photo: Ajrakh Kali kurti, Pink Jaipuri, Brown Bandhani, Royal Blue
  Leheriya, Yellow, Baby Pink and Parrot Green Jaipuri, Maroon Striped, and the three cotton
  tunics. Add 2–4 more photos each (back, close-up of the craft, styled).

## Round 8 — two more blog posts (1 Nov 2026)

| Post | URL | Target searches |
|---|---|---|
| What to Wear to an Indian Wedding as a Guest: Haldi, Mehendi, Wedding Day and Reception | /blogs/journal/what-to-wear-indian-wedding-guest | wedding guest outfit, what to wear for haldi / mehendi |
| Ethnic Office Wear for Women: 7 Easy Kurti and Suit Set Looks for Work | /blogs/journal/ethnic-office-wear-for-women | ethnic office wear for women, office kurti, office suit set |

Both have an SEO title, meta description, cover image (from a product photo) and links to
specific products, collections, the Size Guide and earlier posts. Delivery times and the size
exchange mentioned in the wedding post match the shipping and exchange policies.

## Round 9 — kurti size guide post (1 Nov 2026)

- New post: **How to Choose Your Kurti Size: Measure at Home in 5 Minutes**
  (`/blogs/journal/how-to-choose-your-kurti-size`) — how to measure bust, waist, hip and
  shoulder, a bust/waist/shoulder table (M–3XL), choosing by bust first, between-sizes advice,
  lengths (long kurti ~46 in, set kurtas 44–46 in, pants ~38 in), ±0.5 in handmade variation,
  WhatsApp help and the one-time size exchange. No festival references.
- Size Guide page now links to the post.

**To fix (owner):** the Size Guide page lists hip as 38/40/42/44/46 in for M–3XL, but the
size charts on product pages say 40/42/44/46/48 in. Bust, waist and shoulder match. Decide which
is right and update the other. The new post leaves hip out of its table and points readers to
each product's own chart, so it is correct either way.

## Round 10 — Navratri references removed (1 Nov 2026)

- Chanderi collection FAQ: "Diwali, Navratri, weddings and pujas" → "Diwali, weddings and pujas".
- Fabric guide post quick-guide table: "Diwali, Navratri, weddings" → "Diwali and weddings".
- Verified: no collection or blog post mentions Navratri now. Still mentioned (owner's choice):
  homepage "Festive Edit" banner text and the Our Story page photo caption.

## Round 10b — remaining Navratri mentions (1 Nov 2026)

Navratri is over; Diwali is still on, so every Diwali mention stays.

- **Our Story page**: the second founders photo's alt text changed from "Sonal Kotak and Aman
  Kotak celebrating Navratri in Ahmedabad" to "Sonal Kotak and Aman Kotak in festive wear in
  Ahmedabad", both in the page and in Files. The file name still contains "navratri";
  renaming it would change the image URL, and shoppers never see it.
- **Checked clean**: all 61 products (text, tags, SEO, image alt), collections, blog posts,
  pages and menus.
- **Done by owner, verified 1 Nov**: Online Store → Themes → Customize →
  Home page → "Kala Kari festive" (The Festive Edit) → Text. Change
  "From Navratri evenings to Diwali mornings — hand-block prints and hand-embroidered
  Chikankari, made for celebrating." to
  "From Diwali mornings to wedding evenings — hand-block prints and hand-embroidered
  Chikankari, made for celebrating."
- Optional and not visible: the header offer bar (Diwali Dhamaka Sale) still has an old
  "Celebrate Navratri," banner heading and the "Dandiya sticks" ornament saved. The slim-bar
  style doesn't show either of them. Change them only if you ever switch it to "Large banner".

---

# Round 11 — re-check (1 Nov 2026)

## Checked, no problems found
- All 61 products: SEO title and description present and within length, alt text on every
  image, product category set (Google taxonomy), brand "Kala Kari Creations".
- 16 collections, 10 published blog posts and all pages have SEO titles and descriptions.
- Every internal link in published posts, collections, pages, products and menus points to a
  page that exists.
- Product and blog post structured data come from the theme (product-information,
  main-blog-post); OnlineStore, WebSite and BreadcrumbList come from meta-tags.

## Fixed (live now)
- **Collection images added** to 6 collections that had none: Kurtis, 2-Piece Sets,
  3-Piece Suit Sets, Tunics Shirts & Shrugs, Featured, Pair With. Each uses a product photo
  with descriptive alt text. Shared links and Google now show these photos instead of the
  default image. The homepage "Shop by style" tiles keep their own chosen images. Diwali Sale
  was left without one because it ends on 9 Nov.

## Flagged
- **Draft post "What is Ajrakh Printing?"** (unpublished, created 1 Nov) links to
  `/blogs/journal/how-to-care-for-hand-block-printed-cotton`, and that post doesn't exist.
  Fix or remove the link before publishing.

## Round 11b — cleaner product URLs + Mashru (1 Nov 2026)

16 product web addresses changed. Each old address has a permanent (301) redirect to the
new one (Online Store → Navigation → URL redirects), so old links, shares and Google
results still work.

| Old address (/products/…) | New address (/products/…) |
|---|---|
| ivory-coral-silk-embroidered-3-piece-suit-set-with-pink-yoke-pants-sheer-dupatta | cream-coral-silk-embroidered-3-piece-suit-set |
| blush-pink-pure-mul-cotton-floral-print-anarkali-suit-set | baby-pink-mul-cotton-anarkali-3-piece-suit-set |
| beige-jamdani-silk-paisley-woven-3-piece-suit-set-with-zari-dupatta | cream-jamdani-silk-paisley-3-piece-suit-set-with-zari-dupatta |
| beige-jamdani-silk-deer-motif-3-piece-dress | cream-jamdani-silk-deer-motif-3-piece-suit-set |
| light-grey-cotton-smocked-back-midi-dress | light-grey-chambray-smocked-back-midi-dress |
| pink-jaipuri-cotton-floral-print-short-top-with-gathered-flare-side-tie-up | pink-jaipuri-cotton-floral-print-short-top |
| maroon-jaipuri-handblock-print-3-piece-dress | maroon-olive-green-jaipuri-handblock-print-3-piece-suit-set |
| navy-blue-jaipuri-3-piece-dress | navy-blue-jaipuri-3-piece-suit-set |
| ocean-green-jaipuri-3-piece-dress | ocean-green-jaipuri-3-piece-suit-set |
| mustard-jaipuri-3-piece-dress | mustard-jaipuri-3-piece-suit-set |
| off-white-3-piece-chanderi-dress | off-white-chanderi-3-piece-suit-set |
| mustard-mul-chanderi-embroidered-3-piece-dress | mustard-mul-chanderi-embroidered-3-piece-suit-set |
| mustard-pure-mul-cotton-paisley-embroidered-3-piece-dress | mustard-mul-cotton-paisley-embroidered-3-piece-suit-set |
| indigo-dabu-block-print-cotton-3-piece-dress | indigo-dabu-block-print-cotton-3-piece-suit-set |
| dusty-pink-mul-chanderi-embroidered-3-piece-dress | dusty-pink-mul-chanderi-embroidered-3-piece-suit-set |
| beige-mul-chanderi-zari-embroidered-3-piece-dress | beige-mul-chanderi-zari-embroidered-3-piece-suit-set |

- SEO titles and descriptions of these products did not change (checked).
- Links in 3 blog posts updated to the new addresses directly: the fabric guide, the wedding
  guest guide and the office wear post (11 links). No theme setting, menu, page or
  collection used the old addresses.
- **Mashru:** the grey silk kurti's SEO title is now "Mashru Silk Mirror Work Grey Kurti |
  Kala Kari Creations". Its meta description now says "Mashru (Mushroo)" so both
  spellings are covered. The product name and its web address stay the same.
- If you shared any of the old product links on Instagram or WhatsApp, they still work
  through the redirects.

## Round 11c — Ajrakh draft link + newer posts (1 Nov 2026)

- **Ajrakh draft** ("What is Ajrakh Printing?", scheduled for 15 Nov): the broken link was
  already gone. The "Our full guide" sentence was removed at 07:51 today. The
  care guide it pointed to now exists as a scheduled post ("How to Wash and Care for
  Hand-Block Printed Cotton", 22 Nov). Once that post is live, the link can go back into the
  Ajrakh post's care paragraph. **Scheduled:** a task on 22 Nov at 11:00 IST checks
  that the care guide is live, then puts the link back (it waits a day if the guide isn't live yet).
- Two newer posts were written before the product address change, so their links went
  through redirects. They now point straight at the new addresses:
  - "Which Kurti Style Suits Your Body Shape?" (live): the Baby Pink Anarkali link.
  - "How to Wash and Care for Hand-Block Printed Cotton" (scheduled 22 Nov): the Indigo
    Dabu link.
- Checked: all 14 posts (11 live, 3 scheduled for 8, 15 and 22 Nov) now have no broken or
  old-address links. Their publish dates are unchanged.

---

# Round 12 — Google & YouTube check (1 Nov 2026)

## What the owner has done (checked from the store)
- **Google & YouTube sales channel installed**, with all 61 active products published to it.
- **Judge.me** installed. 1 review so far, on the Ajrakh silk kurti.

## Fixed (live now): product details Google Shopping uses for clothing
- **Age group = Adults** on all 61 products. It was empty everywhere. I enabled Shopify's standard
  "Age group" category field and created the "Adults" value.
- **Gender = Female** added to 4 products that had none: Handcrafted Rayon 2-Piece Suit,
  Chocolate Grid Co-Ord Set, Cream Jamdani Paisley set, Mustard Mul Chanderi set.
- **Colour** added to 2 products that had none: Cream Jamdani Paisley set (Cream), Mustard
  Mul Chanderi set (Mustard).
- Every product already had a Google product category and a Size option, and every variant has a SKU.

## Can't be checked from Shopify (owner to confirm)
- **Google Search Console** verification and sitemap submission. There's no verification tag in the
  theme, so if it was verified through DNS or the Google app, it can't be seen from here.
- **Google Merchant Center** product approvals and warnings. Check them in the Google & YouTube app
  → Overview / Products.
- **Google Business Profile.**

## Noticed
- The 10 newest products (added 28–29 Oct) are **not** in the Facebook & Instagram channel.
  The other 51 are.

---

# Round 13 — SEO checker "Site Compliance" warnings (1 Nov 2026)

New unpublished theme **"Kala Kari - SEO Fixes 4"** (copy of the live "SEO Fixes 3"). It changes 3 files,
and each upload was checked against its checksum:

| Warning | Fix |
|---|---|
| Encoding: charset not in the first 1024 bytes | `<meta charset="utf-8">` is now the first tag inside `<head>` (`layout/theme.liquid`). The old one was removed from `snippets/meta-tags.liquid`, so there's no duplicate. |
| Colour contrast too low | `snippets/kk-base.liquid`: the small gold text (section labels like "THE COLLECTION", card labels, filter labels) changed from #A9833A to #82632A. Contrast on ivory went from 3.1:1 to 5.0:1. Grey crossed-out prices and small notes changed from #8d8279 to #716760 (3.4:1 → 4.9:1). Gold text on the maroon offer banner changed from #CDA85C to #D9B871 (4.3:1 → 5.1:1). Decorative gold lines use the same colour, so they're slightly darker too. |

Not changed:
- **robots.txt / sitemap "missing"**: Shopify creates both automatically: `/robots.txt` (with a Sitemap line) and `/sitemap.xml`. The theme has no custom robots file overriding them. The checker most likely couldn't fetch them; it may have been blocked by Shopify's bot protection, or it checked a different address. Open both URLs in a browser to confirm.
- **Skip link "missing"**: the theme already has one ("Skip to content", jumping to `#MainContent`). It's hidden until you press Tab, which is standard. The checker probably doesn't detect off-screen links.
- **Map & geo signals**: optional, and aimed at shops with a walk-in location. The address is a home, so no map was added. A Google Business Profile covers local search.

## Round 14 — re-check after publishing "SEO Fixes 4" (1 Nov 2026)

- "SEO Fixes 4" is live. All 3 changed files match what was uploaded: charset first in
  `<head>`, contrast fixes, and meta tags without a duplicate charset.
- All 61 products: SEO titles and descriptions are present, within length and not repeated. Every image has alt text.
- All 15 collections, all pages (except the hidden size-exchange form) and the homepage have SEO titles and descriptions.
- All 14 blog posts have SEO titles, descriptions and cover alt text, and no broken internal links.
- **Fixed:** "Which Kurti Style Suits Your Body Shape?" meta description was 162 characters. It's now 156,
  so Google won't cut it off.

---

# Round 15 — re-check (4 Nov 2026)

## Fixed (live now)
- **Alt text and file names for 24 new product photos.** The owner replaced the single photo on 8 products
  with 3 new ones (2–3 Nov). None had alt text, and all were named `Gemini_Generated_Image_….png`.
  Each now has alt text ("<product> - Kala Kari Creations - view N") and a descriptive file name.
  The 8 products are: Ajrakh Kali flair kurti; Pink Jaipuri, Rich Brown Bandhani, Royal Blue Leheriya,
  Yellow, Baby Pink, Parrot Green and Maroon Striped 3-piece suit sets.

## Theme: "Kala Kari - SEO Fixes 7 (one H1 + alt text)" (unpublished — preview, then publish)
- The live theme, "SEO Fixes 6 (speed + H1)", added a second hidden H1 in the homepage slideshow.
  The header already prints the homepage H1, so the homepage had **two H1s**.
- Fixes 7 is a copy of Fixes 6. The only change is `sections/kk-slideshow.liquid`, which no longer has its
  H1 or the "Homepage H1" setting. The header's H1 ("Kala Kari Creations – Handcrafted Chikankari,
  Jaipuri & Kutchi Ethnic Wear") is now the only one. Fixes 6's speed changes are kept, and the upload
  was checked against its checksum.

## Checked, no problems found
- Fixes 6 still has every earlier fix: charset first in `<head>`, contrast colours, meta tags,
  structured data, a single charset tag, and the Festive Edit text without Navratri.
- All 61 products: SEO titles and descriptions are unique and within length. Every image has alt text.
- All 15 collections and 14 blog posts have SEO text. 16 product redirects are in place.

## Round 15b — homepage H1 again + 5 new collections (4 Nov 2026)

### Homepage H1 (again)
A new live theme, "Kala Kari - No Compare & Save", was made from "SEO Fixes 6", so it still had the
second (slideshow) H1. I made a new copy, **"Kala Kari - No Compare & Save + one H1"**, with the
same one-file fix (`sections/kk-slideshow.liquid`, checksum 8f36a71c…). Publish this copy. "SEO Fixes 7"
is now out of date: it doesn't include the "No Compare & Save" change.
**Tip:** before you duplicate a theme to make another change, publish the latest SEO copy first, or
tell me and I'll apply the fix to the new copy.

### New collections (live, published to the Online Store)
These are automatic collections: new products join on their own when they have the right tag or type.

| Collection | URL | Rule | Products now |
|---|---|---|---|
| Dresses | /collections/dresses | tag "Dresses" (added to the 2 midi dresses) | 2 |
| Tunics | /collections/tunics | product type = Tunics | 7 |
| Cotton Kurtis | /collections/cotton-kurtis | tag "Cotton Kurti" | 6 |
| Long Kurtis | /collections/long-kurtis | tag "Long Kurti" | 7 |
| Short Kurtis | /collections/short-kurtis | tag "Short Kurti" | 4 |

Each collection has an SEO title and description, a collection image with alt text, an intro line, a
"Read more" section with links to products, related collections and blog posts, and 3–4 FAQs. The FAQ
answers match the exchange, sizing and care policies.
The Kurtis and Tunics, Shirts & Shrugs collections now link to the new ones ("Shop by style").

**Owner to-do:** add the new collections to the top menu (Online Store → Navigation → Main menu) so
shoppers and Google find them easily. When you add a product, give it the right tag ("Long Kurti",
"Short Kurti", "Cotton Kurti", "Dresses") or the type "Tunics", and it joins automatically.

## Round 16 — re-check (4 Nov 2026)

- Live theme is **"Kala Kari - No Compare & Save + one H1"**. It has a single homepage H1, and the charset,
  contrast, meta tags and structured data all match the checked files.
- **Menus updated (live):** the new collections weren't in any menu.
  - Main menu → More: added Cotton Kurtis, Long Kurtis and Short Kurtis (after Kurtis), and Tunics and
    Dresses (after Tunics, Shirts & Shrugs).
  - Footer menu: added the same 5 collections.
  - In both menus, the "3-Piece Dresses" label is now "3-Piece Suit Sets". The link (/collections/3-piece-dresses) is unchanged.
- Products, collections and blog posts: no new problems. Every image has alt text, and SEO text is unique and within length.
- Still open (owner): the 3 cotton tunics have only 1 photo each. 6 images keep their
  `Gemini_Generated_Image_…` names because the homepage theme points to them by file name. They all have alt
  text, so the effect is small.
