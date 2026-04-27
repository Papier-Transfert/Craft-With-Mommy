#!/usr/bin/env python3
"""Generate all images for kawaii-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "kawaii-paper-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm soft natural daylight from a window. "
    "Light wood or pale pastel craft table surface. "
    "Soft pastel kawaii aesthetic, clean and cozy mood. "
    "Landscape orientation 4:3, fills the entire frame edge to edge. "
    "No cartoon rendering, no digital illustration. Real handmade paper materials only. "
    "Charming and slightly imperfect, clearly handmade by a child. Pinterest-worthy. "
    "Tiny dot eyes, a small curved smile, and pink blush cheeks drawn with pen and crayon."
)

IMAGES = [
    {
        "filename": "kawaii-paper-crafts.webp",
        "prompt": (
            "A pastel flat lay of handmade kawaii paper crafts on a light wood craft table: "
            "a smiling pastel pink paper donut with sprinkles, a pastel mint cloud with a tiny smile, "
            "small white paper sushi rolls with happy faces, a soft yellow paper sun with rosy cheeks, "
            "a pastel lilac mochi with a sleepy smile, and a kawaii paper teacup with steam. "
            "Pastel scrap papers, glue stick, kid scissors, and a black pen visible at the edges. "
            "Warm cozy kawaii mood, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-cloud-pal.webp",
        "prompt": (
            "A handmade kawaii white paper cloud cut from cardstock with a soft fluffy outline, "
            "two tiny black dot eyes, a small curved smile, and two pink blush circles on the cheeks. "
            "A small pastel ribbon loop is glued at the top so it can hang. "
            "Photographed flat on a pale pastel pink craft surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-sushi-roll.webp",
        "prompt": (
            "Three handmade kawaii paper sushi rolls in a row on a small white paper plate. "
            "Each roll has a white paper rectangle wrapped around a pink and green paper strip. "
            "Each roll has tiny black dot eyes, a small curved smile, and pink blush cheeks. "
            "Cute and slightly chubby. Photographed flat on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-bento-box.webp",
        "prompt": (
            "A handmade kawaii paper bento box: a shallow pastel pink rectangular paper box "
            "lined with green tissue paper, filled with a smiling white paper rice ball, "
            "a happy orange paper carrot, and a sleepy white paper egg with a yellow yolk. "
            "Each food item has tiny dot eyes, a small smile, and pink blush cheeks. "
            "Photographed flat on a pastel wooden surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-sun-face.webp",
        "prompt": (
            "A handmade kawaii yellow paper sun: a large yellow circle with triangular paper rays "
            "around it, a sweet kawaii face with tiny dot eyes, a curved smile, and pink blush cheeks. "
            "Taped to a clean white window with soft daylight. Cheerful and bright. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-cherry-blossom-card.webp",
        "prompt": (
            "A handmade kawaii pastel pink folded paper card lying open on a craft table. "
            "Glued onto the front: a small brown paper branch and a cluster of tiny five-petal "
            "cherry blossom flowers in soft pink and white. One blossom has a small kawaii face "
            "with dot eyes and a curved smile. Photographed flat on a pale pastel surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-sandwich.webp",
        "prompt": (
            "A handmade kawaii paper sandwich: stacked paper rectangles cut to look like bread, "
            "green leaf lettuce, yellow cheese, and red tomato slices. Layers slightly off-center. "
            "The top slice of bread has a tiny kawaii face with dot eyes, a small smile, and pink cheeks. "
            "Photographed flat on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-cat-onigiri.webp",
        "prompt": (
            "A handmade kawaii paper triangle rice ball: a white paper triangle with two pointed "
            "cat ears at the top, a thin black paper strip across the bottom for seaweed. "
            "Sleepy black dot eyes, tiny whiskers, a small curved smile, and pink blush cheeks. "
            "Photographed flat on a pastel pink surface next to two more rice balls. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-strawberry-card.webp",
        "prompt": (
            "A handmade kawaii red paper strawberry shape decorated with tiny white paper seed dots "
            "and a green leafy paper top. A happy kawaii face in the middle: dot eyes, curved smile, "
            "and pink blush cheeks. Standing alone on a soft pastel mint craft surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-cloud-mobile.webp",
        "prompt": (
            "A handmade kawaii paper mobile hanging from a small wooden chopstick: four small "
            "white paper clouds with smiling faces, one pastel yellow sun, and one pale blue "
            "raindrop with a friendly face. Each piece dangles from a white string at different "
            "lengths. Photographed against a clean pastel wall. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-donut.webp",
        "prompt": (
            "A handmade kawaii paper donut: a wide pastel pink paper ring with a slightly smaller "
            "pastel mint icing ring on top and tiny rectangle paper sprinkles in pastel colors. "
            "A small kawaii face with dot eyes, a curved smile, and pink blush cheeks in the middle. "
            "Photographed flat on a light pastel craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-mochi-family.webp",
        "prompt": (
            "A handmade kawaii paper mochi family: five small chubby soft-edged round paper shapes "
            "in pastel pink, mint, lilac, cream, and peach. Each one has a different sweet face: "
            "happy, sleepy, surprised, blushing, smiling. Pink cheeks on each one. "
            "Arranged on a small pastel paper plate. Photographed flat on a light wood surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-cactus-buddy.webp",
        "prompt": (
            "A handmade kawaii green paper cactus shape standing in a small terracotta-colored "
            "paper pot. Tiny white paper spike marks on the cactus body. A happy kawaii face on the "
            "cactus: dot eyes, small curved smile, and pink blush cheeks. A tiny pink paper flower "
            "glued at the top of the cactus. Photographed flat on a pastel craft surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-bunny-card.webp",
        "prompt": (
            "A handmade kawaii white paper pop-up card open and standing upright, photographed at "
            "a slight angle. A kawaii white bunny with long pink-lined ears pops out from the inside "
            "fold. The bunny has dot eyes, a tiny pink nose, a small smile, and pink blush cheeks. "
            "Small paper carrots, hearts, and stars decorate the inside. Pastel pink craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-toast-friends.webp",
        "prompt": (
            "A handmade kawaii paper toast and fried egg: a square of light brown paper for the "
            "toast and a wavy white paper shape with a yellow circle yolk for the egg. "
            "Each one has a sleepy kawaii face with dot eyes, a small curved smile, and pink cheeks. "
            "Leaning against each other on a small white paper plate. Light wood table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-tea-cup.webp",
        "prompt": (
            "A handmade kawaii pastel light blue paper teacup with a small handle on the side. "
            "A kawaii face on the front of the cup: dot eyes, curved smile, pink blush cheeks. "
            "A tiny paper tea bag tag peeks over the rim and three soft white paper steam wisps "
            "float above. Photographed flat on a pastel pink craft surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-flower-pots.webp",
        "prompt": (
            "Three handmade kawaii small terracotta-colored paper pots, each with a happy kawaii "
            "face: dot eyes, curved smile, pink blush cheeks. Above each pot is a colorful tissue "
            "paper flower in pink, yellow, or lilac. Lined up in a row on a sunny windowsill with "
            "soft daylight. Cheerful indoor garden mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-rainbow.webp",
        "prompt": (
            "A handmade kawaii pastel paper rainbow: a wide arc of layered paper strips in soft "
            "pastel rainbow colors (pink, peach, yellow, mint, lavender). A tiny kawaii face right "
            "in the middle: dot eyes, curved smile, pink cheeks. A small fluffy white paper cloud "
            "at each end. Photographed flat on a pale blue craft surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-boba-tea.webp",
        "prompt": (
            "A handmade kawaii paper boba tea drink: a tall pale beige cup shape with several "
            "small dark brown paper circles at the bottom for tapioca pearls. A thin paper strip "
            "straw sticks out the top. A small kawaii face on the cup: dot eyes, curved smile, "
            "pink blush cheeks. Photographed flat on a soft pastel pink craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-star-garland.webp",
        "prompt": (
            "A handmade kawaii paper star garland: about ten small five-point stars in pastel "
            "yellow, peach, and pale pink, each with a tiny kawaii face (dot eyes, small smile, "
            "pink cheeks). Strung together on a soft white string and hanging gently above a "
            "small bed in a cozy pastel bedroom. Soft daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "kawaii-paper-mini-notebook.webp",
        "prompt": (
            "A handmade kawaii mini paper notebook: a small folded paper booklet stapled along "
            "the spine. The pastel pink cover has a smiling kawaii character drawn with a "
            "fine-tip black pen, plus small hearts and stars in soft pastel colors. The booklet "
            "lies flat next to a few colored pencils on a light wood craft table. "
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
