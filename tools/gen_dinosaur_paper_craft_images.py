#!/usr/bin/env python3
"""Generate all images for dinosaur-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "dinosaur-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "dinosaur-paper-craft.webp",
        "prompt": (
            "A finished handmade dinosaur paper craft on a white craft table. "
            "A friendly stegosaurus-style dinosaur made from a peanut-shaped green "
            "construction paper body about 8 inches long, with six triangular back spikes "
            "alternating orange and yellow glued along the curved top. "
            "Four short green rectangle legs on the bottom, a small green tail tip, "
            "two large googly eyes near the front, a curved black marker smile, "
            "and a few colorful marker spots on the body. "
            "Clearly handmade by a young child, slightly imperfect edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dinosaur-paper-craft-mom-child.webp",
        "prompt": (
            "A mom and a young child around four years old sitting together at a light wood "
            "craft table, smiling and excited to start a dinosaur paper craft. "
            "On the table are sheets of green construction paper, orange and yellow paper, "
            "a glue stick, blunt-tip kid scissors, and a black marker. "
            "Warm, cozy family atmosphere. Both look happy and engaged. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dinosaur-paper-craft-cut-body.webp",
        "prompt": (
            "Close-up of a child's small hands using blunt-tip kid scissors to cut "
            "a peanut-shaped dinosaur body from a sheet of green construction paper. "
            "A pencil outline of the body shape is faintly visible on the green paper. "
            "On the craft table next to the green paper are scraps of green paper "
            "and a pencil. Bright daylight, clean composition. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dinosaur-paper-craft-cut-spikes.webp",
        "prompt": (
            "A flat lay close-up of a small pile of six paper triangle spikes "
            "freshly cut for a dinosaur paper craft, alternating orange and yellow "
            "construction paper triangles each about 1.5 inches tall, "
            "arranged next to a green peanut-shaped dinosaur body cut-out. "
            "Blunt-tip kid scissors and orange paper scraps visible at the edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dinosaur-paper-craft-glue-spikes.webp",
        "prompt": (
            "Close-up of a child's hands gluing orange and yellow paper triangle spikes "
            "along the curved top edge of a green peanut-shaped dinosaur body, "
            "with the pointy tips of the triangles facing upward. Six spikes total, "
            "alternating orange and yellow, partly attached. A purple Elmer's glue stick "
            "lies next to the work. Bright, clean craft table photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dinosaur-paper-craft-add-legs.webp",
        "prompt": (
            "A handmade green paper dinosaur lying on a craft table, with orange and yellow "
            "triangle back spikes already glued on, and four small green paper rectangle legs "
            "freshly glued to the underside of the body, two near the front and two near the back. "
            "A small green triangle tail tip is attached at the narrow end. "
            "A child's hands visible, finishing the gluing. Clean and cute. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dinosaur-paper-craft-draw-face.webp",
        "prompt": (
            "Close-up of a child's hand using a black washable marker to draw "
            "a curved smile on the front of a green paper dinosaur craft. "
            "Two large round googly eyes are stuck above the smile. "
            "The dinosaur body has orange and yellow triangle spikes on the back "
            "and small green legs underneath. Bright natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "dinosaur-paper-craft-finished.webp",
        "prompt": (
            "A completed handmade green paper dinosaur craft taped to a white refrigerator door. "
            "The dinosaur has six orange and yellow triangle back spikes, googly eyes, "
            "a friendly black marker smile, four short green rectangle legs, a small tail tip, "
            "and colorful marker spots and zigzags scattered across the body. "
            "Bright, cheerful kitchen setting with soft natural light. "
            "Clearly child-made, joyful display. "
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
