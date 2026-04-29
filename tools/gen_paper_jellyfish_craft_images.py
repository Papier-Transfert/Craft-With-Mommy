#!/usr/bin/env python3
"""Generate all images for paper-jellyfish-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-jellyfish-craft"
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
        "filename": "paper-jellyfish-craft.webp",
        "prompt": (
            "A finished handmade paper jellyfish craft displayed on a white craft table. "
            "The jellyfish has a soft pink construction paper half-circle dome body, "
            "decorated with small dots and swirls drawn in teal and purple washable marker. "
            "Two large googly eyes are stuck on the front of the dome with a tiny black marker smile below. "
            "Underneath the dome, six to eight long wavy strips of pink, light purple, and teal tissue paper "
            "hang down like flowing tentacles, slightly curling. "
            "A few scraps of pink tissue paper, a glue stick, and a marker are visible nearby. "
            "Cheerful, soft, dreamy, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-jellyfish-craft-why-kids-love.webp",
        "prompt": (
            "A mom and young child (around age 4) sitting together at a light wood craft table, "
            "smiling and looking excited at light pink construction paper, sheets of pink and purple tissue paper, "
            "child-safe scissors, a glue stick, and washable markers spread out in front of them. "
            "The mom is gently pointing at the pink paper, explaining the jellyfish craft. "
            "Warm, cozy, joyful family moment, soft natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-jellyfish-craft-cut-body.webp",
        "prompt": (
            "A child's hands using child-safe scissors with colorful plastic handles "
            "to cut along a pencil-traced half-circle dome shape "
            "drawn on light pink construction paper. "
            "The dome is large, filling most of the paper, with the flat straight edge at the bottom. "
            "A pencil and pink paper scraps are visible on the white craft table. "
            "Close-up on the cutting action, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-jellyfish-craft-decorate-body.webp",
        "prompt": (
            "A child's hand drawing small colorful dots and swirls on a light pink construction paper "
            "half-circle jellyfish dome body using teal and purple washable markers. "
            "The dome shape is fully cut out and lying flat on the white craft table. "
            "Decorative marker dots and tiny swirls are visible across the pink dome. "
            "A few washable markers with caps off are scattered nearby. "
            "Close-up showing the decorating action, soft and cheerful. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-jellyfish-craft-cut-tentacles.webp",
        "prompt": (
            "A child's hands cutting long thin wavy strips from pink and light purple tissue paper "
            "using child-safe scissors. "
            "On the white craft table next to the strips: the decorated pink construction paper jellyfish dome "
            "(with marker dots and swirls already drawn on it), more sheets of pink and teal tissue paper, "
            "and a few already-cut tissue paper strips. "
            "The strips are long and slightly uneven, perfect for jellyfish tentacles. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-jellyfish-craft-glue-tentacles.webp",
        "prompt": (
            "A child pressing long pink and purple tissue paper strips onto the bottom straight edge "
            "of a light pink construction paper jellyfish dome body. "
            "The dome is decorated with marker dots and swirls and is positioned with its flat edge facing the child. "
            "A glue stick is visible on the white craft table, with several tissue paper strips already attached "
            "and hanging down from the dome. "
            "Close-up of the assembling moment, the child's small fingers carefully pressing a strip into place. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-jellyfish-craft-add-eyes.webp",
        "prompt": (
            "A child's small finger pressing a self-adhesive googly eye onto the front of a light pink "
            "construction paper jellyfish dome that already has long pink and purple tissue paper "
            "tentacle strips hanging down from the bottom edge. "
            "One googly eye is already attached to the dome, and the child is placing the second one. "
            "The dome has decorative marker dots and swirls. "
            "A small pack of googly eyes is visible nearby on the white craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-jellyfish-craft-finished.webp",
        "prompt": (
            "A completely finished paper jellyfish craft lying flat on a white craft table. "
            "The jellyfish has a light pink construction paper half-circle dome decorated with teal and purple "
            "marker dots and swirls. Two googly eyes are pressed onto the front of the dome with a tiny black "
            "marker smile drawn below the eyes. Long wavy strips of pink, light purple, and teal tissue paper "
            "hang from the bottom edge as flowing tentacles, slightly curling and overlapping. "
            "Washable markers and a few scraps of tissue paper are visible nearby. "
            "Cheerful, dreamy, complete, ready to display, clearly child-made. "
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
