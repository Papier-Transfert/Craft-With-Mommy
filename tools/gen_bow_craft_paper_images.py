#!/usr/bin/env python3
"""Generate all images for bow-craft-paper.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "bow-craft-paper"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "bow-craft-paper.webp",
        "prompt": (
            "Finished handmade paper bow craft sitting on top of a small wrapped gift box. "
            "The paper bow is made from pink and red cardstock with two soft pinched loops, "
            "a wrapped center band, and two notched ribbon tails peeking out below. "
            "The gift is wrapped in soft cream paper, set on a light wood craft table. "
            "A few additional paper scraps and a small pair of kid scissors visible nearby. "
            "The bow looks cute, polished but clearly handmade, slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bow-craft-paper-mom-child.webp",
        "prompt": (
            "A warm scene of a young American mom and her 5 year old child sitting at a light wood "
            "craft table together, smiling, with colorful pink, red, and yellow cardstock paper strips "
            "spread out in front of them. Kid scissors, a purple Elmer's glue stick, a roll of clear "
            "double-sided tape, and a small ruler are also on the table. They are about to start making "
            "a paper bow craft together. Both look relaxed and happy, warm natural light from a window. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bow-craft-paper-cut-strips.webp",
        "prompt": (
            "Three pink cardstock paper strips of three different lengths laid out neatly side by side "
            "on a light wood craft table. The longest strip is about 8 inches, the medium strip about 5 "
            "inches, and the small strip about 3 inches, all roughly the same width. Kid pointed-tip "
            "scissors and a pencil are placed next to the strips. Clean flat lay composition, no bow "
            "assembled yet. Slightly imperfect cut edges, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bow-craft-paper-loop.webp",
        "prompt": (
            "Close-up of a child's small hands pinching the middle of a long pink cardstock paper strip. "
            "The two ends of the strip have been brought into the center and overlap, forming a "
            "flat figure-eight shape with two soft loops on either side, like the start of a paper bow. "
            "A small piece of clear double-sided tape holds the two ends together at the meeting point. "
            "Light wood craft table background. No tail strip yet, no center band yet, just the loop. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bow-craft-paper-tails.webp",
        "prompt": (
            "A medium length pink cardstock paper strip lying flat on a light wood craft table, "
            "with a small upside-down V notch cut into each short end to create classic ribbon tails. "
            "Kid pointed-tip scissors lie beside the strip. The notches are slightly uneven, clearly "
            "child-cut. Plain clean composition, only the notched tail strip is visible, no bow loop assembled. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bow-craft-paper-center-band.webp",
        "prompt": (
            "Close-up of a small pink cardstock paper strip being wrapped snugly around the pinched "
            "middle of a pink figure-eight paper bow loop. A child's fingers hold the band tight against "
            "the back of the bow where the two ends of the small strip are being tucked and pressed "
            "together with a tiny piece of double-sided tape. The two loops on either side puff out softly. "
            "Light wood craft table background. No tail strip visible yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bow-craft-paper-glued.webp",
        "prompt": (
            "A completed pink paper bow with two soft pinched loops and a wrapped center band being "
            "pressed down onto the middle of a separate notched pink paper tail strip. The notched ends "
            "of the tail strip peek out from below the bow. A purple Elmer's glue stick lies open next to "
            "the assembly. A child's hand presses firmly on the center of the bow to set the glue. "
            "Light wood craft table background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bow-craft-paper-finished.webp",
        "prompt": (
            "A finished handmade pink paper bow with soft loops, a wrapped center band, and notched "
            "ribbon tails, taped on top of a small cream-wrapped gift box. Next to the gift sits a "
            "homemade folded greeting card with a smaller red paper bow attached to the front. "
            "Light wood craft table background with a few paper scraps and a purple glue stick nearby. "
            "Warm cheerful presentation, the bows look gorgeous but clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
]


def generate_image(client, prompt, output_path):
    from google.genai import types as genai_types
    from PIL import Image as PILImage
    full_prompt = f"{prompt} Aspect ratio: 4:3. Wide rectangular landscape orientation."
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=full_prompt,
        config=genai_types.GenerateContentConfig(response_modalities=["IMAGE"]),
    )
    image_bytes = None
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_bytes = part.inline_data.data
            break
    if image_bytes is None:
        log.warning(f"No image data for {output_path.name}")
        return False

    with PILImage.open(io.BytesIO(image_bytes)) as img:
        w, h = img.size
        target_ratio = TARGET_W / TARGET_H
        current_ratio = w / h
        if current_ratio > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            img = img.crop((left, 0, left + new_w, h))
        elif current_ratio < target_ratio:
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            img = img.crop((0, top, w, top + new_h))
        resized = img.resize((TARGET_W, TARGET_H), PILImage.LANCZOS)
        resized.save(output_path, "WEBP", quality=82, method=6)

    size_kb = output_path.stat().st_size // 1024
    log.info(f"  Saved: {output_path.name} ({TARGET_W}x{TARGET_H}px, {size_kb}KB)")
    return True


def main():
    import google.genai as genai
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        log.error("GOOGLE_API_KEY not set")
        return

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=api_key)

    for img in IMAGES:
        out = IMG_DIR / img["filename"]
        if out.exists():
            log.info(f"SKIP (exists): {img['filename']}")
            continue
        log.info(f"Generating {img['filename']}...")
        success = False
        for attempt in range(1, MAX_RETRIES + 1):
            if attempt > 1:
                log.info(f"  Retry {attempt}/{MAX_RETRIES}...")
                time.sleep(3)
            try:
                if generate_image(client, img["prompt"], out):
                    success = True
                    break
            except Exception as e:
                log.warning(f"  Error: {e}")
            time.sleep(2)
        if not success:
            log.error(f"  FAILED after {MAX_RETRIES} attempts: {img['filename']}")
        time.sleep(2)

    log.info("All done.")


if __name__ == "__main__":
    main()
