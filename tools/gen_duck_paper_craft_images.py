#!/usr/bin/env python3
"""Generate all images for duck-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "duck-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White craft table or light wood surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "Image fills the full frame edge to edge with no white borders or padding."
)

IMAGES = [
    {
        "filename": "duck-paper-craft.webp",
        "prompt": (
            "A finished handmade paper duck craft displayed on a white craft table. "
            "The duck is made from a large bright yellow construction paper oval body and a smaller "
            "round yellow paper head glued slightly overlapping the body. A folded orange paper "
            "diamond beak points outward from the front of the head, and a small black googly eye "
            "sits just above the beak. A smaller yellow oval wing is glued onto the side of the body, "
            "and two small orange paper triangle feet peek out from the bottom edge. "
            "The duck is mounted onto a wavy strip of light blue construction paper that represents a pond, "
            "with a few thin green construction paper grass blades along one edge and tiny marker drawn water "
            "ripples around the duck. Cheerful, simple, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "duck-paper-craft-mom-child.webp",
        "prompt": (
            "A warm photo of an American mom in her early thirties and her young child around four years old, "
            "sitting together at a clean white craft table, smiling and getting ready to start a paper duck craft. "
            "On the table in front of them: bright yellow, orange, and light blue construction paper sheets, "
            "a pair of blue blunt-tip kids scissors, a purple Elmer's glue stick, a small bag of googly eyes, "
            "and a pencil. Soft natural light from a window. Both look engaged and excited about the activity. "
            "No craft pieces are cut yet, the supplies are fresh and laid out. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "duck-paper-craft-cut-shapes.webp",
        "prompt": (
            "A flat lay close-up photo on a white craft table showing two shapes freshly cut from bright "
            "yellow construction paper: one large oval roughly the size of an open hand for the duck body, "
            "and one smaller round circle about the size of a clementine for the duck head. The edges are "
            "soft and slightly uneven, clearly cut by a child. A pair of blue blunt-tip kid scissors and a "
            "yellow pencil rest beside the shapes. A few tiny yellow paper scraps are scattered around. "
            "No glue or other paper pieces yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "duck-paper-craft-beak-feet-wing.webp",
        "prompt": (
            "A flat lay photo on a white craft table showing several paper shapes laid out neatly side by side: "
            "the large yellow oval body and smaller yellow round head from before, plus three new pieces in front: "
            "a small orange construction paper diamond shape about the size of a quarter for the beak, "
            "two small orange paper triangle shapes for the feet, and one smaller yellow paper oval for the wing. "
            "All shapes are unglued and arranged separately on the table. Edges are soft, child-cut. "
            "Blue kid scissors and a pencil rest at the edge of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "duck-paper-craft-attach-head.webp",
        "prompt": (
            "A flat lay photo on a white craft table showing a paper duck in progress: the small round yellow "
            "construction paper head is now glued onto the upper left side of the larger yellow oval body, "
            "slightly overlapping the body so the duck looks like one connected creature. The duck has no beak, "
            "eye, wing, or feet yet, just the body and head joined together. A purple Elmer's glue stick lies "
            "open beside the duck shape. The unglued orange beak, orange feet, and yellow wing pieces are "
            "visible nearby on the table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "duck-paper-craft-add-face.webp",
        "prompt": (
            "A flat lay close-up photo on a white craft table showing the paper duck with the body and head "
            "joined, now with a face added: a small folded orange construction paper diamond beak is glued onto "
            "the front of the round yellow head and points outward like a real bird beak. A small black googly "
            "eye is stuck just above the beak. The duck still has no wing or feet yet, just body, head, beak, "
            "and eye. The unglued yellow oval wing and two orange triangle feet rest on the table nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "duck-paper-craft-add-wing-feet.webp",
        "prompt": (
            "A flat lay photo on a white craft table showing the paper duck nearly finished: the yellow body "
            "and head are joined, the orange beak points outward from the head, a small black googly eye sits "
            "above the beak, a smaller yellow oval wing is now glued onto the middle side of the body slightly "
            "tilted, and two orange paper triangle feet peek out from the bottom edge of the body. "
            "The duck is not yet on a pond background. A purple Elmer's glue stick rests beside it. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "duck-paper-craft-pond-scene.webp",
        "prompt": (
            "A flat lay photo on a white craft table showing the completely finished paper duck craft mounted "
            "on a scene: a long wavy strip of light blue construction paper as a pond is glued onto a piece of "
            "white cardstock background, and the yellow paper duck (body, head, folded orange beak, googly eye, "
            "yellow oval wing, two orange triangle feet) sits on top of the pond as if floating. A few thin "
            "green construction paper grass blades rise along one edge of the pond, and small marker drawn "
            "water ripples are sketched around the duck. Cheerful, complete, clearly child-made. "
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
