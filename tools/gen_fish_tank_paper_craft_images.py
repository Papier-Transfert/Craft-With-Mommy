#!/usr/bin/env python3
"""Generate all images for fish-tank-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "fish-tank-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper and cardstock only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

# Critical continuity note: the craft is a FLAT paper collage, not a 3D model.
FLAT = (
    "This craft is a FLAT paper collage on a single flat sheet, lying flat on the table "
    "and photographed from directly above. It is NOT a three-dimensional box, NOT a standing "
    "aquarium, NOT a shoebox tank, NOT a framed shadow box, and NOT a folded greeting card. "
    "It is just flat construction paper shapes glued onto a flat light blue paper rectangle "
    "that has a thin dark blue paper border around it. "
)

IMAGES = [
    {
        "filename": "fish-tank-paper-craft.webp",
        "prompt": (
            "A finished handmade paper fish tank craft made from a light blue cardstock rectangle "
            "framed by a thin dark blue construction paper border like the edge of a glass aquarium. "
            "Inside: a tan paper sand strip along the bottom with small colored paper pebbles, "
            "tall wavy green paper seaweed standing up, and four bright paper fish in orange, yellow, "
            "pink, and purple, each fish a simple oval body with a triangle tail and a googly eye. "
            "Small white marker bubble dots rise from the fish. Lying flat on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fish-tank-paper-craft-mom-child.webp",
        "prompt": (
            "A young mother and her happy preschool child sitting together at a light wood craft table, "
            "smiling as they make a paper fish tank craft. On the table are sheets of light blue cardstock, "
            "colorful construction paper, a glue stick, child-safe scissors, and a few cut paper fish shapes. "
            "The child holds a small bright orange paper fish. Warm, loving shared moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fish-tank-paper-craft-blue-water-background.webp",
        "prompt": (
            "Step one of a paper fish tank craft: a plain light blue cardstock rectangle glued onto a "
            "slightly larger dark blue construction paper sheet so a thin dark border frames it like the "
            "edge of a glass aquarium. Nothing else added yet, just the empty blue water background. "
            "Lying flat on a light wood craft table next to a glue stick and child-safe scissors. "
            f"{FLAT}{STYLE}"
        ),
    },
    {
        "filename": "fish-tank-paper-craft-sand-pebbles.webp",
        "prompt": (
            "Step two of a paper fish tank craft: the light blue cardstock tank with a dark blue paper "
            "border now has a wavy tan paper strip glued along the bottom for sand, with several small "
            "round colored paper pebble dots glued on the sand. No fish or seaweed yet. "
            "Lying flat on a light wood craft table. Clearly child-made and slightly imperfect. "
            f"{FLAT}{STYLE}"
        ),
    },
    {
        "filename": "fish-tank-paper-craft-green-seaweed.webp",
        "prompt": (
            "Step three of a paper fish tank craft, photographed from directly above, lying flat on a "
            "light wood table. A flat light blue paper rectangle with a thin dark blue paper border, "
            "a wavy tan paper sand strip along the bottom with small colored paper pebble dots, and now "
            "three tall wavy green construction paper seaweed strips glued so they stand up from the sand "
            "and reach toward the top. No fish yet. Only flat paper shapes glued on the flat blue sheet. "
            f"{FLAT}{STYLE}"
        ),
    },
    {
        "filename": "fish-tank-paper-craft-cut-paper-fish.webp",
        "prompt": (
            "Step four of a paper fish tank craft, photographed from directly above on a light wood table. "
            "Four bright flat paper fish, freshly cut and lying loose, not yet glued down. Each fish is a "
            "simple oval body in orange, yellow, pink, or purple construction paper with a small triangle "
            "tail and one googly eye stuck on. Beside them sits the FLAT blue paper tank rectangle with a "
            "dark blue paper border, a tan paper sand strip with pebbles, and tall wavy green paper seaweed, "
            "lying flat and waiting for the fish. Child-safe scissors and paper scraps nearby. "
            f"{FLAT}{STYLE}"
        ),
    },
    {
        "filename": "fish-tank-paper-craft-glue-fish.webp",
        "prompt": (
            "Step five of a paper fish tank craft, photographed from directly above, lying flat on a light "
            "wood table. A flat light blue paper rectangle with a thin dark blue paper border, a tan paper "
            "sand strip with colored pebbles along the bottom, and tall wavy green paper seaweed. Now four "
            "bright flat paper fish in orange, yellow, pink, and purple are glued inside, arranged swimming "
            "among the seaweed, each with a googly eye. No bubbles yet and no marker smiles yet. "
            "Only flat paper shapes glued on the flat blue sheet. "
            f"{FLAT}{STYLE}"
        ),
    },
    {
        "filename": "fish-tank-paper-craft-finished-bubbles.webp",
        "prompt": (
            "The finished paper fish tank craft: light blue cardstock tank with a dark blue paper border, "
            "tan sand strip with pebbles along the bottom, tall wavy green seaweed, and four bright paper "
            "fish in orange, yellow, pink, and purple with googly eyes swimming inside. Small white marker "
            "bubble dots rise up from the fish toward the top of the tank. Tiny marker smiles on the fish. "
            "Lying flat on a light wood craft table. Happy, complete, clearly child-made. "
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
