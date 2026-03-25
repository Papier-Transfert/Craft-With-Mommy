#!/usr/bin/env python3
"""Generate all images for top-10-paper-christmas-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "top-10-paper-christmas-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "top-10-paper-christmas-crafts.webp",
        "prompt": (
            "A festive flat lay of 10 handmade paper Christmas crafts on a white craft table: "
            "a paper plate wreath, a toilet paper roll Christmas tree, a red paper cone Santa hat, "
            "a tissue paper candy cane, a paper snowman collage, a folded paper star ornament, "
            "a paper plate gingerbread man, a paper Christmas lights garland, "
            "a white paper cone angel, and a red paper poinsettia. "
            "All crafts are clearly child-made, imperfect, and charming. "
            "Scissors, glue stick, and construction paper scraps visible at the edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-wreath.webp",
        "prompt": (
            "A handmade Christmas wreath craft made from a paper plate with the center cut out, "
            "covered in torn and cut green construction paper leaf shapes glued all around the ring. "
            "Small red paper circles for holly berries and a big red paper bow at the bottom. "
            "Sits on a white craft table. Slightly imperfect, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roll-christmas-tree.webp",
        "prompt": (
            "A small 3D Christmas tree craft made from a toilet paper roll wrapped in green construction paper. "
            "Triangle paper branches of different sizes glued around it, with colorful marker dot ornaments "
            "and a yellow paper star on top. Stands upright on a white craft table. "
            "Two more similar trees of different heights visible in the background. "
            "Clearly child-made and charming. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-santa-hat.webp",
        "prompt": (
            "A wearable red construction paper cone Santa hat sitting on a white craft table. "
            "Wide white paper strip trim around the base and a small white paper ball at the tip. "
            "The cone is slightly imperfect, taped closed at the back. "
            "Scissors and red paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-candy-cane.webp",
        "prompt": (
            "A handmade tissue paper candy cane craft on a white craft table. "
            "A cardstock candy cane outline covered in alternating red and white tissue paper squares "
            "that are scrunched and glued on to create a bumpy textured surface. "
            "The stripes are slightly uneven, clearly made by a young child. "
            "Tissue paper scraps and a glue stick visible nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-snowman-collage.webp",
        "prompt": (
            "A handmade paper snowman collage on dark blue construction paper. "
            "Three white paper circles of graduating sizes stacked vertically as the snowman body. "
            "A black construction paper top hat, a colorful paper scarf, "
            "an orange paper carrot nose, and black paper buttons. "
            "A big marker smile on the face. "
            "Glue stick and extra paper scraps on the white table nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-star-ornament.webp",
        "prompt": (
            "A handmade folded paper star ornament made from five gold or yellow paper diamond shapes "
            "each folded in half and glued together at their bases in a five-pointed star. "
            "A thin loop of string through a hole at the top for hanging. "
            "Sits flat on a white craft table. Two more stars visible in the background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-gingerbread-man.webp",
        "prompt": (
            "A handmade paper plate gingerbread man craft on a white craft table. "
            "The paper plate is colored or painted brown, with brown construction paper arms and legs attached. "
            "White marker or paint icing squiggles, round button dots, and a cheerful smiley face. "
            "Slightly imperfect, made by a young child. Markers and paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-christmas-lights.webp",
        "prompt": (
            "A handmade paper Christmas lights garland laid out on a white craft table. "
            "A long strip of black construction paper as the wire, with colorful teardrop and bulb shapes "
            "cut from bright red, yellow, blue, and green paper glued along it. "
            "The bulb shapes are slightly varied and imperfect, clearly child-cut. "
            "Scissors and construction paper scraps visible nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-angel.webp",
        "prompt": (
            "A handmade paper cone angel craft on a white craft table. "
            "A white paper semicircle rolled into a cone for the body, "
            "a small yellow paper circle head on top, two white teardrop wings glued to the back, "
            "and a thin gold paper strip halo above the head. "
            "Three similar angels displayed in a row, slightly different sizes. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poinsettia.webp",
        "prompt": (
            "A handmade paper poinsettia craft on a white craft table. "
            "Six to eight large red construction paper teardrop petal shapes arranged in a circle, "
            "slightly overlapping, with a cluster of small yellow paper dots in the center. "
            "The petals are slightly uneven and child-cut. "
            "Red paper scraps and scissors visible at the edge of the table. "
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
        # Crop to 4:3 ratio before resizing to avoid white borders
        w, h = img.size
        target_ratio = TARGET_W / TARGET_H  # 4/3
        current_ratio = w / h
        if current_ratio > target_ratio:
            # Image is too wide — crop sides
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            img = img.crop((left, 0, left + new_w, h))
        elif current_ratio < target_ratio:
            # Image is too tall — crop top/bottom
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

    log.info("All done.")


if __name__ == "__main__":
    main()
