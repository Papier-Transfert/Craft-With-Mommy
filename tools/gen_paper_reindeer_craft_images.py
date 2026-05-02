#!/usr/bin/env python3
"""Generate all images for paper-reindeer-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-reindeer-craft"
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
        "filename": "paper-reindeer-craft.webp",
        "prompt": (
            "A finished handmade paper reindeer craft on a white craft table. "
            "The face is a large brown construction paper heart turned upside down "
            "so the pointed tip is at the bottom. Two child handprint shapes cut from "
            "darker brown paper are glued behind the top of the heart and stick up "
            "like reindeer antlers, fingers spread wide as antler points. "
            "Two large googly eyes are stuck to the upper face. "
            "A fluffy bright red pom pom is glued to the bottom point as the Rudolph nose. "
            "Two small tan teardrop ears sit just below the antlers. "
            "Two tiny pink cheek dots and a small black marker smile under the nose. "
            "A few brown paper scraps and a glue stick visible at the edges. "
            "Top-down flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-reindeer-craft-mom-child.webp",
        "prompt": (
            "A warm photo of a young American mom in her thirties and her four year old child "
            "sitting together at a light wood craft table, getting ready to start a paper reindeer craft. "
            "On the table are sheets of brown construction paper, a small bowl of red pom poms, "
            "a sheet of self-adhesive googly eyes, kid-friendly scissors, a glue stick, and a pencil. "
            "The mom is smiling and looking at her child. The child is excited, hands on the brown paper. "
            "Cozy realistic family moment. No craft is finished yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-reindeer-craft-cut-head.webp",
        "prompt": (
            "A large brown construction paper heart shape cut out and lying flat on a white craft table, "
            "turned upside down so the rounded top is up and the pointed tip is at the bottom. "
            "The heart was cut by a child so the edges are slightly uneven. "
            "Kid-friendly scissors and a pencil sit next to the heart. "
            "Brown paper scraps from the cut visible at the edges of the table. "
            "No antlers, no eyes, no nose yet, just the brown heart shape. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-reindeer-craft-trace-antlers.webp",
        "prompt": (
            "Two child handprint shapes cut out of darker brown construction paper, "
            "lying flat on a light wood craft table next to each other with fingers spread wide. "
            "Next to them is a third sheet of brown paper with the pencil outline of a small hand still showing, "
            "and a sharpened pencil resting on the paper. "
            "The handprints will be used as antlers for a paper reindeer craft. "
            "Brown paper scraps around the edges. No reindeer face visible yet, only the hand shapes. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-reindeer-craft-attach-antlers.webp",
        "prompt": (
            "An upside-down brown construction paper heart on a white craft table with two darker brown "
            "child handprint cutouts glued to the back of the heart at the top corners. "
            "The fingers of both handprints stick up above the heart like reindeer antlers, spread wide. "
            "Viewed from the front so the heart face is showing. "
            "No googly eyes, no nose, no inner ears yet, just the brown heart with handprint antlers attached. "
            "A glue stick rests next to the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-reindeer-craft-add-ears.webp",
        "prompt": (
            "A paper reindeer craft in progress on a white craft table. "
            "An upside-down brown heart face with two darker brown handprint antlers attached at the top, "
            "fingers sticking up. Two small tan or beige teardrop-shaped paper inner ears glued to the "
            "sides of the head just below where the antlers meet the heart, slightly tilted outward. "
            "No googly eyes and no red nose yet. A few small tan paper scraps visible. "
            "Front-facing flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-reindeer-craft-add-eyes.webp",
        "prompt": (
            "A paper reindeer craft in progress on a white craft table. "
            "An upside-down brown heart face with handprint antlers spread above and tan teardrop "
            "inner ears in place. Two large white googly eyes with black pupils have just been stuck "
            "onto the upper middle of the brown heart, with a small space between them. "
            "No red pom pom nose yet. A small sheet of self-adhesive googly eyes rests next to the craft. "
            "Front-facing flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-reindeer-craft-red-nose.webp",
        "prompt": (
            "A nearly finished paper reindeer craft on a white craft table. "
            "An upside-down brown heart face with handprint antlers spread above, tan teardrop inner ears, "
            "and two large googly eyes already in place. A bright fluffy red pom pom has just been glued "
            "to the bottom point of the heart as the Rudolph nose. "
            "No marker smile or cheeks yet. A small bowl of extra red pom poms next to the craft. "
            "Front-facing flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-reindeer-craft-finished.webp",
        "prompt": (
            "A completed paper reindeer craft on a white craft table. "
            "An upside-down brown construction paper heart face with two darker brown handprint antlers "
            "spread above, two tan teardrop inner ears, two large googly eyes, and a bright red pom pom nose. "
            "A small black marker smile drawn under the nose, and two soft pink cheek circles on either side. "
            "The reindeer looks sweet, slightly imperfect, and clearly child-made. "
            "A few brown paper scraps and a glue stick at the edges of the table. "
            "Front-facing flat lay, full reindeer visible. "
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
