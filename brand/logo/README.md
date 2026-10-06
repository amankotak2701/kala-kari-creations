# Kala Kari Creations logo

Mughal jharokha arch in antique gold with a mirrored "KK" monogram and lotus,
beside a Cinzel / Cormorant Garamond wordmark. Brand colours: maroon `#752C39`,
cream `#F7F2E9`, gold gradient `#8E6A2E` → `#D9BC79`.

| File | Use |
|---|---|
| `kalakari-logo-horizontal.png` | Header logo on light backgrounds |
| `kalakari-logo-horizontal-inverse.png` | Logo on dark / maroon backgrounds |
| `kalakari-logo-stacked.png` | Password page, social profiles, packaging |
| `kalakari-favicon.png` | Browser tab icon (square monogram) |

The `.svg` files are scalable masters with fonts embedded. To re-render after
editing `defs.svgfrag` or `render.js`:

    npm pack @fontsource/cinzel @fontsource/cormorant-garamond   # extract to <fonts>/cinzel and <fonts>/cormorant-garamond
    node render.js "$PWD" <fonts>
