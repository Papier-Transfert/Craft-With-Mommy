#!/usr/bin/env python3
"""Generate all images for reindeer-handprint-craft.html."""
import io, os, time, logging
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "reindeer-handprint-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
if load_dotenv:
    load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly Christmas atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "reindeer-handprint-craft.webp",
        "prompt": (
            "A finished handprint reindeer craft on a sheet of white cardstock, lying flat on a light wood table. "
            "The reindeer is a single brown painted child's handprint: the palm forms the reindeer's round face "
            "and the five spread fingers point upward to form the antlers. "
            "Two small googly eyes are stuck in the middle of the palm, and a single bright red fluffy pom-pom "
            "is glued at the bottom of the palm as Rudolph's nose. A small smile is drawn under the nose with marker. "
            "A few sprigs of pine and a couple of small craft supplies sit at the edges. "
            "Cozy Christmas mood, clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "reindeer-handprint-craft-mom-child.webp",
        "prompt": (
            "A warm candid photo of a young mom and her small child sitting together at a light wood craft table, "
            "painting the child's open hand with brown washable paint using a foam brush. "
            "A plate with a puddle of brown paint, a sheet of white cardstock, googly eyes, and a red pom-pom "
            "are on the table in front of them. Both look happy and engaged in the moment. "
            "Soft Christmas decorations blurred in the background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "reindeer-handprint-brown-paint-setup.webp",
        "prompt": (
            "A flat lay of craft supplies on a light wood table ready for a reindeer handprint craft: "
            "a blank sheet of white cardstock, a paper plate with a single puddle of brown washable paint, "
            "a foam brush resting on the plate, two small googly eyes, and one bright red fluffy pom-pom. "
            "Everything laid out neatly before painting begins. Cozy Christmas crafting mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "reindeer-handprint-painting-hand.webp",
        "prompt": (
            "A close-up of a foam brush spreading brown washable paint evenly over a young child's open hand, "
            "covering the palm and all five fingers. The hand is held open and flat above a light wood craft table. "
            "A plate of brown paint and a sheet of white cardstock are visible nearby. "
            "Warm, gentle, family-friendly Christmas crafting moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "reindeer-handprint-pressing-hand.webp",
        "prompt": (
            "A young child's brown painted hand pressing down firmly onto a sheet of white cardstock, "
            "with the fingers spread wide and pointing upward. As the hand lifts slightly, "
            "it reveals a fresh brown handprint where the palm is the reindeer's face and the spread fingers are the antlers. "
            "No eyes or nose yet, just the brown print. On a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "reindeer-handprint-drying.webp",
        "prompt": (
            "A finished brown handprint drying on a sheet of white cardstock on a light wood craft table. "
            "The print clearly shows a reindeer shape: a round palm face with five finger antlers pointing up. "
            "There are no eyes or nose yet, only the plain brown print. "
            "A pack of baby wipes and a freshly cleaned child's hand are next to the paper. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "reindeer-handprint-adding-eyes-nose.webp",
        "prompt": (
            "A child's fingers pressing a bright red fluffy pom-pom onto the bottom of a dry brown reindeer handprint "
            "on white cardstock, with two googly eyes already stuck in the middle of the palm face. "
            "A small bottle of tacky craft glue sits nearby on the light wood table. "
            "The brown handprint has finger antlers pointing up. Close, warm, hands-on Christmas craft moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "reindeer-handprint-finished-reindeer.webp",
        "prompt": (
            "A completed reindeer handprint craft on white cardstock on a light wood table. "
            "The brown handprint has a round palm face with five finger antlers, two googly eyes, "
            "a bright red pom-pom nose, and a small smile drawn with marker. "
            "The words 'Merry Christmas' are written beside the antlers in colorful marker, "
            "with a child's first name and the year signed underneath. "
            "Cheerful, proud, finished holiday keepsake, clearly made by a young child. "
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
        img = img.convert("RGB")
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
