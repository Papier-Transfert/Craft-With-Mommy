#!/usr/bin/env python3
"""Generate all images for gingerbread-house-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "gingerbread-house-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood or white craft table surface. Cozy December atmosphere. "
    "Clean, family-friendly, Pinterest-worthy. Landscape orientation 4:3. "
    "No cartoon elements. Real flat construction paper craft only. "
    "Charming and slightly imperfect, clearly handmade by a young child."
)

IMAGES = [
    {
        "filename": "gingerbread-house-paper-craft.webp",
        "prompt": (
            "A finished flat handmade gingerbread house paper craft made from light brown "
            "construction paper: a square house body with a wide brown triangle roof on top, "
            "a small brown rectangular door in the center, two small brown square windows on "
            "either side of the door. Wavy white gel pen icing trim runs along the bottom edge "
            "of the roof, around the door, and around each window. Tiny colorful paper candy "
            "circles in red, pink, green, and yellow are glued in a row across the roof and "
            "scattered on the walls. The whole craft is mounted on a clean white cardstock "
            "background with a soft white paper snow line under the house and a few tiny "
            "marker stars in the sky. Photographed flat lay on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gingerbread-house-paper-craft-mom-child.webp",
        "prompt": (
            "A warm cozy photo of an American mom in her early thirties and her young child "
            "around four years old sitting side by side at a light wood craft table. In front "
            "of them are sheets of brown, white, red, green, and yellow construction paper, "
            "kid-sized blunt scissors, a purple glue stick, a few colorful markers, and a "
            "pencil. They are smiling at each other, clearly excited to start a gingerbread "
            "house paper craft. Soft window light, calm December morning feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gingerbread-house-paper-craft-base-shape.webp",
        "prompt": (
            "A single freshly cut light brown construction paper square, about four inches "
            "wide, with slightly uneven hand-cut edges, lying flat in the center of a clean "
            "white craft table. A pencil and a pair of small kid-sized blunt scissors rest "
            "next to the square. Nothing else has been added yet, just the bare brown "
            "gingerbread house base shape. Top-down flat lay photograph. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gingerbread-house-paper-craft-roof-door.webp",
        "prompt": (
            "Flat lay on a white craft table showing the brown construction paper square "
            "gingerbread house base from before, with three more freshly cut brown paper "
            "pieces arranged neatly beside it: a wide darker brown triangle for the roof "
            "(slightly wider than the base), a small light brown rectangle the size of a "
            "postage stamp for the door, and two small brown squares for the windows. "
            "Pieces have slightly uneven hand-cut edges. A pencil rests at the edge of the "
            "frame. Top-down photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gingerbread-house-paper-craft-assembled.webp",
        "prompt": (
            "A handmade flat paper gingerbread house freshly assembled and lying flat on a "
            "white craft table. The wide brown triangle roof is glued on top of the brown "
            "square base, overhanging slightly on either side. The small brown rectangular "
            "door is glued in the bottom center, with two small brown square windows glued "
            "on either side of the door. The pieces are clearly construction paper, with "
            "slightly uneven edges. No icing or candy decoration yet, just the bare "
            "assembled house. A purple glue stick rests beside it. Top-down flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gingerbread-house-paper-craft-icing-trim.webp",
        "prompt": (
            "The same flat paper gingerbread house from before, still lying flat on the "
            "white craft table, now decorated with wavy white gel pen icing trim. White wavy "
            "icing lines run along the bottom edge of the brown triangle roof, around the "
            "rectangular door, around each square window, and along the side edges of the "
            "house. The icing lines look hand-drawn, slightly wobbly, and charming, like "
            "real piped royal icing. Still no candy yet, just the icing trim. A white gel "
            "pen rests beside the craft. Top-down photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gingerbread-house-paper-craft-candy-details.webp",
        "prompt": (
            "The flat paper gingerbread house from before, lying flat on the white craft "
            "table, now covered in tiny colorful paper candy details. A neat row of small "
            "red and pink paper circles is glued across the brown triangle roof like "
            "jellybeans. A small yellow paper circle sits on the door as a doorknob. Two "
            "tiny green paper hearts are glued just above the windows. Small scattered "
            "colored paper dots in red, green, and yellow are glued randomly across the "
            "walls like sprinkles. Wavy white icing trim is still visible underneath. "
            "Top-down photo, very cheerful and Christmas-festive. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gingerbread-house-paper-craft-finished-scene.webp",
        "prompt": (
            "The fully finished paper gingerbread house from before, now mounted on a clean "
            "white cardstock background. A soft white snowy ground line made from white "
            "paper or white gel pen runs underneath the house. A few tiny marker stars are "
            "drawn in the sky above the roof. Small white snowflakes are drawn around the "
            "edge of the roof. A small dark green pine tree silhouette stands beside the "
            "gingerbread house. Cozy, festive Christmas mood. Top-down flat lay photo on a "
            "light wood craft table. "
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
