#!/usr/bin/env python3
"""Generate all images for nutcracker-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "nutcracker-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly Christmas atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper and cardstock materials only. "
    "Charming and imperfect, clearly handmade. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "nutcracker-paper-craft.webp",
        "prompt": (
            "A finished handmade nutcracker paper craft soldier displayed standing on a light wood craft table. "
            "The soldier is built from layered flat construction paper pieces and shows: a tall black rectangular hat "
            "with a thin gold band at the bottom, a round white face with two googly eyes, fluffy white paper beard, "
            "small white paper mustache, drawn pink rosy cheeks, a tiny black drawn mouth, a bright red rectangular "
            "jacket with three small shiny gold paper circle buttons down the front, two red sleeve strips on the sides, "
            "a thin gold ribbon belt across the waist, a blue rectangular paper pants section, and two small black paper "
            "boots peeking out at the bottom. A small sprig of green pine and a single small red Christmas ornament rest "
            "next to the soldier. Festive Christmas mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "nutcracker-paper-craft-mom-child.webp",
        "prompt": (
            "A mother and a young child around 5 years old sitting together at a light wood craft table, both smiling and "
            "looking down at the materials in front of them. On the table: sheets of red, blue, white, and black "
            "construction paper, a sheet of white cardstock, a pair of kid safety scissors, a purple glue stick, "
            "small gold paper circles for buttons, a small roll of gold ribbon, and a pencil. They are about to start "
            "making a nutcracker paper craft. Cozy holiday lighting from a nearby window, soft warm Christmas feeling. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "nutcracker-paper-craft-cut-body.webp",
        "prompt": (
            "A flat lay close-up on a light wood craft table showing two simple white cardstock shapes: one tall vertical "
            "rectangle about four inches tall and two inches wide for a nutcracker body, and one smaller round white "
            "circle about two inches across for the head, placed just above the rectangle. A pair of kid safety scissors "
            "and a sharpened pencil rest next to the shapes. A few small white paper scraps from cutting are visible. "
            "Nothing else is on the body yet, just the two plain white base shapes. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "nutcracker-paper-craft-red-coat.webp",
        "prompt": (
            "A nutcracker paper craft in progress on a light wood craft table. The base is a vertical white cardstock "
            "rectangle for the body with a small round white circle head above it. A bright red construction paper "
            "rectangle is glued onto the top half of the white body as the soldier's jacket, and two thin red paper "
            "strips are glued one on each side of the body as sleeves. The bottom half of the white body is still bare "
            "white, no pants or boots yet, and the head is still plain white with no face yet. Small red paper scraps "
            "are visible nearby along with kid safety scissors and a purple glue stick. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "nutcracker-paper-craft-blue-pants.webp",
        "prompt": (
            "A nutcracker paper craft in progress on a light wood craft table. The figure shows a small round white "
            "circle head still plain on top, a bright red rectangular paper jacket on the upper body with two red "
            "sleeve strips, and now a new blue construction paper rectangle glued onto the bottom half of the white "
            "body as the pants with a tiny vertical gap down the middle suggesting two trouser legs. Two small black "
            "paper rectangle boots are glued just below the blue pants peeking out at the bottom. The head is still "
            "plain white with no face yet and there is no hat yet. Small blue and black paper scraps nearby with kid "
            "safety scissors and a purple glue stick. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "nutcracker-paper-craft-tall-hat.webp",
        "prompt": (
            "A nutcracker paper craft in progress on a light wood craft table. The body shows a red rectangular jacket "
            "with two red sleeve strips, blue pants below with a center gap, and small black boots at the bottom. "
            "The head is still a plain round white circle with no face yet, but now a tall black construction paper "
            "rectangle about three inches tall is glued directly above the head as the iconic nutcracker hat, with a "
            "thin red paper strip glued across the bottom of the hat as a band. The face is still bare with no eyes, "
            "no beard, no mouth yet. Small black paper scraps and a glue stick nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "nutcracker-paper-craft-white-beard.webp",
        "prompt": (
            "A nutcracker paper craft in progress on a light wood craft table. The figure has a tall black paper hat "
            "with a red band on top, and below the hat the round white face is now decorated: a small fluffy white "
            "paper beard shape covers the lower half of the face, a tiny white paper mustache cloud shape sits right "
            "above the beard, two small round black googly eyes are placed on the upper half of the face, a small "
            "black drawn mouth is just visible under the mustache, and two soft pink dot cheeks have been drawn with "
            "a marker. Below the head, the red jacket with sleeves, blue pants, and black boots are all in place. "
            "There are no gold buttons or gold belt yet. A black marker and pink marker rest on the table nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "nutcracker-paper-craft-gold-details.webp",
        "prompt": (
            "The fully finished handmade nutcracker paper craft soldier displayed on a light wood craft table. "
            "Complete soldier from top to bottom: tall black rectangular paper hat with a red band at its bottom and a "
            "thin shiny gold metallic ribbon strip across the bottom of the hat, round white face with two googly eyes, "
            "fluffy white paper beard, small white paper mustache, drawn pink rosy cheeks, tiny drawn black mouth, "
            "bright red paper jacket with three small shiny gold paper circle buttons running vertically down the front, "
            "two red sleeve strips on the sides, a thin shiny gold metallic ribbon strip glued across the waist as a "
            "belt, blue rectangular paper pants with a center gap, and two small black paper boots at the bottom. "
            "Holiday styling around the figure: a few small green pine sprigs and one tiny red Christmas ornament. "
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
