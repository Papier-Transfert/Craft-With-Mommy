#!/usr/bin/env python3
"""Generate all images for lion-craft-paper.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "lion-craft-paper"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "The craft must fill the whole image frame edge to edge. "
    "No white borders, no padding, no letterboxing, no blank canvas around the photo."
)

IMAGES = [
    {
        "filename": "lion-craft-paper.webp",
        "prompt": (
            "A finished handmade paper lion craft displayed on a white craft table. "
            "The lion has a large yellow construction paper circle face (about 5 inches wide), "
            "surrounded by a fluffy fringed mane made of orange construction paper strips "
            "that have been snipped along one edge to look like fur. "
            "Two small brown rounded paper ears are glued to the top of the face, "
            "two medium googly eyes are stuck to the upper half of the face, "
            "a small brown heart-shaped nose sits in the middle, "
            "and a curved black marker mouth with whiskers is drawn below the nose. "
            "Cheerful, charming, clearly child-made. Photographed from above. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lion-craft-paper-mom-child.webp",
        "prompt": (
            "A warm photo of an American mom and her young child (around 4 years old) sitting "
            "together at a light wood craft table, smiling and getting ready to start a paper lion craft. "
            "Yellow, orange, and brown construction paper, kid-safe scissors, a glue stick, "
            "googly eyes, and a black marker are laid out neatly between them. "
            "The mom is gently pointing at the orange paper while the child holds a pair of scissors. "
            "Cozy at-home atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lion-craft-paper-cut-face.webp",
        "prompt": (
            "A child's small hands using blunt-tipped kid scissors to carefully cut out a large "
            "yellow construction paper circle (about 5 inches across) on a white craft table. "
            "A pencil line traces the circle outline on the yellow paper. "
            "A small jar lid sits beside the paper as a tracing template. "
            "No mane or other lion pieces are visible yet, just the plain yellow face being cut. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lion-craft-paper-fringe-mane.webp",
        "prompt": (
            "A close-up of a child's hands using kid scissors to make small straight snips along one "
            "long edge of a long orange construction paper strip, creating a fringed mane effect. "
            "Several similar orange paper strips are laid out on the white craft table, "
            "some already fringed with neat tiny snips, others still plain. "
            "The yellow circle face from the previous step is visible at the edge of the table "
            "but is not yet attached to anything. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lion-craft-paper-glue-mane.webp",
        "prompt": (
            "A child's hands gluing fringed orange construction paper strips around the back edge of "
            "the yellow circle face for the paper lion. The yellow face circle is flipped face-down on "
            "the white craft table, and fringed orange strips are being pressed onto its back edge "
            "with a glue stick so the fringe pokes outward all around like a fluffy mane. "
            "Some strips are already glued, others are being added. "
            "No ears, eyes, or face details yet, just the mane being attached around the yellow face. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lion-craft-paper-add-ears.webp",
        "prompt": (
            "A child's hands gluing two small rounded brown construction paper ears to the top of the "
            "yellow paper lion face on a white craft table. The lion already has its fluffy orange "
            "fringed paper mane fully attached around the yellow face. "
            "The two small brown half-circle ears are being pressed onto the top of the yellow circle, "
            "tucked slightly behind the fringed orange mane so they peek up like little lion ears. "
            "No eyes, nose, or mouth on the face yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lion-craft-paper-add-eyes.webp",
        "prompt": (
            "A child's hands pressing two self-adhesive googly eyes onto the upper half of the yellow "
            "paper lion face. The lion already has its fluffy orange fringed paper mane all around and "
            "two small brown rounded ears glued to the top of the yellow face. "
            "The googly eyes are being placed side by side, leaving a little space between them. "
            "No nose, no mouth, no whiskers yet on the lion face. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lion-craft-paper-add-nose.webp",
        "prompt": (
            "A child's hands gluing a small brown construction paper heart-shaped nose to the middle "
            "of the yellow paper lion face, just below the two googly eyes. The lion already has its "
            "fluffy orange fringed paper mane, two small brown rounded ears at the top, "
            "and two googly eyes stuck to the upper half of the face. "
            "The heart-shaped nose is being pressed into place with a glue stick. "
            "Still no mouth or whiskers drawn yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lion-craft-paper-finished.webp",
        "prompt": (
            "A finished handmade paper lion craft sitting on a white craft table from above. "
            "The lion has a yellow construction paper circle face surrounded by a fluffy orange "
            "fringed paper mane. Two small brown rounded paper ears are glued to the top of the face. "
            "Two medium googly eyes are stuck on the upper half of the face. "
            "A small brown heart-shaped nose is glued in the middle of the face, and a curved black "
            "marker mouth with three short whisker lines on each side of the nose has been drawn under "
            "the nose. A few tiny dots above each whisker line add a furry look. "
            "Cheerful, charming, clearly child-made. Photographed from slightly above. "
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
