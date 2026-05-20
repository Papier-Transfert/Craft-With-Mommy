#!/usr/bin/env python3
"""Generate all images for fox-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "fox-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "fox-paper-craft.webp",
        "prompt": (
            "A finished handmade paper fox craft standing upright on a light wood craft table. "
            "The fox is made from orange construction paper folded into a triangle face card shape, "
            "with two pointed orange ears at the top with smaller white triangle insides. "
            "The fox has a white snout glued onto the bottom half of the face, "
            "a small black paper triangle nose, two large googly eyes, "
            "and tiny black marker whiskers. The card stands on its own. "
            "Scattered around it: a small pair of kid scissors, a glue stick, and orange and white paper scraps. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fox-paper-craft-mom-child.webp",
        "prompt": (
            "A mom and a young child around 5 years old sitting at a light wood craft table, smiling and excited, "
            "with sheets of orange and white construction paper, kid scissors, a glue stick, a black marker, "
            "and a small pack of googly eyes laid out in front of them. They are about to start making "
            "a handmade paper fox craft together. Warm shared moment, natural daylight, cheerful and cozy mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fox-paper-craft-fold-triangle.webp",
        "prompt": (
            "A large square of bright orange construction paper folded diagonally in half to form a triangle, "
            "sitting on a light wood craft table. The folded edge is at the top and the open edge is at the bottom, "
            "so the triangle stands like a tent pointing downward when set up. A child's hand is pressing down on the crease. "
            "Plain triangle shape, no decorations yet. Beginning of a fox paper craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fox-paper-craft-cut-ears.webp",
        "prompt": (
            "Two small pointed orange paper triangle ear shapes freshly cut from orange construction paper, "
            "lying next to the larger folded orange triangle fox face base on a light wood craft table. "
            "A pair of kid blunt-tip scissors lies beside them along with orange paper scraps. "
            "The ears are clearly cut by a child, slightly uneven and charming. No glue applied yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fox-paper-craft-glue-ears.webp",
        "prompt": (
            "The folded orange triangle fox face card on a light wood craft table with two small pointed orange paper ears "
            "now glued to the top, each ear with a smaller white paper triangle glued inside it as the inner ear. "
            "A glue stick lies open next to the craft. The fox does not yet have a snout or eyes. "
            "Clearly child-made, slightly imperfect ear placement. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fox-paper-craft-add-snout.webp",
        "prompt": (
            "The orange triangle fox face card on a light wood craft table with a white paper rounded snout shape "
            "freshly glued onto the lower half of the orange triangle face. The fox already has its two pointed orange ears "
            "with small white triangle insides at the top. No nose or eyes yet, just the white snout glued in place. "
            "Glue stick visible next to the craft. Handmade child-friendly look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fox-paper-craft-add-face.webp",
        "prompt": (
            "The orange paper fox face card on a light wood craft table now with two large googly eyes glued above the white snout, "
            "a small black paper triangle nose at the top of the snout, and tiny black marker whisker lines drawn on the white snout. "
            "The fox already has its two pointed orange ears with small white triangle insides at the top. "
            "Black marker lying next to the craft. Sweet and silly handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fox-paper-craft-finished-card.webp",
        "prompt": (
            "The completed paper fox craft standing open on a light wood craft table, showing the inside of the folded card "
            "with a child's hand-drawn message in bright crayon colors that reads I love you, with a small heart "
            "and a stick figure drawing of a child and a fox. The outside of the card visible behind shows the cute "
            "orange fox face with two pointed ears, white snout, googly eyes, small black triangle nose, and whiskers. "
            "Crayons scattered around the card. Charming and warm family moment. "
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
