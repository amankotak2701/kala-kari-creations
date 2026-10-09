# Size exchange: free process (no paid app)

Customer page: https://<your-store>/pages/size-exchange (also in the footer under Support).
Requests arrive in your email inbox as "New customer message"; photos arrive on WhatsApp.

## Steps for each request (about 5 minutes)

1. **Check (Shopify app → Orders → the order)**
   - Delivered 3 days ago or less? Not already exchanged? Not Final Sale? Photos show tags on?
   - Requested size in stock? (Products → the product → variant stock)
   - If not eligible or out of stock, send WhatsApp template B or C below and stop.

2. **Send ONE payment link (Shopify → Orders → Drafts → Create order)**
   - Add the product in the **new size**. Click its price → Discount → **100%** (reason: Size exchange #ORDER).
   - Add custom item: **"Size exchange fee", ₹99**, qty 1 (untick "Item is physical").
   - Shipping: **Free shipping**. Select the customer.
   - Tick **Reserve items** if shown (holds the size), then **Send invoice**.
   - When the customer pays ₹99, Shopify creates the replacement order automatically,
     takes the new size out of stock, and it appears in Shiprocket.
     **Do not ship it yet.** Tag it `exchange-hold` in Shopify so you remember.

3. **Book reverse pickup (Shiprocket → Returns → Create Return / Add Return Order)**
   - Pick the original order, the item, reason "Size exchange", ask for quality check if offered.
   - Shiprocket charges your wallet its normal reverse rate (the ₹99 fee covers this).

4. **When the item arrives and passes your check**
   - Ship the replacement order in Shiprocket as normal.
   - Shopify → the returned product → old size stock **+1**.
   - Tag the original order `exchanged` (so it can't be exchanged twice).

If the item comes back worn/washed/tags removed: send it back, fee not refunded (template D).

## WhatsApp templates

A, Approved:
"Hi {name}, your size exchange for order #{order} is approved. Size {size} is reserved for you. Please pay the ₹99 exchange fee here: {invoice link}. Once paid, our courier will pick up the item within 1–3 days. Please pack it unworn and with tags on. Team Kala Kari"

B, Out of stock:
"Hi {name}, we're sorry, size {size} of {product} is currently out of stock, so we're unable to exchange it. As per our policy, returns or refunds aren't available. If you'd like, we can tell you when it's back in stock. Team Kala Kari"

C, Not eligible:
"Hi {name}, thank you for reaching out. Unfortunately order #{order} isn't eligible for a size exchange because {it's past the 3-day window / it's a Final Sale item / it has already been exchanged once}. Team Kala Kari"

D, Failed check:
"Hi {name}, we received your item, but it doesn't meet our exchange conditions ({reason}). We'll send it back to you at no further charge. The exchange fee isn't refundable. Team Kala Kari"

E, Shipped:
"Hi {name}, your new size has been shipped! Track it here: {tracking link}. Thank you for shopping with Kala Kari."
