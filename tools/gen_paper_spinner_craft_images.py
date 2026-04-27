#!/usr/bin/env python3
"""Generate all images for paper-spinner-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-spinner-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-spinner-craft.webp",
        "prompt": (
            "A finished cute handmade paper spinner toy laying on a light wood craft table, "
            "shown from above. The spinner is a round cardstock disc about four inches across, "
            "divided into six bright rainbow pie-slice sections in red, orange, yellow, green, "
            "blue, and purple, hand-colored with bold marker strokes. A sharpened yellow pencil "
            "is pushed straight down through the exact center of the disc, sticking up like the "
            "handle of a spinning top, with the disc resting near the pencil tip. A few markers "
            "and a small bowl visible at the edge of the table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spinner-craft-mom-child.webp",
        "prompt": (
            "A young American mom and her five-year-old child sitting together at a light wood "
            "craft table getting ready to make a paper spinner craft. On the table in front of "
            "them is a sheet of bright white cardstock, a set of bright Crayola markers spread "
            "out, kid safety scissors, a sharpened yellow pencil, and a small round bowl used "
            "as a tracing guide. Both are smiling and looking down at the supplies, hands "
            "relaxed. Warm cozy atmosphere, indoor daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spinner-craft-cut-circle.webp",
        "prompt": (
            "A close-up of a child's small hands using kid-safe blunt-tip scissors to cut along "
            "a faint pencil-traced circle on a sheet of bright white cardstock. The circle is "
            "about four inches across. A small round bowl used as the tracing guide sits next "
            "to the paper. A pencil is on the table. Light wood craft table surface, top down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spinner-craft-divide-sections.webp",
        "prompt": (
            "A flat top-down view on a light wood craft table showing a round white cardstock "
            "disc about four inches across. The disc has been divided into six pie-slice "
            "sections by light pencil lines drawn from the center to the edge. A clear plastic "
            "ruler lies next to the disc, and a sharpened pencil sits on top of the ruler. "
            "Bright Crayola markers are arranged neatly along one edge of the table, capped, "
            "ready to be used. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spinner-craft-color-sections.webp",
        "prompt": (
            "A top-down close-up of a child's hand using a bright red Crayola marker to color "
            "inside one pie-slice section of a white cardstock disc. The disc is about four "
            "inches across and divided into six pie-slice sections. Three sections are already "
            "colored solid in red, orange, and yellow, while the others are still uncolored. "
            "A few uncapped bright markers in green, blue, and purple sit nearby on the light "
            "wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spinner-craft-mark-center.webp",
        "prompt": (
            "A top-down close-up of a child's small finger pointing to a tiny pencil dot at the "
            "exact center of a fully rainbow-colored cardstock disc. The disc is about four "
            "inches across and divided into six bright pie-slice sections in red, orange, "
            "yellow, green, blue, and purple, all colored with bold marker strokes. Two faint "
            "fold creases cross at the center where the dot is marked. A sharpened pencil rests "
            "next to the disc on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spinner-craft-pencil-through-center.webp",
        "prompt": (
            "A side-angle view of a finished paper spinner toy resting on a light wood craft "
            "table. The spinner is a round cardstock disc about four inches across, divided "
            "into six bright rainbow pie-slice sections in red, orange, yellow, green, blue, "
            "and purple. A sharpened yellow pencil is pushed straight down through the exact "
            "center of the disc, with the disc sitting about one inch from the tip and the "
            "rest of the pencil sticking up. The disc is perpendicular to the pencil, balanced "
            "and ready to spin. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spinner-craft-spinning.webp",
        "prompt": (
            "A top-down view of a paper spinner toy mid-spin on a light wood craft table. The "
            "rainbow disc is in motion, so the bright six pie-slice colors blur into a soft "
            "swirled pastel rainbow ring with very slight motion blur, while the sharpened "
            "yellow pencil through the center stays sharp and in focus. Background shows a "
            "few markers and the small tracing bowl off to the side, slightly out of focus. "
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
