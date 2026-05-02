#!/usr/bin/env python3
"""Generate all images for paper-roses-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-roses-craft"
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
        "filename": "paper-roses-craft.webp",
        "prompt": (
            "A beautiful finished bouquet of three handmade paper roses arranged on a white craft table. "
            "Each rose is rolled from a spiral-cut circle of construction paper: one bright red rose, "
            "one soft pink rose, and one warm yellow rose. Each rose has two simple green construction "
            "paper leaves peeking out from below the petals, and each rose is attached to a green pipe "
            "cleaner stem. The three roses are tied together with a thin pastel ribbon to form a small "
            "bouquet, lying flat on the table next to a few paper scraps and a glue stick. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roses-craft-mom-child.webp",
        "prompt": (
            "A warm photo of a young mom and her preschool-age child sitting together at a light wood "
            "craft table. On the table are sheets of red, pink, and green construction paper, a pair "
            "of kid-safe scissors, a purple glue stick, and a few green pipe cleaners. The mom is "
            "smiling at her child as they get ready to make a paper roses craft together. Gentle, "
            "cozy lighting, sweet shared moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roses-craft-cut-circles.webp",
        "prompt": (
            "Three round paper circles, each about four inches across, cut from red, pink, and yellow "
            "construction paper, laid out flat on a white craft table. A small ceramic bowl used as the "
            "tracing template sits next to them, along with a pair of kid-safe scissors and a pencil. "
            "A few small construction paper scraps are visible at the edges. Clean, calm composition. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roses-craft-draw-spiral.webp",
        "prompt": (
            "Close-up of a child's hand using a pencil to draw a wavy spiral line on a red construction "
            "paper circle. The spiral starts at the outer edge and curves inward toward the center, "
            "with about half an inch of space between each loop. The circle sits flat on a white craft "
            "table next to scissors and a glue stick. Soft natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roses-craft-cut-spiral.webp",
        "prompt": (
            "A child's small hands holding kid-safe scissors and cutting along a pencil-drawn spiral "
            "line inside a pink construction paper circle. The cut has progressed about halfway, and "
            "the curling outer strip is starting to separate from the small disk left at the center. "
            "Paper scraps and a pencil are visible nearby on the white craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roses-craft-roll-rose.webp",
        "prompt": (
            "Close-up of two hands rolling a long red construction paper spiral strip tightly from the "
            "outer end toward the center. The rolled portion is starting to look like the layered petals "
            "of a real rose, with a tightly closed inner bud and slightly looser outer petals. The hands "
            "are working over a white craft table with a pencil and scissors visible nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roses-craft-glue-base.webp",
        "prompt": (
            "A finished rolled red paper rose sitting upright on a white craft table, pressed firmly "
            "onto a small round paper disk base coated with washable purple glue stick. The layered "
            "petals are clearly visible from the top, holding their natural rose shape. A purple glue "
            "stick lies open beside the rose. Clean, calm composition. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roses-craft-leaves.webp",
        "prompt": (
            "A finished red rolled paper rose viewed from slightly above, with two simple green "
            "construction paper leaves freshly glued onto the back so they peek out from underneath "
            "the petals. The rose lies flat on a white craft table. Green paper scraps and a pair of "
            "scissors are visible at the edge of the frame. Charming, handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roses-craft-finished.webp",
        "prompt": (
            "A finished bouquet of three handmade paper roses with green pipe cleaner stems and green "
            "construction paper leaves, tied together with a thin pastel pink ribbon. One rose is red, "
            "one pink, and one yellow. The bouquet is lying on a white craft table in soft natural "
            "daylight, ready to be gifted. The pipe cleaner stems are clearly visible and slightly "
            "bent into a natural curve. Sweet, gift-worthy composition. "
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
