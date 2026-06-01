#!/usr/bin/env python3
"""Generate all images for paper-poppy-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-poppy-craft"
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
        "filename": "paper-poppy-craft.webp",
        "prompt": (
            "A finished handmade paper poppy flower craft lying on a white craft table. "
            "It has bright red construction paper petals curled upward into a rounded cupped bloom, "
            "a fuzzy round black pom pom in the center with tiny black marker seed dots around it, "
            "and a green pipe cleaner stem with two pointed green paper leaves. "
            "A few red and green paper scraps and a glue stick visible at the edges. "
            "Clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poppy-craft-mom-child.webp",
        "prompt": (
            "A mom and her young child sitting together at a light wood craft table, smiling, "
            "about to start a paper poppy craft. On the table are sheets of red, black, and green "
            "construction paper, a black pom pom, a green pipe cleaner, kid-safe scissors, "
            "and a purple glue stick. Warm, happy, cozy family moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poppy-craft-cut-petals.webp",
        "prompt": (
            "Two flat flower shapes cut from bright red construction paper, each with four or five "
            "rounded petals like a simple clover shape, one slightly larger than the other, "
            "lying side by side on a white craft table. A pair of blunt-tip kid scissors and a few "
            "red paper scraps next to them. The cut edges are slightly uneven, clearly cut by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poppy-craft-cupped-petals.webp",
        "prompt": (
            "Two red construction paper flower shapes stacked and glued together, with all the petals "
            "curled gently upward to form a rounded, cupped poppy bloom. The smaller flower sits on top "
            "with its petals offset between the bottom petals. A yellow pencil lies beside it, used for "
            "curling the petals. No black center yet. On a white craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poppy-craft-black-center.webp",
        "prompt": (
            "A cupped red paper poppy bloom with a fuzzy round black pom pom glued firmly into the center, "
            "and a ring of small black marker seed dots drawn on the red paper around the base of the pom pom. "
            "A black broad-line marker rests next to it. Close flat lay on a white craft table. "
            "Bright red petals and bold black center, classic poppy look, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poppy-craft-green-stem.webp",
        "prompt": (
            "The back of a finished red paper poppy flower with a black pom pom center, "
            "showing a green pipe cleaner stem laid against the back and held in place with a piece of tape "
            "and a small green paper square glued over the join. The flower lies face-down then turned "
            "to show the stem attached. On a light wood craft table with a tape roll nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poppy-craft-green-leaves.webp",
        "prompt": (
            "A finished red paper poppy with a black pom pom center and a green pipe cleaner stem, "
            "now with two long pointed green construction paper leaves attached partway down the stem. "
            "The leaves have a few small notches snipped along the edges. Lying on a white craft table "
            "with green paper scraps and scissors beside it. Clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poppy-craft-finished-display.webp",
        "prompt": (
            "A finished handmade paper poppy craft standing upright in a small clear glass jar on a "
            "bright windowsill. The poppy has bright red cupped construction paper petals, a fuzzy black "
            "pom pom center with marker seed dots, a green pipe cleaner stem, and two pointed green paper leaves. "
            "Soft natural daylight, cheerful and cozy. Clearly child-made and proudly displayed. "
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
