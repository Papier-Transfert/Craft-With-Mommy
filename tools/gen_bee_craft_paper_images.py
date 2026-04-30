#!/usr/bin/env python3
"""Generate all images for bee-craft-paper.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "bee-craft-paper"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "bee-craft-paper.webp",
        "prompt": (
            "A finished handmade paper bee craft on a white craft table. "
            "The bee has a bright yellow oval body made of construction paper, "
            "three thin black paper stripes glued horizontally across the body, "
            "two rounded white paper wings sticking out from behind near the top, "
            "two large googly eyes near the top of the body, "
            "two short curly black pipe cleaner antennae above the eyes, "
            "and a tiny black marker smile drawn just below the eyes. "
            "A few yellow and black paper scraps and a glue stick visible at the edges. "
            "Cheerful spring craft mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bee-craft-paper-mom-child.webp",
        "prompt": (
            "A young American mom around 30 and her young child around 5 sitting together "
            "at a light wood craft table, smiling and looking at sheets of yellow, black, "
            "and white construction paper laid out in front of them. Safety scissors, a glue stick, "
            "googly eyes, and black pipe cleaners are arranged on the table. They are about to "
            "start making a paper bee craft. Warm natural daylight. Cozy, family-friendly atmosphere. "
            "The mom is wearing a casual sweater. The child is excited and holding up a piece of yellow paper. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bee-craft-paper-cut-body.webp",
        "prompt": (
            "A young child's hands using safety scissors to cut out a large yellow oval shape "
            "from a sheet of yellow construction paper on a white craft table. A pencil line "
            "outlines the oval body of the bee. A few yellow paper scraps are visible around the work area. "
            "Close-up showing the cutting in progress. Just yellow paper at this stage, no other bee parts yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bee-craft-paper-add-stripes.webp",
        "prompt": (
            "A young child's hands gluing three thin black construction paper strips horizontally "
            "across a large yellow paper oval body on a white craft table. The yellow oval is fully cut out. "
            "Two of the three black stripes are already glued in place, and the child is pressing down the "
            "third stripe with a glue stick visible nearby. Small gaps of yellow show between the stripes. "
            "Black paper scraps visible around the edges. The bee has stripes but no wings, eyes, or antennae yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bee-craft-paper-cut-wings.webp",
        "prompt": (
            "A young child's hands gluing two rounded white paper teardrop-shaped wings onto the back "
            "of a yellow paper bee body that already has three black horizontal stripes across it. "
            "The wings stick out from behind the body near the top, one on each side. "
            "The bee is on a white craft table with white paper scraps and a glue stick nearby. "
            "Still no eyes or antennae at this stage, just the body, stripes, and wings. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bee-craft-paper-add-eyes.webp",
        "prompt": (
            "A young child's small fingers pressing two self-adhesive googly eyes onto the upper part "
            "of a yellow paper bee body with three black horizontal stripes and two white rounded wings "
            "sticking out from behind. The bee is lying on a white craft table. The googly eyes have been just placed "
            "above the first stripe. No antennae or smile yet. A small sheet of googly eyes is on the table beside the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bee-craft-paper-add-antennae.webp",
        "prompt": (
            "A young child's hands placing clear tape on two short curly black pipe cleaner antennae "
            "attached to the top of a paper bee head. The bee has a yellow oval body with three "
            "black horizontal stripes, two white rounded wings sticking out behind, and two googly eyes near the top. "
            "The antennae stick up above the eyes with cute little spiral curls at the tips. "
            "Black pipe cleaner pieces and a roll of clear tape visible on the white craft table. "
            "No smile drawn yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bee-craft-paper-finished.webp",
        "prompt": (
            "A completely finished handmade paper bee craft displayed on a white craft table. "
            "The bee has a yellow oval body with three thin black paper stripes glued across it, "
            "two rounded white paper wings sticking out from behind near the top, "
            "two large googly eyes, two cute curly black pipe cleaner antennae sticking up above the eyes, "
            "and a tiny black marker U-shaped smile drawn just below the eyes. "
            "A small paper flower sits next to the bee for decoration. "
            "Bright cheerful spring craft mood, clearly child-made and slightly imperfect. "
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
