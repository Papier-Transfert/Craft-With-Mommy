#!/usr/bin/env python3
"""Generate all images for paper-campfire-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-campfire-craft"
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
        "filename": "paper-campfire-craft.webp",
        "prompt": (
            "A finished handmade paper campfire craft on a white craft table: "
            "three or four rolled brown construction paper logs stacked in a crisscross, "
            "with tall layered paper flames standing up in the center, "
            "a big red flame in back, an orange flame in the middle, and a small yellow flame in front. "
            "A few small gray paper rocks arranged in a ring around the base. "
            "Clearly made by a child, slightly imperfect and charming. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-campfire-craft-mom-child.webp",
        "prompt": (
            "A mom and her young child sitting together at a light wood craft table, "
            "smiling, with sheets of red, orange, yellow, and brown construction paper, "
            "child-safe scissors, a glue stick, and markers spread out in front of them, "
            "ready to start making a paper campfire craft. "
            "Warm, joyful shared moment between mother and child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-campfire-craft-cut-flames.webp",
        "prompt": (
            "Three layered paper flame shapes freshly cut from red, orange, and yellow "
            "construction paper, with wavy pointed tops, stacked from largest red in back "
            "to smallest yellow in front. Lying flat on a white craft table next to "
            "blunt-tip child scissors and paper scraps. Clearly cut by a child, slightly uneven edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-campfire-craft-rolled-logs.webp",
        "prompt": (
            "Three or four brown construction paper rectangles each rolled into a tube-shaped log "
            "about as thick as a marker, with a piece of clear tape holding each seam closed. "
            "The paper logs are lying in a small pile on a light wood craft table. "
            "Clearly handmade by a child, tubes slightly uneven. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-campfire-craft-log-bark.webp",
        "prompt": (
            "A child's hand using a brown marker to draw short bark lines along a rolled "
            "brown paper log, with small ring circles drawn on the open cut end of the tube. "
            "Two more decorated paper logs rest nearby on a white craft table. "
            "Cozy handmade craft scene, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-campfire-craft-stacked-logs.webp",
        "prompt": (
            "Several brown rolled paper logs stacked in a crisscross campfire shape, "
            "two logs on the bottom and one or two across the top, glued together, "
            "with a small open space in the center. Sitting on a white craft table, no flames yet. "
            "Clearly built by a child, slightly wonky and charming. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-campfire-craft-glue-flames.webp",
        "prompt": (
            "A child's hands standing layered red, orange, and yellow paper flames upright "
            "in the open center of a crisscross stack of brown rolled paper logs, "
            "tucking the base of the flames between the logs. On a white craft table. "
            "Bright cheerful colors, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-campfire-craft-finished-display.webp",
        "prompt": (
            "A finished paper campfire craft displayed for pretend play: brown rolled paper logs "
            "stacked in a crisscross with tall layered red, orange, and yellow paper flames "
            "in the center and a ring of small gray paper rocks around the base. "
            "A couple of small stuffed animals sit nearby as if gathered around the fire. "
            "Cozy warm scene on a light wood surface, clearly child-made. "
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
