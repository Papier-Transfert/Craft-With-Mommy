#!/usr/bin/env python3
"""Generate all images for fathers-day-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "fathers-day-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

SHIRT_DESCRIPTION = (
    "a folded light blue cardstock card shaped like a short-sleeve dress shirt, "
    "with the top two corners of the front panel folded inward to form two pointed "
    "white-ish collar flaps meeting in a clean V at the top center. "
)

TIE_DESCRIPTION = (
    "a tall thin downward-pointing red and dark blue striped patterned paper tie, "
    "with a small trapezoid knot at the top tucked between the two collar flaps, "
    "and the body of the tie hanging straight down the center of the shirt. "
)

IMAGES = [
    {
        "filename": "fathers-day-paper-craft.webp",
        "prompt": (
            f"A finished handmade Father's Day paper craft on a light wood craft table: "
            f"{SHIRT_DESCRIPTION}{TIE_DESCRIPTION}"
            "Three small black marker button dots run down the center of the shirt below the tie. "
            "A tiny square patterned paper pocket sits on the chest, slightly to one side of the tie. "
            "The card stands open at a soft angle, propped slightly so it can be seen from the front. "
            "Crayons, kid scissors, and small paper scraps are casually placed around it. "
            "Cheerful Father's Day craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fathers-day-paper-craft-mom-child.webp",
        "prompt": (
            "A warm overhead-angled photo of a mom in a soft pastel shirt and her young "
            "child around four or five years old sitting side by side at a light wood craft table, "
            "smiling as they work on a Father's Day shirt and tie paper craft together. "
            "On the table in front of them: a sheet of light blue cardstock, a strip of red and "
            "dark blue striped patterned scrapbook paper, a small pair of blunt kid scissors, "
            "a purple glue stick, and a few crayons. The mom is gently holding the cardstock steady "
            "while the child reaches for the patterned paper. "
            "Warm, intimate, family-friendly mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fathers-day-paper-craft-fold-card.webp",
        "prompt": (
            "A single sheet of light blue cardstock about 8.5 by 11 inches folded clean in half "
            "horizontally on a light wood craft table. The open edge sits at the top and the "
            "sharp folded crease runs along the bottom. The card is closed flat at this stage "
            "with no tie or collar yet, just a plain rectangular blue folded card forming the body "
            "of a future dress shirt. A small ruler and a kid pair of blunt scissors sit nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fathers-day-paper-craft-fold-collar.webp",
        "prompt": (
            "The same folded light blue cardstock card on a light wood craft table, now with "
            "both top corners of the front panel folded down and inward to form two sharp "
            "triangular collar flaps meeting in the center with a clean V shaped opening between them. "
            "The collar flaps reveal a small triangle of white inside the fold. "
            "No tie has been added yet. Just a blue shirt card with a freshly folded collar. "
            "Tiny crease lines visible on the cardstock. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fathers-day-paper-craft-cut-tie.webp",
        "prompt": (
            "A close shot on a light wood craft table of a small pair of blue blunt-tip kid scissors "
            "cutting a tall thin downward-pointing tie shape from a sheet of red and dark blue striped "
            "patterned scrapbook paper. A separately cut small trapezoid knot piece in the same "
            "striped pattern lies next to the half-cut tie. "
            "The previously folded light blue shirt card with its V-shaped collar sits in the background "
            "of the same table, waiting for the tie. A pencil and ruler rest nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fathers-day-paper-craft-glue-tie.webp",
        "prompt": (
            f"A handmade Father's Day shirt card on a light wood craft table, with {SHIRT_DESCRIPTION}"
            f"{TIE_DESCRIPTION}"
            "The tie has just been glued in place, no buttons or pocket yet. "
            "A purple Elmer's glue stick lies open next to the card, with a small glue smear visible "
            "behind the tie knot. The card lies flat for this step. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fathers-day-paper-craft-add-buttons.webp",
        "prompt": (
            f"A close detail shot of a handmade Father's Day paper craft shirt on a light wood craft table: "
            f"{SHIRT_DESCRIPTION}{TIE_DESCRIPTION}"
            "Three small black marker button dots run down the center of the shirt below the tie, "
            "evenly spaced and slightly imperfect like a child drew them. "
            "A tiny square patterned paper pocket cut from the same red and dark blue striped paper "
            "is glued to the chest just to the side of the tie, with a thin marker stitch line "
            "drawn around its edge. A black Crayola marker rests next to the card. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fathers-day-paper-craft-finished-card.webp",
        "prompt": (
            "A completed Father's Day paper craft shirt and tie card on a light wood craft table, "
            "standing open with the inside fully visible. "
            "The outside is a folded light blue cardstock shirt with a pointed V collar, "
            "a red and dark blue striped patterned paper tie, three black marker button dots, "
            "and a tiny striped paper pocket. "
            "Inside the card, in bright cheerful marker handwriting, the words 'Happy Father's Day' "
            "are written in large colorful letters at the top, with a small heart drawn next to them. "
            "Below the message is a simple stick-figure crayon drawing of a tall dad and a smaller "
            "child holding hands, drawn in childlike style. "
            "Bright cheerful Father's Day card, clearly made by a young child. "
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
