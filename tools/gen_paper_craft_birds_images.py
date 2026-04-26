#!/usr/bin/env python3
"""Generate all images for paper-craft-birds.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-craft-birds"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper and craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-craft-birds.webp",
        "prompt": (
            "A bright flat lay of handmade paper craft birds spread across a white craft table: "
            "a paper plate owl with big yellow eyes, a red cardstock cardinal, a paper bowl penguin, "
            "an origami crane, a colorful peacock with paper strip tail feathers, a yellow paper duck, "
            "and a pink flamingo from a paper cup. Scissors, glue stick, googly eyes, and "
            "scraps of construction paper visible at the edges. "
            "Cheerful and playful collection of paper bird crafts, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-owl-bird.webp",
        "prompt": (
            "A handmade paper plate owl craft made from a regular white paper plate painted brown, "
            "with two large white circle eyes glued on, big black googly eye pupils, "
            "a small orange triangle paper beak, and two pointed paper ear tufts at the top. "
            "Brown paper feather shapes glued on the body for texture. Sitting flat on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-cardinal.webp",
        "prompt": (
            "A handmade paper cardinal bird craft made from bright red construction paper: "
            "a rounded body shape, a triangular crest on top of the head, a small black face mask area, "
            "a tiny orange paper beak, one googly eye, and a single red paper tail. "
            "Glued onto a small brown paper branch with two tiny green leaves. "
            "Lying flat on a light wood craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-bowl-penguin.webp",
        "prompt": (
            "A handmade paper bowl penguin craft made from an upside down white paper bowl "
            "painted black on the back to form the body. A white paper oval glued on the front for the belly, "
            "two googly eyes, a small orange triangle beak, two tiny black paper flipper wings on the sides, "
            "and two orange triangular feet poking out at the bottom. Standing on a white craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-paper-crane.webp",
        "prompt": (
            "A handmade origami paper crane folded from a single square of light blue paper. "
            "Wings raised slightly, long folded neck and beak, classic origami crane shape. "
            "Crisp visible folds. Standing upright on a wooden craft table next to a small piece of square origami paper "
            "and a few orange and yellow folded squares. Clearly handmade and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strip-peacock.webp",
        "prompt": (
            "A handmade paper peacock craft made from layered colored paper strips fanned out as a tail: "
            "blue, green, purple, and teal paper strips arranged in a fan shape, each ending in a small "
            "round eye spot of yellow and dark blue paper. A round dark blue paper body with two googly eyes, "
            "a tiny orange beak, and a small crest of three thin paper feathers at the top. "
            "Lying flat on a craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-eagle-bird.webp",
        "prompt": (
            "A handmade handprint paper eagle craft: a small child's tracing on brown construction paper "
            "with two tan handprint outlines for the spread wings, glued on either side of a brown body. "
            "A white paper head with a yellow triangle beak and one googly eye. "
            "Glued onto a light cardstock background. Clearly child-made and slightly uneven. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cup-flamingo.webp",
        "prompt": (
            "A handmade paper flamingo craft built around an upside down pink paper cup as the body. "
            "A long pink paper neck curves up from the top of the cup, ending in a flat pink head shape "
            "with a black and pink paper beak and one googly eye. Two pink paper wings on the sides, "
            "and two thin pink paper legs sticking out underneath. "
            "Standing on a white craft table. Charming and playful. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "toilet-roll-robin-bird.webp",
        "prompt": (
            "A handmade toilet paper roll robin craft: a cardboard tube covered in brown construction paper, "
            "with a bright red-orange paper oval glued on the front for the breast. Two small brown paper wings "
            "on the sides, two googly eyes, a tiny yellow triangle beak, and a small brown paper tail at the back. "
            "Standing upright on a wooden craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-parrot.webp",
        "prompt": (
            "A handmade paper plate parrot craft made from a paper plate cut in half and folded "
            "to form the body. The body is colored bright red, with overlapping yellow, blue, and green "
            "paper feather strips along the back and tail. A round red head with a curved black paper beak, "
            "one googly eye, and bright blue paper wing pieces. Lying flat on a white craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-bag-chicken.webp",
        "prompt": (
            "A handmade paper bag chicken craft using a small white paper lunch bag as the body. "
            "A round white paper head with a small red paper comb on top, a yellow triangle beak, "
            "two googly eyes, and a tiny red wattle. White paper wings on the sides and yellow paper feet "
            "poking out at the bottom. Clearly child-made and slightly lopsided, sitting on a wooden craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-bluebird-craft.webp",
        "prompt": (
            "A handmade bluebird craft made from bright blue construction paper: a teardrop body shape, "
            "an orange paper chest patch, two folded blue paper wings, a small triangular blue paper tail, "
            "a tiny yellow beak, and one googly eye. Glued onto a light cardstock background. "
            "Lying flat on a craft table. Clearly handmade by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-toucan-craft.webp",
        "prompt": (
            "A handmade toucan paper craft: a black construction paper rounded body with a white paper "
            "throat patch. A huge curved paper beak made of bright orange and yellow paper layers. "
            "One large googly eye, a green paper accent around the eye area, and small black paper feet. "
            "Glued flat on a light cardstock background with a green paper leaf nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-hummingbird.webp",
        "prompt": (
            "A handmade tissue paper hummingbird craft made from a small green and purple cardstock body shape "
            "with two crinkled green tissue paper wings glued on each side, slightly raised from the body. "
            "A long thin black paper beak, a tiny googly eye, and a small fanned paper tail. "
            "Glued near a small pink paper flower. Lying flat on a white craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-paper-pigeon.webp",
        "prompt": (
            "A handmade simple origami pigeon folded from a square of light grey paper, "
            "with a small triangle beak fold and a folded tail flap. The fold is a gentle classic "
            "paper bird shape, slightly imperfect. Sitting on a wooden craft table next to two more "
            "smaller folded paper birds. Clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-duck.webp",
        "prompt": (
            "A handmade paper plate duck craft: a yellow painted paper plate as the body, a small yellow "
            "paper circle head with one googly eye and an orange triangle paper beak. Two small yellow paper "
            "wings on the sides, and two orange webbed paper feet at the bottom. "
            "Lying flat on a light wood craft table. Cheerful and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-swan.webp",
        "prompt": (
            "A handmade paper swan craft made from white construction paper: a round body shape with a long "
            "curved neck, a small head with a tiny orange triangle beak and one googly eye. "
            "A row of fanned white paper feather strips along the back of the body for wings. "
            "Glued flat on a soft blue paper background to look like water. Charming and clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roll-woodpecker.webp",
        "prompt": (
            "A handmade paper roll woodpecker craft: a cardboard toilet paper tube covered in red construction paper "
            "around the head and black on the body, with two small white paper wing patches on the sides. "
            "A long pointed black paper beak, two googly eyes, and a small red feather crest at the top of the head. "
            "Standing upright on a wooden craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pelican-craft.webp",
        "prompt": (
            "A handmade paper pelican craft: a large rounded white construction paper body with a small white "
            "head, a tiny dark eye, and a very large yellow paper beak with a wide pouch underneath. "
            "Two short paper wings on the sides and two small orange feet at the base. "
            "Glued flat on a light blue paper background to suggest water. Clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strip-crow.webp",
        "prompt": (
            "A handmade paper crow craft made from black construction paper: a rounded body with a "
            "tail of three black paper strip feathers, two folded black paper wings, a small black head, "
            "a yellow triangle beak, and one bright googly eye. Glued onto a brown paper branch. "
            "Lying flat on a craft table. Charming and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-rooster.webp",
        "prompt": (
            "A handmade paper plate rooster craft: a paper plate cut in half and turned vertically as the body, "
            "painted brown and orange. A red paper comb on top of a round head, a tiny yellow paper beak, "
            "a red paper wattle, one googly eye, and a colorful fan of red, orange, and yellow paper strip "
            "feathers as the long tail rising behind the body. Sitting flat on a craft table. "
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
