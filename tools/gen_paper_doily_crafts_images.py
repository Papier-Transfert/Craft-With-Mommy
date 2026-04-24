#!/usr/bin/env python3
"""Generate all images for paper-doily-crafts.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "blog" / "images" / "paper-doily-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-doily-crafts.webp",
        "prompt": (
            "A colorful flat lay of handmade paper doily crafts on a white craft table: "
            "a doily flower bouquet tied with ribbon, a lacy doily heart garland, "
            "a doily angel ornament, a doily butterfly, a doily fan, and a lacy doily bunny. "
            "White round paper doilies scattered around, with scissors, glue stick, ribbons, "
            "and construction paper scraps visible at the edges. Soft pastel tones, feminine and pretty. "
            "Clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-flower-bouquet.webp",
        "prompt": (
            "A handmade bouquet of three paper doily flowers on green pipe cleaner stems, "
            "each flower made from a pinched white round paper doily in the center. "
            "The bouquet is tied together with a pink satin ribbon bow. "
            "Lying flat on a white craft table with extra doilies and pipe cleaners around. "
            "Sweet and feminine. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-snowflake-window.webp",
        "prompt": (
            "Three white paper doilies glued to a blue construction paper background, arranged as snowflakes, "
            "with small white cotton ball clouds and silver glitter accents. "
            "The finished scene is taped to a bright window, with soft daylight shining through. "
            "The lacy doily pattern is clearly visible. Cozy winter atmosphere, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-angel-ornament.webp",
        "prompt": (
            "A handmade paper doily angel ornament made from a white round doily folded into a cone body, "
            "with a small peach paper circle glued as a face, a smaller white doily behind as wings, "
            "and a gold paper halo on top. A thin ribbon loop hangs from the head for hanging. "
            "Sitting on a light wood craft table next to scissors and doily scraps. "
            "Sweet and delicate. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-butterfly.webp",
        "prompt": (
            "A handmade paper doily butterfly made from a white round doily pinched at the center "
            "to form two lacy wings. A brown pipe cleaner is wrapped around the center as the body "
            "with the ends curled up into antennae. Two small googly eyes are glued near the top. "
            "Resting flat on a white craft table. Charming and simple. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-mothers-day-card.webp",
        "prompt": (
            "A handmade Mother's Day card made from a folded pink cardstock rectangle "
            "with a white round paper doily glued on the front, and a small red construction paper "
            "heart centered on top of the doily. Lying open on a craft table with pink ribbons, "
            "scissors, and a glue stick visible nearby. The lacy doily pattern is clearly visible. "
            "Warm, sweet, and handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-valentine-heart-garland.webp",
        "prompt": (
            "A handmade paper doily Valentine garland: five white doily hearts strung on a long red satin ribbon, "
            "each doily folded and cut into a heart shape. The garland is draped along a white shelf "
            "with soft daylight behind it. Delicate and romantic Valentine's Day craft. "
            "The lacy pattern of each doily is clearly visible. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-dreamcatcher.webp",
        "prompt": (
            "A handmade paper doily dreamcatcher: a large white round doily glued inside a cardstock ring, "
            "with long pastel ribbons, strings of wooden beads, and small paper feathers in pink, blue, "
            "and yellow hanging from the bottom. Hanging against a plain neutral wall with soft natural light. "
            "Bohemian and peaceful, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-umbrella.webp",
        "prompt": (
            "Three tiny handmade paper doily umbrellas arranged on a white craft table. "
            "Each umbrella is a white round doily folded into a small cone-shaped umbrella, "
            "with a bent pink pipe cleaner forming the curved handle at the bottom. "
            "Cute and miniature. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-ballerina-princess.webp",
        "prompt": (
            "A handmade paper doily ballerina craft: a simple paper doll figure drawn on white cardstock "
            "with a white round paper doily folded and glued around her waist as a fluffy lacy tutu skirt. "
            "A small gold paper crown sits on her head, and a tiny pink ribbon bow is in her hair. "
            "Lying flat on a craft table. Sweet and whimsical. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-jellyfish.webp",
        "prompt": (
            "A handmade paper doily jellyfish craft: a white round paper doily glued onto the top of a blue "
            "construction paper background, with long curly pastel ribbon strips hanging underneath as tentacles. "
            "Two googly eyes and a small smiling mouth drawn on the doily. Cheerful and cute ocean craft. "
            "Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-wreath.webp",
        "prompt": (
            "A handmade paper doily wreath: a cardstock ring covered with seven or eight overlapping "
            "white round paper doilies, glued down to form a frilly lacy wreath. A pink satin ribbon bow "
            "is tied at the top for hanging. Lying flat on a light wood surface. Soft, romantic, and feminine. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-sun-catcher.webp",
        "prompt": (
            "A watercolor-painted paper doily sun catcher taped to a sunny window. "
            "The round white doily has been gently painted with soft pink, yellow, and coral watercolors "
            "that reveal the lacy pattern. Bright daylight streams through, creating soft colored shadows on the sill. "
            "A small watercolor palette and paintbrush sit on the windowsill. Warm and magical. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-easter-bonnet.webp",
        "prompt": (
            "A handmade paper doily Easter bonnet made from a paper plate base with a white round paper doily "
            "glued on top so the lacy edges peek out. Decorated with three pastel paper flowers in pink, yellow, "
            "and blue, plus two small white paper bunny ears at the front and a pink ribbon tied in a bow at the back. "
            "Sitting on a craft table. Sweet springtime craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-paper-lantern.webp",
        "prompt": (
            "A handmade paper doily lantern: a cylinder made of pink cardstock wrapped with a white round paper doily "
            "glued around the outside so the lacy pattern shows. A thin ribbon handle is threaded through two holes "
            "at the top. A small battery tea light inside makes the lantern glow softly. "
            "Sitting on a craft table in dim evening light so the lace pattern is visible. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-princess-crown.webp",
        "prompt": (
            "A handmade paper doily princess crown: a white round paper doily cut in half to form a curved crown shape, "
            "decorated with colorful marker dots and small sparkly stickers as jewels, taped onto a cardstock headband strip. "
            "Resting on a white craft table next to markers and sticker sheets. Cute and girly, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-garland.webp",
        "prompt": (
            "A handmade paper doily garland: six white round paper doilies threaded onto a long pink satin ribbon "
            "and draped across a white wooden shelf. The lacy pattern of each doily is clearly visible. "
            "Soft, romantic, and feminine home decoration, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-fan.webp",
        "prompt": (
            "A handmade accordion-folded paper doily fan: a white round paper doily folded back and forth, "
            "pinched at the bottom and secured with tape to form a handheld fan shape. "
            "A pink ribbon loop hangs from the bottom. Lying flat on a white craft table "
            "next to scissors and a second unfolded doily. Charming and delicate. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-bookmark.webp",
        "prompt": (
            "A handmade paper doily bookmark: a long lacy strip cut from a white paper doily glued onto "
            "a strip of lavender cardstock, with a small hole punched at the top and a pink ribbon threaded "
            "through as a tassel. Lying on top of an open book on a craft table. Pretty and thoughtful gift craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-rainbow-fish.webp",
        "prompt": (
            "A handmade paper doily rainbow fish craft: a large fish shape cut from bright teal cardstock, "
            "covered with many small overlapping white paper doily circles glued as shimmery lacy scales. "
            "One large googly eye near the head and a small smiling mouth drawn with a black marker. "
            "Lying flat on a craft table. Cheerful and magical. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "doily-bunny.webp",
        "prompt": (
            "A handmade paper doily bunny craft: a white round paper doily glued onto cream cardstock as a fluffy body, "
            "with two long white paper ear shapes on top (lined with pink inside), a small white pom-pom tail, "
            "a pink paper triangle nose, and whiskers and a smiling face drawn with a black marker. "
            "Lying flat on a craft table. Soft, cuddly, and adorable spring craft. "
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
