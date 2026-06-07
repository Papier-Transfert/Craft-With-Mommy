#!/usr/bin/env python3
"""Generate all images for paper-squirrel-craft.html."""
import io, os, time, logging
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-squirrel-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

# Consistent description of the squirrel so every image matches.
SQUIRREL = (
    "a chubby handmade paper squirrel made from brown construction paper, "
    "with a plump rounded teardrop body, a big curved fluffy tail that swoops up "
    "over its back, a light tan oval tummy patch, two small rounded brown ears, "
    "two googly eyes, and a tiny drawn nose and smile"
)

IMAGES = [
    {
        "filename": "paper-squirrel-craft.webp",
        "prompt": (
            f"A finished handmade paper squirrel craft: {SQUIRREL}. "
            "The squirrel holds a small brown and tan paper acorn between its two little front paws. "
            "Displayed flat on a light wood craft table with a few brown and tan paper scraps nearby. "
            "Cute, cuddly, woodland feel, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-squirrel-craft-mom-child.webp",
        "prompt": (
            "A warm scene of a young mom and her happy preschool child sitting together at a light wood craft table, "
            "smiling as they get ready to make a paper squirrel craft. On the table are sheets of brown and tan "
            "construction paper, blunt kid scissors, a glue stick, a small pile of googly eyes, and colorful markers. "
            "A partly finished brown paper squirrel body and curved tail sit in front of them. "
            "Cozy, loving, family-friendly moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-squirrel-body-cut.webp",
        "prompt": (
            "A single plump teardrop body shape cut from brown construction paper for a paper squirrel craft, "
            "rounder at the bottom for the belly and narrower at the top for the head, about the size of a hand. "
            "Lying flat on a light wood craft table next to blunt kid scissors and a pencil. "
            "Just the one brown paper body shape, nothing assembled yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-squirrel-fluffy-tail.webp",
        "prompt": (
            "A large curved fluffy squirrel tail shape cut from brown construction paper, swooping up and over "
            "like a question mark, with a soft bumpy wavy outer edge so it looks fluffy. "
            "It lies on a light wood craft table right next to the plump brown paper teardrop squirrel body from before. "
            "Two separate brown paper pieces, the body and the big tail, not yet glued together. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-squirrel-ears-paws-tummy.webp",
        "prompt": (
            "Small paper squirrel craft pieces freshly cut and laid out on a light wood craft table: "
            "two small rounded brown paper ears, two little brown paper front paws, and one rounded light tan "
            "paper oval for the tummy patch. The plump brown body shape and the big curved fluffy tail sit beside them. "
            "All flat paper pieces, clearly cut by a child, nothing glued yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-squirrel-body-assembled.webp",
        "prompt": (
            "A handmade paper squirrel partly assembled on a light wood craft table: the big curved fluffy brown tail "
            "is glued behind the plump brown body and curves up one side, a light tan oval tummy patch is glued to the "
            "lower front of the body, and two small rounded brown ears are glued at the top of the head. "
            "No face yet, no eyes drawn, just the assembled brown and tan paper shapes. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-squirrel-face-added.webp",
        "prompt": (
            f"A handmade paper squirrel with its face just added: {SQUIRREL}, "
            "showing two googly eyes stuck near the top of the head and a small marker nose, a sweet smile, "
            "and a few thin whisker lines drawn on each side, plus tiny pink cheeks. "
            "The big fluffy tail curves up behind the body and the tan tummy patch is on the front. "
            "It does not hold an acorn yet. Lying flat on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-squirrel-finished-acorn.webp",
        "prompt": (
            f"The finished handmade paper squirrel craft held up by a young child's hand: {SQUIRREL}. "
            "Two little front paws are glued to the tummy and hold a small acorn made from a brown paper oval "
            "with a light tan paper cap on top. The big fluffy tail curves proudly up behind the body. "
            "Soft blurred cozy home background. Proud finished craft, clearly made by a child. "
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
        img = img.convert("RGB")
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
