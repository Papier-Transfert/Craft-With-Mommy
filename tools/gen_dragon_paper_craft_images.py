#!/usr/bin/env python3
"""Generate all images for dragon-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "dragon-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper, scissors, and glue stick visible. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "dragon-paper-craft.webp",
        "prompt": (
            "A finished handmade paper dragon craft made entirely from construction paper, "
            "lying flat on a white craft table. The dragon has a long curvy S-shaped green "
            "construction paper body, a row of yellow zigzag triangular spikes glued along "
            "its back from head to tail, a rounded green head with a small snout, two large "
            "googly eyes glued on top of the head, two small black marker nostril dots on the snout, "
            "two purple bat-style wings glued to the middle of the body, four short stubby green "
            "legs along the underside, and small red, orange, and yellow layered paper flames "
            "glued in front of the snout to look like the dragon is breathing fire. "
            "Slightly wonky and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dragon-paper-craft-why-kids-love.webp",
        "prompt": (
            "A warm overhead photo of an American mom and her young child sitting together at a "
            "white craft table, smiling and starting a paper dragon craft project. Sheets of green, "
            "yellow, purple, red, and orange construction paper are laid out, along with a glue stick, "
            "kids' safety scissors, and a small box of self-adhesive googly eyes. The child is holding "
            "a piece of green construction paper, looking excited. Cozy, family-friendly atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dragon-paper-craft-body-shape.webp",
        "prompt": (
            "A long curvy S-shaped dragon body shape cut from green construction paper, "
            "lying flat on a white craft table. The shape looks like a chubby snake curving "
            "across the page, about as long as the page is wide, with slightly wobbly hand-cut edges. "
            "Next to the green body sits a pair of children's safety scissors and a pencil with a "
            "faint pencil outline still visible on a leftover green paper scrap. "
            "Just the body shape, no other dragon parts attached yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dragon-paper-craft-back-spikes.webp",
        "prompt": (
            "The same green curvy S-shaped paper dragon body now has a long yellow construction "
            "paper zigzag strip glued along its top edge from head end to tail end, forming a row "
            "of bright triangular back spikes that follow the curve of the body. The dragon does "
            "not yet have a head, eyes, wings, legs, or flames attached. Sitting flat on a white "
            "craft table next to a glue stick and small yellow paper scraps. Charming child-made look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dragon-paper-craft-head-snout.webp",
        "prompt": (
            "The same paper dragon project now has a rounded green construction paper head with "
            "a small protruding snout glued to one end of the curvy green body. The yellow zigzag "
            "back spikes still run along the top of the body. There are no eyes, nostrils, wings, "
            "legs, or flames yet. The head shape is slightly imperfect and clearly hand cut. "
            "Lying flat on a white craft table next to a glue stick and green paper scraps. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dragon-paper-craft-eyes-nostrils.webp",
        "prompt": (
            "The same paper dragon now has two large self-adhesive googly eyes pressed onto the "
            "top of the green head and two small black marker nostril dots drawn on the snout. "
            "The dragon body is curvy green construction paper with a yellow zigzag back spike strip "
            "running along its top from head to tail. There are still no wings, legs, or flames "
            "attached. Sitting flat on a white craft table. Friendly cute expression on the face. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dragon-paper-craft-wings.webp",
        "prompt": (
            "The same paper dragon now has two purple construction paper bat-style wings glued "
            "to the middle of its curvy green body, spreading outward and slightly overlapping the "
            "yellow zigzag back spikes. The dragon already has a green head with a snout, two googly "
            "eyes, and two black marker nostril dots, but still has no legs or flames attached. "
            "Sitting flat on a white craft table next to small purple paper scraps and a glue stick. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dragon-paper-craft-legs-feet.webp",
        "prompt": (
            "The same paper dragon now has four small green construction paper legs glued along "
            "the underside of its curvy body, two near the front and two near the back, each ending "
            "in a softly rounded little foot. The dragon already has a green head with snout, googly "
            "eyes, marker nostrils, yellow zigzag back spikes, and two purple bat-style wings, but "
            "still has no flames in front of its mouth yet. Sitting flat on a white craft table "
            "next to green paper scraps. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dragon-paper-craft-fire-flames.webp",
        "prompt": (
            "The completely finished friendly paper dragon now has small layered flame shapes cut "
            "from red, orange, and yellow construction paper glued in front of its snout, looking "
            "like it is breathing fire. Each flame has a yellow center inside an orange flame inside "
            "a red flame. The dragon has a curvy green body, a row of yellow zigzag back spikes, a "
            "green head with snout, two googly eyes, marker nostril dots, two purple bat-style wings, "
            "and four short green legs with rounded feet. Lying flat on a white craft table next to "
            "small red, orange, and yellow paper flame scraps and a glue stick. Charming child-made "
            "fire-breathing dragon, complete and ready to display. "
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
