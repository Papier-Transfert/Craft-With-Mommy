#!/usr/bin/env python3
"""Generate all images for fortune-teller-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "fortune-teller-paper-craft"
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
        "filename": "fortune-teller-paper-craft.webp",
        "prompt": (
            "A finished handmade paper fortune teller (cootie catcher) sitting on a white craft table. "
            "It is folded from bright origami paper and stands with its four square outer flaps colored "
            "in red, blue, yellow, and green using washable markers. The four pockets are slightly opened "
            "showing the folded paper structure. A few extra colorful origami squares and scattered "
            "marker caps are visible at the edges. Top-down photograph. Crisp clean folds, vibrant colors. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fortune-teller-paper-craft-mom-child.webp",
        "prompt": (
            "A warm photograph of a mother and her young child (around age 6) sitting at a white "
            "wooden craft table, smiling and folding bright colored origami paper together for a "
            "fortune teller paper craft. Several sheets of red, yellow, and blue paper are spread out "
            "between them. The mother is helping the child line up a corner fold. Soft natural daylight, "
            "cozy home atmosphere. Both look engaged and happy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fortune-teller-paper-craft-cut-square.webp",
        "prompt": (
            "A bright colored square sheet of paper, about 7 inches by 7 inches, sitting flat on a "
            "white wooden craft table. The square is freshly cut with crisp clean edges, ready for "
            "folding into a fortune teller. A pair of kid-safe blunt scissors and a thin paper offcut "
            "strip rest beside it. Top-down view. Solid bright color paper (turquoise blue or coral red). "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fortune-teller-paper-craft-diagonal-folds.webp",
        "prompt": (
            "A flat square of bright colored origami paper lying open on a white craft table after "
            "being folded along both diagonals and unfolded. Two visible diagonal crease lines form "
            "an X across the square. Crisp clean creases visible. Childs hand resting at the edge "
            "smoothing the paper flat. Top-down view. Solid bright color (turquoise or red). "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fortune-teller-paper-craft-corners-folded.webp",
        "prompt": (
            "A bright colored origami paper square with all four corners folded inward to meet exactly "
            "at the center point. Four neat triangular flaps form a smaller square shape. The paper "
            "lies flat on a white wooden craft table. A childs small hand is pressing one of the "
            "triangle folds into place. Top-down view. Crisp clean folds, vibrant solid color. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fortune-teller-paper-craft-flipped-corners-folded.webp",
        "prompt": (
            "A small folded paper square in bright color, flipped over so the smooth side faces up. "
            "The four new corners have been folded inward to the center, creating four smaller triangle "
            "flaps on top. Clearly an in-progress fortune teller paper craft. Lying flat on a white "
            "craft table. Top-down view. Crisp folds, solid bright color paper. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fortune-teller-paper-craft-pockets-formed.webp",
        "prompt": (
            "A childs small hands holding an opened paper fortune teller (cootie catcher), with the "
            "four finger pockets visible. The thumbs and index fingers are slipped into the four "
            "pockets, ready to open and close the fortune teller game. Bright colored paper in solid "
            "shade. Photographed against a white craft table background. Charming handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fortune-teller-paper-craft-add-colors.webp",
        "prompt": (
            "A folded paper fortune teller lying flat on a white craft table with its four outer "
            "square flaps colored in solid bold blocks: red on one flap, blue on the next, yellow on "
            "the next, and green on the last. The colors are filled in with washable markers. A few "
            "Crayola-style washable markers in red, blue, yellow, and green rest beside the fortune teller. "
            "Top-down view. Bright cheerful colors. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fortune-teller-paper-craft-add-numbers.webp",
        "prompt": (
            "An opened paper fortune teller laid flat showing the inside, with eight small triangle "
            "sections each labeled with a hand-written colorful number from 1 to 8 using markers. "
            "Numbers are written in different bright colors (red, blue, green, purple). "
            "The outer four flaps still show the colored square blocks (red, blue, yellow, green). "
            "Lying flat on a white craft table. Top-down view. Clear handwritten numbers. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fortune-teller-paper-craft-finished.webp",
        "prompt": (
            "A finished colorful paper fortune teller craft with one numbered triangle flap lifted up "
            "to reveal a small handwritten fortune underneath: 'You will get extra hugs today!'. "
            "The four outer flaps are colored red, blue, yellow, and green. The numbers 1 through 8 "
            "are visible on the inner triangles. The fortune teller is propped slightly open on a "
            "white craft table next to a few colorful markers. Cheerful, ready-to-play look. "
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
