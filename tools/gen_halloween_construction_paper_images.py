#!/usr/bin/env python3
"""Generate all images for halloween-construction-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "halloween-construction-paper-crafts"
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
        "filename": "halloween-construction-paper-crafts.webp",
        "prompt": (
            "A colorful flat lay of handmade halloween construction paper crafts on a white craft table: "
            "an orange paper jack-o-lantern with black triangle eyes and a jagged mouth, "
            "several black construction paper bats with googly eyes, a white paper ghost garland, "
            "a black cat silhouette on an orange paper moon, a black paper witch hat with an orange band, "
            "paper candy corn pieces in white orange and yellow, and a paper mummy. "
            "Scissors, glue stick, and orange and black construction paper scraps visible at the edges. "
            "Festive Halloween mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-jack-o-lantern.webp",
        "prompt": (
            "A handmade paper jack-o-lantern made from a large orange construction paper circle "
            "with black paper triangle eyes, a small square black nose, "
            "and a wide jagged smiling mouth all glued on. A short green paper stem at the top. "
            "Lying flat on a wooden craft table with orange and black paper scraps nearby. "
            "Clearly child-made, slightly imperfect, and very charming. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-bat.webp",
        "prompt": (
            "Several handmade black construction paper bats laid flat on a light wood craft table. "
            "Each bat has symmetrical wings cut from folded black paper and a small oval body. "
            "Two googly eyes glued onto each bat face. Different sizes. "
            "Scissors and black paper strips visible nearby. "
            "Playful and cute Halloween craft, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-ghost-garland.webp",
        "prompt": (
            "A handmade paper ghost garland made from accordion-folded white construction paper "
            "with five connected ghost shapes cut out, each slightly different. "
            "The chain of ghosts is laid flat on a light wood surface. "
            "Simple friendly ghost shapes with small dot eyes drawn on with a black marker. "
            "White paper accordion folds visible at each side where the ghosts connect. "
            "Cheerful Halloween craft, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spider-and-web.webp",
        "prompt": (
            "A handmade paper spider sitting on a white chalk marker spider web drawn "
            "on a piece of black construction paper. The spider body is a black paper circle "
            "with eight thin black paper strip legs and two small googly eyes. "
            "The web has concentric circles connected by straight white radial lines. "
            "Flat lay on a craft table with white chalk marker and paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "black-cat-paper-craft.webp",
        "prompt": (
            "A handmade black cat paper silhouette with two pointy ears and a curved tail "
            "cut from black construction paper and glued onto a large bright orange circle "
            "representing a full moon. Displayed on a light wood craft table surface. "
            "Bold, graphic Halloween craft. The cat shape is clearly cut by a child, slightly uneven edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-witch-hat.webp",
        "prompt": (
            "A handmade wearable paper witch hat made from black construction paper rolled into a tall cone "
            "with a wide flat brim circle attached at the base. An orange paper band wraps around "
            "the lower part of the cone. Sitting on a craft table next to scissors and black paper scraps. "
            "The hat is slightly lopsided and charming, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-frankenstein-craft.webp",
        "prompt": (
            "A handmade paper Frankenstein face craft: a large light green construction paper "
            "rectangle for the head with a strip of black paper hair across the top, "
            "two small grey square neck bolts on the sides, two googly eyes glued on, "
            "thick black crayon eyebrows, and a flat drawn grin with stitches drawn in black marker. "
            "Lying flat on a craft table. Friendly and silly Halloween craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-paper-skeleton.webp",
        "prompt": (
            "A handmade paper skeleton collage: white paper oval and rectangle shapes "
            "cut and arranged to look like a full skeleton including a skull, ribcage, "
            "arms, legs, and hands, all glued onto a black construction paper background. "
            "The shapes are uneven and clearly cut by a child. Clean flat lay photo on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-paper-owl.webp",
        "prompt": (
            "A handmade halloween paper owl craft made from an orange construction paper teardrop body shape "
            "with two large white circle eyes with black paper pupils, "
            "a small orange triangle beak, and two accordion-folded brown paper wings attached to the sides. "
            "Standing upright on a craft table via a folded paper base tab. "
            "Charming autumn Halloween character, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-candy-corn-craft.webp",
        "prompt": (
            "Several handmade paper candy corn pieces made from stacked white, orange, "
            "and yellow construction paper triangle shapes in the classic candy corn pattern. "
            "Five or six pieces arranged in a cheerful cluster on a white craft table. "
            "Each one slightly different size, clearly cut by a child. "
            "Bright and cheerful Halloween craft photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-mummy.webp",
        "prompt": (
            "A handmade construction paper mummy craft: a white oval body shape "
            "with thin horizontal strips of white paper glued across it in overlapping layers like bandages. "
            "Two googly eyes peeking out from between the wrapping near the top. "
            "Displayed flat on a light wood craft table. Playful and cute Halloween craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-paper-bat-mobile.webp",
        "prompt": (
            "A handmade paper bat mobile with three black construction paper bat shapes "
            "hanging on strings from a small wooden twig at different heights. "
            "Each bat has two small googly eyes. Photographed against a light background. "
            "String is clearly visible. Charming handmade Halloween decoration. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-haunted-house.webp",
        "prompt": (
            "A handmade paper haunted house scene: a dark grey paper house shape with a peaked roof "
            "and yellow rectangle window cutouts, a crooked paper moon, "
            "and small white ghost shapes peeking from behind the roofline. "
            "Bare tree shapes cut from dark paper framing the sides. "
            "All glued on a black construction paper background. "
            "Flat on a craft table. Spooky Halloween mood, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-paper-witch.webp",
        "prompt": (
            "A handmade paper witch craft: a tall black pointed hat, a wide triangular black cape body, "
            "stick arms, and a small circular pale head with a tiny orange paper nose and a drawn grin. "
            "Mounted on a brown paper stick with yellow paper strip fringe bristles as a broomstick. "
            "Displayed flat on a light wood craft table. Spooky and fun Halloween character. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-paper-cauldron.webp",
        "prompt": (
            "A handmade paper cauldron cut from black construction paper, "
            "wide and round at the bottom with slightly flared sides and a rim at the top. "
            "A looping black paper strip handle attached at the top. "
            "Colorful paper scraps in green, purple, and orange layered inside the top opening "
            "to represent bubbling potion. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-vampire.webp",
        "prompt": (
            "A handmade construction paper vampire craft: a pale oval face with a sharp black widow's peak "
            "paper hairline at the top, two small white paper fangs at the bottom, "
            "a dramatic wide black paper cape behind the body. "
            "Thin arched eyebrows and sleepy eyes drawn with a black marker. "
            "Lying flat on an orange craft table surface. Fun and spooky Halloween craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-eyeball-garland.webp",
        "prompt": (
            "A handmade paper eyeball garland: white construction paper circles of various sizes "
            "each decorated with a colored iris (blue, green, or brown) drawn with markers "
            "and a black paper pupil glued on. The circles are threaded onto string "
            "and displayed as a garland across a light wood surface. "
            "Creepy and fun Halloween decoration, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-paper-lantern.webp",
        "prompt": (
            "A handmade halloween paper lantern made from a sheet of orange construction paper "
            "with parallel vertical cuts from the fold forming a rounded barrel shape when rolled into a cylinder. "
            "A strip of black paper serves as the handle at the top. "
            "Two or three lanterns in orange and black grouped together on a craft table. "
            "Warm Halloween atmosphere, charming and clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-paper-scarecrow.webp",
        "prompt": (
            "A handmade paper scarecrow craft made from layered construction paper shapes: "
            "a brown straw hat with yellow paper strip fringe peeking out from the brim, "
            "a colorful patchwork paper shirt in multiple colors, trouser shapes, "
            "and yellow paper fringe at the cuffs for straw hands. Mounted on a brown paper stick. "
            "Autumn Halloween craft feel. Displayed flat on a craft table, cheerful and slightly wonky. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-trick-or-treat-bag.webp",
        "prompt": (
            "A handmade trick-or-treat bag made from folded orange construction paper "
            "stapled at the sides with a purple ribbon handle threaded through two holes at the top. "
            "Decorated with a child's marker drawings of a jack-o-lantern face and small bats. "
            "Sitting upright on a craft table with orange and black paper scraps around it. "
            "Fun and festive Halloween craft, clearly child-made. "
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
