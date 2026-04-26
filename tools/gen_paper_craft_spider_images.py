#!/usr/bin/env python3
"""Generate all images for paper-craft-spider.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-craft-spider"
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
        "filename": "paper-craft-spider.webp",
        "prompt": (
            "A cute handmade paper craft spider laying flat on a light wood craft table. "
            "The spider has a round black construction paper body about three inches across, "
            "two large white-and-black googly eyes stuck to the front of the body, "
            "a small white crayon smile drawn between the eyes, and eight thin black "
            "paper strips folded into accordion-style zigzag legs sticking out around the body, "
            "four legs on each side. A few black paper scraps and a glue stick visible at the edge. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-spider-mom-child.webp",
        "prompt": (
            "A young American mom and her four-year-old child sitting together at a light wood "
            "craft table getting ready to make a paper spider craft. On the table in front of them "
            "is a sheet of black construction paper, kid safety scissors, a purple Elmer's glue stick, "
            "a small package of self-adhesive googly eyes, and a white crayon. Both are smiling and "
            "looking down at the supplies, hands relaxed. Warm cozy atmosphere, indoor daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-spider-cut-body-circle.webp",
        "prompt": (
            "A close-up of a child's small hand using kid-safe blunt-tip scissors to cut along "
            "a faint pencil-traced circle on a sheet of black construction paper. The circle is "
            "about three inches across. A small round bowl used as the tracing guide sits next to "
            "the paper. A pencil is on the table. Light wood craft table surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-spider-cut-leg-strips.webp",
        "prompt": (
            "A flat lay on a light wood craft table showing a round black construction paper "
            "circle (the spider body) sitting in the center, surrounded by eight thin black "
            "paper strips lined up neatly above and below the circle. Each strip is about three "
            "inches long and very thin, all roughly the same size. A pair of kid scissors and "
            "small bits of black paper trim visible at the edge of the table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-spider-accordion-fold.webp",
        "prompt": (
            "A close-up flat lay on a light wood craft table showing eight thin black paper "
            "strips that have been accordion-folded into springy zigzag shapes, lined up neatly "
            "next to a round black paper circle (the spider body). Each strip clearly shows "
            "multiple back-and-forth folds creating a zigzag fan look. A child's small hand "
            "is mid-fold on one of the strips. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-spider-glue-legs.webp",
        "prompt": (
            "A close-up of a child's hands gluing accordion-folded black paper zigzag legs "
            "onto the back of a round black paper circle (the spider body, flipped upside down). "
            "Several legs are already glued in place along one edge of the circle, sticking out "
            "like fanned legs. A purple Elmer's glue stick is held in the child's other hand. "
            "Light wood craft table surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-spider-finished.webp",
        "prompt": (
            "A finished cute handmade paper craft spider laying face-up on a light wood craft "
            "table. The spider has a round black construction paper body about three inches "
            "across, two large self-adhesive googly eyes stuck to the front, and a tiny curved "
            "white crayon smile drawn underneath the eyes. Eight accordion-folded black paper "
            "zigzag legs poke out around the body, four on each side. The finished spider looks "
            "friendly and cute, clearly handmade by a young child. "
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
