#!/usr/bin/env python3
"""Generate all images for christmas-handprint-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "christmas-handprint-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
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
        "filename": "christmas-handprint-crafts.webp",
        "prompt": (
            "A colorful flat lay of handmade Christmas handprint crafts on a white craft table: "
            "a green handprint Christmas tree, a brown handprint reindeer, a red and white handprint Santa "
            "with a cotton beard, a white handprint snowman, a handprint angel with paint wings, "
            "and a handprint wreath. Each craft is made from a child's painted handprint on white paper. "
            "Red and green paint, paintbrushes, and paper scraps visible at the edges. "
            "Festive cozy Christmas mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-christmas-tree.webp",
        "prompt": (
            "A handmade Christmas tree made from green painted child handprints stacked in a column "
            "on white cardstock, fingers pointing downward to form layered tree branches. "
            "A small brown paper trunk at the bottom and a yellow paper star on top. "
            "Tiny colorful fingerprint dots act as ornaments. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-reindeer.webp",
        "prompt": (
            "A handmade reindeer made from a single brown painted child handprint on white paper, "
            "the palm forming the reindeer face and the spread fingers forming the antlers. "
            "Two googly eyes and a round red pom-pom nose glued on the palm. "
            "Charming and slightly uneven, clearly child-made. Flat lay on a wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-santa-claus.webp",
        "prompt": (
            "A handmade Santa Claus made from a child handprint on white paper turned upside down, "
            "the palm painted peach for the face and a red triangular paper hat above it, "
            "with a fluffy white cotton ball beard covering the four fingers and a cotton hat trim. "
            "Two small googly eyes and a tiny red nose. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-snowman.webp",
        "prompt": (
            "A handmade snowman made from a white painted child handprint on blue cardstock, "
            "the palm and fingers covered in white paint with three black dot buttons, "
            "an orange paper carrot nose, two black dot eyes, and a small black paper top hat. "
            "A tiny knitted-look paper scarf in red. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-christmas-angel.webp",
        "prompt": (
            "A handmade Christmas angel made from two white painted child handprints placed back to back "
            "to form wings on blue paper, with a folded white paper cone body and a round paper head "
            "with a gold pipe cleaner halo. Simple drawn smiling face. "
            "Soft and sweet, clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-christmas-wreath.webp",
        "prompt": (
            "A handmade Christmas wreath made from many green painted child handprints arranged "
            "in a circular ring on white cardstock, overlapping like leaves. "
            "Small red fingerprint berries dotted around and a red paper bow at the bottom. "
            "Cheerful and full, clearly made by a child. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-penguin.webp",
        "prompt": (
            "A handmade penguin made from a black painted child handprint on light blue paper, "
            "the palm forming the round penguin body with a white paper belly, "
            "an orange paper triangle beak and feet, and two small googly eyes. "
            "A tiny red paper scarf. Charming winter craft, clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-christmas-lights.webp",
        "prompt": (
            "A handmade Christmas lights craft on white paper: a swooping black drawn cord "
            "with colorful child fingerprints pressed all along it like dangling glowing bulbs, "
            "in red, green, blue, and yellow paint. A small marker base drawn on each bulb. "
            "Cheerful string of holiday lights, clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-poinsettia.webp",
        "prompt": (
            "A handmade poinsettia flower made from several red painted child handprints arranged "
            "in a star burst on white paper, fingers spread to form the pointed red petals. "
            "A cluster of small yellow pom-poms in the center. "
            "Bright festive Christmas flower, clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-candy-cane.webp",
        "prompt": (
            "A handmade candy cane made from red and white painted child handprints arranged "
            "in a curved candy cane stripe pattern on white cardstock, alternating red and white. "
            "A small green paper bow tied near the top curve. "
            "Cheerful and slightly uneven, clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-elf.webp",
        "prompt": (
            "A handmade Christmas elf made from a peach painted child handprint on white paper, "
            "the palm forming the elf face with a green and red striped paper hat with a pom-pom, "
            "two pointed paper ears, rosy cheeks, and a small smiling drawn face. "
            "Playful and cute, clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-mittens.webp",
        "prompt": (
            "A pair of handmade paper mittens made from two traced and cut child handprints "
            "on red and green cardstock, decorated with white cotton trim at the cuffs "
            "and glitter glue snowflake patterns. Connected by a length of yarn like a mitten string. "
            "Cozy winter craft, clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-christmas-stocking.webp",
        "prompt": (
            "A handmade Christmas stocking made from a traced and cut child handprint and forearm shape "
            "on red cardstock, forming an L-shaped stocking, with a white cotton fluffy cuff at the top "
            "and glitter glue decorations. A small paper name tag. "
            "Festive and sweet, clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-holly-berries.webp",
        "prompt": (
            "A handmade holly decoration made from green painted child handprints on white paper, "
            "fingers spread to form pointed holly leaves arranged in pairs, "
            "with a cluster of round red fingerprint or pom-pom berries in the center. "
            "Classic Christmas holly, clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-polar-bear.webp",
        "prompt": (
            "A handmade polar bear made from a white painted child handprint on light blue paper, "
            "the palm forming the round bear head and body, with two small white paper ears, "
            "a black paper nose, and two googly eyes. Soft and cuddly winter craft, "
            "clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-gingerbread-man.webp",
        "prompt": (
            "A handmade gingerbread man made from a brown painted child handprint on white paper, "
            "the palm forming the round body and the thumb and fingers as arms and legs, "
            "decorated with white glue dot buttons, a white zigzag icing smile, and two dot eyes. "
            "Warm and cheerful Christmas cookie craft, clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-christmas-card-keepsake.webp",
        "prompt": (
            "A handmade folded Christmas card with a small green handprint Christmas tree on the front "
            "and a child's handwritten Merry Christmas greeting. The card stands open on a craft table "
            "next to crayons and a red envelope. A heartfelt handmade keepsake, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-dove.webp",
        "prompt": (
            "A handmade peace dove made from a single white painted child handprint on light blue paper, "
            "the palm forming the dove body and the four fingers forming the wing feathers, "
            "the thumb as the head with a small orange paper beak and a green paper olive branch in its mouth. "
            "Gentle and sweet Christmas craft, clearly child-made. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "salt-dough-handprint-ornament.webp",
        "prompt": (
            "A handmade salt dough Christmas ornament with a small child's handprint pressed into the "
            "center of a round flat beige dough disc, painted with a red and green border, "
            "a hole at the top threaded with red ribbon for hanging. Sitting on a wood craft table "
            "next to pine sprigs. A treasured keepsake ornament, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-nativity-sheep.webp",
        "prompt": (
            "A handmade nativity sheep made from a white painted child handprint on brown paper, "
            "the palm forming the fluffy white wool body dabbed with cotton, "
            "a small grey or black paper head and ears, and four tiny paper legs. "
            "Two small dot eyes. Gentle Christmas nativity craft, clearly child-made. "
            "Flat lay on a craft table. "
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
