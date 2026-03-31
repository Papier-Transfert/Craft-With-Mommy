#!/usr/bin/env python3
"""Generate all images for paper-lantern-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-lantern-craft"
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
        "filename": "paper-lantern-craft.webp",
        "prompt": (
            "Three finished colorful paper lanterns with carrying handles, displayed on a white craft table. "
            "Each lantern is a cylinder made from a sheet of construction paper with evenly spaced horizontal slits "
            "cut through the middle section, causing the paper strips to bow outward beautifully. "
            "One lantern is bright red, one is yellow, one is blue, each decorated with hand-drawn markers. "
            "The lanterns stand upright next to scattered paper scraps, a glue stick, and child-safe scissors. "
            "Warm and inviting craft table scene, clearly handmade by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-lantern-craft-why-kids-love.webp",
        "prompt": (
            "A mom and a young child aged 4 to 6 sitting side by side at a light wood craft table, "
            "both smiling and looking at colorful sheets of construction paper spread in front of them. "
            "Washable markers, child-safe scissors, and a glue stick are visible on the table. "
            "The child is holding a bright orange sheet of paper and the mom is pointing at it encouragingly. "
            "Warm natural window light. Cozy, joyful, family-friendly atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-lantern-cut-handle.webp",
        "prompt": (
            "A bright yellow sheet of construction paper on a white craft table. "
            "A thin strip about one inch wide has been cut from one of the short ends of the paper. "
            "The small handle strip lies parallel beside the larger sheet. "
            "Child-safe scissors rest nearby. "
            "Clean, simple flat-lay composition showing both pieces clearly. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-lantern-decorated.webp",
        "prompt": (
            "A young child aged 3 to 5 drawing colorful diagonal stripes and small stars on a flat sheet "
            "of bright blue construction paper using washable markers. "
            "The paper is laid flat on a white craft table. "
            "Several open marker caps lie nearby and a small glue stick and scissors are visible at the edge. "
            "The drawing is joyful and imperfect, clearly done by a young child. "
            "Warm natural daylight, cozy craft atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-lantern-cut-slits.webp",
        "prompt": (
            "A sheet of red construction paper folded in half lengthwise on a white craft table. "
            "Eight evenly spaced horizontal scissor cuts are visible running from the folded edge toward "
            "the open edge, stopping about one inch before the open side. "
            "The cuts are clearly child-made and slightly uneven, giving it a handmade charm. "
            "Child-safe scissors rest beside the folded paper. "
            "Clean flat-lay photo, warm lighting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-lantern-opened.webp",
        "prompt": (
            "A sheet of colorfully decorated construction paper unfolded and lying flat on a white craft table. "
            "The slit pattern from the cutting is clearly visible: a series of horizontal cuts running across "
            "the center of the paper from fold to just before the edges, creating a beautiful striped window pattern. "
            "The paper is decorated with rainbow stripes in marker. "
            "The paper lies completely flat, ready to be curled into a lantern. "
            "Clean flat-lay photo with warm natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-lantern-cylinder.webp",
        "prompt": (
            "A sheet of green construction paper curled into a round cylinder shape on a white craft table. "
            "The horizontal slit strips in the middle section bow outward to create the classic paper lantern shape. "
            "A small piece of double-sided tape holds the two short edges together. "
            "The lantern shape is clearly visible with the strips fanning out around the middle. "
            "Child-safe scissors and a tape dispenser visible nearby. "
            "Warm natural light, handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-lantern-finished.webp",
        "prompt": (
            "Three finished colorful paper lanterns hanging from a single piece of twine string "
            "stretched across the scene, backlit by a bright window. "
            "Each lantern is a cylinder of construction paper with horizontal slit strips bowing outward "
            "in the classic lantern shape and a small paper strip handle looped over the string. "
            "One lantern is red, one orange, one yellow, each decorated with different marker patterns. "
            "The warm light shines through the gaps between the strips, creating a beautiful glowing effect. "
            "Cozy and festive family craft atmosphere. "
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

    from PIL import Image as PILImage
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
