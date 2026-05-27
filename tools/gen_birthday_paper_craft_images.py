#!/usr/bin/env python3
"""Generate all images for birthday-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "birthday-paper-craft"
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
    "Charming and slightly imperfect, clearly handmade by a child. Pinterest-worthy. "
    "The photo fills the whole frame edge to edge with no white borders, no padding, no letterboxing."
)

IMAGES = [
    {
        "filename": "birthday-paper-craft.webp",
        "prompt": (
            "A finished sparkly handmade paper birthday crown made from gold cardstock "
            "with five tall zigzag triangle points across the top. The middle band of the crown "
            "is decorated with two horizontal strips of pretty pink floral washi tape. "
            "Five small colorful construction paper jewel shapes (oval and diamond) in pink, blue, "
            "green, purple, and yellow are glued in a row between the washi tape stripes, each topped "
            "with a shiny round self-adhesive rhinestone gem sticker. A child's name written in big "
            "bouncy bright pink marker across the front center. A tiny fluffy pom pom in red, yellow, "
            "blue or pink glued to the top tip of each zigzag point. The crown is laid flat on a "
            "light wood craft table. Hero shot of the finished birthday paper craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "birthday-paper-craft-mom-child.webp",
        "prompt": (
            "A warm cozy photo of a smiling mom in her early thirties and a young child around "
            "five years old sitting side by side at a light wood craft table. On the table in front "
            "of them are sheets of gold and bright yellow cardstock, several colorful rolls of washi tape, "
            "a sheet of self-adhesive rhinestone gem stickers, a small clear container of tiny pom poms, "
            "kid scissors, a glue stick, and Crayola broad line markers. Both are looking down at the "
            "supplies with happy excited expressions, ready to start a birthday crown craft together. "
            "Soft natural window light. Warm family bonding atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "birthday-paper-craft-cut-strip.webp",
        "prompt": (
            "One long plain rectangle strip of gold cardstock about four inches tall and twenty inches "
            "wide laid out perfectly flat on a light wood craft table. Next to the gold strip are a pair "
            "of red kid scissors, a yellow pencil, and a clear plastic ruler. No decorations on the strip "
            "yet, just a clean simple gold rectangle ready to become a birthday paper crown. "
            "Top-down flat lay angle. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "birthday-paper-craft-zigzag-points.webp",
        "prompt": (
            "The same long gold cardstock strip now with a clean zigzag of five tall triangle points "
            "cut along the top edge to look like the classic crown shape. The bottom edge is still "
            "straight. Each triangle point is about two inches tall and two inches wide, slightly uneven "
            "in a charming child-made way. The crown strip is laid flat on a light wood craft table next "
            "to red kid scissors and a yellow pencil. No washi tape or decorations yet. Top-down flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "birthday-paper-craft-washi-tape.webp",
        "prompt": (
            "The gold zigzag paper crown with five triangle points along the top now decorated with two "
            "horizontal strips of pretty washi tape running across the middle band from one short end "
            "to the other. One strip is pink with tiny white florals, the other is rose gold with thin "
            "stripes. No jewels, no gems, no pom poms yet, just the gold crown with two washi tape "
            "stripes. Laid flat on a light wood craft table next to a few washi tape rolls. Top-down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "birthday-paper-craft-jewels-gems.webp",
        "prompt": (
            "The gold zigzag paper birthday crown decorated with two horizontal washi tape strips, now "
            "also decorated with five small colorful construction paper jewel shapes glued in a row "
            "between the washi tape stripes: a pink oval, a blue diamond, a green oval, a purple diamond, "
            "and a yellow oval. Each paper jewel has a shiny self-adhesive round rhinestone gem sticker "
            "pressed in its center, catching the light. No marker writing yet, no pom poms on the points. "
            "Crown laid flat on a light wood craft table. Top-down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "birthday-paper-craft-name-poms.webp",
        "prompt": (
            "The gold paper birthday crown fully decorated with washi tape stripes, colorful paper jewels "
            "topped with rhinestone gem stickers, the child's name 'Mila' written in big bouncy bright "
            "pink marker across the front center between the washi tape strips, and a small fluffy pom "
            "pom in red, yellow, blue, or pink glued to the very top tip of each zigzag crown point. "
            "Crown laid completely flat on a light wood craft table, viewed from directly above. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "birthday-paper-craft-worn-finished.webp",
        "prompt": (
            "A smiling young child around five years old wearing the finished sparkly handmade paper "
            "birthday crown on their head. The gold cardstock crown has tall zigzag triangle points, "
            "two washi tape stripes across the middle band, colorful paper jewel shapes topped with "
            "shiny gem stickers, the name 'Mila' written in bright pink marker across the front, and "
            "fluffy little pom poms on each point. The child is grinning happily and looking slightly "
            "off camera. Soft cozy living room or kitchen background slightly blurred. Warm natural "
            "light. Happy birthday moment captured. "
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
