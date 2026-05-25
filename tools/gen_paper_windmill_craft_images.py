#!/usr/bin/env python3
"""Generate all images for paper-windmill-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-windmill-craft"
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
        "filename": "paper-windmill-craft.webp",
        "prompt": (
            "A finished handmade paper windmill held up against a bright sunny blue sky background. "
            "The windmill has four diagonal blades made from a six inch square of bright pink construction paper "
            "with a yellow back side showing on the folded flaps, forming a classic four-bladed pinwheel shape. "
            "The blades are pinned at the center with a small silver push pin to a thin natural wooden dowel handle. "
            "The blades look caught mid-spin in a gentle breeze. Cheerful, springtime mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-windmill-craft-mom-child.webp",
        "prompt": (
            "A warm photo of a mom and her young child around 5 years old sitting together at a white craft table. "
            "Sheets of bright pink and yellow construction paper, blunt-tip kid scissors, a wooden ruler, a yellow pencil, "
            "a small cup of colorful push pins, and a thin natural wooden dowel rod are laid out in front of them. "
            "Both mom and child are smiling, looking at the supplies, getting ready to start a paper windmill craft together. "
            "Cozy daylight from a window. Real handmade craft mood, not a stock photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-windmill-square-cut.webp",
        "prompt": (
            "A freshly cut perfect square of bright pink construction paper, about six inches by six inches, "
            "with a yellow back side visible at one folded corner. The square sits flat on a white craft table "
            "next to a wooden 12 inch ruler with metric markings, a yellow pencil, and a pair of blue blunt-tip "
            "kid scissors. The square has straight clean edges. No windmill cuts yet, just a plain colored square. "
            "Flat lay top-down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-windmill-diagonal-lines.webp",
        "prompt": (
            "A bright pink construction paper square lying flat on a white craft table, "
            "now marked with two faint pencil diagonal lines drawn from corner to corner forming a clear X shape "
            "across the middle of the square. The pencil lines are thin, light gray, and slightly imperfect. "
            "A wooden ruler and a yellow pencil rest beside the square. No cuts yet, only pencil marks. "
            "Flat lay top-down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-windmill-diagonal-cuts.webp",
        "prompt": (
            "The same bright pink construction paper square on a white craft table, now showing four diagonal cuts "
            "made along the pencil X lines from each outer corner inward toward the center. Each cut stops about one inch "
            "before the very middle, so the square stays connected as one piece with four loose triangular flaps. "
            "The blue blunt-tip kid scissors lie next to it. The yellow back side of the paper is visible through the cuts. "
            "Flat lay top-down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-windmill-corners-folded.webp",
        "prompt": (
            "The bright pink paper square on a white craft table, now folded into a classic four-bladed pinwheel shape: "
            "every other corner of the four triangular flaps has been pulled inward and the four pointed tips overlap "
            "neatly at the center of the square. The yellow back side of the paper now shows on the folded flaps, "
            "creating a beautiful two-tone windmill pattern. No push pin in place yet. "
            "Flat lay top-down view on a clean craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-windmill-pin-center.webp",
        "prompt": (
            "A close-up of a mom's hand carefully pressing a bright blue plastic-headed push pin "
            "through the four overlapping folded paper tips at the very center of a pink and yellow paper windmill. "
            "The four blades of the windmill are clearly visible in the classic pinwheel shape with yellow flap backs showing. "
            "The pin is centered, and the sharp tip is just starting to poke through the back of the square. "
            "The windmill rests on a white craft table. Warm daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-windmill-finished.webp",
        "prompt": (
            "The finished completed paper windmill craft held up by a small child's hand against a bright sunny blue sky. "
            "Four pink and yellow construction paper blades arranged in the classic pinwheel shape, pinned with a bright "
            "blue push pin to the top of a thin natural wooden dowel handle. The blades look slightly motion-blurred "
            "as if caught mid-spin in a gentle breeze. Joyful springtime outdoor mood. "
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
