#!/usr/bin/env python3
"""Generate all images for hello-kitty-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "hello-kitty-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper materials only. "
    "Charming and slightly imperfect, clearly handmade by a child. Pinterest-worthy."
)

# Description of the kitty look used across all images for visual consistency
KITTY_DESCRIPTION = (
    "a child's handmade white paper kitty face: a large white construction paper oval "
    "for the head, two small white pointed triangle ears glued to the upper corners, "
    "a small red paper bow on the right ear, two small black paper oval eyes, "
    "a small yellow paper oval nose centered below the eyes, "
    "and three short black marker whiskers fanning out on each side of the nose. "
    "Cute, simple, recognizable kitty character."
)

IMAGES = [
    {
        "filename": "hello-kitty-paper-craft.webp",
        "prompt": (
            "Hero photo of " + KITTY_DESCRIPTION + " "
            "The finished white paper kitty face is displayed flat on a light wood craft table, "
            "with a few red and white paper scraps and a glue stick visible at the edges of the frame. "
            "Warm afternoon light. Top-down flat lay composition. "
            + STYLE
        ),
    },
    {
        "filename": "hello-kitty-paper-craft-why-kids-love.webp",
        "prompt": (
            "A young mom in a soft cream sweater sitting at a light wood craft table next to her "
            "small daughter aged around 5, both smiling and looking at the materials in front of them. "
            "On the table: a sheet of white construction paper, a sheet of red construction paper, "
            "a small piece of yellow paper, a small piece of black paper, a pair of kid-safe scissors, "
            "a purple glue stick, and a black marker. "
            "They look excited to start a hello kitty paper craft together. "
            "Warm cozy home atmosphere, natural daylight from a window. "
            + STYLE
        ),
    },
    {
        "filename": "hello-kitty-paper-craft-cut-head.webp",
        "prompt": (
            "Close-up of a child's small hands using kid-safe scissors with light blue handles "
            "to cut a large white oval head shape from a sheet of white construction paper. "
            "A pencil-traced oval outline is faintly visible on the paper. "
            "A small white dessert plate sits on the table nearby as the tracing guide. "
            "A purple Elmer's glue stick rests on the corner of the table. "
            "Light wood craft table surface. Top-down view. Clearly child-made, charming and imperfect. "
            + STYLE
        ),
    },
    {
        "filename": "hello-kitty-paper-craft-ears.webp",
        "prompt": (
            "Top-down photo of a handmade craft in progress: a large white construction paper oval "
            "lying flat on a light wood craft table, with two small white paper triangle ears just glued "
            "to the upper left and upper right corners. The pointy tips of the ears stick up clearly above "
            "the curve of the head. No eyes, nose, bow, or whiskers yet, just the white head shape with ears. "
            "A pair of kid-safe scissors and a purple glue stick are visible at the edge of the frame. "
            "Small white paper scraps scattered around. "
            + STYLE
        ),
    },
    {
        "filename": "hello-kitty-paper-craft-bow.webp",
        "prompt": (
            "Top-down photo of a handmade craft in progress: a large white construction paper oval "
            "head with two small white pointed triangle ears at the top corners, "
            "and a small bright red paper bow freshly glued onto the right ear, tilting slightly. "
            "No eyes, nose, or whiskers yet. The face is still blank white. "
            "On the table around the craft: a small piece of red construction paper with bow shapes "
            "cut out of it, a pair of kid-safe scissors, and a purple Elmer's glue stick. "
            "Light wood craft table surface. Cheerful and clearly child-made. "
            + STYLE
        ),
    },
    {
        "filename": "hello-kitty-paper-craft-eyes-nose.webp",
        "prompt": (
            "Top-down photo of a handmade paper kitty face nearly complete: a white construction paper "
            "oval head with two small white pointed triangle ears at the top corners, "
            "a small red paper bow on the right ear, two small black paper oval eyes glued onto the "
            "center of the face spaced wider apart than usual, and one small yellow paper oval nose "
            "glued directly below and centered between the eyes. "
            "No whiskers drawn yet. "
            "Small scraps of black and yellow paper around it. Light wood craft table. "
            + STYLE
        ),
    },
    {
        "filename": "hello-kitty-paper-craft-whiskers.webp",
        "prompt": (
            "Top-down close-up photo of the finished " + KITTY_DESCRIPTION + " "
            "All elements are clearly visible: white head, white pointed ears, red bow on right ear, "
            "two black oval eyes, yellow oval nose, three short black marker whiskers on each side "
            "of the nose. A child's hand is just finishing drawing the last whisker with a black marker. "
            "Light wood craft table. Cheerful warm daylight. "
            + STYLE
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
