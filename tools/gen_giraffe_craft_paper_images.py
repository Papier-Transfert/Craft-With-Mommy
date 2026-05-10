#!/usr/bin/env python3
"""Generate all images for giraffe-craft-paper.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "giraffe-craft-paper"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. Clean, cozy, family-friendly atmosphere. "
    "Landscape orientation 4:3. No cartoon elements. Real construction paper only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

GIRAFFE_DESC = (
    "A handmade flat paper giraffe craft made from yellow construction paper: "
    "a rounded rectangle yellow body about 5 inches wide, a tall curved yellow neck "
    "rising from the top right of the body, a small yellow head with two tiny stubby "
    "ossicones (little horns) on top, four long thin yellow paper legs along the bottom, "
    "and a short yellow tail with a tiny brown tuft at the back. The body and neck "
    "are covered in about ten to fifteen small irregular brown paper spots in different "
    "shapes and sizes. A thin fringed brown paper mane runs along the back of the neck. "
    "Two small black paper circle eyes and a tiny black oval nose on the head. "
    "A black marker has drawn a soft smile, two tiny nostrils, and tiny hoof marks "
    "at the bottom of each leg."
)

IMAGES = [
    {
        "filename": "giraffe-craft-paper.webp",
        "prompt": (
            f"Hero photo of a finished {GIRAFFE_DESC} "
            "Lying flat on a light wood craft table surface, photographed from directly above. "
            "A few yellow and brown construction paper scraps and a glue stick visible at the edges. "
            "The giraffe fills most of the frame, tall and proud. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "giraffe-craft-paper-mom-child.webp",
        "prompt": (
            "A warm candid photo of a young American mom in her early thirties and her four year old child "
            "sitting close together at a light wood craft table, both smiling and looking down at "
            "yellow and brown construction paper, kid safety scissors, and a glue stick laid out in front of them. "
            "On the table there are pre-cut paper shapes for a giraffe: a yellow body rectangle, a tall yellow neck strip, "
            "a small yellow head shape, four long thin yellow legs, and a small pile of brown paper spots. "
            "The mom is gently helping the child press a brown spot onto the yellow body. "
            "Soft natural daylight from a side window, cozy kitchen background slightly blurred. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "giraffe-craft-paper-cut-body-neck.webp",
        "prompt": (
            "A close-up photo of a child's small hands using red kid safety scissors to finish cutting "
            "a long curved yellow construction paper neck strip about 5 inches tall and 1.5 inches wide. "
            "Next to the neck strip on the light wood craft table is an already cut yellow rounded rectangle "
            "body shape about 5 inches wide and 3 inches tall. A pencil and a few yellow paper scraps lie nearby. "
            "No spots, no head, no legs yet, only the freshly cut yellow body and neck shapes. "
            "Step 1 of a giraffe paper craft tutorial. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "giraffe-craft-paper-attach-head.webp",
        "prompt": (
            "An overhead photo of an in-progress paper giraffe craft on a light wood craft table. "
            "A yellow rounded rectangle paper body is lying flat with a tall curved yellow neck strip glued to "
            "the top right corner of the body, standing tall above it. A small rounded yellow paper head shape "
            "about 2 inches long is glued to the very top of the neck. Two tiny stubby yellow paper ossicones "
            "(small rounded ovals about half an inch tall) are glued onto the very top of the head, side by side. "
            "No spots, no legs, no eyes yet. A glue stick lies next to the craft. "
            "Step 2 of a giraffe paper craft tutorial, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "giraffe-craft-paper-add-legs-tail.webp",
        "prompt": (
            "An overhead photo of an in-progress paper giraffe craft on a light wood craft table. "
            "A yellow rounded rectangle body has a tall curved yellow neck rising from its top right, "
            "topped by a small yellow head with two tiny ossicones. Four long thin yellow paper legs about 3 inches tall "
            "and three quarters of an inch wide are now glued along the bottom edge of the body, two near the front "
            "and two near the back. A short thin yellow paper tail strip is glued onto the back edge of the body, "
            "with a tiny brown paper tuft at its tip. No brown spots and no eyes yet. A glue stick lies next to the craft. "
            "Step 3 of a giraffe paper craft tutorial. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "giraffe-craft-paper-add-spots.webp",
        "prompt": (
            "An overhead photo of an in-progress paper giraffe craft on a light wood craft table. "
            "The full yellow giraffe (body, tall curved neck, head with two tiny ossicones, four long legs, "
            "and a short tail with a brown tuft) is now being decorated with small irregular brown paper spots. "
            "About ten to fifteen brown paper spots in different shapes and sizes are glued across the body, "
            "neck, and a few on the legs, leaving little gaps of yellow showing between each spot. "
            "A child's small hand is gently pressing one final brown spot onto the neck. "
            "A few extra brown paper scraps and a glue stick lie nearby. No eyes or mane yet. "
            "Step 4 of a giraffe paper craft tutorial. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "giraffe-craft-paper-add-face.webp",
        "prompt": (
            "An overhead photo of an in-progress paper giraffe craft on a light wood craft table. "
            "The yellow giraffe (body, tall curved neck, head with two tiny ossicones, four long legs, "
            "tail with a brown tuft, and brown paper spots all over) now has two small black paper circle eyes "
            "glued onto the head, a tiny black paper oval nose at the front of the head, and a thin brown "
            "paper mane with a fringed top edge running along the back of the neck. The mane fringe sticks up "
            "like little brown spikes. No marker details yet. A glue stick and a few paper scraps lie nearby. "
            "Step 5 of a giraffe paper craft tutorial. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "giraffe-craft-paper-decorate.webp",
        "prompt": (
            f"An overhead photo of {GIRAFFE_DESC} "
            "A child's small hand is using a black fine-tip marker to add a final tiny hoof line at the bottom of one leg. "
            "The giraffe is fully finished, lying flat on a light wood craft table. The black marker rests next to it "
            "alongside a few brown paper scraps. The face shows a soft smile, tiny nostrils, and small inner ear lines. "
            "Step 6 of a giraffe paper craft tutorial, clearly handmade by a child, charming and slightly imperfect. "
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
