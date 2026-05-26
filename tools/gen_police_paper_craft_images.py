#!/usr/bin/env python3
"""Generate all images for police-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "police-paper-craft"
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
        "filename": "police-paper-craft.webp",
        "prompt": (
            "A finished handmade paper police officer craft figure standing on a light wood craft table. "
            "The officer has a tall navy blue cardstock uniform rectangle for a body, a skin-tone construction paper oval head, "
            "two small blue paper arms on the sides, a black paper hat with a wide brim and a small gold shield badge on the front, "
            "two large googly eyes, a marker-drawn friendly smile and small eyebrows, "
            "a bright yellow five-point gold star badge glued on the chest, "
            "a thin black paper belt with a silver square buckle, and small black uniform buttons drawn down the middle. "
            "Photographed from the front, full body visible. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "police-paper-craft-mom-child.webp",
        "prompt": (
            "A warm scene at a light wood craft table with a mom and her young child of about 5 years old sitting side by side. "
            "They are smiling together, just starting a paper police officer craft project. "
            "On the table in front of them: navy blue construction paper, a black paper sheet for the hat, "
            "a small yellow gold star, googly eyes, a glue stick, child-safe scissors, and a few markers. "
            "Cozy bright kitchen atmosphere, soft natural light from a window. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "police-paper-craft-cut-shapes.webp",
        "prompt": (
            "A flat lay on a light wood craft table showing freshly cut paper shapes for a police paper craft: "
            "a tall navy blue cardstock rectangle about 4 by 6 inches for the uniform body, "
            "a skin-tone construction paper oval for the head, "
            "a black paper rectangle for the tall hat crown and a thin black strip for the hat brim, "
            "a bright yellow paper five-point star for the chest badge, "
            "and a small gold shield shape for the hat badge. "
            "A pair of child-safe scissors and a glue stick visible at the edge of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "police-paper-craft-glue-body.webp",
        "prompt": (
            "A child's hands gluing a skin-tone paper oval head onto the top of a tall navy blue cardstock "
            "uniform rectangle laid flat on a light wood craft table. "
            "Two small navy blue paper arm strips are positioned on each side of the uniform body. "
            "A purple glue stick is visible near the corner. No hat or badge attached yet. "
            "Charming and slightly imperfect, clearly being made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "police-paper-craft-build-hat.webp",
        "prompt": (
            "A child's hands placing a tall black paper police hat with a wide brim and a small gold shield badge "
            "on top of the skin-tone oval paper head of a half-built police officer paper craft. "
            "The navy blue uniform body and arms are visible underneath. No face details added yet. "
            "Lying flat on a light wood craft table. The hat sits proudly on top of the head. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "police-paper-craft-add-face.webp",
        "prompt": (
            "A close-up of the skin-tone paper face of a paper police officer craft on a light wood table. "
            "Two large googly eyes are stuck on under the black hat brim, a small pink dot serves as a nose, "
            "a curved marker-drawn friendly smile is below the nose, and two small black marker eyebrows are above the eyes. "
            "The tall black hat with the small gold shield badge is visible on top of the head. "
            "Navy blue uniform body partially visible below. No chest badge yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "police-paper-craft-gold-star-badge.webp",
        "prompt": (
            "A bright yellow gold five-point star badge being glued onto the upper left chest of a navy blue paper "
            "uniform body for a police officer craft. The word POLICE is lightly written in black marker across the star. "
            "The officer has a skin-tone head with googly eyes, a friendly smile, and a black hat with a small badge on top, "
            "all visible above the chest. Laid flat on a light wood craft table. A glue stick is nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "police-paper-craft-belt-and-tie.webp",
        "prompt": (
            "An almost finished paper police officer craft laid flat on a light wood craft table. "
            "A thin black paper belt strip with a small silver foil square buckle is glued across the waist of the navy blue uniform body. "
            "Three small black marker dots run down the middle of the chest as uniform buttons. "
            "A small black paper tie shape is glued just under the head. "
            "Above, the officer has a skin-tone face with googly eyes, a friendly smile, a black hat with a gold shield, "
            "and a yellow five-point star badge on the chest. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "police-paper-craft-finished.webp",
        "prompt": (
            "A completely finished handmade paper police officer craft proudly standing upright on a light wood craft table "
            "with a small folded paper tab at the bottom as a stand. "
            "The officer has a navy blue paper uniform with a yellow five-point gold star badge on the chest, "
            "a thin black belt with a silver buckle, small black uniform buttons drawn down the middle, "
            "a skin-tone face with two googly eyes, a marker-drawn friendly smile and eyebrows, "
            "and a tall black paper hat with a wide brim and a tiny gold shield on the front. "
            "Two small navy blue arms point slightly outward. "
            "Photographed from the front, full body visible, showing the finished craft as a proud display piece. "
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
