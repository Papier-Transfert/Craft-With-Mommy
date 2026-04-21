#!/usr/bin/env python3
"""Generate all images for tissue-paper-suncatcher-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "tissue-paper-suncatcher-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "tissue-paper-suncatcher-craft.webp",
        "prompt": (
            "A finished handmade tissue paper suncatcher hanging in a bright sunny window. "
            "The suncatcher has a large circular flower frame cut from black construction paper, "
            "filled with overlapping pieces of colorful tissue paper in pink, orange, yellow, green, "
            "blue, and purple. The sunlight shines through the tissue paper layers creating a beautiful "
            "stained glass glow effect with warm light patterns. The black frame is neat and clean. "
            "A piece of yellow ribbon hangs it from a white curtain rod. "
            "The overall look is vibrant, glowing, and beautiful. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-suncatcher-mom-child.webp",
        "prompt": (
            "A mom and her young child (around 4 years old) sitting together at a white craft table, "
            "happily tearing small pieces of brightly colored tissue paper. "
            "The table has sheets of tissue paper in pink, orange, yellow, green, blue, and purple, "
            "along with a black construction paper flower frame and a roll of clear contact paper. "
            "The mom is smiling and encouraging the child. "
            "The child is focused and excited. The atmosphere is warm, cozy, and joyful. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-suncatcher-frame-cut.webp",
        "prompt": (
            "A piece of black construction paper on a white craft table with a large flower shape "
            "drawn on it. The center of the flower has been carefully cut out, leaving a clean black "
            "flower frame about one inch wide around the opening. "
            "Small scissors with colorful handles sit beside the frame on the table. "
            "A pencil and ruler are visible nearby. "
            "The frame is clearly handcut, slightly imperfect and charming. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-suncatcher-contact-paper.webp",
        "prompt": (
            "A piece of clear self-adhesive contact paper laid sticky-side-up on a white craft table. "
            "A black construction paper flower frame is being pressed firmly down onto the sticky surface, "
            "centered so the flower-shaped opening is surrounded by contact paper. "
            "The contact paper backing paper is peeled back and visible to the side. "
            "The black frame is clearly pressed flat against the clear sticky surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-suncatcher-tearing-tissue.webp",
        "prompt": (
            "A child's small hands tearing a sheet of bright orange tissue paper into small irregular "
            "pieces on a white craft table. "
            "Several piles of already-torn tissue paper pieces in different colors are visible: "
            "pink, yellow, green, blue, and purple pieces scattered in small groups. "
            "The torn pieces are roughly one to two inches each, soft and colorful. "
            "The table surface has a playful, cheerful feel with all the colors together. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-suncatcher-filling-frame.webp",
        "prompt": (
            "A child pressing small pieces of colorful tissue paper one by one onto the sticky "
            "clear contact paper inside a black construction paper flower frame. "
            "The flower frame is placed sticky-side-up on a white craft table. "
            "The inside of the flower is being filled with overlapping pieces of tissue paper in "
            "pink, orange, yellow, green, blue, and purple. "
            "Some pieces overlap and blend colors together. About half the frame opening is filled. "
            "The child's small hand is pressing a yellow piece onto the surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-suncatcher-seal.webp",
        "prompt": (
            "Hands pressing a sheet of clear contact paper sticky-side-down over a colorful tissue "
            "paper suncatcher on a white craft table. "
            "The suncatcher below shows a black flower frame completely filled with bright overlapping "
            "tissue paper pieces in many colors. "
            "The second contact paper sheet is being smoothed from one edge across slowly to seal "
            "everything in place. "
            "The contact paper backing is partially peeled back to the side. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-suncatcher-trimming.webp",
        "prompt": (
            "Small scissors carefully trimming the excess clear contact paper around the outside "
            "edge of a completed tissue paper suncatcher. "
            "The suncatcher is a flower shape with a black construction paper frame filled with "
            "colorful overlapping tissue paper in pink, orange, yellow, green, blue, and purple, "
            "sealed between two layers of contact paper. "
            "The scissors follow the curve of the black frame neatly. "
            "The craft table is white and the lighting is warm. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-suncatcher-hanging.webp",
        "prompt": (
            "A finished tissue paper suncatcher hanging in a bright sunny window. "
            "The suncatcher is a flower shape with a neat black construction paper border, "
            "filled with overlapping tissue paper pieces in vivid pink, orange, yellow, green, "
            "blue, and purple. "
            "Warm sunlight shines through the tissue paper layers, creating a glowing stained glass "
            "effect with colored light patterns on the white wall below the window. "
            "A yellow ribbon holds it from the window latch. "
            "The view feels warm, cheerful, and magical. "
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
