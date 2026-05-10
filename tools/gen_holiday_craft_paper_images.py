#!/usr/bin/env python3
"""Generate all images for holiday-craft-paper.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "holiday-craft-paper"
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
        "filename": "holiday-craft-paper.webp",
        "prompt": (
            "A festive flat lay of handmade holiday paper crafts on a white craft table: "
            "a pink and red paper heart garland, a small Halloween paper pumpkin lantern, "
            "a brown paper turkey with colorful feathers, white paper snowflakes, "
            "a small layered paper Christmas tree, a green paper shamrock, "
            "and a few pastel paper Easter eggs. "
            "Scissors, a glue stick, and bakers twine visible at the edges. "
            "Festive multi-holiday spread, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "valentines-heart-garland.webp",
        "prompt": (
            "A handmade Valentine's Day heart garland made from paper hearts in pink, red, and white "
            "strung on a piece of natural twine. About eight hearts of slightly different sizes. "
            "Draped against a soft light wall, with the twine sagging gently between hearts. "
            "Clearly child-made with slightly uneven heart edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "heart-pop-up-card.webp",
        "prompt": (
            "A handmade Valentine's pop-up greeting card opened to reveal a layered red and pink "
            "paper heart standing up from the inside fold. White cardstock outer card, "
            "layered hearts in two sizes glued onto a small pop-up paper shelf in the middle. "
            "Sitting on a craft table with paper scraps and a glue stick beside it. "
            "Charming and handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shamrock-paper-wreath.webp",
        "prompt": (
            "A handmade St. Patrick's Day shamrock wreath made from layered green paper shamrocks "
            "in two shades of green glued around a paper plate ring with the center cut out. "
            "A green ribbon bow tied at the top for hanging. The wreath is full and lush with overlapping "
            "shamrocks. Hanging against a light wood door or wall. Clearly child-made with charming uneven cuts. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "easter-egg-garland.webp",
        "prompt": (
            "A handmade Easter egg paper chain garland with about seven pastel paper egg shapes "
            "decorated with marker stripes, dots, and zigzag patterns in soft pastel colors "
            "of yellow, pink, mint green, and lavender. Strung on natural twine and draped across a "
            "light wall. Each egg is slightly different and clearly decorated by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "easter-bunny-mask.webp",
        "prompt": (
            "A handmade white paper Easter bunny mask laid flat on a light wood craft table. "
            "Wide oval mask shape with two cut-out eye holes, two tall white paper bunny ears with "
            "pink paper inner ears, a small pink paper triangle nose, and three thin pipe-cleaner "
            "whiskers on each side. Two small holes punched at the sides with thin elastic tied through. "
            "Clearly child-made with charming imperfections. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "mothers-day-tulip-bouquet.webp",
        "prompt": (
            "A handmade Mother's Day card showing a paper tulip bouquet of pink, yellow, and purple "
            "paper tulip shapes with green paper stems and leaves, tied with a paper ribbon in the "
            "middle. Glued onto a folded green cardstock card. Sitting flat on a light craft table. "
            "Clearly made by a young child with imperfect cut edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fathers-day-tie-card.webp",
        "prompt": (
            "A handmade Father's Day card shaped like a dress shirt, made from white cardstock folded "
            "in half with a small triangle cut at the top to form a shirt collar. A blue and white "
            "striped paper necktie glued in the middle and a small paper button at the collar. "
            "Lying flat on a light wood craft table. Clearly handmade by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fourth-july-star-banner.webp",
        "prompt": (
            "A handmade Fourth of July paper star banner with about eight chunky paper stars in red, "
            "white, and blue cardstock strung along natural baker's twine. Some stars decorated with "
            "silver glitter dots or marker dots. Banner draped across a light wooden porch railing in "
            "warm summer daylight. Clearly child-made with charming uneven cuts. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-pumpkin-lantern.webp",
        "prompt": (
            "A handmade Halloween paper pumpkin lantern made from orange construction paper rolled into "
            "a tube with vertical cut-out slits glowing softly with a small battery tea light inside. "
            "A small green paper stem on top and a thin paper handle. Sitting on a wooden table at dusk "
            "with warm light shining through the slits. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "halloween-bat-mobile.webp",
        "prompt": (
            "A handmade Halloween bat mobile with three black construction paper bat shapes in different "
            "sizes, each with two small googly eyes, hanging on thin black thread at different heights "
            "from a small wooden twig. Hanging against a light wall. Charming and friendly Halloween craft, "
            "clearly child-made with slightly uneven bat shapes. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "thanksgiving-paper-turkey.webp",
        "prompt": (
            "A handmade Thanksgiving paper turkey craft with a brown paper teardrop body and "
            "colorful red, orange, and yellow paper feathers fanning out behind it. Two googly eyes, "
            "a small orange paper triangle beak, and a red paper waddle. Each feather has a "
            "child-handwritten name. Sitting flat on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "thanksgiving-gratitude-tree.webp",
        "prompt": (
            "A handmade Thanksgiving gratitude tree on cardstock: a brown paper bare tree trunk and "
            "branches with about ten paper leaves in red, orange, and yellow taped on. "
            "Each leaf has a short child-handwritten gratitude message. The tree is on a piece of "
            "white cardstock displayed on a craft table. Cozy autumn feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "hanukkah-paper-menorah.webp",
        "prompt": (
            "A handmade Hanukkah paper menorah on a wide blue cardstock base with nine tall paper "
            "candles standing up. The middle shamash candle is slightly taller than the eight others. "
            "Each candle topped with a small yellow and orange paper flame. Sitting flat on a craft table. "
            "Clearly child-made with charming uneven cuts. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "diwali-paper-lantern.webp",
        "prompt": (
            "A handmade Diwali paper lantern made from bright orange and pink construction paper folded "
            "and snipped with evenly spaced vertical slits, glued into a small cylindrical lantern shape "
            "with a paper handle on top. Displayed on a wooden table with warm cozy lighting. "
            "Bright and festive Diwali craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "christmas-paper-snowflakes.webp",
        "prompt": (
            "A row of five handmade white paper snowflakes taped to a sunny window with thread, each one "
            "showing a different lacy cut-out pattern. Soft daylight shines through, highlighting the "
            "delicate cut shapes. Clearly child-made with slight asymmetry, charming imperfect snowflake patterns. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-christmas-tree-card.webp",
        "prompt": (
            "A handmade Christmas card on white cardstock with three layered green paper triangles in "
            "different sizes stacked to form a Christmas tree, topped with a yellow paper star. Tiny "
            "paper dot ornaments in red, blue, and pink scattered on the tree. A small brown paper trunk "
            "at the base. Sitting flat on a light wood craft table. Charming and child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-stocking-garland.webp",
        "prompt": (
            "A handmade Christmas paper stocking garland with about six paper stockings in red and green "
            "cardstock, each with a white paper cuff at the top, strung on natural baker's twine across "
            "a wooden mantel. Each stocking is slightly uneven, clearly child-made. Cozy holiday feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-reindeer-card.webp",
        "prompt": (
            "A handmade Christmas reindeer card on white folded cardstock featuring two brown paper "
            "handprint cutouts as antlers stretching upward, a brown oval paper face, two googly eyes, "
            "and a bright round red paper nose. Sitting flat on a light wood craft table. "
            "Clearly child-made with charming uneven cuts. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-christmas-wreath.webp",
        "prompt": (
            "A handmade Christmas paper wreath with green paper holly leaves and small red paper berries "
            "glued densely around a paper plate ring with the center cut out. A red ribbon bow tied at "
            "the bottom. Hanging against a light wooden door or wall. Clearly child-made and charming. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "new-years-paper-crown.webp",
        "prompt": (
            "A handmade New Year's Eve paper crown made from a strip of gold metallic cardstock with "
            "zigzag pointy peaks along the top, decorated with shiny sticker gems and silver glitter star "
            "dots. The two ends taped together to form a circular crown. Sitting on a light wood craft table "
            "with confetti scattered around it. Clearly child-made and festive. "
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
