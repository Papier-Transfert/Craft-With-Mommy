#!/usr/bin/env python3
"""Generate all images for octopus-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "octopus-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper, real scissors, real glue stick. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "octopus-paper-craft.webp",
        "prompt": (
            "A finished handmade paper octopus craft made from purple construction paper. "
            "It has a round purple paper head, two large googly eyes glued near the top, "
            "a small black marker smile drawn beneath the eyes, and eight long curled "
            "purple paper tentacle strips fanning outward below the head, each spiral "
            "tightly curled. Tiny pink marker dots run along each tentacle as suction cups. "
            "Lying flat on a light wood craft table with a few purple paper scraps and a "
            "glue stick visible at the edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "octopus-paper-craft-why-kids-love.webp",
        "prompt": (
            "A warm scene of a young mother and her 5 year old child sitting side by side "
            "at a light wood craft table, both smiling, ready to make a paper octopus. "
            "On the table in front of them: sheets of purple construction paper, a pair of "
            "blue safety scissors, a glue stick, a small bowl of googly eyes, and a black marker. "
            "The mom is gently guiding the child. Natural daylight, cozy home kitchen vibe, "
            "real handmade craft moment, no finished octopus yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "octopus-paper-craft-cut-head.webp",
        "prompt": (
            "A close up of a child's small hands carefully cutting a round circle from a sheet "
            "of purple construction paper using blue blunt tip safety scissors. The traced pencil "
            "circle is faintly visible on the paper. The cut circle is partly free and the rest "
            "is still attached. A pencil and a small bowl used for tracing sit nearby on the light "
            "wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "octopus-paper-craft-cut-tentacles.webp",
        "prompt": (
            "A flat lay on a light wood craft table showing eight long thin purple construction "
            "paper strips arranged in a neat row, each strip about half an inch wide and several "
            "inches long, freshly cut. Next to the strips sits the round purple paper head circle "
            "from the previous step, plus blue safety scissors and a yellow pencil. No octopus "
            "is assembled yet, only the cut pieces. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "octopus-paper-craft-curled-tentacles.webp",
        "prompt": (
            "A flat lay on a light wood craft table showing eight tightly spiral-curled purple "
            "construction paper tentacle strips, each one coiled like a tiny spring after being "
            "wrapped around a pencil and released. They sit in a loose group next to the round "
            "purple paper head circle and a yellow pencil. The curls vary slightly in tightness, "
            "clearly made by a child. No octopus is assembled yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "octopus-paper-craft-glued-tentacles.webp",
        "prompt": (
            "A handmade purple paper octopus on a light wood craft table, viewed from above. "
            "A round purple paper head with eight curled purple paper tentacle strips glued "
            "along the bottom edge of the head, fanning out evenly to the left and right "
            "like an octopus body. The tentacles are tightly spiral-curled. The face is still "
            "blank, no eyes or smile yet. A glue stick sits open beside the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "octopus-paper-craft-googly-eyes.webp",
        "prompt": (
            "A handmade purple paper octopus on a light wood craft table, viewed from above. "
            "Two large round black and white googly eyes are stuck onto the front of the round "
            "purple head, slightly above center and spaced about an inch apart. Eight curled "
            "purple paper tentacle strips fan out beneath the head. No smile or suction cup "
            "dots yet, just the eyes added. A small packet of googly eyes sits at the edge. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "octopus-paper-craft-finished.webp",
        "prompt": (
            "The completed handmade purple paper octopus craft on a light wood craft table, "
            "viewed from above. Round purple paper head with two large googly eyes, a small "
            "curved black marker smile drawn beneath the eyes, and eight tightly curled purple "
            "paper tentacles fanning outward below. Small pink marker dots run along each "
            "tentacle as suction cups. A pink fine line marker and a black marker rest beside "
            "the craft. The finished octopus looks cheerful and clearly child-made. "
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
