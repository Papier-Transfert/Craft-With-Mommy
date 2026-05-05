#!/usr/bin/env python3
"""Generate all images for easy-paper-fruit-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "easy-paper-fruit-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and imperfect, clearly handmade by a young child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "easy-paper-fruit-craft.webp",
        "prompt": (
            "A finished handmade paper apple craft sitting flat on a clean white craft table. "
            "The apple body is a large round shape cut from bright cherry red construction paper, "
            "with a small dip at the very top where the stem sits. A small brown construction paper "
            "rectangle stem peeks out of the dip, with a green construction paper teardrop leaf "
            "glued beside it angling outward, with a soft folded crease running down its center. "
            "Two simple small black marker drawn round eyes near the upper third of the apple, "
            "a tiny curved black smile below them, and two soft pink marker cheek dots. "
            "A pencil and kid scissors visible at the edge of the frame. Cheerful and adorable. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "easy-paper-fruit-craft-mom-child.webp",
        "prompt": (
            "A warm photo of an American mom in her early thirties and her four year old child "
            "sitting together at a clean white craft table. They are smiling and getting ready "
            "to start a paper apple craft. On the table in front of them: sheets of bright red, "
            "green, and brown construction paper, a glue stick, blue handled kid scissors, "
            "a small set of Crayola markers, and a pencil. Mom is leaning in with her arm gently "
            "around her child. Soft window light. Cozy family atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "easy-paper-fruit-craft-cut-apple-body.webp",
        "prompt": (
            "A large round bright cherry red construction paper apple body shape, freshly cut, "
            "with a small soft dip at the top center where a stem will later sit. "
            "The shape is mostly circular with very slightly uneven hand cut edges, clearly cut by a child. "
            "Resting flat on a clean white craft table next to a pair of blue handled kid scissors "
            "and a yellow pencil. Some leftover red construction paper scraps visible at the edge. "
            "No stem, no leaf, no face yet, just the plain red round apple body. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "easy-paper-fruit-craft-cut-stem-leaf.webp",
        "prompt": (
            "A flat lay close up showing three pieces neatly arranged side by side on a clean white craft table: "
            "a large round bright cherry red construction paper apple body shape with a small dip at the top, "
            "a small brown construction paper rectangle the size of a postage stamp for the stem, "
            "and a green construction paper teardrop shaped leaf, slightly larger than the stem, freshly cut. "
            "All edges are slightly uneven, clearly hand cut by a child. Kid scissors at the edge of frame. "
            "No glue applied yet. The pieces are not assembled. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "easy-paper-fruit-craft-attach-stem.webp",
        "prompt": (
            "A round bright cherry red construction paper apple body lying flat on a clean white craft table, "
            "with a small brown construction paper rectangle stem now glued into the dip at the top center "
            "of the apple, where about half of the brown rectangle peeks above the apple silhouette and the "
            "other half is hidden behind the red paper. No leaf yet. No face yet. A purple Elmer's glue stick "
            "is open and resting next to the apple. Slight gentle press marks visible from a finger holding the stem. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "easy-paper-fruit-craft-add-leaf.webp",
        "prompt": (
            "A round bright cherry red construction paper apple body lying flat on a clean white craft table, "
            "with a small brown rectangular paper stem peeking out of the top dip of the apple, and now a "
            "green construction paper teardrop shaped leaf glued to the side of the brown stem, angled outward "
            "as if reaching toward the sun, with a soft folded crease visible running down the center of the "
            "green leaf for a natural folded look. No face drawn on the apple yet, just the assembled apple, "
            "stem, and leaf. A glue stick visible at the edge. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "easy-paper-fruit-craft-draw-face.webp",
        "prompt": (
            "A round bright cherry red construction paper apple body with a brown rectangular stem and a green "
            "teardrop leaf with a folded crease on top, now decorated with a sweet face drawn in marker: "
            "two simple small black round eyes in the upper third of the apple, a tiny curved black smile below "
            "them, and two soft pink marker cheek dots that look like a gentle blush. The apple is lying flat on "
            "a clean white craft table next to a small set of Crayola broad line markers, with the black and "
            "pink marker caps off as if just used. Cheerful and friendly looking. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "easy-paper-fruit-craft-finished-scene.webp",
        "prompt": (
            "A finished paper apple craft glued onto a piece of clean white cardstock as a background. "
            "The apple is round and bright cherry red, with a brown rectangular stem peeking up, a green "
            "teardrop leaf with a folded crease beside the stem, two small black marker drawn eyes, a small "
            "curved smile, and two soft pink cheek dots. Around the apple on the white cardstock: a few small "
            "white marker drawn sparkle dots, a soft pencil drawn shadow line just under the apple, and a few "
            "thin green marker grass blades along the bottom edge. Displayed on a light wood craft table. "
            "The full scene is complete and ready to be hung on a fridge. "
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
