# Order Printer templates: Kala Kari Creations

To add one: Shopify admin → Apps → **Order Printer** → **Templates**, then:
- for the invoice, open the existing **Invoice** template, replace everything and Save;
- for the others, click **Create template**, give it the name below, paste the file and Save.

| File | Template name | Use it for |
|---|---|---|
| invoice.liquid | Invoice | A4 tax invoice / bill for every order |
| packing-slip.liquid | Packing slip | Packing checklist (no prices) |
| thermal-receipt.liquid | Thermal bill (80mm) | Billing/thermal printer (58 mm: see note inside) |
| size-exchange-slip.liquid | Size exchange slip | Goes in the parcel for ₹99 exchange replacement orders |
| thank-you-card.liquid | Thank-you card | Note from Sonal & Aman + care + exchange info, every parcel |
| address-label.liquid | Address label 4x6 | Only for parcels you send yourself (Shiprocket prints its own labels) |

To print: Orders → tick one or more orders → **More actions → Print with Order Printer** → choose the template.
For every order, print the invoice, packing slip and thank-you card. Print the exchange slip only for exchange replacement orders.
If you register for GST, uncomment the GSTIN line in invoice.liquid and thermal-receipt.liquid.
