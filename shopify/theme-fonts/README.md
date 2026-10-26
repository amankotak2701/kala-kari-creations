# Website typography refresh

Theme copy: **Kala Kari - New Fonts** (id 138965516496), duplicated from the live "Kala Kari - Payment Icons" theme
on 26 Oct 2026. Publish it from Online Store → Themes.

| Where | Before | After |
|---|---|---|
| Headings | Cormorant 500 | Cormorant **600** (`type_heading_font: cormorant_n6`) |
| Italic accents | Cormorant 500 italic | Cormorant **600 italic** (`type_accent_font: cormorant_i6`) |
| Body text | Jost 14px | Jost **16px**, line height 1.75 in Kala Kari sections |
| Main menu, eyebrow labels, Kala Kari buttons | Jost | **Cinzel 600** (self-hosted `assets/kk-cinzel-600.woff2`, SIL OFL), echoing the KALA KARI wordmark |

Files changed in the theme:
- `snippets/kk-fonts.liquid` (new): preload + @font-face for Cinzel and the CSS overrides.
- `layout/theme.liquid`: one line, `{%- render 'kk-fonts' -%}` after `color-palette` in the head.
- `config/settings_data.json`: the three typography settings above.
- `assets/kk-cinzel-600.woff2` (new): from @fontsource/cinzel 5.3.0 (latin, 600).

Preview: https://kalakaricreations.com/?preview_theme_id=138965516496
