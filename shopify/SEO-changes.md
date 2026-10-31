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
