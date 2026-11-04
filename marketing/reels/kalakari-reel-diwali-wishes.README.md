# kalakari-reel-diwali-wishes.mp4

This is the "May your home glow with warmth…" Diwali greeting reel. The reference animation and audio are
unchanged, and the "Bunaai" wordmark is swapped for the Kala Kari Creations logo in two passes, because the
wordmark appears at two sizes and positions:

    python3 logo_swap_reel.py ref.mp4 pass1.mp4 240 284,167,436,216
    ffmpeg -i pass1.mp4 -vf scale=720:1280:flags=lanczos -c:v libx264 -crf 12 -c:a copy pass1_720.mp4
    LOGO_LEAD=18 python3 logo_swap_reel.py pass1_720.mp4 kalakari-reel-diwali-wishes.mp4 420 295,236,426,281
