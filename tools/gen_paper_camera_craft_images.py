#!/usr/bin/env python3
"""Generate all images for paper-camera-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-camera-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

CAMERA_DESC = (
    "a handmade paper camera made from a black construction paper rectangle body about "
    "the size of a small book, with a large round black paper lens circle glued in the center, "
    "a smaller grey paper inner lens ring, a small square viewfinder hole near the top corner, "
    "a small yellow square flash next to the viewfinder, and a tiny red paper circle button on top. "
    "A black ribbon paper strap loops at the sides."
)

IMAGES = [
    {
        "filename": "paper-camera-craft.webp",
        "prompt": (
            f"A finished {CAMERA_DESC} "
            "Photographed from above as a flat lay on a white craft table with a few black and "
            "yellow construction paper scraps beside it, a glue stick, and a pair of kids scissors. "
            "The camera looks cute, friendly, and clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-camera-craft-mom-child.webp",
        "prompt": (
            "A warm photo of a young American mom and her four year old child sitting together "
            "at a light wood craft table, both smiling and excited. They are starting a paper "
            "camera craft. On the table in front of them are sheets of black, grey, yellow, and "
            "red construction paper, a glue stick, kids safety scissors, and a few cut paper shapes. "
            "Soft natural window light. The mood is cheerful, calm, and full of connection. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-camera-craft-cut-body.webp",
        "prompt": (
            "Top-down photo of a sheet of black construction paper on a craft table. A child's "
            "hand is gently holding a pair of red kids safety scissors and has just finished cutting "
            "out a rectangle shape about 5 inches wide and 3 inches tall from the black paper. "
            "The cut rectangle and the leftover paper scraps are clearly visible. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-camera-craft-glue-lens.webp",
        "prompt": (
            "Top-down photo on a craft table showing a black construction paper rectangle, "
            "5 inches wide by 3 inches tall, with a large black paper circle being glued onto its "
            "center as the camera lens. A smaller grey paper circle sits ready beside it to be added "
            "on top. A purple glue stick is open next to the rectangle. No other camera parts yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-camera-craft-inner-lens.webp",
        "prompt": (
            "Top-down photo of a black paper rectangle on a craft table. The rectangle has a large "
            "black paper circle glued in the center and a smaller grey paper circle glued on top of "
            "the black circle, creating a layered camera lens. The lens has visible imperfect edges "
            "from a child's cutting. A glue stick lies next to the craft. No viewfinder or flash yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-camera-craft-add-viewfinder.webp",
        "prompt": (
            "Top-down photo of the same paper camera in progress on a craft table: a black "
            "rectangle camera body with a layered black and grey paper circle lens in the center. "
            "A small white paper square about 1 inch wide is now glued to the upper right corner "
            "as the viewfinder window. No flash yet. Still flat on the craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-camera-craft-add-flash.webp",
        "prompt": (
            "Top-down photo of the same paper camera in progress: a black rectangle with a layered "
            "circle lens in the center and a small white square viewfinder in the upper right. "
            "Now a small bright yellow paper square about 1 inch wide is glued in the upper left "
            "corner as the camera flash. The craft is sitting flat on a light wood table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-camera-craft-decorate.webp",
        "prompt": (
            "Top-down photo of the paper camera with the layered lens, viewfinder, and yellow "
            "flash already in place. A child's hand is using a black sharpie marker to draw "
            "small details onto the camera: a tiny dial circle and brand-style lettering on the "
            "top edge. A tiny round red paper sticker has just been added on top as the shutter "
            "button. The craft sits on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-camera-craft-add-strap.webp",
        "prompt": (
            "Top-down photo of the finished paper camera body: black rectangle, layered black and "
            "grey lens, white viewfinder, yellow flash, red shutter button, and small marker details. "
            "Two thin black paper strips have been glued to the back top corners and looped together "
            "to form a simple paper neck strap. The strap is laid out neatly above the camera "
            "on the craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-camera-craft-finished.webp",
        "prompt": (
            "A cheerful young child, about five years old, holding the finished handmade paper "
            "camera up to one eye and pretending to take a photo, with both hands gripping the "
            "sides. The camera is a black rectangle with a layered round lens, white viewfinder "
            "square, yellow flash, and a paper strap looping around the child's neck. "
            "Bright, joyful expression. Living room background, slightly soft and warm. "
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
