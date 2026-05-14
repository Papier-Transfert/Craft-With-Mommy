#!/usr/bin/env python3
"""Generate all images for paper-scarecrow-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-scarecrow-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-scarecrow-craft.webp",
        "prompt": (
            "A finished handmade paper scarecrow craft lying flat on a light wood craft table. "
            "The scarecrow is made from layered construction paper shapes: a round tan circle face, "
            "a red and orange plaid rectangle shirt body, a wide brown triangle straw hat with a thin "
            "brown hatband, and fluffy yellow paper straw strips poking out from under the hat brim, "
            "from the sleeve cuffs, and from the bottom of the pants. The face has two simple round black "
            "marker eyes, a small black triangle nose, and a stitched curved black smile. "
            "Charming, slightly wonky, and clearly child-made. A few small paper scraps visible nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-scarecrow-craft-mom-child.webp",
        "prompt": (
            "A warm cozy scene of a young American mom and her four year old child sitting together "
            "at a light wood craft table, about to start a paper scarecrow craft. "
            "On the table: stacks of tan, brown, yellow, red, and orange construction paper, "
            "small blue handled kid scissors, a purple glue stick, a single black fine point marker, "
            "and a pencil. Both look happy and ready to start. "
            "Soft natural daylight from a window. Warm autumn family moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-scarecrow-craft-cut-shapes.webp",
        "prompt": (
            "A child's small hands holding small blue handled kid scissors, cutting out a round tan "
            "construction paper circle for a scarecrow face. Next to the hands, a red and orange plaid "
            "construction paper rectangle has just been cut for the scarecrow's shirt body. "
            "Light wood craft table. A pencil and a few tan and plaid paper scraps visible around the work. "
            "Clear focus on the cutting in progress, very beginner-friendly handmade craft scene. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-scarecrow-craft-cut-hat.webp",
        "prompt": (
            "A child's hands cutting a wide brown construction paper triangle for a scarecrow's floppy "
            "straw hat with small blue handled kid scissors. A thin brown paper strip for the hatband "
            "lies next to the triangle. To the side of the work area: the already-cut tan paper circle "
            "face and red and orange plaid paper rectangle shirt body waiting to be assembled. "
            "Light wood craft table with small brown paper scraps. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-scarecrow-craft-cut-straw.webp",
        "prompt": (
            "A child snipping thin yellow construction paper strips, each about two inches long and "
            "very narrow like paper spaghetti, to make scarecrow straw. A small pile of about fifteen "
            "cut yellow strips already gathered next to the child's hands. Also visible on the craft "
            "table: the previously cut tan paper face circle, red and orange plaid shirt rectangle, "
            "and wide brown triangle hat with hatband, all ready for assembly. "
            "Light wood craft surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-scarecrow-craft-assemble-body.webp",
        "prompt": (
            "A child's hands pressing a tan construction paper circle face onto the top of a red and "
            "orange plaid construction paper rectangle shirt body. A wide brown paper triangle hat is "
            "already glued on top of the face, with a thin brown paper hatband strip glued across the "
            "bottom edge of the hat. The assembled scarecrow figure lies flat on a light wood craft "
            "table, no straw added yet. A purple glue stick lying open beside the work. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-scarecrow-craft-add-straw.webp",
        "prompt": (
            "A child's hands carefully pressing small bundles of thin yellow paper straw strips along "
            "the bottom edge of the brown hat brim of a paper scarecrow. The scarecrow already has a "
            "tan circle face glued to a red and orange plaid shirt body and a wide brown triangle hat "
            "with a hatband on top. Additional small clusters of yellow straw strips are also glued at "
            "the bottom corners of the shirt sleeves and at the bottom of the pants area. No face drawn "
            "yet. Light wood craft table, purple glue stick beside the work. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-scarecrow-craft-finished-face.webp",
        "prompt": (
            "A finished handmade paper scarecrow craft displayed on the front of a refrigerator with "
            "a small magnet, next to two child-drawn paper pumpkins and a few paper fall leaves. "
            "The scarecrow has a tan round face with two simple black marker round eyes, a small black "
            "triangle nose, and a stitched curved black smile. The body is a red and orange plaid "
            "paper rectangle, the hat is a wide brown triangle with a thin brown hatband, "
            "and fluffy yellow paper straw strips poke out from under the hat brim, sleeve cuffs, "
            "and pant legs. A small colored patch is drawn on the shirt. "
            "Cozy autumn family kitchen scene. "
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
