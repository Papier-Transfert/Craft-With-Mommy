#!/usr/bin/env python3
"""Generate all images for paper-crown-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-crown-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table or white surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-crown-craft.webp",
        "prompt": (
            "A finished handmade paper crown craft lying flat on a light wood craft table. "
            "The crown is made from a long strip of bright purple cardstock with a row of "
            "triangular points cut along the top. The surface is decorated with colorful "
            "marker stripes and polka dots, shiny metallic gold circles and star shapes "
            "glued to the front, and several self-adhesive gem stickers in pink, blue, and "
            "green pressed across it. One large round gem sits in the center point. "
            "The crown is closed into a loop. A few marker pens, a glue stick, and paper "
            "scraps are visible at the edges of the frame. Charming and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crown-craft-why-kids-love.webp",
        "prompt": (
            "A warm, realistic photo of a young mom and her young child sitting together "
            "at a light wood craft table, smiling as they prepare to make a paper crown "
            "craft. On the table in front of them are sheets of bright purple and gold "
            "cardstock, a sheet of colorful gem stickers, a glue stick, blunt-tip kid "
            "scissors, and a few broad-line markers. Natural daylight from a window, cozy "
            "home atmosphere. The mom is helping the child look at the materials. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crown-cut-strip.webp",
        "prompt": (
            "A long rectangular strip of bright purple cardstock about 4 inches tall and "
            "24 inches long, cut neatly and lying flat on a light wood craft table. "
            "Next to the strip are a wooden ruler, a yellow pencil, and a pair of "
            "blunt-tip kid scissors. A few small purple paper scraps sit near the "
            "edges. The strip has a straight, clean top edge with no points yet. "
            "Clean, simple composition. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crown-cut-points.webp",
        "prompt": (
            "The same long purple cardstock strip now with the top edge cut into a neat "
            "row of triangular crown points. About eight to ten pointed peaks along the "
            "top, each roughly 2 inches tall with small valleys between them. The bottom "
            "edge of the strip remains straight. The strip lies flat on a light wood "
            "craft table. Small purple paper triangle scraps from the cutting are "
            "scattered next to the strip. Blunt-tip kid scissors rest beside it. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crown-decorate-markers.webp",
        "prompt": (
            "A child's small hand holding a bright orange broad-line marker, drawing "
            "colorful stripes, polka dots, and small stars across a purple cardstock "
            "crown strip with triangular points along the top. The strip lies flat on a "
            "light wood craft table. Several other broad-line markers in red, yellow, "
            "green, and blue are scattered nearby, along with a few colored construction "
            "paper scraps. Colorful marker pattern covers part of the crown already. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crown-gold-accents.webp",
        "prompt": (
            "A purple paper crown strip with triangular points along the top, already "
            "decorated with colorful marker stripes and dots, now with about eight small "
            "shiny metallic gold paper shapes glued on the front: small gold circles, "
            "gold star shapes, and gold diamond shapes. The gold shapes are spaced evenly "
            "across the decorated surface. A glue stick and gold cardstock scraps sit "
            "beside the crown on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crown-add-gems.webp",
        "prompt": (
            "The decorated purple paper crown strip with marker patterns and gold paper "
            "accents, now also covered with colorful self-adhesive gem stickers: pink, "
            "blue, green, and clear round rhinestone gems pressed onto the crown, with "
            "one large round gem in the center. A child's finger is pressing a small "
            "pink gem onto the crown. A sheet of peel-and-stick gem stickers sits next "
            "to the crown on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crown-fit-size.webp",
        "prompt": (
            "A mom gently wrapping a decorated paper crown strip around her young "
            "child's head to measure the fit. The crown has triangular points, marker "
            "decorations, gold paper accents, and colorful gem stickers. The mom holds "
            "a yellow pencil and is marking the overlap spot on the crown where the "
            "two ends meet. The child is standing still and smiling slightly. Warm, "
            "cozy home setting with natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crown-finished-wearing.webp",
        "prompt": (
            "A smiling young child, around 4 or 5 years old, wearing the finished "
            "handmade paper crown on their head. The crown is bright purple with "
            "triangular points, colorful marker patterns, shiny gold paper shapes, and "
            "sparkling gem stickers. The child looks proud and happy, standing in a warm "
            "cozy room with soft natural daylight. A craft table with a few leftover "
            "paper scraps and markers is slightly visible in the background. "
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
