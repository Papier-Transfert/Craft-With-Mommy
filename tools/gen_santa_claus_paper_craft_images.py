#!/usr/bin/env python3
"""Generate all images for santa-claus-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "santa-claus-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real paper and cotton ball materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "The craft photo fills the full 1200x900 frame edge to edge, no white borders or padding."
)

IMAGES = [
    {
        "filename": "santa-claus-paper-craft.webp",
        "prompt": (
            "A finished handmade paper Santa Claus craft displayed flat on a light wood craft table. "
            "The Santa is made from layered construction paper: a round peach face circle about five inches across, "
            "a wide red triangular hat with the tip bent floppy to one side, "
            "a white paper trim strip across the bottom of the hat, "
            "a single fluffy white cotton ball as the pom pom on the bent tip, "
            "fluffy white cotton balls glued in a U shape around the lower face for the beard, "
            "two smaller cotton balls forming a curved mustache, "
            "two round black marker eyes drawn above the mustache, "
            "a small red paper circle nose between the eyes, "
            "and two small pink circles on the cheeks. "
            "A few cotton balls and red paper scraps scattered nearby. "
            "Festive Christmas mood, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "santa-claus-paper-craft-mom-child.webp",
        "prompt": (
            "A warm overhead photo of an American mom in her early thirties and her young child around five years old "
            "sitting together at a light wood craft table, smiling and looking happy. "
            "Spread out on the table in front of them: sheets of red, white, peach, pink, and black construction paper, "
            "a small pile of fluffy white cotton balls, kid scissors with green handles, "
            "a purple Elmer's glue stick, and a black Sharpie marker. "
            "They are clearly about to start a Santa Claus paper craft together. "
            "Cozy Christmas atmosphere with soft natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "santa-claus-paper-craft-cut-face.webp",
        "prompt": (
            "Close-up overhead photo of a young child's hands using small green kid scissors "
            "to cut out a round peach construction paper circle, about five inches across, "
            "that will become the face of a Santa Claus paper craft. "
            "On the light wood craft table next to the child's hands: "
            "a sheet of red construction paper, a sheet of white construction paper, "
            "a few fluffy white cotton balls, a pencil, and a purple glue stick. "
            "Only the peach circle is cut so far. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "santa-claus-paper-craft-cut-hat.webp",
        "prompt": (
            "Close-up overhead photo of a young child's hands cutting a wide red construction paper triangle "
            "for a Santa hat. The base of the triangle is slightly wider than the peach face circle lying "
            "on the craft table next to it. The tip of the red triangle is gently bent to one side, "
            "giving it the classic floppy Santa hat look. "
            "A sheet of white paper and a few white cotton balls are visible nearby. "
            "Only the peach face circle and the red triangle hat are visible. No beard or trim yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "santa-claus-paper-craft-white-trim.webp",
        "prompt": (
            "Close-up overhead photo of a young child's hands cutting a long thin white construction paper strip, "
            "about one inch tall and slightly wider than the base of the red Santa hat triangle. "
            "On the light wood craft table: the peach face circle, the red floppy triangle hat with bent tip, "
            "the partially cut white trim strip, and one single fluffy white cotton ball set aside as the pom pom. "
            "Scissors and a purple glue stick visible at the edge of the frame. "
            "No beard, no face details yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "santa-claus-paper-craft-hat-glued.webp",
        "prompt": (
            "Overhead photo of a partially assembled paper Santa Claus craft on a light wood craft table. "
            "The wide red triangle hat is glued onto the top half of the peach face circle with the tip bent floppy to one side, "
            "a long thin white paper trim strip glued across the base of the hat where it meets the forehead, "
            "and a single fluffy white cotton ball glued to the bent tip of the hat as the pom pom. "
            "No beard, no mustache, no face details yet. "
            "A purple Elmer's glue stick lying open next to the craft. "
            "A few extra cotton balls in a small pile nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "santa-claus-paper-craft-cotton-beard.webp",
        "prompt": (
            "Overhead photo of a paper Santa Claus craft with the beard being added. "
            "The peach face circle has a red floppy triangle hat with white trim and a cotton ball pom pom on top. "
            "A young child's hand is pressing fluffy white cotton balls in a U shape around the lower half of the face circle: "
            "about six to eight cotton balls forming a thick fluffy beard from cheek to cheek under the chin. "
            "Two smaller cotton ball pieces are placed in a horizontal curve above where the mouth will go, forming the mustache. "
            "No drawn face details yet, no nose, no eyes. "
            "Light wood craft table with a purple glue stick and a small pile of extra cotton balls nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "santa-claus-paper-craft-finished-face.webp",
        "prompt": (
            "Overhead photo of a finished handmade paper Santa Claus craft displayed on the front of a white refrigerator door "
            "next to a homemade Christmas card. "
            "The Santa has a peach face circle, a wide red floppy triangle hat with white paper trim "
            "and a fluffy white cotton ball pom pom on the bent tip, "
            "a thick fluffy white cotton ball beard in a U shape around the lower face, "
            "two smaller cotton ball pieces forming a horizontal mustache, "
            "two round friendly black marker eyes drawn above the mustache, "
            "a small red paper circle nose glued between the eyes, "
            "and two small pink circles drawn on the cheeks for that classic rosy Santa glow. "
            "Festive cozy Christmas atmosphere, clearly child-made. "
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
