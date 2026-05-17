#!/usr/bin/env python3
"""Generate all images for box-craft-paper.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "box-craft-paper"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "box-craft-paper.webp",
        "prompt": (
            "A finished handmade folded paper gift box made from soft pink cardstock with a small floral pattern, "
            "sitting open on a light wood craft table. The box is about three inches square, with crisp clean folds "
            "and four neat walls standing upright. A few small wrapped candies and a tiny folded paper note "
            "are nestled inside the box. A second smaller pink folded paper box sits next to it. "
            "A roll of pastel washi tape and a few extra sheets of patterned cardstock visible at the edge. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "box-craft-paper-mom-child.webp",
        "prompt": (
            "A mom and a young child around five years old sitting close together at a light wood craft table, "
            "both smiling and working on folding a paper gift box. Several square sheets of pastel patterned cardstock "
            "(pink, mint, yellow) are spread out on the table. A clear acrylic ruler, a pencil, and three rolls of "
            "colorful washi tape sit beside the paper. The mom is gently smoothing a crease while the child watches. "
            "Warm, peaceful, real family moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "box-craft-paper-square-paper.webp",
        "prompt": (
            "A single square sheet of pastel pink and floral patterned cardstock lying flat on a light wood craft table, "
            "patterned side down so the plain back side is facing up. The square is about eight inches by eight inches. "
            "A clear plastic ruler and a sharpened pencil sit beside the paper. Nothing folded yet, just a clean flat square "
            "ready to begin folding into a paper box. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "box-craft-paper-diagonal-folds.webp",
        "prompt": (
            "A single square sheet of pastel pink and floral patterned cardstock lying flat on a light wood craft table, "
            "patterned side up. Two sharp diagonal creases run corner to corner forming a clear X shape across the paper. "
            "The creases are visible as crisp folded lines. The paper is otherwise flat and unfolded. "
            "A child's small hand smoothing one crease at the edge. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "box-craft-paper-corners-folded.webp",
        "prompt": (
            "A square sheet of pastel pink and floral patterned cardstock with all four corners folded inward to meet at the center, "
            "creating a smaller square shape with four triangular diamond flaps pointing inward toward the middle. "
            "The folded paper is sitting flat on a light wood craft table. The folds are crisp and even. "
            "A pair of small kid scissors visible at the edge of the table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "box-craft-paper-side-creases.webp",
        "prompt": (
            "A square sheet of pastel pink and floral patterned cardstock with the four corners folded inward to the center, "
            "and additional horizontal and vertical creases forming a clear tic tac toe grid pattern on top. "
            "The paper is otherwise still flat on a light wood craft table. The creases are sharp and crisp. "
            "Beside the paper is a clear plastic ruler. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "box-craft-paper-walls-up.webp",
        "prompt": (
            "A piece of pastel pink and floral patterned cardstock partway through being folded into a gift box. "
            "Two opposite side walls are lifted up vertically while two pointed end flaps still stick outward flat on the craft table. "
            "The shape is recognizably becoming a small open box. A hand gently holds one wall upright. "
            "Light wood craft table surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "box-craft-paper-finished.webp",
        "prompt": (
            "A completed handmade folded paper gift box made from soft pink cardstock with a small floral pattern, "
            "standing upright on a light wood craft table. The box is square with crisp neat walls about an inch and a half tall, "
            "and a clean flat bottom inside. The folds are sharp and the box holds its shape on its own. "
            "Empty inside, just the finished box. Photographed from a slight three quarter angle. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "box-craft-paper-decorated.webp",
        "prompt": (
            "A finished pastel pink folded paper gift box decorated with a colorful pastel washi tape strip wrapped around the rim "
            "and a small handmade pink paper bow taped on top. A second smaller folded paper box in mint green sits next to it. "
            "Both boxes are on a light wood craft table. A few tiny wrapped candies peek out from one of the boxes. "
            "Soft cheerful gift wrap atmosphere. "
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
