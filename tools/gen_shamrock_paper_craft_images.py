#!/usr/bin/env python3
"""Generate all images for shamrock-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "shamrock-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood or cream craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

# The shamrock is always made of three medium-green paper hearts whose pointed
# tips meet in the center, plus a darker green paper stem pointing down, on a
# cream background sheet. Keep this craft visually consistent across all steps.
IMAGES = [
    {
        "filename": "shamrock-paper-craft.webp",
        "prompt": (
            "A finished handmade shamrock paper craft for St. Patrick's Day: three "
            "medium-green construction paper hearts arranged with their pointed tips "
            "meeting in the center to form a three-leaf shamrock, with a darker green "
            "paper stem pointing down from the center. Thin marker leaf veins drawn down "
            "each heart and a few gold glitter glue accents around the edges. Glued flat "
            "on a cream background sheet. A few green paper scraps, a glue stick, and "
            "child-safe scissors at the edges of the table. Bright, cheerful, clearly "
            "made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shamrock-paper-craft-mom-child.webp",
        "prompt": (
            "A warm scene of a young mom and her small child sitting together at a craft "
            "table, smiling and getting ready to make a green shamrock paper craft. "
            "Sheets of green construction paper, a glue stick, and child-safe scissors "
            "are spread out in front of them. One green paper heart is already cut. "
            "Cozy home kitchen background, soft daylight. Loving, happy family moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shamrock-cut-green-hearts.webp",
        "prompt": (
            "Three medium-green construction paper hearts of roughly the same size, "
            "freshly cut and laid out separately on a light wood craft table. The heart "
            "edges are slightly uneven, clearly cut by a child. A pair of child-safe "
            "scissors and a folded sheet of green paper rest nearby. No shamrock shape "
            "assembled yet, just the three loose green hearts. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shamrock-cut-paper-stem.webp",
        "prompt": (
            "Three medium-green paper hearts, all the same size, plus one thin "
            "darker-green paper strip for a stem, all cut out and laid in a row on a "
            "light wood craft table. The three hearts are clearly equal in size. The thin "
            "green stem strip is about three inches long, straight with a very gentle "
            "curve at the top. Child-safe scissors rest beside them. Pieces are loose and "
            "not yet assembled into a shamrock. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shamrock-arrange-hearts.webp",
        "prompt": (
            "Three medium-green paper hearts arranged on a cream background sheet with "
            "their pointed tips all meeting in the center to form a three-leaf shamrock "
            "shape. The hearts are only placed in position, not glued, sitting loosely. "
            "A thin darker-green paper stem strip waits to the side. A child's hand gently "
            "adjusting one heart. Flat top-down view on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shamrock-glue-hearts.webp",
        "prompt": (
            "Three medium-green paper hearts glued flat onto a cream background sheet, "
            "their pointed tips pressed together in the center to clearly form a "
            "three-leaf shamrock. No stem attached yet. A glue stick lies open beside the "
            "craft. The paper looks freshly pressed down and slightly imperfect, clearly "
            "child-made. Flat top-down view on a light wood table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shamrock-glue-stem.webp",
        "prompt": (
            "A green shamrock made of three paper hearts glued on a cream background "
            "sheet, now with a thin darker-green paper stem glued below the center, "
            "pointing straight down so it looks like it grows from the shamrock. The full "
            "shamrock-and-stem shape is complete but not yet decorated. Flat top-down view "
            "on a craft table with a glue stick nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shamrock-finished-craft.webp",
        "prompt": (
            "A finished decorated shamrock paper craft on a cream background sheet: three "
            "medium-green paper hearts forming a three-leaf shamrock with a darker-green "
            "stem below. Thin black marker leaf veins are drawn down the center of each "
            "heart, and lines of gold and green glitter glue sparkle around the edges. "
            "Bright, festive, and cheerful St. Patrick's Day craft, clearly made by a "
            "child. Flat top-down view on a light wood craft table with a few green paper "
            "scraps around it. "
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
