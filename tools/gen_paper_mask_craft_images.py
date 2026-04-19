#!/usr/bin/env python3
"""Generate all images for paper-mask-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-mask-craft"
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
        "filename": "paper-mask-craft.webp",
        "prompt": (
            "A finished handmade paper butterfly mask lying flat on a white craft table. "
            "The mask is cut from bright purple and pink construction paper with two large "
            "butterfly wings and two oval eye holes. The wings are decorated with colorful "
            "marker swirls, polka dots in yellow and orange, and two small curled paper "
            "antennae attached to the top center. A piece of white elastic cord is threaded "
            "through holes on each side. Scattered markers and paper scraps visible nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mask-craft-why-kids-love.webp",
        "prompt": (
            "A cheerful mom and her young child (around age 4) sitting side by side at a "
            "bright craft table, both smiling and looking excited. The table has colorful "
            "construction paper, washable markers, scissors, and the beginning of a butterfly "
            "mask shape laid out. The child is pointing at the paper with delight. "
            "Warm family craft moment, cozy home setting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mask-craft-trace-cut.webp",
        "prompt": (
            "A sheet of bright yellow construction paper folded in half on a white craft table. "
            "On the folded half, a pencil-drawn outline of one half of a butterfly mask shape "
            "is visible: a wide curved top wing and a smaller rounded bottom wing meeting at "
            "the fold line. A pencil lies nearby. The paper is about to be cut out. "
            "Clean, simple, beginner-friendly craft setup. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mask-craft-cut-eye-holes.webp",
        "prompt": (
            "A yellow paper butterfly mask lying flat on a white craft table. The mask has been "
            "cut out symmetrically with two large wings. Two small oval eye holes have been "
            "neatly cut out near the center of the mask. A pair of child-safe scissors lies "
            "next to the mask. No decorations yet, just the clean cut mask shape with eye holes. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mask-craft-color-wings.webp",
        "prompt": (
            "A young child's hand holding a pink washable marker, actively coloring the wing "
            "of a paper butterfly mask on a white craft table. The left wing is already "
            "decorated with bright pink and purple swirls. The right wing is still plain yellow. "
            "Several uncapped markers in pink, blue, purple, and orange are scattered nearby. "
            "Warm, joyful craft moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mask-craft-add-details.webp",
        "prompt": (
            "A fully colored paper butterfly mask lying on a white craft table. The wings are "
            "covered in pink and purple swirls. Small orange and yellow paper circle dots have "
            "been glued onto the wings as decorative spots. Two thin curled paper strips are "
            "glued to the top center of the mask as antennae, curling upward. A glue stick "
            "and paper scraps are visible nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mask-craft-attach-elastic.webp",
        "prompt": (
            "A completed decorated paper butterfly mask lying flat on a white craft table. "
            "A single hole has been punched on the outer edge of each wing. White elastic "
            "cord is threaded through the left hole and tied in a secure knot. The right end "
            "of the cord lies next to the right hole, ready to be threaded. A small single "
            "hole punch tool lies nearby. The mask wings are fully decorated with swirls and dots. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mask-craft-child-wearing.webp",
        "prompt": (
            "A smiling young child (around age 4-5) wearing a handmade colorful paper butterfly "
            "mask over their eyes. The mask has pink and purple wings with orange and yellow "
            "paper dots and two curled paper antennae at the top. The elastic holds the mask "
            "snugly against the child's face. The child looks proud and happy, standing in a "
            "bright home interior. Warm, joyful family moment. "
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
