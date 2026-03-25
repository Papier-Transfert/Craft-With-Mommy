#!/usr/bin/env python3
"""Generate all images for paper-halloween-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-halloween-crafts"
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
        "filename": "paper-halloween-crafts.webp",
        "prompt": (
            "A colorful flat lay of handmade paper Halloween crafts on a white craft table: "
            "black paper bats with googly eyes, an orange cardstock jack-o-lantern, "
            "a white paper ghost garland, a paper black cat silhouette on an orange moon, "
            "a paper witch hat, a paper roll mummy, and paper candy corn pieces. "
            "Scissors, glue stick, and construction paper scraps visible at the edges. "
            "Festive Halloween mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-bat-mobile.webp",
        "prompt": (
            "A handmade paper bat mobile with three black construction paper bat shapes "
            "hanging on strings from a small wooden twig. Each bat has two small googly eyes. "
            "Photographed against a light background. Bats hang at different heights. "
            "String is clearly visible. Charming handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-jack-o-lantern.webp",
        "prompt": (
            "A handmade paper jack-o-lantern made from a large orange cardstock circle "
            "with cut-out black paper triangular eyes, a square black nose, "
            "and a jagged smiling mouth glued on. Small green paper stem at the top. "
            "Lying flat on a wooden craft table with orange paper scraps around it. "
            "Clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-ghost-garland.webp",
        "prompt": (
            "A handmade paper ghost garland made from accordion-folded white paper "
            "with five connected ghost shapes cut out, each ghost slightly different. "
            "The chain of ghosts is laid out flat on a light wood surface. "
            "Simple friendly ghost shapes with small dot eyes drawn on. "
            "Cheerful Halloween craft, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spider-web.webp",
        "prompt": (
            "A handmade paper spider sitting on a white chalk marker spider web drawn "
            "on a piece of black construction paper. The spider is made from a black paper "
            "circle body with eight thin black strip legs and two small googly eyes. "
            "The web has concentric circles connected by straight radial lines drawn in white. "
            "Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-witch-hat.webp",
        "prompt": (
            "A handmade wearable paper witch hat made from black cardstock rolled into a tall cone "
            "with a wide flat brim circle attached at the base. An orange paper band wraps around "
            "the base of the cone. The hat sits on a craft table next to scissors and black paper scraps. "
            "The hat is slightly lopsided and charming, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roll-mummy.webp",
        "prompt": (
            "A handmade paper roll mummy craft: a small tube made from rolled white paper, "
            "wrapped with thin white paper strips criss-crossing like bandages. "
            "Two googly eyes peek out from between the wrapping near the top. "
            "Stands upright on a light wood craft table. Playful and cute Halloween craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-skeleton-collage.webp",
        "prompt": (
            "A handmade paper skeleton collage: white paper oval and rectangle shapes "
            "cut and arranged to look like a full skeleton including a skull, ribcage, "
            "arms, legs, and hands, all glued onto a black construction paper background. "
            "The shapes are uneven and clearly cut by a child. Clean flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-black-cat-silhouette.webp",
        "prompt": (
            "A handmade paper black cat silhouette with two pointy ears and a curved tail "
            "glued onto a large bright orange circle cut from cardstock, representing a full moon. "
            "Displayed against a dark background. Bold, graphic Halloween craft look. "
            "The cat shape is clearly cut by a child, slightly uneven edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-trick-or-treat-bag.webp",
        "prompt": (
            "A handmade trick-or-treat bag made from folded orange cardstock stapled at the sides "
            "with a purple ribbon handle threaded through two holes at the top. "
            "Decorated with a child's marker drawings of a jack-o-lantern face and small stars. "
            "Sitting upright on a craft table with paper scraps around it. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-pumpkin.webp",
        "prompt": (
            "A handmade origami pumpkin folded from an orange square of paper, "
            "three-dimensional with visible fold lines creating a rounded pumpkin shape. "
            "A small twisted green paper strip serves as the stem on top. "
            "Sitting on a wooden surface next to two more smaller orange origami pumpkins. "
            "Autumn craft feel, warm lighting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-haunted-house.webp",
        "prompt": (
            "A handmade paper haunted house scene: a dark grey paper house shape with "
            "yellow rectangle window cutouts, a crooked paper moon, and small white ghost shapes "
            "peeking from behind the roofline. All glued on a black background. "
            "Bare tree shapes cut from dark paper framing the sides. "
            "Flat on a craft table. Spooky Halloween mood, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-monster-bookmark.webp",
        "prompt": (
            "A handmade paper monster bookmark: a green paper rectangle with the top two corners "
            "folded down to form a pointed monster face pocket. Decorated with large googly eyes, "
            "small white paper triangle teeth, and two tiny paper horns at the top corners. "
            "Sitting on the corner of an open book, gripping the page. "
            "Cute and playful Halloween craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-frankenstein.webp",
        "prompt": (
            "A handmade paper Frankenstein face craft: a large light green construction paper "
            "rectangle for the head with black paper hair across the top, two small grey square "
            "neck bolts on the sides, two googly eyes, marker-drawn stitches across the forehead, "
            "heavy black crayon eyebrows, and a flat drawn grin with small teeth. "
            "Lying flat on a craft table. Friendly and silly Halloween craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-owl.webp",
        "prompt": (
            "A handmade paper owl craft made from an orange paper teardrop body shape "
            "with two large white circle eyes with black paper pupils, "
            "a small orange triangle beak, and two accordion-folded brown paper wings "
            "attached to the sides. Standing upright on a craft table via a folded paper base tab. "
            "Charming autumn Halloween craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-vampire-mask.webp",
        "prompt": (
            "A handmade paper vampire mask made from a wide oval of black cardstock "
            "with a dramatic widow's peak cut at the top center, two eye holes, "
            "a white scalloped paper collar glued at the bottom, and white drawn-on vampire fangs. "
            "Lying flat on an orange craft table surface next to scissors and a glue stick. "
            "Fun and spooky Halloween craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-scarecrow.webp",
        "prompt": (
            "A handmade paper scarecrow craft made from layered paper shapes: "
            "a straw hat cut from brown paper, a patchy colourful shirt, ragged trouser shapes, "
            "and yellow paper strip fringe poking out from the hat brim and sleeve cuffs. "
            "Mounted on a brown paper stick. Autumn Halloween craft feel. "
            "Displayed flat on a craft table, cheerful and slightly wonky. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-eyeball-wreath.webp",
        "prompt": (
            "A handmade paper eyeball wreath: a large cardstock ring covered in white paper circles "
            "of various sizes, each one decorated with a colored iris (blue, green, brown) "
            "and a black paper pupil. Dozens of eyes covering the entire ring. "
            "Lying flat on a dark background. Creepy and fun Halloween craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-witch-broomstick.webp",
        "prompt": (
            "A handmade paper witch silhouette with a tall pointy hat and a flowing triangular cape, "
            "cut from black construction paper. Attached to a broomstick made from a brown paper stick "
            "with yellow paper strip fringe bristles at one end. Hanging from a white thread "
            "against a light wall as if flying. Charming spooky Halloween craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-candy-corn.webp",
        "prompt": (
            "Several handmade paper candy corn pieces made from stacked white, orange, "
            "and yellow construction paper triangles in the classic candy corn shape. "
            "Five or six pieces arranged in a cheerful cluster on a white craft table. "
            "Each one slightly different size, clearly cut by a child. "
            "Bright and cheerful Halloween craft photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pumpkin-chain.webp",
        "prompt": (
            "A handmade paper pumpkin chain garland: orange paper ring loops each decorated "
            "with a marker jack-o-lantern face, linked together with smaller black paper rings "
            "as spacers. The garland is draped loosely on a light wood surface showing about "
            "eight pumpkin rings. Festive Halloween decoration, clearly child-made. "
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
