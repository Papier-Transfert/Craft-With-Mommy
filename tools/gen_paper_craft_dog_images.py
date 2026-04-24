#!/usr/bin/env python3
"""Generate all images for paper-craft-dog.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-craft-dog"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-craft-dog.webp",
        "prompt": (
            "A finished handmade paper craft dog face lying flat on a light wood craft table. "
            "Large tan cardstock oval for the head, two dark brown teardrop-shaped floppy ears "
            "glued to the top sides and hanging down, a cream-colored rounded paper snout in the "
            "center-lower face, a small black paper oval nose, two wiggly googly eyes above the snout, "
            "a drawn smiling mouth in black marker with a tiny pink paper tongue, and a bright red "
            "construction paper collar strip at the bottom with a gold heart-shaped name tag. "
            "Paper scraps, a glue stick and child-safe scissors visible at the edges of the frame. "
            "Warm, cheerful, clearly child-made puppy craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-dog-mom-child.webp",
        "prompt": (
            "A warm, realistic photo of a young American mom and her child (around 4 years old) "
            "sitting together at a bright craft table, smiling gently as they get ready to make "
            "a paper dog craft. On the table in front of them: sheets of tan and brown construction "
            "paper, a pack of googly eyes, child-safe blunt-tip scissors, a glue stick, and colored "
            "markers. The mom is pointing at an oval cardstock shape. Cozy kitchen or playroom "
            "background, soft natural light. Sweet shared moment between mom and child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-dog-head-shape.webp",
        "prompt": (
            "A single large tan cardstock oval, about 6 inches tall, just cut out and lying flat "
            "on a light wood craft table. A pencil and a pair of blunt-tip kids' scissors rest "
            "right next to the oval. A few small paper scraps of the same tan cardstock around. "
            "Clean bright background, nothing else on the table. "
            "This is the first step of a paper dog craft: just the base head shape, no features yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-dog-cut-ears.webp",
        "prompt": (
            "On a light wood craft table: a single large tan cardstock oval head shape (about 6 inches tall) "
            "lying in the center, with two freshly cut dark brown construction paper ears next to it. "
            "Each ear is a long teardrop shape, about 4 inches tall. The ears are NOT glued on yet, "
            "they are simply lying beside the oval. A pair of kids' scissors and small brown paper "
            "scraps visible. Step 2 of a paper dog craft tutorial: ears prepared but not attached. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-dog-ears-glued.webp",
        "prompt": (
            "A tan cardstock dog head oval with two dark brown floppy teardrop ears now glued to "
            "the top left and top right of the head, each ear hanging down naturally over the edges "
            "of the face. No eyes, no nose, no mouth, no snout yet. Just the head and ears. Lying "
            "flat on a light wood craft table. A glue stick with cap off nearby. Clean, simple photo. "
            "Step 3 of a paper dog craft tutorial. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-dog-snout-nose.webp",
        "prompt": (
            "The paper dog head shape continues to progress. Tan cardstock oval head with two "
            "dark brown floppy ears glued at the top, plus a cream-colored rounded paper snout glued "
            "to the lower center of the face and a small black paper oval nose glued on top of the "
            "snout. NO googly eyes yet, NO mouth drawn yet. Flat on a light wood craft table. "
            "Step 4 of a paper dog craft tutorial. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-dog-googly-eyes.webp",
        "prompt": (
            "The paper dog face progresses further: tan cardstock oval head with two dark brown "
            "floppy ears glued at the top, cream-colored rounded paper snout with a small black "
            "paper oval nose in the lower center, plus two wiggly googly eyes now stuck just above "
            "the snout, spaced apart. No drawn mouth yet. Lying flat on a light wood craft table. "
            "The dog is starting to look alive. Step 5 of a paper dog craft tutorial. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-dog-mouth-details.webp",
        "prompt": (
            "Almost finished paper dog craft: tan cardstock oval head with dark brown floppy ears, "
            "cream snout with small black paper nose, two googly eyes, plus a black marker drawn "
            "smiling mouth (simple upside-down Y shape) just below the nose, a small pink paper "
            "tongue peeking out, and tiny black whisker dots on each side of the snout. "
            "No collar yet. Lying on a light wood craft table, a black fine-tip marker visible nearby. "
            "Step 6 of a paper dog craft tutorial. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-dog-collar-finished.webp",
        "prompt": (
            "The completely finished paper craft dog: tan cardstock oval head with dark brown "
            "floppy teardrop ears, cream snout with small black nose, two googly eyes, black "
            "drawn smiling mouth with a small pink tongue, tiny whisker dots, plus a bright red "
            "construction paper collar strip glued across the bottom of the head with a gold "
            "heart-shaped paper name tag in the center of the collar. Lying flat on a light wood "
            "craft table. Paper scraps, glue stick, and child-safe scissors visible at the edges. "
            "Final step of a paper dog craft, very cheerful. "
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
