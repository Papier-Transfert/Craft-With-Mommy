#!/usr/bin/env python3
"""Generate all images for paper-craft-egg.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-craft-egg"
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
        "filename": "paper-craft-egg.webp",
        "prompt": (
            "A finished handmade paper craft egg displayed on a light wood craft table. "
            "The egg shape is cut from white cardstock and decorated with small colorful "
            "construction paper squares glued in horizontal stripes: a row of pink, a row of "
            "yellow, a row of light blue, a row of mint green, and a row of orange. "
            "Small marker dots and zigzag patterns add finishing details between the rows. "
            "A loop of thin twine is threaded through a small hole at the top of the egg. "
            "Surrounded by a few extra paper scraps, a glue stick, and kid-safe scissors. "
            "Soft pastel spring color palette, cheerful Easter mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-egg-why-kids-love.webp",
        "prompt": (
            "A warm photo of a young mother and her preschool-aged child sitting together at a "
            "white craft table, both smiling, holding small pieces of colorful construction paper "
            "scraps in pink, yellow, blue, and green. A large white cardstock egg shape sits on "
            "the table between them, partially decorated. A glue stick and kid-safe scissors are "
            "nearby. The mother is gently pointing at the egg, the child looks delighted. "
            "Cozy spring afternoon lighting from a window. Natural family moment, warm and real. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-egg-cut-shape.webp",
        "prompt": (
            "A large egg shape drawn in pencil on a piece of white cardstock, partially cut out "
            "with kid-safe Fiskars scissors with bright orange handles resting on top of the paper. "
            "About half the egg outline is already cut, the rest still attached to the surrounding "
            "cardstock with the pencil line visible. Small white paper trimmings sit beside the egg. "
            "A pencil rests at the edge of the table. Flat overhead view on a light wood craft surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-egg-paper-scraps.webp",
        "prompt": (
            "Small colorful construction paper squares and rectangles cut into roughly half-inch "
            "pieces, sorted into small piles by color: pink pieces, yellow pieces, light blue pieces, "
            "mint green pieces, and orange pieces. The piles sit on a light wood craft table next to "
            "the white cardstock egg shape (now fully cut out and blank). A pair of kid-safe scissors "
            "with bright orange handles rests at the edge of the photo. Charming handmade preparation "
            "for a colorful paper craft. Flat overhead view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-egg-arranging.webp",
        "prompt": (
            "A child's small hand placing a small pink construction paper square onto a blank white "
            "cardstock egg shape on a light wood craft table. About one third of the egg is already "
            "loosely arranged with small colorful paper squares in horizontal stripes (one row of pink, "
            "starting a row of yellow). The pieces are not yet glued down, just resting in position. "
            "Small piles of yellow, blue, green, and orange paper squares sit beside the egg ready to "
            "be added. Warm cozy lighting. Flat overhead view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-egg-glued-pattern.webp",
        "prompt": (
            "A white cardstock egg shape now fully decorated with small colorful construction paper "
            "squares glued down in five neat horizontal stripes from top to bottom: a row of pink, a "
            "row of yellow, a row of light blue, a row of mint green, and a row of orange. The pieces "
            "are slightly imperfect and clearly placed by a child. An open Elmer's purple glue stick "
            "with the cap off rests beside the egg on a light wood craft table. Some leftover paper "
            "squares scattered around. Flat overhead view, cheerful spring colors. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-egg-marker-details.webp",
        "prompt": (
            "The same colorful paper craft egg with five horizontal stripes of pink, yellow, blue, "
            "green, and orange paper squares, now with finishing details added by markers: small "
            "white marker dots between the colored squares, tiny zigzag lines along the edges of some "
            "rows, and small heart shapes drawn in the center of a few squares. A handful of bright "
            "Crayola Super Tips washable markers in various colors lie next to the egg on a light wood "
            "craft table. Charming, slightly imperfect handmade decoration. Flat overhead view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-egg-hanging.webp",
        "prompt": (
            "The finished paper craft egg with five colorful horizontal stripes (pink, yellow, blue, "
            "green, orange) hanging from a thin natural twine loop threaded through a small hole "
            "punched at the top. A small metal single-hole punch with blue grip handles sits on a "
            "light wood craft table below the hanging egg. The egg is hanging against a soft white "
            "background, slightly turning, ready to be displayed. Cheerful, handmade, springtime feel. "
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
