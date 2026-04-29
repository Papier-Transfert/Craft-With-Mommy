#!/usr/bin/env python3
"""Generate all images for foil-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "foil-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood or white craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "foil-paper-craft.webp",
        "prompt": (
            "A finished handmade foil paper craft fish made from blue cardstock, "
            "completely covered in overlapping shiny metallic foil paper scales in silver, "
            "gold, pink, and aqua blue colors. The fish has a sparkly metallic foil tail and "
            "two foil triangle fins on top and bottom. A small black googly eye and a tiny smile. "
            "Lying flat on a white craft table with a few extra foil paper sheets and scraps "
            "around the edges. The metallic scales catch the warm daylight beautifully. "
            "Clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "foil-paper-craft-mom-child.webp",
        "prompt": (
            "A young American mom and her preschool-aged child sitting together at a white craft table, "
            "smiling and getting ready to start a foil paper craft. On the table in front of them are "
            "sheets of shiny metallic foil paper in silver, gold, pink, and blue, blue construction paper, "
            "child-safe scissors, and a glue stick. Warm, cozy daylight from a side window. "
            "Both look engaged and happy, clearly excited to begin. Realistic family moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "foil-paper-craft-cut-fish-body.webp",
        "prompt": (
            "Close-up of a child's small hands using kid-safe blunt-tip scissors to cut out a simple "
            "oval-shaped fish body from a sheet of blue cardstock for a foil paper craft. "
            "A pencil sketch line is faintly visible along the cut edge. The fish body shape is about "
            "six inches long with a slight point at the front for the mouth and a flat back where the tail "
            "will attach later. Pencil and a few foil paper sheets visible at the edges of the table. "
            "Clear, focused, instructional photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "foil-paper-craft-cut-foil-squares.webp",
        "prompt": (
            "A small colorful pile of freshly cut one-inch squares of metallic foil paper in silver, "
            "gold, pink, and aqua blue. About thirty squares are arranged in a loose pile next to "
            "kid-safe scissors and a few full sheets of metallic foil paper on a white craft table. "
            "The squares clearly catch the daylight and shimmer. Each square is slightly imperfect, "
            "showing it was cut by a child. Bright cheerful flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "foil-paper-craft-glue-shiny-scales.webp",
        "prompt": (
            "A child's small hands using a purple glue stick to stick a shiny silver metallic foil paper "
            "square onto a blue cardstock fish body. About half of the fish body is already covered with "
            "overlapping foil paper squares in silver, gold, pink, and aqua blue arranged in shingled rows "
            "from the tail end forward. The remaining half of the fish body is still bare blue paper. "
            "The scales catch the daylight beautifully. A few extra foil squares scattered around. "
            "Clear, instructional in-progress photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "foil-paper-craft-add-tail-fins.webp",
        "prompt": (
            "A blue cardstock fish body fully covered with overlapping shiny metallic foil paper scales "
            "in silver, gold, pink, and aqua blue. A bright pink metallic foil paper triangle tail with "
            "a soft V-cut at the wide end is freshly glued at the back. Two smaller gold foil paper "
            "triangle fins are glued on top and bottom of the body. No googly eye yet. "
            "Lying flat on a white craft table. The shiny scales reflect the warm daylight. "
            "Clearly handmade by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "foil-paper-craft-add-eye-details.webp",
        "prompt": (
            "A finished sparkly foil paper craft fish with overlapping silver, gold, pink, and aqua blue "
            "metallic foil scales, a pink foil tail, and two gold foil fins. A small black googly eye is "
            "stuck near the front of the fish, with a tiny black marker smile drawn just below it. "
            "A few small marker bubbles and tiny sparkle stars drawn on the white craft table around "
            "the fish, showing finishing touches. Bright daylight, charming handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "foil-paper-craft-finished-display.webp",
        "prompt": (
            "A finished sparkly foil paper craft fish taped to a sunny window. The metallic foil scales "
            "in silver, gold, pink, and aqua blue clearly catch the afternoon sunlight and shimmer. "
            "The fish has a googly eye, a smiling mouth, a pink foil tail, and gold foil fins. "
            "Through the window soft daylight streams in, and a hint of greenery is visible outside. "
            "Cozy, warm, and proudly displayed. Photo taken from inside a home. "
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
