#!/usr/bin/env python3
"""Generate all images for banana-craft-paper.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "banana-craft-paper"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper and cardstock only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "banana-craft-paper.webp",
        "prompt": (
            "A finished handmade paper banana craft. A tall curved banana made of yellow "
            "construction paper, cut into three long strips that are folded open and down like "
            "an opened banana peel, revealing a smaller cream-white cardstock banana inside. "
            "The cream banana has two small googly eyes and a happy marker smile, with a few "
            "tiny brown marker spots. A small brown paper stem at the top and brown colored tips. "
            "The whole craft is glued flat on a light blue paper background, lying on a wood table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "banana-craft-paper-mom-child.webp",
        "prompt": (
            "A young mother and her small child sitting together at a light wood craft table, "
            "smiling and getting ready to make a paper banana craft. On the table are sheets of "
            "bright yellow construction paper, a sheet of white cardstock, child-safe scissors, "
            "a glue stick, and washable markers. Warm and cheerful family moment, "
            "the child looks excited to start. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "banana-craft-paper-cut-yellow-peel.webp",
        "prompt": (
            "A single tall curved banana shape cut from bright yellow construction paper, "
            "lying flat and whole on a light wood craft table. The shape is a simple long "
            "banana crescent with slightly uneven child-cut edges. Child-safe scissors and a "
            "yellow paper scrap rest beside it. Nothing else added yet, just the plain yellow peel shape. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "banana-craft-paper-cut-cream-inside.webp",
        "prompt": (
            "Two paper banana shapes lying side by side on a light wood craft table: one tall "
            "curved bright yellow construction paper banana, and next to it a slightly smaller, "
            "simpler banana shape cut from plain cream-white cardstock. Both have soft child-cut "
            "edges. The cream banana has no face or details yet. Scissors rest nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "banana-craft-paper-glue-inside.webp",
        "prompt": (
            "A plain cream-white cardstock banana shape glued flat onto a light blue paper "
            "background sheet, centered on the page, lying on a wood craft table. The cream banana "
            "is smooth with no face or details yet. A glue stick rests beside the background sheet. "
            "Simple, clean, clearly a craft in progress. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "banana-craft-paper-peel-strips.webp",
        "prompt": (
            "A yellow construction paper banana laid over a cream banana on a light blue background "
            "sheet, so only the yellow shows like a closed banana. The yellow peel has been cut into "
            "three long strips with two visible slits running from the top down toward the bottom, "
            "where the strips stay joined and glued. The strips still lie flat and closed, not yet "
            "folded open. On a wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "banana-craft-paper-peeled-open.webp",
        "prompt": (
            "A handmade paper banana being peeled open. The yellow construction paper peel is cut "
            "into three long strips that are folded outward and down, curling away from the center, "
            "revealing the smaller cream-white cardstock banana underneath. The cream banana inside "
            "is still plain with no face yet. Joined and glued at the bottom on a light blue "
            "background sheet, on a wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "banana-craft-paper-finished.webp",
        "prompt": (
            "A finished handmade paper banana craft. The yellow construction paper peel is cut into "
            "three strips folded open and down, revealing a cream-white cardstock banana inside. "
            "The cream banana has two googly eyes, a happy marker smile, and a few small brown "
            "marker spots. A small brown paper stem at the top and brown colored tips on the peel. "
            "Glued on a light blue paper background, on a wood craft table. Cheerful and complete. "
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
