# Theme update: new collections, shop filters, "Complete the look"

Theme copy: **Kala Kari - New Collections & Filters** (duplicated from "Kala Kari - Exchange on Product").

| File | Change |
|---|---|
| `templates/index.json` | Homepage tabs: New In, Featured, Kurtis, 2-Piece, 3-Piece, Tunics & Shirts, **Pants**, **Chanderi**. Shop-by-style tiles: added **Co-Ord Sets, Pants, Chanderi, Mul Cotton**. |
| `sections/kk-tabs.liquid` | Allow up to 8 tabs (was 5). |
| `sections/kk-collection.liquid` | Shop page filter bar: **Style** (product type) and **Fabric** (`custom.fabric`) filters that work straight away, plus any filters switched on in the Search & Discovery app (price, size…). Sort and "In stock only" keep the other filters. Links like `/collections/all?fabric=chanderi&style=pants` open with the filters applied. |
| `templates/collection.json` | Shop page links: New Arrivals, Chikankari, Jaipuri Prints, Kutchi Work, Chanderi, Mul Cotton, Co-Ord Sets, Pants. |
| `snippets/kk-card.liquid` | Cards carry `data-type` / `data-fabric` for the filters; "Pants" and "Dress" labels. |
| `blocks/kk-pair-with.liquid` | "Complete the look": pinned products, then the **Pair With** collection (cheapest first), then Shopify recommendations. Skips anything over ₹1,000 and anything of the same type as the product being viewed. |
| `templates/product.json` | Complete the look shows 4 picks: the 3 mul cotton pants + the Chanderi shirt pinned, Pair With as the add-on collection. |

Store data changed alongside (Shopify admin): product types for the 7 new products, `custom.fabric`
metafield on all 45 products, tags `Mul Cotton` / `Chanderi` / `Pair With` / `New Arrivals`, and new
collections Pants, Chanderi, Mul Cotton, Co-Ord Sets, Pair With.

To add a product to the suggestions later, give it the tag **Pair With** (keep it under ₹1,000).
