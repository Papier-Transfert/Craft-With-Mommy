#!/usr/bin/env python3
"""Generate all images for paper-elephant-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-elephant-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood or white craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3, fills the entire frame edge to edge. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and slightly imperfect, clearly handmade by a child. "
    "Photo fills the full frame, no white borders or padding."
)

# The same elephant project must visually persist across all step images:
# light grey rounded body with four short stubby legs, soft pink inner ears,
# a long curled grey trunk, two small white tusks, a single googly eye, and
# a thin grey tail with a tiny black fringe.

IMAGES = [
    {
        "filename": "paper-elephant-craft.webp",
        "prompt": (
            "A finished handmade paper elephant craft displayed flat on a light wood craft table. "
            "The elephant body is one rounded light grey construction paper shape with four short stubby legs. "
            "It has two large floppy grey paper ears with soft pink oval inner ears glued inside. "
            "A long curved grey paper trunk curls down the front of the face and curls upward at the tip. "
            "Two small white curved paper tusks sit on either side of the trunk. "
            "One small googly eye is stuck above the trunk. "
            "A thin grey paper tail with a tiny black paper fringe peeks out the back. "
            "Tiny marker details: small toenails on the feet, a smiling mouth under the trunk, and small heart patterns on the ears. "
            "Cute, friendly, clearly child-made. Slightly imperfect cuts. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-elephant-craft-mom-child.webp",
        "prompt": (
            "A warm overhead photograph of an American mom in her early thirties and her young child around age four "
            "sitting together at a light wood craft table. They are smiling and starting a paper elephant craft. "
            "On the table in front of them: a sheet of light grey construction paper, a sheet of soft pink paper, "
            "a sheet of white paper, a glue stick, kid-safe scissors, a pencil, and a small pile of googly eyes. "
            "A partially cut grey rounded elephant body shape sits in the middle of the table. "
            "Cozy family kitchen feel. Warm natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-elephant-craft-cut-body.webp",
        "prompt": (
            "Close-up overhead photograph of a young child's hand holding kid-safe scissors and cutting "
            "a large rounded light grey construction paper shape on a light wood craft table. "
            "The shape is a chunky rounded elephant body with the head bumping up on one side, "
            "the back curving down on the other side, and four short stubby legs at the bottom. "
            "About 6 inches wide and 5 inches tall. A pencil sketch outline is faintly visible on the paper. "
            "Slightly imperfect cuts, clearly child-made. Construction paper scraps around the edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-elephant-craft-cut-trunk.webp",
        "prompt": (
            "Overhead photograph on a light wood craft table showing the rounded light grey paper elephant body "
            "(with four stubby legs and the head bump on one side) lying on the left side of the frame. "
            "Next to it on the right lies a long curved light grey construction paper strip about 4 inches long "
            "and 1 inch wide, gently tapered, with the end curling slightly upward. "
            "This strip is the trunk, freshly cut, ready to be attached. "
            "Kid-safe scissors and a few grey paper scraps are visible nearby. "
            "Clearly handmade and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-elephant-craft-attach-trunk.webp",
        "prompt": (
            "Overhead photograph on a light wood craft table showing the same rounded light grey paper elephant body "
            "with four short stubby legs. A long curved light grey paper strip has been glued to the front of the head bump "
            "to form the elephant's trunk. The trunk curves down the front of the body and curls slightly upward at the tip. "
            "A small purple-tinged glue stick is open beside the body. "
            "No ears, eyes, or tusks added yet. "
            "Slightly imperfect cuts, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-elephant-craft-glue-ears.webp",
        "prompt": (
            "Overhead photograph on a light wood craft table of a light grey paper elephant body with four stubby legs "
            "and a long curled grey paper trunk attached to the front of the face. "
            "Two large rounded grey paper ears, each with a soft pink oval inner-ear shape glued inside, "
            "have just been glued onto the sides of the elephant's head, slightly behind the trunk attachment point. "
            "One ear is gently bent forward to look floppy. "
            "Still no eyes or tusks at this stage. "
            "A glue stick and pink paper scraps are visible nearby. "
            "Slightly imperfect cuts, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-elephant-craft-add-eyes-tusks.webp",
        "prompt": (
            "Overhead photograph on a light wood craft table of the in-progress paper elephant craft: "
            "rounded light grey paper body with four stubby legs, a long curled grey paper trunk on the front of the face, "
            "and two large floppy grey paper ears with soft pink inner ovals on the sides of the head. "
            "Now a small black-and-white self-adhesive googly eye has been added on the face above the trunk, "
            "and two short white curved paper tusks (about half an inch long) have been glued on either side of the trunk near the base. "
            "The tusks are soft, friendly, crescent-shaped, never sharp. "
            "Still no tail at this stage. "
            "Slightly imperfect cuts, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-elephant-craft-add-tail.webp",
        "prompt": (
            "Overhead photograph on a light wood craft table of the same in-progress paper elephant craft: "
            "rounded light grey paper body with four stubby legs, curled grey paper trunk, two pink-lined grey ears, "
            "one googly eye, and two small white paper tusks. "
            "Now a thin grey paper strip about 2 inches long has been glued onto the back of the elephant body to form a tail, "
            "with a tiny black paper fringe at the tip representing the tuft of hair. "
            "Tail points down and slightly away from the body. "
            "No marker details added yet on the body. "
            "Slightly imperfect cuts, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-elephant-craft-decorate.webp",
        "prompt": (
            "Overhead photograph on a light wood craft table of a fully finished paper elephant craft: "
            "rounded light grey paper body with four stubby legs, curled grey paper trunk, two pink-lined grey ears with one ear bent forward, "
            "one small googly eye, two short white paper tusks, and a thin grey tail with a small black fringe at the tip. "
            "The elephant has been decorated with marker details: small black toenail lines on each foot, "
            "a curved smiling mouth drawn under the trunk, three tiny dots on the cheek, "
            "and small heart and flower patterns drawn on the inside of the ears. "
            "A few colorful broad line markers and Crayola-style markers are visible around the elephant. "
            "Cheerful, finished, and clearly child-made. "
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
