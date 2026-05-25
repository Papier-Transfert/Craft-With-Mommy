#!/usr/bin/env python3
"""Generate all images for paper-strawberry-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-strawberry-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-strawberry-craft.webp",
        "prompt": (
            "A finished handmade paper strawberry craft displayed flat on a white craft table. "
            "A bright red construction paper body shaped like a chubby teardrop, wider at the top "
            "and tapering to a soft point at the bottom, about the size of a child's open hand. "
            "On top sits a fresh green construction paper crown with five or six gently pointed "
            "leaves arranged like a star, peeking up above the rounded shoulders of the berry. "
            "About fifteen to twenty small yellow marker seed dots are scattered evenly across "
            "the front of the red body. A cute smiling face is drawn in black marker near the top "
            "middle: two small oval eyes with tiny white sparkle dots and a sweet curved U smile. "
            "Two or three small white marker shine dots on the cheeks for a glossy look. "
            "The strawberry is mounted on a piece of white cardstock. Cheerful spring craft mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strawberry-craft-mom-child.webp",
        "prompt": (
            "A warm photo of a mom in her early thirties and her young child around four years old "
            "sitting together at a light wood craft table, both smiling, getting ready to start a "
            "paper strawberry craft. On the table in front of them are sheets of red and green "
            "construction paper, a pair of blue kid scissors with blunt tips, a purple glue stick, "
            "a yellow marker, a black marker, and a pencil. A pinch of red paper scraps lies to one "
            "side. The child is looking at the supplies with eager excitement. Natural daylight "
            "from a window, cozy and family-friendly atmosphere. Photo composition is wide landscape. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strawberry-red-body-cut.webp",
        "prompt": (
            "A large rounded red construction paper strawberry body shape freshly cut out, "
            "shaped like a chubby teardrop with rounded shoulders at the top and a soft point at "
            "the bottom, about the size of a child's open hand. The shape is lying flat on a white "
            "craft table next to a yellow pencil and a pair of blue kid scissors with blunt tips. "
            "A few small red paper scraps are nearby. The edges of the shape are slightly uneven "
            "in a charming child-cut way. No green crown attached yet, no seeds, no face. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strawberry-green-crown.webp",
        "prompt": (
            "A fresh green construction paper crown freshly cut into a star shape with five or six "
            "gently pointed leaves radiating from a flat bottom edge. The green crown is laid flat "
            "next to the previously cut red strawberry body shape on a white craft table. The red "
            "body is still plain with no crown attached yet and no seeds. Both pieces are arranged "
            "side by side so the bright red and fresh green colors are clearly visible. A small "
            "green paper scrap is nearby. Edges are slightly uneven in a charming child-cut way. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strawberry-crown-glued.webp",
        "prompt": (
            "The green paper crown now glued onto the top of the red strawberry body. "
            "The pointed green leaves peek up above the rounded shoulders of the bright red "
            "construction paper berry. The bottom edge of the crown covers the top edge of the red "
            "shape neatly. The berry is sitting flat on a white craft table. A purple glue stick "
            "lies beside it. No yellow seed dots yet, no face yet. The paper looks freshly pressed "
            "and the colors are bright. Edges are slightly uneven in a charming child-cut way. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strawberry-yellow-seeds.webp",
        "prompt": (
            "The red paper strawberry body now decorated with about fifteen to twenty small yellow "
            "marker seed dots scattered evenly across the front, with a little gap between each dot, "
            "like real strawberry seeds. The green leafy crown is still in place on top of the red "
            "body with its pointed leaves peeking up. The berry is sitting flat on a white craft "
            "table with a yellow marker resting beside it. No face drawn yet, no shine dots yet. "
            "Bright red, fresh green, sunny yellow dots. Slightly uneven dots in a child-drawn way. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strawberry-cute-face.webp",
        "prompt": (
            "The paper strawberry craft now decorated with a cute smiling face drawn in black marker "
            "near the top middle of the red body, just below the green crown. Two small oval eyes "
            "with tiny white sparkle dots inside, and a sweet curved U-shaped smiling mouth a bit "
            "lower. The strawberry already has its green leafy crown and about fifteen to twenty "
            "yellow marker seed dots scattered across the red body. The berry is sitting flat on a "
            "white craft table with a black marker resting beside it. No white shine dots on cheeks "
            "yet, and not mounted on cardstock yet. Bright, cheerful, friendly little character. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strawberry-finished.webp",
        "prompt": (
            "The completely finished paper strawberry craft mounted on a piece of white cardstock. "
            "A bright red construction paper body topped with a green leafy crown of five or six "
            "pointed leaves, fifteen to twenty scattered yellow marker seed dots across the front, "
            "a cute black marker face with two oval eyes (with white sparkle dots) and a curved "
            "smiling mouth, and two or three tiny white marker shine dots on the cheeks for a "
            "glossy just-picked look. The whole craft is laid flat on a light wood craft table "
            "with a black marker and a white correction pen lying alongside. Final stage, looks "
            "complete and Pinterest-worthy, clearly child-made and charmingly imperfect. "
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
