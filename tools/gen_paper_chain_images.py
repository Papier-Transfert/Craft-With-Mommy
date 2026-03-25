#!/usr/bin/env python3
"""Generate all images for paper-chain-craft.html tutorial."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-chain-craft"
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
        "filename": "paper-chain-craft.webp",
        "prompt": (
            "A finished colorful paper chain craft coiled on a white craft table. "
            "The chain is made of interlocked paper loops in bright construction paper colors: "
            "red, orange, yellow, green, blue, and purple. "
            "About 25 links visible, some overlapping in a loose pile. "
            "The loops are slightly imperfect, clearly made by a child. "
            "Scissors and leftover paper strips sit in the background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-chain-craft-why-kids-love.webp",
        "prompt": (
            "A mom and young child (about 4 years old) sitting side by side at a craft table, "
            "both smiling and excited. "
            "The table has colorful construction paper strips, a tape dispenser, and scissors. "
            "A short paper chain of colorful loops sits in front of them. "
            "The child is pointing at the chain with delight. "
            "Warm, cozy home setting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "step1-cutting-strips.webp",
        "prompt": (
            "Close-up of a child's hands cutting a sheet of bright red construction paper "
            "into strips using child-safe rounded scissors on a light wood craft table. "
            "A ruler and pencil are nearby showing measured lines. "
            "Several already-cut colorful strips in orange, yellow, green, and blue "
            "are stacked to one side. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "step2-decorating-strips.webp",
        "prompt": (
            "A young child drawing patterns on flat paper strips with washable markers. "
            "The strips are laid out in a row on a white craft table. "
            "Some strips have stripes, zigzags, and hearts drawn on them in various colors. "
            "Open markers and crayons are scattered around. "
            "The child's hand is mid-drawing on a yellow strip. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "step3-first-link.webp",
        "prompt": (
            "Close-up of a child's hands forming the very first paper loop. "
            "A colorful paper strip is curled into a circle with the two ends overlapping, "
            "and a small piece of clear tape is being pressed over the overlap to seal it. "
            "The resulting loop is held up slightly from the table so it is clearly visible. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "step4-adding-links.webp",
        "prompt": (
            "A child threading a new paper strip through an existing paper loop. "
            "The new strip is passed through the previous loop and is being curled "
            "into a circle ready to be taped closed. "
            "A growing colorful chain of 6-8 loops lies on the table. "
            "The child's fingers are holding the new loop in shape. "
            "Tape dispenser visible nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "step5-hanging-chain.webp",
        "prompt": (
            "A long colorful paper chain garland draped across a doorway or mantel. "
            "The chain has about 20-25 loops in bright rainbow colors: "
            "red, orange, yellow, green, blue, and purple alternating. "
            "The loops are slightly imperfect, clearly child-made. "
            "The chain sags naturally in a gentle arc. "
            "Warm home interior visible in the background. "
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

    log.info("All done.")


if __name__ == "__main__":
    main()
