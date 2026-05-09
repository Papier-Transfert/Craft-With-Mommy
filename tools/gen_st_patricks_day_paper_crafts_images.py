#!/usr/bin/env python3
"""Generate all images for st-patricks-day-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "st-patricks-day-paper-crafts"
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
        "filename": "st-patricks-day-paper-crafts.webp",
        "prompt": (
            "A colorful flat lay of handmade St Patrick's Day paper crafts on a light wood craft table: "
            "a green paper shamrock garland, a paper plate rainbow with a small black pot of gold, "
            "a leprechaun paper bag puppet with an orange beard, a paper plate shamrock wreath, "
            "several gold paper coins, and a tall green paper leprechaun top hat. "
            "Scissors, glue stick, and green paper scraps visible at the edges. "
            "Festive March holiday mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-shamrock-garland.webp",
        "prompt": (
            "A handmade paper shamrock garland on a light wood surface: about ten green construction paper "
            "shamrocks of similar sizes strung along a piece of white yarn or string. "
            "Each shamrock has three rounded green leaves and a small green stem. "
            "The garland is laid out flat, gently curving across the table. "
            "Charming handmade look, slightly imperfect cuts. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-rainbow-pot-of-gold.webp",
        "prompt": (
            "A handmade paper plate rainbow craft: a paper plate cut in half forming an arch, "
            "with curved strips of red, orange, yellow, green, blue, and purple construction paper "
            "glued in rainbow rows across the top. A small black paper pot shape sits at one end "
            "with bright gold cardstock circle coins spilling out of it. "
            "Lying flat on a white craft table. Cheerful spring craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "leprechaun-paper-bag-puppet.webp",
        "prompt": (
            "A handmade leprechaun paper bag puppet made from a small brown paper lunch bag: "
            "the flap forms a face with a circle nose, marker-drawn smile, and round eyes. "
            "A tall green paper top hat with a yellow square buckle is glued at the top of the flap, "
            "and a curly orange paper beard hangs below the face. "
            "Standing upright on a craft table. Playful and friendly look, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-heart-shamrock.webp",
        "prompt": (
            "A handmade paper shamrock craft made from four green construction paper hearts "
            "arranged with their points meeting in the center to form a four-leaf clover shape. "
            "A small green paper stem at the bottom. Glued onto white cardstock. "
            "Lying flat on a light wood craft table. Slightly uneven hearts, clearly cut by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-shamrock-card.webp",
        "prompt": (
            "A handmade St Patrick's Day greeting card with a chunky shamrock built from four "
            "green paper handprints arranged with all the wrists meeting in the center. The fingers "
            "of each handprint splay outward like the leaves of a shamrock. The card is folded "
            "white cardstock, opened slightly to show the handprint shamrock on the front. "
            "Lying on a craft table. Sweet, child-made look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strip-shamrock.webp",
        "prompt": (
            "A handmade dimensional paper shamrock craft: three long green construction paper strips, "
            "each looped into a teardrop shape, glued together at the bottom point with a tiny green "
            "paper stem. The looped petals create a 3D shamrock that stands slightly above the surface. "
            "Lying on a light wood craft table. Charming and clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-leprechaun-hat.webp",
        "prompt": (
            "A handmade paper leprechaun top hat made from green cardstock rolled into a tall cylinder "
            "with a wide flat circular brim attached at the base. A black paper band wraps around "
            "the bottom of the cylinder with a yellow square paper buckle on the front. "
            "The hat sits upright on a craft table next to scissors and green paper scraps. "
            "Slightly lopsided and charming, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pot-of-gold.webp",
        "prompt": (
            "A handmade paper pot of gold craft on white cardstock: a black paper pot shape with a "
            "curved bottom and a wide rim, glued flat. Several shiny gold metallic cardstock circles "
            "are piled inside the pot and spilling over the rim like coins. A few small marker-drawn "
            "sparkle stars surround the pot. Lying flat on a craft table. "
            "Bright, cheerful, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rainbow-mobile.webp",
        "prompt": (
            "A handmade paper rainbow mobile: a white cloud-shaped piece of cardstock with curved "
            "rainbow paper strips in red, orange, yellow, green, blue, and purple glued in arches "
            "across the front. Small paper raindrops in light blue dangle from the bottom of the "
            "cloud on white threads. Hanging against a light wall near a window. "
            "Cheerful spring craft, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-shamrock-suncatcher.webp",
        "prompt": (
            "A handmade shamrock suncatcher: a large green construction paper shamrock outline "
            "with the inside cut out, filled with overlapping squares of green and yellow tissue paper "
            "taped across the back. Stuck to a window with sunlight glowing through the tissue paper "
            "like stained glass. Bright, glowing colors. Charming child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-shamrock-wreath.webp",
        "prompt": (
            "A handmade paper plate shamrock wreath: a paper plate with the center cut out forming a ring, "
            "wrapped in green construction paper, with about eight small green paper shamrocks glued "
            "evenly around the front of the ring. A green ribbon bow is tied at the top for hanging. "
            "Hanging on a light wall or laid flat on a craft table. Festive March decor, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-shamrock-crown.webp",
        "prompt": (
            "A handmade paper shamrock crown: a long strip of green construction paper sized to fit "
            "around a child's head, with five green paper shamrocks glued across the front so they "
            "stand up like crown points. Several small gold star stickers are placed between the "
            "shamrocks. Lying flat on a light wood craft table. Cheerful, child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-shamrock.webp",
        "prompt": (
            "A handmade origami shamrock craft: a small four-leaf clover made by folding four small "
            "squares of green origami paper into heart-shaped petals, then arranging the four hearts "
            "with their points meeting in the center on a wooden craft table. Crisp paper folds visible. "
            "Charming handmade look, with a small folded paper stem. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-lucky-charm-necklace.webp",
        "prompt": (
            "A handmade paper lucky charm necklace: a long piece of yarn or thin ribbon threaded with "
            "small paper charms including a green paper shamrock, a gold paper coin, a brown paper "
            "horseshoe, and a small paper rainbow. The necklace is laid out flat in a loop on a "
            "white craft table. Cheerful, child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-leprechaun-beard.webp",
        "prompt": (
            "A handmade orange paper leprechaun beard: a wide curly beard cut from orange construction "
            "paper with curls created by accordion folds and rolled paper strips along the bottom edge. "
            "Two small ear loops attached to the sides for wearing. The beard is lying flat on a "
            "light wood craft table next to scissors and orange paper scraps. Silly, playful, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-coin-garland.webp",
        "prompt": (
            "A handmade gold paper coin garland: about ten round shiny gold metallic cardstock circles "
            "with shamrocks and dollar signs drawn on each one, taped along a long piece of green "
            "ribbon. The garland is laid out gently across a light wood craft table. "
            "Festive March holiday decoration, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shamrock-stamp-print.webp",
        "prompt": (
            "A handmade shamrock stamp print: a piece of white paper covered in a repeating pattern "
            "of green stamped shamrocks made by pressing a paper-shamrock stamp glued to a small "
            "cardboard block. The stamp itself sits beside the print on a craft table along with a "
            "small dish of green paint. Charming child-made craft, slightly imperfect prints. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cup-leprechaun.webp",
        "prompt": (
            "A handmade paper cup leprechaun craft: a small paper cup wrapped in green construction "
            "paper, with a small skin-toned circle face glued on the front, two googly eyes, a "
            "marker-drawn smile, a curly orange paper beard glued under the face, and a wide-brim "
            "green paper hat with a yellow paper buckle on top. Standing upright on a light wood "
            "craft table. Charming and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lucky-greeting-card.webp",
        "prompt": (
            "A handmade St Patrick's Day greeting card: white folded cardstock with three green paper "
            "shamrocks, a small paper rainbow with a gold paper coin, and a handwritten message "
            "reading 'Happy St Patrick's Day' in green marker on the front. The card is open slightly "
            "showing a tiny gold paper coin tucked inside. Lying on a craft table. Sweet, child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-leprechaun-face.webp",
        "prompt": (
            "A handmade paper plate leprechaun face craft: a paper plate painted in a soft skin tone, "
            "with a curly orange paper beard glued around the lower half of the plate, two googly eyes, "
            "a small pink paper smile, and a green paper top hat with a yellow buckle glued on top. "
            "Lying flat on a light wood craft table. Cheerful and clearly child-made. "
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
