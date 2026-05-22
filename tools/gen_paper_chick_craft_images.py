#!/usr/bin/env python3
"""Generate all images for paper-chick-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-chick-craft"
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
        "filename": "paper-chick-craft.webp",
        "prompt": (
            "A finished paper chick craft displayed on a white craft table. "
            "The chick is made from a large round bright yellow construction paper body "
            "with a smaller round yellow construction paper head glued slightly overlapping on top. "
            "A small folded orange paper diamond beak is glued to the front of the head. "
            "A single black googly eye is stuck just above the beak. "
            "A small yellow teardrop-shaped paper wing is glued to the side of the body. "
            "Two tiny orange triangle feet peek out from the bottom of the body. "
            "The chick stands behind a half brown paper eggshell with a wavy zigzag cracked top, "
            "as if hatching out of the egg. A few thin green paper grass blades are scattered around. "
            "Cheerful spring atmosphere, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-chick-craft-mom-child.webp",
        "prompt": (
            "A warm photo of an American mom around 30 years old and her young child around 4 years old "
            "sitting together at a white craft table, smiling and getting ready to start a paper chick craft. "
            "On the table in front of them: sheets of bright yellow construction paper, orange construction paper, "
            "brown construction paper, and green construction paper, a pair of blunt tip kid scissors, "
            "a purple Elmer's glue stick, and a small pile of black googly eyes. "
            "No craft is started yet, just the supplies laid out. Cozy spring morning atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-chick-craft-cut-shapes.webp",
        "prompt": (
            "A close-up overhead photo on a white craft table showing two yellow construction paper shapes "
            "freshly cut by a child: one large round body shape about the size of a palm and one smaller "
            "round head shape about the size of a clementine, both with slightly imperfect wobbly edges. "
            "Next to them: a pair of blunt tip kid scissors and a pencil. No other shapes or decorations yet. "
            "Soft natural light, clearly the very first step of a paper chick craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-chick-craft-beak-feet-wing.webp",
        "prompt": (
            "An overhead photo on a white craft table showing the same large yellow round body shape "
            "and smaller yellow round head shape from before, still separate and not yet glued. "
            "Next to them, freshly cut: one small orange paper diamond shape about the size of a quarter "
            "for the beak, two tiny orange paper triangles for the feet, and one small yellow paper "
            "teardrop shape for the wing. All pieces arranged neatly on the white table. "
            "A pair of blunt tip kid scissors visible at the edge of the frame. "
            "Clearly the second preparation step of a paper chick craft, before any gluing. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-chick-craft-attach-head.webp",
        "prompt": (
            "An overhead photo on a white craft table showing a paper chick craft in progress. "
            "The small round yellow paper head has just been glued onto the top of the larger round "
            "yellow paper body, slightly overlapping the body curve so the chick shape looks snuggly and "
            "connected as one creature. No beak, no eye, no wing, no feet yet. Just the body and head joined. "
            "A purple Elmer's glue stick lies open beside the chick. The orange paper beak, "
            "orange feet triangles, and yellow teardrop wing are visible nearby waiting for the next step. "
            "Clearly step 3 of a paper chick craft, mid assembly. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-chick-craft-add-face.webp",
        "prompt": (
            "An overhead photo on a white craft table showing a paper chick craft in progress. "
            "The yellow paper body and head are already glued together with the head on top. "
            "A small folded orange paper diamond beak has just been glued onto the front of the head "
            "so it points outward like a real chick beak. A single black googly eye has been stuck "
            "just above the beak, giving the chick a sweet little face. "
            "Still no wing and no feet yet. The yellow teardrop wing and two orange triangle feet "
            "are visible on the table beside the chick, waiting for the next step. "
            "Clearly step 4 of a paper chick craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-chick-craft-add-wing-feet.webp",
        "prompt": (
            "An overhead photo on a white craft table showing a paper chick craft nearly finished. "
            "The yellow paper chick has body and head glued together, an orange folded diamond beak, "
            "a black googly eye, and now a small yellow teardrop wing glued onto the side of the body "
            "tilted slightly upward, plus two tiny orange triangle feet glued along the bottom edge "
            "of the body with just the points peeking out so the chick looks like it is standing tall. "
            "No eggshell or grass scene yet, the chick is on its own on the bare white craft table. "
            "Clearly step 5 of a paper chick craft, almost complete. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-chick-craft-egg-scene.webp",
        "prompt": (
            "An overhead photo of the fully finished paper chick craft mounted on a white cardstock "
            "background. The yellow paper chick with its head, beak, googly eye, teardrop wing, and "
            "orange triangle feet stands behind a half brown construction paper eggshell with a wavy "
            "zigzag cracked top, looking as if it is hatching out of the egg. A few thin green paper "
            "grass blades are glued around the bottom. Small marker-drawn cracks decorate the eggshell "
            "and a tiny chirp mark is drawn near the beak. Cheerful finished spring craft, clearly handmade. "
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
