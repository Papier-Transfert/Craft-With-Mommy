#!/usr/bin/env python3
"""Generate all images for leaf-craft-paper.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "leaf-craft-paper"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "Image must fill the entire frame edge to edge. No white borders, "
    "no padding, no letterboxing. Composition fits a 4:3 landscape rectangle naturally."
)

IMAGES = [
    {
        "filename": "leaf-craft-paper.webp",
        "prompt": (
            "A finished handmade paper leaf bouquet on a white cardstock background, "
            "lying flat on a light wood craft table. The bouquet shows three fall paper leaves "
            "fanning out from a thin curved brown construction paper twig: "
            "a red five point maple leaf, an orange wavy lobed oak leaf, and a long yellow "
            "teardrop poplar leaf. Each leaf has hand drawn brown marker veins running down "
            "the center with smaller branching veins, plus tiny colorful marker freckles. "
            "Slightly imperfect cut edges, clearly child made. Close up overhead photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "leaf-craft-paper-mom-child.webp",
        "prompt": (
            "A young American mom in her early thirties and her preschool aged daughter "
            "sitting side by side at a clean white craft table, smiling and excited to start a craft. "
            "On the table: stacks of red, orange, yellow, and brown construction paper sheets, "
            "blunt tip kid scissors with bright handles, a purple Elmer's glue stick, "
            "Crayola broad line markers, a sharpened pencil, and a few real fall leaves "
            "on the side as inspiration. Warm cozy autumn afternoon light from a window. "
            "Wholesome, candid family moment, no craft pieces cut yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "leaf-craft-paper-cut-maple.webp",
        "prompt": (
            "A single freshly cut red construction paper maple leaf shape lying flat on a "
            "white craft table. The leaf has five points: three at the top and two smaller "
            "side points, palm sized with slightly imperfect child cut edges. "
            "Next to the leaf: a small pile of red paper scraps, a sharpened pencil, "
            "and bright handled blunt tip kid scissors lying open. Overhead close up shot. "
            "Nothing else on the table yet, only the maple leaf and the cutting tools. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "leaf-craft-paper-cut-oak.webp",
        "prompt": (
            "A freshly cut orange construction paper oak leaf shape with wavy rounded lobes "
            "down each side and a small stem at the bottom, lying on a white craft table "
            "right next to the previously cut red paper maple leaf. The orange oak leaf is "
            "slightly longer than the red maple leaf. Around them: orange and red paper scraps, "
            "blunt tip kid scissors, a pencil. Slightly imperfect child cut edges. "
            "Overhead close up shot. Two paper leaves visible, no other leaves yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "leaf-craft-paper-cut-yellow-leaf.webp",
        "prompt": (
            "A long yellow construction paper poplar leaf shape, gently teardrop pointed at "
            "one end and rounded at the other, lying on a white craft table next to a red "
            "paper maple leaf and an orange paper oak leaf. The three paper leaves sit close "
            "together on the table. Yellow paper scraps and blunt tip kid scissors nearby. "
            "Slightly imperfect child cut edges. Overhead close up shot. "
            "Three paper leaves visible, no twig yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "leaf-craft-paper-cut-stem.webp",
        "prompt": (
            "A long thin curved brown construction paper twig with a small Y shape branch "
            "at the top, freshly cut and lying on a white craft table next to the three "
            "previously cut paper leaves: a red maple leaf, an orange oak leaf, and a long "
            "yellow poplar leaf. Brown paper scraps and blunt tip kid scissors nearby. "
            "All four pieces clearly visible and ready to assemble. Overhead close up shot. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "leaf-craft-paper-glued-arrangement.webp",
        "prompt": (
            "A white sheet of cardstock in portrait orientation lying flat on a light wood "
            "craft table. A thin curved brown construction paper twig with a small Y branch at the top "
            "is glued vertically down the middle of the cardstock. A red paper maple leaf, an "
            "orange paper oak leaf, and a long yellow paper poplar leaf are glued so they fan "
            "out from the twig like a small fall bouquet, each leaf overlapping the twig "
            "slightly. The leaves do NOT have any marker veins drawn on them yet, just plain "
            "colored paper. An open purple Elmer's glue stick lying next to the cardstock. "
            "Overhead close up shot. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "leaf-craft-paper-finished.webp",
        "prompt": (
            "A finished handmade paper leaf bouquet held up by small child hands at the edges "
            "of the frame. The white cardstock shows a brown paper twig down the middle with "
            "a red paper maple leaf, an orange paper oak leaf, and a long yellow paper poplar "
            "leaf fanning out from it. Each leaf has hand drawn brown marker veins down the "
            "center with smaller branching veins out to the edges, plus tiny red, orange, and "
            "yellow marker freckles dotted across the leaves. Charming child made result, "
            "slightly imperfect lines. Warm cozy daylight. "
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
