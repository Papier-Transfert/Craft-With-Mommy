#!/usr/bin/env python3
"""Generate all images for snow-globe-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "snow-globe-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "snow-globe-paper-craft.webp",
        "prompt": (
            "A handmade paper snow globe craft displayed on a light wood craft table. "
            "A round white cardstock paper circle about 7 inches across forms the globe dome, "
            "glued onto a thick brown construction paper rectangle base with slightly rounded bottom corners. "
            "Inside the white circle: a small handmade paper snowman with three stacked white circles "
            "of graduated sizes, two black marker dot eyes, an orange paper carrot nose, three tiny black buttons, "
            "and a small red marker scarf. The snowman stands on a thin white snowy ground strip glued across the bottom. "
            "On either side of the snowman are two small green construction paper triangle trees, one slightly taller than the other. "
            "Tiny white acrylic paint dots are dabbed all over the inside of the globe to look like falling snowflakes. "
            "The whole craft is photographed flat lay from above. Construction paper scraps and a cotton swab visible at the edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "snow-globe-paper-craft-mom-child.webp",
        "prompt": (
            "A mom and a young child around 5 years old sitting side by side at a light wood craft table. "
            "Both are smiling and focused. The child is gluing a small white paper snowman onto a large white cardstock circle. "
            "On the table in front of them: sheets of white cardstock, brown and green construction paper, "
            "blue handled kid scissors, a purple glue stick, a few small green triangle paper trees, "
            "and a small white bowl. Warm afternoon daylight through a kitchen window. "
            "Mom is leaning in gently, helping. Cozy winter craft moment between mother and child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "snow-globe-paper-craft-supplies.webp",
        "prompt": (
            "A neat flat lay of supplies for a snow globe paper craft on a light wood table. "
            "A sheet of white cardstock paper, a sheet of brown construction paper, a sheet of green construction paper, "
            "a few sheets of additional white construction paper, blue handled kid scissors with rounded tips, "
            "a purple disappearing glue stick, a small jar of white acrylic craft paint, several cotton swabs lined up, "
            "a yellow pencil, a small upside down white ceramic bowl for tracing the circle, "
            "and a few colored markers. Items neatly arranged with a small amount of negative space. "
            "Top down photograph. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "snow-globe-paper-craft-cut-circle.webp",
        "prompt": (
            "A child's small hands cutting a large traced pencil circle out of a sheet of white cardstock. "
            "The circle is about 7 inches across and traced with a faint pencil line. "
            "Blue handled kid scissors with rounded tips are partway around the circle. "
            "Small white cardstock scraps lie nearby. A small white ceramic bowl sits to the side. "
            "Photographed from a slight overhead angle on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "snow-globe-paper-craft-cut-base.webp",
        "prompt": (
            "A small brown construction paper rectangle about 7 inches wide and 2 inches tall, "
            "with the bottom two corners gently rounded, sitting on a light wood craft table next to "
            "a large round white cardstock circle. Blue handled kid scissors with rounded tips lie to the side, "
            "along with brown construction paper scraps. The pieces are clearly the body and base of a future paper snow globe. "
            "Photographed flat lay from directly above. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "snow-globe-paper-craft-winter-scene-pieces.webp",
        "prompt": (
            "A flat lay of cut paper pieces for a snow globe winter scene on a light wood craft table. "
            "A long thin white construction paper strip about 7 inches long and 1 inch tall serves as the snowy ground. "
            "Three white paper circles in graduated sizes, large to small, ready to stack into a snowman. "
            "Two small green construction paper triangle trees, one slightly taller than the other. "
            "A black marker, an orange marker, and a purple glue stick lie nearby. "
            "Construction paper scraps visible at edges. Photographed from directly above. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "snow-globe-paper-craft-glued-scene.webp",
        "prompt": (
            "A flat round white cardstock circle about 7 inches across lying on a light wood craft table. "
            "Inside the circle: a thin white snowy ground strip glued across the bottom. "
            "Standing on the snowy ground, a small handmade paper snowman with three stacked white paper circles of graduated sizes, "
            "two small black marker dot eyes, an orange paper carrot nose, three tiny black buttons drawn down the body, "
            "and a small red marker scarf. On either side of the snowman, "
            "two small green construction paper triangle trees, one a bit taller than the other. "
            "Construction paper scraps and a purple glue stick visible at the edges. Photographed flat lay from above. "
            "No painted snow dots yet, just the glued scene. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "snow-globe-paper-craft-snow-dots.webp",
        "prompt": (
            "A child's hand holding a cotton swab dipped in white acrylic paint, "
            "dabbing tiny white paint dots onto the inside of a white cardstock snow globe circle. "
            "Inside the circle there is a small handmade paper snowman with three stacked white circles, "
            "an orange carrot nose, and a small red scarf, standing on a thin white snowy ground strip "
            "with two green triangle paper trees on either side. "
            "Several tiny white painted dots are already visible scattered across the open white space above the snowman. "
            "A small foil square with a puddle of white paint sits nearby. Light wood craft table. "
            "Photographed from a slight overhead angle. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "snow-globe-paper-craft-finished.webp",
        "prompt": (
            "A small smiling child around 5 years old holding up a finished handmade snow globe paper craft, "
            "facing the camera. The snow globe is a large round white cardstock circle attached to a brown construction paper rectangle base. "
            "Inside the white circle: a tiny paper snowman with three stacked white circles, an orange paper carrot nose, "
            "two black marker eyes, three black buttons, and a small red marker scarf, standing on a thin white snowy ground strip. "
            "Two small green construction paper triangle trees stand on either side of the snowman. "
            "Tiny white painted dots scatter across the inside of the circle to look like falling snowflakes. "
            "The child is proudly displaying their craft. Cozy kitchen background slightly out of focus, warm daylight. "
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
