#!/usr/bin/env python3
"""Generate all images for paper-skeleton-craft.html."""
import io, os, time, logging
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv(*a, **k):
        return False

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-skeleton-craft"
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
        "filename": "paper-skeleton-craft.webp",
        "prompt": (
            "A finished handmade paper skeleton craft glued onto a sheet of black construction paper. "
            "The skeleton is made entirely of white cardstock pieces: a rounded white skull with a small jaw "
            "and a friendly face drawn in black marker (two round eyes, a small triangle nose, and a row of teeth), "
            "a long white spine strip down the center, four curved white rib strips across the chest, "
            "two straight white arm strips, two white leg strips, and small white oval hands and feet. "
            "The white bones stand out boldly against the black background. "
            "Lying flat on a light wood craft table with a few paper scraps and a black marker nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-skeleton-craft-mom-child.webp",
        "prompt": (
            "A mom and her young child sitting together at a white craft table, smiling and getting ready to "
            "make a paper skeleton craft. On the table are sheets of white cardstock, a sheet of black "
            "construction paper, a pair of blunt kid scissors, a glue stick, and a black marker. "
            "The child looks excited and the mom is leaning in warmly. Cozy at-home crafting moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-skeleton-skull-face.webp",
        "prompt": (
            "A single white cardstock skull shape for a paper skeleton craft, rounded at the top with a small "
            "narrower jaw at the bottom. It is decorated with a friendly face drawn in black marker: two round "
            "eyes, a small upside-down triangle nose, and a row of short vertical lines for teeth. "
            "Lying flat on a light wood craft table next to a black marker and a pair of kid scissors. "
            "Clearly cut and drawn by a child, slightly uneven edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-skeleton-spine-ribs-cut.webp",
        "prompt": (
            "Cut white cardstock pieces for a paper skeleton craft laid out on a craft table: one long white "
            "paper strip for the spine and four shorter, slightly curved white paper strips for the ribs, "
            "arranged in a row. The decorated white skull with a marker face sits nearby. "
            "Light wood craft table, scissors and paper scraps at the edge. Clearly child-cut, charming and imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-skeleton-arms-legs-cut.webp",
        "prompt": (
            "Cut white cardstock pieces for a paper skeleton craft on a craft table: two straight white paper "
            "arm strips, two slightly longer white paper leg strips, and four small white paper ovals for the "
            "hands and feet, all laid out neatly. The white skull, spine strip, and rib strips are grouped to one side. "
            "Light wood surface, kid scissors and white paper scraps visible. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-skeleton-skull-spine-glued.webp",
        "prompt": (
            "An in-progress paper skeleton craft: a white cardstock skull with a marker face glued near the top "
            "center of a sheet of black construction paper, with a long white spine strip glued straight down "
            "the middle just below it. Only the skull and spine are attached so far; the loose rib, arm, and leg "
            "strips wait to the side of the black paper. Glue stick nearby. Flat lay on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-skeleton-ribs-arms-attached.webp",
        "prompt": (
            "An in-progress paper skeleton craft on black construction paper: the white skull and spine are glued "
            "in place, a row of four curved white rib strips is glued across the upper spine to form a ribcage, "
            "and two straight white arm strips are attached at the shoulders reaching down each side. "
            "The leg strips and small oval hands and feet still wait to the side, not yet glued. "
            "Flat lay on a light wood craft table, glue stick nearby. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-skeleton-finished.webp",
        "prompt": (
            "A completed paper skeleton craft held up by a child's hand: a smiling white cardstock skull with a "
            "black marker face, a white spine, a row of curved white ribs, two white arms, two white legs, and "
            "small white oval hands and feet, all glued onto a sheet of black construction paper. "
            "The white bones pop against the black background. Warm at-home setting, proud finished result. "
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
        img = img.convert("RGB")
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
