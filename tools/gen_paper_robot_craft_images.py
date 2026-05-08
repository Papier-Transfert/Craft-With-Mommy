#!/usr/bin/env python3
"""Generate all images for paper-robot-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-robot-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

# Consistent robot description used across step images for continuity:
# bright blue cardstock body, silver chest plate and small silver buttons,
# large googly eyes, red construction paper smile, gold mini brads at the
# arm and leg joints, curled pink pipe cleaner antenna on top of the head.

IMAGES = [
    {
        "filename": "paper-robot-craft.webp",
        "prompt": (
            "A finished handmade paper robot craft standing upright on a light wood "
            "craft table. The robot is built from bright blue cardstock with a tall "
            "rectangular torso, a square head, two thin rectangular arms, and two "
            "thicker rectangular legs. A shiny silver metallic cardstock chest plate "
            "sits in the middle of the torso, decorated with small silver circles, "
            "squares, and rectangles drawn over with small dial markings in black "
            "marker. Two large googly eyes, a small red construction paper smile, "
            "and small silver square ears on the head. Small gold colored mini brad "
            "fasteners visible at the shoulder and hip joints where the arms and legs "
            "swivel. A curled pink pipe cleaner antenna pokes out the top of the head. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-robot-craft-mom-child.webp",
        "prompt": (
            "A young American mother with shoulder length brown hair sitting at a light "
            "wood craft table next to her cheerful 6 year old child, both smiling and "
            "starting a paper robot craft. On the table are several sheets of bright "
            "blue cardstock, a sheet of silver metallic cardstock, a few sheets of red "
            "and yellow construction paper, blunt-tip kid scissors, a glue stick, a "
            "small pile of self-adhesive googly eyes, a small box of gold mini brad "
            "fasteners, and a few colorful pipe cleaners. Warm natural light from a "
            "window. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-robot-craft-cut-body-shapes.webp",
        "prompt": (
            "Six bright blue cardstock shapes for a paper robot craft, freshly cut "
            "and laid out on a light wood craft table: one tall rectangular torso "
            "about 5 by 6 inches, one square head about 4 by 4 inches, two long "
            "thin rectangular arms about 1 by 4 inches, and two thicker rectangular "
            "legs about 1.5 by 3 inches. Blunt-tip kid scissors and a pencil rest "
            "next to the cardstock. The shapes are still flat, plain, and undecorated, "
            "ready to be assembled into a robot. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-robot-craft-glue-silver.webp",
        "prompt": (
            "A child's hands gluing a shiny silver metallic cardstock rectangle chest "
            "plate onto the center of a tall bright blue cardstock rectangle torso for "
            "a paper robot craft. Several small silver circles, small silver squares, "
            "and small silver rectangles are arranged around the chest plate, ready to "
            "be glued on as buttons, knobs, and dials. A purple Elmer's disappearing "
            "glue stick rests on the light wood craft table. The torso is still flat "
            "on the table, no head or limbs attached yet, no marker drawings yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-robot-craft-decorate-markers.webp",
        "prompt": (
            "A child drawing tiny dial markings, gauge ticks, and small gear lines "
            "with a black fine line marker on the silver metallic chest plate of a "
            "paper robot torso. The torso is bright blue cardstock with a silver "
            "chest plate already glued in place plus several small silver circles "
            "and squares glued around it as buttons and knobs. The buttons now show "
            "small inked details like dial faces and crisscross lines. The torso is "
            "flat on a light wood craft table, no limbs attached yet, no head yet. "
            "A few Crayola broad line markers rest beside the torso. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-robot-craft-add-face.webp",
        "prompt": (
            "A bright blue cardstock square head for a paper robot craft, lying flat "
            "on a light wood craft table, decorated with two large self-adhesive "
            "googly eyes near the top, a small red construction paper rectangle as "
            "a smiling mouth glued just under the eyes, and two small silver metallic "
            "cardstock squares on the left and right sides as ears. The head sits on "
            "its own, not attached to a body yet. A small pile of extra googly eyes "
            "and a glue stick rest nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-robot-craft-attach-brads.webp",
        "prompt": (
            "A paper robot craft body laid flat on a light wood craft table with the "
            "tall bright blue cardstock torso in the center, two long thin arm strips "
            "and two thicker leg rectangles being attached using small gold mini brad "
            "paper fasteners pushed through the joints at the shoulders and hips. The "
            "silver metallic chest plate with small silver buttons and inked dial "
            "details is clearly visible on the torso. A small pile of extra gold brads "
            "rests on the table. The head is not yet attached and lies separately to "
            "the side, showing googly eyes and a red smile. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-robot-craft-pipe-cleaner-antenna.webp",
        "prompt": (
            "A close up view of a bright blue cardstock paper robot head square with "
            "two large googly eyes, a small red construction paper smile, and small "
            "silver square ears. A pink pipe cleaner is being pushed through a small "
            "hole at the top of the head and curled into a fun spiral antenna above "
            "the head. The head sits on a light wood craft table next to the rest of "
            "the assembled robot body which has a silver chest plate, gold brads at "
            "the joints, and arms and legs already attached. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-robot-craft-finished.webp",
        "prompt": (
            "The fully finished paper robot craft standing proudly upright on a light "
            "wood craft table in a cozy room with warm natural light from a window. "
            "Bright blue cardstock body with a tall torso, square head, two thin "
            "swiveling arms posed in a cheerful wave, and two rectangular legs. A "
            "silver metallic cardstock chest plate sits in the middle of the torso "
            "with small silver buttons and inked dial markings. Two large googly "
            "eyes, a red construction paper smile, and small silver square ears on "
            "the head. Small gold mini brad fasteners visible at the arm and leg "
            "joints. A curled pink pipe cleaner antenna spirals proudly above the "
            "head. The robot looks complete, cheerful, and lovingly handmade. "
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
