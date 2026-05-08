#!/usr/bin/env python3
"""Generate all images for paper-umbrella-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-umbrella-craft"
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
        "filename": "paper-umbrella-craft.webp",
        "prompt": (
            "A finished handmade paper umbrella craft made from a bright yellow cardstock circle "
            "shaped into a domed umbrella canopy with visible accordion-style folds creating "
            "umbrella ribs. The canopy is decorated with painted polka dots in pink and turquoise. "
            "A curved white pipe cleaner forms a J-shaped umbrella handle attached to the underside. "
            "The umbrella stands upright on a light wood craft table, with a few colorful paper "
            "raindrop cutouts and a glue stick visible nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-umbrella-craft-mom-child.webp",
        "prompt": (
            "A young American mom around 30 years old and her 4 year old daughter sitting "
            "together at a light wood craft table, smiling and starting a paper umbrella craft "
            "together. On the table: bright yellow and turquoise cardstock circles, child-safe "
            "scissors, a glue stick, white pipe cleaners, washi tape, and crayola markers. "
            "The mom is helping the child draw polka dots on a yellow cardstock circle. "
            "Warm natural daylight from a window, cozy kitchen background, joyful shared moment. "
            "Realistic photo style, clearly a real family scene, not posed, family-friendly atmosphere."
        ),
    },
    {
        "filename": "paper-umbrella-craft-cut-circle.webp",
        "prompt": (
            "A child's small hand cutting a large bright yellow cardstock circle on a light wood "
            "craft table. A dinner plate used as a tracing guide is set beside the paper. "
            "The circle is about 9 inches across with a pencil tracing line still visible. "
            "Child-safe scissors with bright orange handles are halfway around the circle. "
            "Yellow paper scraps from the cutting are around the workspace. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-umbrella-craft-decorate.webp",
        "prompt": (
            "A bright yellow cardstock circle laid flat on a light wood craft table, decorated "
            "with hand-drawn pink and turquoise polka dots evenly spaced across the surface. "
            "A small child's hand is in the frame holding a turquoise crayola marker, "
            "adding more polka dots to the paper. "
            "Other markers in pink, blue, and yellow lie beside the paper. "
            "Slightly imperfect dot placement clearly drawn by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-umbrella-craft-cut-slit.webp",
        "prompt": (
            "A yellow polka dot decorated cardstock circle on a light wood craft table with a "
            "single straight cut made from the outer edge to the exact center of the circle. "
            "Child-safe scissors rest on the paper showing where the slit was just cut. "
            "The polka dots are pink and turquoise. The cut edges are clean and crisp. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-umbrella-craft-form-cone.webp",
        "prompt": (
            "A yellow polka dot cardstock circle being shaped into a shallow cone for an umbrella "
            "canopy by overlapping the two cut edges of the slit by about two inches and pinching "
            "them together. The result is a domed umbrella shape with a clear curved canopy. "
            "Two child hands and one adult hand are holding the overlap in place. "
            "Light wood craft table in the background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-umbrella-craft-attach-handle.webp",
        "prompt": (
            "A finished yellow polka dot paper umbrella canopy upside down on a light wood craft "
            "table with a white pipe cleaner being curved into a J-shape and inserted through a "
            "tiny hole at the very top center of the underside. A child's hand is bending the "
            "pipe cleaner into the umbrella handle shape. A small dab of clear glue is visible "
            "around the hole. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-umbrella-craft-add-ribbon.webp",
        "prompt": (
            "A finished paper umbrella craft displayed standing upright on a light wood craft "
            "table. The umbrella has a bright yellow polka dot canopy, a curved white pipe cleaner "
            "handle, and a small pink ribbon bow tied around the base of the handle. "
            "A few small paper raindrop cutouts in shades of blue are scattered on the table beside it. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-umbrella-craft-finished.webp",
        "prompt": (
            "A small 4 year old child smiling proudly while holding up a finished handmade paper "
            "umbrella craft by its curved white pipe cleaner handle. The umbrella canopy is bright "
            "yellow with pink and turquoise polka dots, with a small pink ribbon bow at the top "
            "of the handle. The child is sitting at a light wood craft table in a cozy kitchen "
            "with warm natural daylight from a window. Joyful, real, family-friendly moment, "
            "clearly handmade craft. "
            "Realistic photo style, not posed, warm atmosphere."
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
