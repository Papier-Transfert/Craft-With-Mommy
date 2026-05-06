#!/usr/bin/env python3
"""Generate all images for paper-angels-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-angels-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood or white craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

ANGEL_DESC = (
    "Each paper angel is small (about 5 inches tall), built from a white cardstock cone body, "
    "a small white circle head glued on top of the cone, a pair of gold glitter cardstock wings "
    "glued to the back of the cone, and a small gold pipe cleaner halo floating above the head. "
    "The face has tiny dot eyes, soft pink marker cheeks, and a small smile. "
)

IMAGES = [
    {
        "filename": "paper-angels-craft.webp",
        "prompt": (
            "A cheerful flat lay or three-quarter view of three or four finished handmade paper angels "
            "standing upright on a light wood craft table. " + ANGEL_DESC +
            "Some angels have plain white wings, others have gold glitter wings. "
            "Soft natural daylight, a sprig of evergreen and a few gold star sequins scattered around for festive feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-angels-mom-child.webp",
        "prompt": (
            "A warm photo of a young American mom in her early thirties and her four-year-old child sitting at a "
            "light wood craft table together, smiling and working on a paper angels craft. "
            "On the table: white cardstock, gold glitter cardstock wings cut out, gold pipe cleaners, "
            "a glue stick, child-safe scissors, and one finished small paper angel. "
            "The mom is helping the child glue a wing onto a paper cone body. "
            "Soft natural light, cozy home craft moment, clearly emotional and shared. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-angels-quarter-circle.webp",
        "prompt": (
            "A flat lay of one large white cardstock quarter-circle shape cut out and laid flat on a light wood "
            "craft table. The quarter-circle is roughly 7 inches along each straight edge with a soft curved outer edge. "
            "Next to it sits a pair of child-safe scissors with bright orange handles and a pencil. "
            "A few small white cardstock scraps from cutting are visible at the edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-angels-cone-body.webp",
        "prompt": (
            "A close-up photo of one white paper cone body for an angel craft, standing upright on a light wood craft table. "
            "The cone is rolled from white cardstock with a visible glued seam down the back. "
            "It is about 5 inches tall, with a pointed top and a wide circular open base. "
            "No head, no wings, no halo yet. Just the simple white cone. "
            "A glue stick lies on the table next to the cone. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-angels-head-attached.webp",
        "prompt": (
            "A close-up photo of one paper angel cone body with a small white round paper head freshly glued to the very top. "
            "The cone is white cardstock, about 5 inches tall, standing upright on a light wood craft table. "
            "The head is a plain white paper circle about 1.25 inches across, with no face drawn on yet. "
            "No wings and no halo yet. A glue stick sits next to the angel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-angels-wings-cut.webp",
        "prompt": (
            "A flat lay close-up of one pair of gold glitter cardstock angel wings cut from folded paper, "
            "now opened flat on a light wood craft table. The wings are symmetrical, about 5 inches across, "
            "with soft rounded curves like two heart halves joined in the middle. "
            "Small bits of gold glitter cardstock scraps are visible from the cutting. "
            "A pair of child-safe scissors lies nearby. The wings are not yet attached to anything. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-angels-wings-attached.webp",
        "prompt": (
            "A three-quarter angle photo of one paper angel craft with gold glitter cardstock wings "
            "freshly glued to the back of a white paper cone body, just below the small white head. "
            "The wings peek out evenly on both sides of the cone, tilted slightly upward. "
            "The angel is about 5 inches tall, standing upright on a light wood craft table. "
            "No halo yet, no face drawn yet. A glue stick lies on the table next to the angel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-angels-halo-added.webp",
        "prompt": (
            "A close-up photo of one paper angel craft with a small gold pipe cleaner halo loop attached just above "
            "the small white round head. The halo is a thin gold sparkly circle floating about half an inch above the head, "
            "anchored down into the head with a tiny pipe cleaner stem. "
            "The angel has white cardstock cone body, gold glitter cardstock wings on the back, and the new halo on top. "
            "No drawn face yet. Standing upright on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-angels-finished-face.webp",
        "prompt": (
            "A close-up photo of the finished handmade paper angels craft. " + ANGEL_DESC +
            "The angel is about 5 inches tall and stands upright on a light wood craft table. "
            "Soft, sweet, and clearly child-decorated. Warm daylight, very Pinterest-worthy. "
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
