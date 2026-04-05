#!/usr/bin/env python3
"""Generate all images for paper-craft-butterfly.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-craft-butterfly"
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
        "filename": "paper-craft-butterfly.webp",
        "prompt": (
            "A finished handmade paper craft butterfly displayed flat on a white craft table. "
            "The butterfly has two large accordion-folded construction paper wings in bright pink and purple "
            "decorated with watercolor dot patterns and swirls. A small rolled paper tube forms the body. "
            "Two curled metallic gold pipe cleaner antennae extend from the top. "
            "Two small googly eyes on the body. "
            "A few colorful paper scraps and a glue stick visible at the edges of the frame. "
            "Cheerful, colorful, clearly handmade by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-butterfly-why-kids-love.webp",
        "prompt": (
            "A mom and a young child aged 4 sitting together at a light wood craft table, "
            "smiling and looking at colorful construction paper sheets and pipe cleaners spread out in front of them. "
            "The table shows the beginning of a paper butterfly craft: colored paper, scissors, and a glue stick. "
            "Warm window light. Cozy and joyful family moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-butterfly-cut-wings.webp",
        "prompt": (
            "A sheet of bright pink construction paper folded in half on a white craft table. "
            "A pencil-drawn butterfly wing shape is visible on the top layer. "
            "A pair of child-safe blunt scissors sits next to the folded paper. "
            "A few colorful construction paper sheets visible at the edge. "
            "Flat lay, clear and simple composition, natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-butterfly-decorate-wings.webp",
        "prompt": (
            "A young child's hands painting colorful polka dot patterns on two large paper butterfly wing shapes "
            "using a small watercolor paint set. The wings are laid out flat on a white craft table. "
            "Bright colors: orange, yellow, and purple dots on pink paper wings. "
            "A small water cup, paintbrush, and open watercolor paint palette visible nearby. "
            "Cheerful and messy in a cute way. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-butterfly-folded-wings.webp",
        "prompt": (
            "Two paper butterfly wings folded in a tight accordion fan pattern on a white craft table. "
            "The wings have colorful painted dots and swirls visible between the folds. "
            "One wing is fully folded and fanned out, the other is partially folded showing the process. "
            "The accordion folds create a beautiful layered, feathery texture. "
            "Bright colors, natural light, clean composition. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-butterfly-roll-body.webp",
        "prompt": (
            "A child's hands pinching the center of two accordion-folded colorful paper butterfly wings together "
            "on a white craft table, with a small rolled paper tube body being positioned along the pinched center. "
            "A glue stick and a small strip of paper used to wrap around the center are visible nearby. "
            "The wings fan out on both sides. Craft in progress, warm natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-butterfly-antennae.webp",
        "prompt": (
            "A close-up of two gold metallic pipe cleaners twisted together and bent into antennae shapes, "
            "with small spiral curls at the tips. The antennae are being tucked into the top of a small rolled "
            "paper tube body that is attached to colorful accordion-folded paper butterfly wings on a craft table. "
            "A dab of glue visible at the insertion point. Natural light, warm tones. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-butterfly-finished-detail.webp",
        "prompt": (
            "A close-up of the finished handmade paper craft butterfly's face and upper body. "
            "Two large self-adhesive wiggle googly eyes are stuck to the front of a small rolled paper body tube. "
            "A tiny marker-drawn smile sits below the eyes. "
            "Gold pipe cleaner antennae with curled tips extend above. "
            "Colorful accordion-folded wings visible on both sides, decorated with watercolor dots. "
            "Warm light, clean white table background, charming handmade look. "
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
