#!/usr/bin/env python3
"""Generate all images for paper-stocking-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-stocking-craft"
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
        "filename": "paper-stocking-craft.webp",
        "prompt": (
            "A finished handmade paper Christmas stocking craft, made from a bright red cardstock "
            "stocking shape about seven inches tall, with a white cardstock cuff across the top. "
            "A neat row of soft white cotton balls is glued along the upper edge of the white cuff "
            "to make a fluffy snowy trim. The red body is decorated with several gold star-shaped sequins "
            "and a few small marker dots. A thin white satin ribbon loops through a small hole punched "
            "in the upper corner of the cuff for hanging. The stocking lies flat on a light wood craft table. "
            "Festive, cozy Christmas mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-stocking-craft-mom-child.webp",
        "prompt": (
            "A warm, realistic photo of a young American mom and her three or four year old child sitting "
            "together at a light wood craft table, just starting to make a paper Christmas stocking craft. "
            "On the table in front of them: a sheet of bright red cardstock, a sheet of white cardstock, "
            "a small pile of white cotton balls in a bowl, a small dish of gold sequins, kid scissors "
            "with blue handles, a purple glue stick, a few crayola markers, and a spool of thin white satin ribbon. "
            "Both are smiling and looking down at the supplies. Cozy family-friendly Christmas atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-stocking-craft-cut-shape.webp",
        "prompt": (
            "A child's hands using small blue-handled kid scissors to cut a simple stocking shape out of a folded "
            "sheet of bright red cardstock. A faint pencil outline of the stocking is visible on the folded paper, "
            "with the long straight back of the stocking running along the fold line. The cut is partway done, "
            "showing one finished curve. Light wood craft table in the background. No final stocking visible yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-stocking-craft-glue-cuff.webp",
        "prompt": (
            "A child's hands pressing a rectangular white cardstock cuff onto the top of a plain red cardstock "
            "stocking shape with no decorations yet. The cuff is clearly white, about one and a half inches tall, "
            "and lines up neatly with the top of the stocking. A purple glue stick lies open next to the work. "
            "The stocking is lying flat on a light wood craft table. No sequins, no cotton balls yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-stocking-craft-decorate-front.webp",
        "prompt": (
            "A child's hands placing small gold star-shaped sequins on the front of a red cardstock stocking "
            "shape with a plain white cardstock cuff already attached at the top. Several gold star sequins are "
            "already scattered across the red body of the stocking, and small bright marker dots are drawn on "
            "the white cuff. No cotton balls or ribbon yet. The decorated stocking is lying flat on a light wood "
            "craft table next to a small dish of gold sequins and a blue marker. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-stocking-craft-glue-back.webp",
        "prompt": (
            "A child's hands pressing the plain back of a red cardstock stocking shape on top of the already "
            "decorated front piece. The decorated front shows gold star sequins and marker dots on a red body "
            "with a white cuff peeking out at the top. A thin line of glue is visible along the curved seam "
            "between the two layers. The top of the cuff is left open so it can become a real stocking pocket. "
            "Lying flat on a light wood craft table. No cotton balls or ribbon yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-stocking-craft-cotton-trim.webp",
        "prompt": (
            "A close-up photo of a finished red cardstock stocking craft with a white cuff at the top. A neat "
            "single row of soft white cotton balls is glued along the upper edge of the white cuff, creating a "
            "fluffy snowy trim. Gold star-shaped sequins decorate the red body of the stocking, and a few marker "
            "dots are visible on the white cuff between the cotton balls. No ribbon loop yet. Lying flat on a "
            "light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-stocking-craft-ribbon-loop.webp",
        "prompt": (
            "A child's small hands threading a thin white satin ribbon through a small punched hole in the upper "
            "corner of the white cuff of a finished red paper Christmas stocking. The stocking has a row of fluffy "
            "white cotton balls along the top edge of the cuff and gold star sequins scattered across the red body. "
            "A blue handheld soft-grip hole punch lies next to the stocking. Lying flat on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-stocking-craft-hanging-finished.webp",
        "prompt": (
            "A finished handmade red paper Christmas stocking craft hanging by a white satin ribbon loop from a "
            "green Christmas tree branch with small twinkly white lights softly out of focus in the background. "
            "The stocking has a white cuff topped with a fluffy row of white cotton balls, gold star sequins on the "
            "red body, and a small candy cane tucked inside the opening at the top. Warm cozy Christmas evening mood. "
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
