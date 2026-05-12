#!/usr/bin/env python3
"""Generate all images for marshmallow-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "marshmallow-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "marshmallow-paper-craft.webp",
        "prompt": (
            "A finished handmade marshmallow paper craft on a light wood craft table: "
            "two stacked puffy white construction paper marshmallow shapes with softly rounded corners, "
            "glued onto the top of a long thin dark brown paper roasting stick. "
            "Small torn light brown paper pieces are glued around the edges of the marshmallows "
            "to look like a lightly toasted color. Each marshmallow has two small googly eyes "
            "and a tiny black marker smile. A few scraps of white and brown construction paper "
            "are visible around the edges of the frame. Cozy campfire snack feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "marshmallow-paper-craft-mom-child.webp",
        "prompt": (
            "A warm overhead photo of a mother and her young child, about four years old, "
            "sitting together at a light wood craft table preparing a marshmallow paper craft. "
            "On the table: sheets of white and brown construction paper, "
            "small blunt-tipped kids scissors, a purple glue stick, a pack of googly eyes, "
            "and a black washable marker. The mom is smiling and pointing at the paper while the child "
            "looks excited and engaged. Sunlit room, soft natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "marshmallow-paper-craft-cut-rectangles.webp",
        "prompt": (
            "A child's small hands using blunt-tip kids scissors to cut a soft white construction paper "
            "rectangle, about three inches tall and four inches wide. A second already-cut white paper "
            "rectangle sits next to it on the light wood craft table. A pencil and a small ruler "
            "are visible nearby. White paper scraps from the cutting are scattered around. "
            "Photographed from above with warm daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "marshmallow-paper-craft-rounded-corners.webp",
        "prompt": (
            "Two soft white construction paper rectangles on a light wood craft table, with their four corners "
            "gently rounded off so they look like puffy pillowy marshmallow shapes. Small white paper "
            "corner trimmings are scattered around them. A pair of small blunt-tip kids scissors lies next to the shapes. "
            "Clear flat lay from above, warm natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "marshmallow-paper-craft-cut-stick.webp",
        "prompt": (
            "A long thin strip of dark brown construction paper, about eight inches long "
            "and half an inch wide, lying on a light wood craft table to represent a roasting stick. "
            "Next to the stick are two finished puffy white paper marshmallow shapes with rounded corners. "
            "A pair of small kids scissors and a pencil are nearby. "
            "Flat lay from above, soft natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "marshmallow-paper-craft-glued-stack.webp",
        "prompt": (
            "Two puffy white paper marshmallow shapes with rounded corners glued onto the top end of "
            "a long thin dark brown paper roasting stick, slightly overlapping like a real stacked roasting marshmallow. "
            "The marshmallows are pure white, no toasted edges yet, no eyes yet. "
            "The whole craft lies flat on a light wood craft table. "
            "A purple glue stick is open and visible to the side. "
            "Photographed from above with warm daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "marshmallow-paper-craft-toasted-edges.webp",
        "prompt": (
            "Two stacked white paper marshmallow shapes on a dark brown paper roasting stick, "
            "now with small irregular torn pieces of light brown construction paper glued softly "
            "around the edges and corners of the marshmallows to imitate a lightly toasted look. "
            "The torn pieces are uneven and clearly child-made. The craft lies flat on a light wood craft table. "
            "Small torn light brown paper scraps are scattered around the craft. "
            "No eyes or smiles yet. Photographed from above. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "marshmallow-paper-craft-finished.webp",
        "prompt": (
            "A finished cheerful marshmallow paper craft on a light wood craft table: "
            "two stacked white construction paper marshmallows with softly rounded corners "
            "and lightly toasted torn brown paper edges, glued onto the top end of a thin dark brown "
            "paper roasting stick. Each marshmallow has two small self-adhesive googly eyes and "
            "a tiny curved black marker smile. Two small pink dots on the cheeks of each marshmallow. "
            "Clearly handmade, slightly wonky, charming. Photographed from above with warm daylight. "
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
