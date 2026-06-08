#!/usr/bin/env python3
"""Generate all images for paper-tulip-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-tulip-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-tulip-craft.webp",
        "prompt": (
            "A finished handmade paper tulip craft displayed on a sheet of light blue "
            "construction paper background: three colorful construction paper tulip blooms "
            "in red, pink, and yellow, each with the classic rounded three-bump tulip top, "
            "glued onto thin green paper stems that rise from a brown terracotta paper flower pot. "
            "Several long pointed green paper leaves around the stems. "
            "The whole picture looks like a cheerful spring tulip flower pot collage made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-tulip-craft-mom-child.webp",
        "prompt": (
            "A young mom and her small child sitting together at a light wood craft table, "
            "smiling and getting ready to make a paper tulip craft. On the table are sheets of "
            "red, pink, yellow, and green construction paper, a glue stick, and child-safe scissors. "
            "A few cut paper tulip shapes are already on the table. Warm, joyful shared moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-tulip-cut-blooms.webp",
        "prompt": (
            "A child's hands using child-safe scissors to cut a classic tulip bloom shape "
            "from a sheet of red construction paper. The tulip shape has a rounded body with "
            "three little bumps across the top. Two more finished paper tulip blooms in pink and "
            "yellow lie nearby on the white craft table with paper scraps around them. "
            "Early stage of the craft, only the colorful tulip blooms are cut out so far. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-tulip-stems-leaves.webp",
        "prompt": (
            "Three thin green construction paper strips cut as tulip stems lying on a white craft "
            "table, next to several long pointed green paper leaves. Child-safe scissors and green "
            "paper scraps are beside them. The three colorful paper tulip blooms in red, pink, and "
            "yellow sit off to the side, already cut. Clear flat lay showing the green stems and leaves stage. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-tulip-paper-pot.webp",
        "prompt": (
            "A flower pot shape cut from brown terracotta-colored construction paper, a simple "
            "trapezoid wider at the top, lying on a white craft table. Beside it are the three "
            "green paper stems, the green leaves, and the three colorful paper tulip blooms in red, "
            "pink, and yellow, all cut and waiting to be assembled. Glue stick nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-tulip-glue-stems.webp",
        "prompt": (
            "A sheet of light blue construction paper background with a brown terracotta paper "
            "flower pot glued near the bottom and three thin green paper stems glued so they rise "
            "up out of the pot. The tulip blooms are not attached yet. A child's hand presses a "
            "stem down with a glue stick nearby. Assembly in progress on a white craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-tulip-glue-blooms.webp",
        "prompt": (
            "A light blue construction paper picture with a brown paper flower pot, three green "
            "paper stems rising from it, and colorful construction paper tulip blooms in red, pink, "
            "and yellow now glued onto the top of each stem. A child's hand presses the yellow tulip "
            "bloom into place. The green leaves are not added yet. White craft table, glue stick nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-tulip-finished-pot.webp",
        "prompt": (
            "The completed paper tulip craft on light blue construction paper: a brown terracotta "
            "paper flower pot at the bottom with three green stems rising up, each topped with a "
            "colorful tulip bloom in red, pink, and yellow, and several long pointed green leaves "
            "added around the stems. A cheerful finished spring tulip flower pot picture made by a child, "
            "propped up slightly on a white craft table. "
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
