#!/usr/bin/env python3
"""Generate all images for ice-cream-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "ice-cream-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

CRAFT_DESCRIPTION = (
    "An ice cream paper craft on a white sheet of cardstock: a tan brown construction "
    "paper triangle cone shape with diagonal criss cross marker lines drawn across it, "
    "a fluffy rounded pink construction paper scoop glued at the top of the cone, "
    "tiny paper sprinkles in red, yellow, blue, and green confetti rectangles glued on the pink scoop, "
    "and a small red paper cherry with a tiny green stem on top of the scoop."
)

IMAGES = [
    {
        "filename": "ice-cream-paper-craft.webp",
        "prompt": (
            f"Finished {CRAFT_DESCRIPTION} "
            "Photographed straight from above on a white craft table with a few "
            "leftover scraps of pink and brown construction paper around the edges, "
            "kid scissors and a purple glue stick visible nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ice-cream-paper-craft-mom-child.webp",
        "prompt": (
            "A happy young American mom and her preschool aged daughter "
            "sitting close together at a white craft table, "
            "smiling and getting ready to start an ice cream paper craft. "
            "On the table in front of them: stacks of colorful construction paper in pink, "
            "tan brown, red, yellow, and blue, a pair of blunt tip kid scissors, "
            "a purple glue stick, broad line markers, and a white sheet of cardstock. "
            "Warm cozy living room atmosphere, eye level photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ice-cream-paper-craft-cut-cone.webp",
        "prompt": (
            "A tan brown construction paper triangle cone shape just cut out by a child, "
            "lying flat on a white craft table next to a pair of blunt tip kid scissors and a pencil. "
            "Beside it sits the larger sheet of brown construction paper with a triangle shaped hole "
            "cut out of it. A few brown paper scraps are scattered on the table. "
            "The cone is pointing downward, like a real ice cream cone, with slightly uneven scissor edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ice-cream-paper-craft-cut-scoop.webp",
        "prompt": (
            "A round fluffy cloud shaped pink construction paper scoop, just cut out by a child, "
            "lying flat on a white craft table next to the brown paper triangle cone from the previous step. "
            "The pink scoop is shaped like a soft bumpy cloud with three little curves on top. "
            "Pink paper scraps and a pair of blunt tip kid scissors visible around the edges. "
            "The cone shape and the pink scoop sit side by side, ready to be assembled. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ice-cream-paper-craft-glue-cone.webp",
        "prompt": (
            "A white sheet of cardstock laid flat on a white craft table with the tan brown paper "
            "triangle cone now glued at the bottom center of the white cardstock background, "
            "with the cone pointing downward. A purple glue stick lies open beside the cardstock. "
            "The pink fluffy paper scoop is still loose on the table next to the cardstock, "
            "waiting to be glued in the next step. Slightly uneven cone, clearly child made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ice-cream-paper-craft-glue-scoop.webp",
        "prompt": (
            "A white cardstock with the tan brown paper triangle cone glued at the bottom center "
            "and now the round fluffy pink construction paper scoop also glued directly above the cone, "
            "where the wide top of the cone meets the rounded bottom of the pink scoop. "
            "The whole ice cream shape is taking form on the white cardstock, "
            "but no sprinkles or cherry yet. Purple glue stick visible nearby on the white craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ice-cream-paper-craft-add-criss-cross.webp",
        "prompt": (
            "A close up of a paper ice cream craft on white cardstock: tan brown paper cone glued at "
            "the bottom with diagonal criss cross marker lines now drawn across the cone in dark brown marker, "
            "creating a classic waffle cone pattern. Pink fluffy paper scoop glued above the cone. "
            "A dark brown broad line marker rests beside the cardstock on a white craft table. "
            "Slightly wobbly handmade marker lines, charming and clearly child drawn. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ice-cream-paper-craft-add-sprinkles.webp",
        "prompt": (
            "A paper ice cream craft on white cardstock: tan brown paper waffle cone with criss cross "
            "marker lines, pink fluffy paper scoop on top, and now ten to fifteen tiny paper rectangle "
            "sprinkles in red, yellow, blue, and green glued randomly across the pink scoop. "
            "Each sprinkle is a small colorful confetti shape pointing in a different direction. "
            "Tiny colorful paper scraps scattered on the white craft table around the cardstock. "
            "Purple glue stick lying open beside the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ice-cream-paper-craft-finished.webp",
        "prompt": (
            f"The finished ice cream paper craft on white cardstock: {CRAFT_DESCRIPTION} "
            "Held up by small child hands at a white craft table with warm window light, "
            "showing off the completed sweet handmade ice cream cone. The paper craft is proudly displayed. "
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
