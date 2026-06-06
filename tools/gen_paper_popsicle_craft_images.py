#!/usr/bin/env python3
"""Generate all images for paper-popsicle-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-popsicle-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper and craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

# Shared description of the finished popsicle so the craft stays consistent across images.
POP = (
    "a handmade paper popsicle: a tall rounded-top shape, the lower half cut from bright "
    "pink construction paper and the upper half a teal construction paper layer glued on top, "
    "a thin wavy white paper strip glued across the middle where the two colors meet like a "
    "melty drip, tiny colorful paper sprinkle dots scattered on the teal top, and a natural "
    "wooden craft stick handle glued to the bottom"
)

IMAGES = [
    {
        "filename": "paper-popsicle-craft.webp",
        "prompt": (
            f"A finished paper popsicle craft flat lay: {POP}. Two small googly eyes and a "
            "marker-drawn happy smile on the pink lower half give it a friendly face. "
            "Lying flat and centered on a white craft table with a few colorful paper scraps "
            "and a glue stick at the edges. Cheerful summer craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-popsicle-craft-mom-child.webp",
        "prompt": (
            "A warm scene of a young mom and her little daughter sitting together at a white "
            "craft table, smiling and getting ready to make a paper popsicle craft. On the "
            "table are sheets of bright pink and teal construction paper, blunt kid scissors, "
            "a glue stick, a few natural wooden craft sticks, and a small pile of googly eyes. "
            "One simple pink and teal paper popsicle shape is already started in front of them. "
            "Cozy, loving family moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-popsicle-shape-cut.webp",
        "prompt": (
            "A single plain bright pink construction paper popsicle shape, an upright tall "
            "rectangle with a rounded top and a straight flat bottom edge. It is just the bare "
            "pink paper shape with absolutely NO wooden stick attached, NO teal layer, and NO "
            "decorations of any kind. Lying flat on a light wood craft table next to a yellow "
            "pencil and a pair of blunt kid scissors. Clean and simple, clearly cut by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-popsicle-two-flavors.webp",
        "prompt": (
            "A single paper popsicle shape lying completely flat on a white craft table, "
            "photographed straight from above as a flat lay. The shape has a rounded top and a "
            "flat bottom. The lower half is bright pink construction paper and a teal "
            "construction paper rounded-top layer is glued over the entire upper half, so there "
            "is teal on top and pink on the bottom with a clean straight horizontal line where "
            "they meet in the middle. The edges are pressed flat against the table. A purple "
            "glue stick rests beside it. Absolutely NO wooden stick of any kind, NO stick poking "
            "out the bottom, NO white drip, NO sprinkles, NO face. Clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-popsicle-craft-stick.webp",
        "prompt": (
            "A single upright vertical two-tone paper popsicle with a teal construction paper "
            "upper half on top and a bright pink construction paper lower half on the bottom, a "
            "clean straight horizontal line dividing them in the middle. A natural light wooden "
            "craft stick is glued to the bottom center of the pink part so about two inches of "
            "the wooden stick pokes straight down below the paper like a handle. Lying flat and "
            "centered on a white craft table. The popsicle still has NO white drip, NO sprinkles, "
            "and NO face yet. Simple and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-popsicle-drip-topping.webp",
        "prompt": (
            "A pink and teal two-tone paper popsicle on a wooden craft stick, now with a thin "
            "wavy white paper strip glued across the middle exactly where the teal top meets the "
            "pink bottom, looking like a soft melty white drip running along the popsicle. "
            "No sprinkles yet and no face yet. Lying flat on a white craft table. "
            "Charming handmade summer craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-popsicle-sprinkles.webp",
        "prompt": (
            "A pink and teal paper popsicle on a wooden craft stick with a wavy white paper drip "
            "across the middle, now decorated with many tiny colorful paper sprinkle dots in red, "
            "yellow, orange, and green glued across the teal top half. No face yet. "
            "Lying flat on a white craft table with a few leftover paper sprinkle scraps nearby. "
            "Playful and cheerful, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-popsicle-finished-face.webp",
        "prompt": (
            f"A completed paper popsicle craft held up by a small child's hand: {POP}. "
            "Two googly eyes are stuck on the pink lower half with a big marker-drawn happy "
            "smile beneath them, giving the popsicle a sweet friendly face. Bright, cheerful, "
            "and clearly handmade, with a softly blurred cozy home background. "
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
