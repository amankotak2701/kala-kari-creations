# Payment methods strip (home page)

Theme copy: **Kala Kari - Payment Icons** (id 138965385424), duplicated from the live theme
"Kala Kari - Speed & Bug Fixes" on 26 Oct 2026. Publish it from Online Store → Themes.

- `sections/kk-payments.liquid` – "100% Secure Payments" strip: Visa, Mastercard, RuPay, UPI, NetBanking, Paytm,
  Amazon Pay, Amex and Maestro (the main methods in the Razorpay checkout), then any other `shop.enabled_payment_types`, so
  the row always shows exactly the payment methods switched on in Settings → Payments. Extra logos (image blocks)
  and text badges (e.g. "UPI", "Cash on Delivery") can be added in the theme editor.
- `templates/index.json` – the live home page with `kk_payments` added at the bottom, above the footer.

Preview: https://kalakaricreations.com/?preview_theme_id=138965385424
