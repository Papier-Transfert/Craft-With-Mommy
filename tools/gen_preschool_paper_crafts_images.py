#!/usr/bin/env python3
"""Generate all images for preschool-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "preschool-paper-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper materials only. "
    "Charming and imperfect, clearly made by a young preschooler. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "preschool-paper-crafts.webp",
        "prompt": (
            "A bright flat lay of finished preschool paper crafts on a sunny white craft table: "
            "a torn paper rainbow collage, a paper plate lion with orange mane, "
            "a colorful paper strip caterpillar, a paper crown, a tissue paper butterfly, "
            "a small paper sun with rays, a handprint paper apple tree, and a paper ladybug. "
            "Crayons, glue stick, and assorted construction paper scraps visible at the edges. "
            "Cheerful and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "torn-paper-rainbow-collage.webp",
        "prompt": (
            "A handmade torn paper rainbow collage made by a preschooler: arched rows of "
            "small torn paper pieces in red, orange, yellow, green, blue, and purple "
            "glued onto a white piece of construction paper. The torn edges are uneven and rough. "
            "Two small white cotton-ball clouds at the base of the rainbow. "
            "Flat lay on a light wood craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-lion.webp",
        "prompt": (
            "A handmade preschool paper plate lion craft: a regular round white paper plate "
            "painted yellow in the center, with thin orange and yellow paper strips glued "
            "around the edge to form a fluffy mane. Two large googly eyes, a small black "
            "triangle nose, and marker-drawn whiskers and smiling mouth. "
            "Lying flat on a light craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strip-caterpillar.webp",
        "prompt": (
            "A handmade paper strip caterpillar made from many small construction paper rings "
            "in alternating bright colors (red, orange, yellow, green, blue, purple) glued "
            "in a long wiggly row. A slightly bigger green ring at the head end with two "
            "googly eyes and two thin paper antennae. Lying flat on a white craft table. "
            "Clearly child-made and slightly uneven. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "easy-paper-crown.webp",
        "prompt": (
            "A handmade preschool paper crown made from a long strip of bright purple "
            "construction paper with triangle points cut along the top edge. "
            "Decorated with marker drawings, sticker dots, and a few small paper jewel cutouts "
            "in red, blue, and gold. The crown is laid open flat on a light craft table "
            "with crayons and paper scraps around it. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-bag-puppet.webp",
        "prompt": (
            "A handmade brown paper bag puppet made for a preschooler: the flap of the lunch bag "
            "forms a face with two big googly eyes glued on, a red paper smiling mouth, "
            "two paper triangle ears, and a few drawn-on whiskers. Standing upright on a craft table. "
            "Clearly child-made and slightly uneven. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-flower-garden.webp",
        "prompt": (
            "A handmade construction paper flower garden craft: several flowers in different shapes "
            "(tulips, daisies, simple round flowers) cut from bright pink, yellow, orange, and red paper, "
            "each glued onto a green paper strip stem with leaf cutouts. "
            "All arranged in a cheerful row on a white sheet of paper background. "
            "Flat lay on a light wood surface. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-heart-bouquet.webp",
        "prompt": (
            "A handmade paper heart bouquet: five paper hearts in pink, red, and white "
            "glued onto thin green paper stems, gathered together and tied with a simple "
            "ribbon at the base. Sitting on a white craft table. "
            "The hearts are slightly uneven, clearly cut by a preschooler. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strip-sun.webp",
        "prompt": (
            "A handmade preschool paper sun craft: a large yellow construction paper circle "
            "with a smiling marker face in the center, surrounded by many thin yellow "
            "and orange paper strips glued around the back as fanning rays. "
            "Taped to a window with bright daylight coming through. "
            "Cheerful and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-butterfly.webp",
        "prompt": (
            "A handmade tissue paper butterfly: bright pink and yellow tissue paper squares "
            "pinched in the middle with a colorful pipe cleaner twisted around the center, "
            "with the two ends of the pipe cleaner curled upward to make antennae. "
            "Lying flat on a white craft table. Charming and child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-apple-tree.webp",
        "prompt": (
            "A handprint paper apple tree craft: a child's small handprint and forearm "
            "traced and cut from brown construction paper to form a tree trunk and branches. "
            "Glued onto a white sheet, with small red paper apple circles and a few green "
            "paper leaf shapes attached around the branches. "
            "Lying flat on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cotton-ball-paper-sheep.webp",
        "prompt": (
            "A handmade preschool paper sheep craft: a black construction paper oval body "
            "covered entirely in fluffy white cotton balls glued tightly together. "
            "A round black paper face at one end with two googly eyes and a tiny pink paper "
            "triangle nose. Four small black paper rectangle legs at the bottom. "
            "Lying on a light wood craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pinwheel.webp",
        "prompt": (
            "A handmade rainbow paper pinwheel made from a square sheet of paper with diagonal "
            "cuts and folded points pinned to a wooden pencil with a small brad. "
            "The pinwheel has bright stripes of red, yellow, blue, and green. "
            "Held up against a sunny outdoor backdrop with grass blurred behind. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-snake-craft.webp",
        "prompt": (
            "A handmade paper snake craft: a colorful spiral cut from a round piece of green paper, "
            "decorated with marker stripes, dots, and zigzag patterns in red, yellow, and black. "
            "The head end has a googly eye and a small red paper forked tongue. "
            "Hanging from a child's hand so the spiral body uncoils and dangles below. "
            "Charming and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rocket.webp",
        "prompt": (
            "A handmade preschool paper rocket craft: a tube made of rolled blue construction paper "
            "with a small red cone on top and three triangle red fins around the base. "
            "Decorated with silver star and round planet stickers along the body. "
            "Standing upright on a white craft table. Clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-boat.webp",
        "prompt": (
            "A small handmade origami paper boat folded from a single sheet of bright blue "
            "construction paper, sitting on a light wood surface. The folds are clearly visible "
            "and slightly uneven, made by a young child. "
            "A second smaller red paper boat is barely visible behind it. "
            "Charming and warm. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fish-scales.webp",
        "prompt": (
            "A handmade paper fish craft: a large fish body shape cut from bright blue "
            "construction paper, with overlapping circles and teardrops in alternating "
            "colors (orange, yellow, pink, purple) glued along the body to form colorful scales. "
            "A googly eye near the mouth and a tail flipped to one side. "
            "Lying flat on a light craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-frog.webp",
        "prompt": (
            "A handmade preschool paper frog craft: a folded green construction paper frog "
            "with a wide cut-open mouth, two googly eyes glued on top of the folded head, "
            "and a small red paper tongue peeking from the mouth. "
            "Two folded green paper legs underneath. Sitting on a green oval paper lily pad "
            "on a craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-owl.webp",
        "prompt": (
            "A handmade preschool paper owl craft: a brown construction paper teardrop body shape "
            "with two large white circle eyes with small black paper pupils, "
            "a small yellow paper triangle beak, and two oval paper wings on the sides. "
            "Standing upright on a small folded paper base tab on a light craft table. "
            "Charming and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-snowflake.webp",
        "prompt": (
            "Three handmade white paper snowflakes, each cut from folded paper with delicate "
            "small notches and curves along the edges, creating different one-of-a-kind patterns. "
            "Lying on a light wood surface with a few small paper scraps around them. "
            "Soft natural lighting. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-ladybug.webp",
        "prompt": (
            "A handmade preschool paper ladybug craft: a bright red paper circle body "
            "with several black paper dot circles glued across the back, a smaller "
            "black half-circle head with two googly eyes and two thin black paper antennae. "
            "Sitting on a large green paper leaf shape on a light wood craft table. "
            "Clearly child-made. "
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
