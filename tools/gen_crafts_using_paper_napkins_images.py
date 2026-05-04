#!/usr/bin/env python3
"""Generate all images for crafts-using-paper-napkins.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "crafts-using-paper-napkins"
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
        "filename": "crafts-using-paper-napkins.webp",
        "prompt": (
            "A bright cheerful flat lay of an assortment of handmade paper napkin crafts on a white craft table: "
            "fluffy pink and yellow paper napkin flowers in a small clear glass jar, two paper napkin butterflies "
            "with pipe cleaner bodies, a clear glass jar decoupaged with a floral napkin pattern, "
            "a tie-dye napkin square with bleeding marker colors, and a few rolled napkin roses scattered around. "
            "Scissors, glue stick, and stacks of folded white and patterned paper napkins visible at the edges. "
            "Warm and welcoming spring craft mood, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-tie-dye-art.webp",
        "prompt": (
            "A flat lay showing both a folded white paper napkin triangle dotted with bright washable marker "
            "colors and an unfolded white paper napkin showing the finished tie-dye effect with soft "
            "swirling patterns of pink, blue, yellow, and green where the marker ink has bled into the paper. "
            "A small fine mist spray bottle and a few washable markers sit beside it on a white craft table. "
            "The paper has visible natural texture and slight wrinkles from the water. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-fluffy-flowers.webp",
        "prompt": (
            "Three handmade fluffy paper napkin flowers in pink, yellow, and pale blue, each made from "
            "stacked accordion-folded paper napkins pinched in the middle and twisted with a green pipe cleaner "
            "as a stem. The petals are gently fluffed up to look full and rounded. "
            "Arranged in a small clear glass jar on a light wood craft table. "
            "Cheerful spring craft, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-butterflies.webp",
        "prompt": (
            "Three handmade paper napkin butterflies on a light wood craft table. Each butterfly is made from "
            "two layered patterned paper napkins (one floral pink, one floral blue, one floral yellow) "
            "pinched at the center with a colored pipe cleaner wrapped around the middle to form the body, "
            "with the two ends of the pipe cleaner curled up as antennae. Wings are spread open and slightly fluffed. "
            "Charming handmade craft, child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-decoupage-jar.webp",
        "prompt": (
            "A clear glass mason jar decoupaged with a floral pattern from a paper napkin: pink and blue blossoms "
            "on a white background covering the front of the jar, sealed with Mod Podge so the napkin lies flat. "
            "A small wide foam brush and an open jar of Mod Podge sit on the white craft table next to the jar. "
            "Soft daylight highlights the glossy finish. Clearly child-made and slightly imperfect at the edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-snowflakes.webp",
        "prompt": (
            "Three delicate white paper napkin snowflakes laid flat on a soft pastel blue surface. "
            "Each snowflake is folded from a square white paper napkin and cut with intricate small triangular "
            "and round notches along the edges, creating a lacy symmetrical pattern when unfolded. "
            "The snowflakes show natural napkin texture and slight imperfections from a child's scissors. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-suncatcher.webp",
        "prompt": (
            "A handmade paper napkin suncatcher hanging on a sunny window. Torn pieces of pink, yellow, blue, "
            "and orange colorful paper napkins are pressed between two layers of clear contact paper, "
            "trimmed into a circle shape. Sunlight glows through the napkin colors, creating a stained-glass effect. "
            "Bright morning light filters through. Cheerful spring craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-ghost-lollipops.webp",
        "prompt": (
            "Three handmade paper napkin ghost lollipops arranged on a white craft table. "
            "Each is a wrapped lollipop with a white paper napkin draped over the top, gathered around "
            "the stick and tied with a small black ribbon to form the head. Two tiny black dot eyes are drawn "
            "on the front of each ghost. Cute friendly Halloween craft, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-rose-bouquet.webp",
        "prompt": (
            "A small handmade bouquet of paper napkin roses tied with a soft pink ribbon. "
            "Five roses made from rolled and twisted pink and red paper napkins form the blooms, "
            "each rose attached to a green pipe cleaner stem with small green paper leaves. "
            "Sitting on a white craft table next to a folded paper napkin and a pair of scissors. "
            "Mother's Day vibe, charming and clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-easter-chick.webp",
        "prompt": (
            "A handmade fluffy yellow paper napkin Easter chick: a crumpled ball of yellow paper napkin "
            "covered with another flat yellow napkin gathered around it to look fluffy. "
            "Two googly eyes glued on the front, a small orange paper triangle beak, and two tiny orange paper "
            "triangle feet at the bottom. Sitting upright on a light wood craft table next to a few yellow napkin scraps. "
            "Sweet spring Easter craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-princess-doll.webp",
        "prompt": (
            "Three handmade paper napkin princess dolls standing in a row on a white craft table. "
            "Each doll is a wooden clothespin or popsicle stick with a colored napkin (pink, pale blue, lavender) "
            "wrapped around it to form a flowing dress, tied at the waist with a small ribbon. "
            "A simple drawn face on the wooden head and a small paper crown glued on top. "
            "Charming child-made craft, slightly uneven and full of personality. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-heart-card.webp",
        "prompt": (
            "A handmade folded greeting card lying flat on a white craft table. The front of the card is pink "
            "cardstock with a large heart shape covered in scrunched bits of pink and red paper napkin glued "
            "all over the inside of the heart, creating a textured fluffy pink filling. "
            "A few napkin scraps and a glue stick sit beside the card. "
            "Sweet Valentine or Mother's Day craft, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-wreath.webp",
        "prompt": (
            "A handmade paper napkin wreath made from a paper plate ring covered all the way around with "
            "small rolled and scrunched paper napkin rosettes in pink, white, soft yellow, and pale green. "
            "A soft pink ribbon ties at the top to form a hanger. "
            "The wreath lies flat on a white craft table next to a few napkin scraps and scissors. "
            "Spring or Mother's Day craft, charming and clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-pom-pom-garland.webp",
        "prompt": (
            "A pastel paper napkin pom pom garland strung on white twine, lying flat on a white craft table. "
            "Five fluffy round pom poms in soft pink, pale yellow, white, mint green, and lavender, "
            "each made from accordion-folded paper napkins tied at the middle and fluffed into ball shapes. "
            "Cheerful celebration craft, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-folded-bunny.webp",
        "prompt": (
            "Three folded white paper napkin bunnies sitting upright on a light wood craft table. "
            "Each bunny is folded from a square white paper napkin into a body shape with two long pointy ears "
            "standing up on top, a tiny drawn face with dot eyes and a small triangle nose, "
            "and a soft white cotton ball tucked at the back as a fluffy tail. "
            "Sweet Easter craft, clearly handmade and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-mini-lantern.webp",
        "prompt": (
            "A row of three small clear glass jars wrapped in colorful paper napkins (pink floral, "
            "blue floral, yellow floral), each tied with a piece of natural twine around the middle. "
            "A small battery-operated tea light glows softly inside each jar, lighting up the napkin patterns "
            "from within. The lanterns sit on a wooden shelf in soft warm evening light. "
            "Dreamy cozy bedroom craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-painted-rocks.webp",
        "prompt": (
            "Five smooth river rocks decoupaged with floral paper napkin patterns, each rock showing different "
            "small flower designs in pink, blue, and green. The napkins are smoothed onto the rocks and sealed "
            "with a glossy Mod Podge finish. The rocks sit clustered on a white craft table next to a foam brush "
            "and an open small jar of Mod Podge. "
            "Garden marker or gift craft, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-tote-bag.webp",
        "prompt": (
            "A natural canvas tote bag laid flat on a wooden craft table with a large floral paper napkin "
            "design decoupaged onto the front of the bag. The napkin pattern shows pink and blue blossoms "
            "with green leaves. A foam brush and an open jar of Mod Podge sit beside the bag. "
            "The decoupaged area looks freshly applied and slightly damp. "
            "Older child or tween craft, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-pumpkins.webp",
        "prompt": (
            "Three handmade orange paper napkin pumpkins arranged in a small wooden bowl on a craft table. "
            "Each pumpkin is made by gathering an orange paper napkin around a crumpled newspaper ball, "
            "twisting the top with a green pipe cleaner stem, and adding a small curly green tendril. "
            "Soft puffy pumpkin shapes, clearly child-made and uneven in size. "
            "Cozy fall craft, warm autumn lighting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "marker-bleed-napkin-painting.webp",
        "prompt": (
            "A child's colorful marker drawing of flowers and a sun on a white paper napkin spread flat on a piece "
            "of cardboard. The marker colors have softly bled and blended together where water was misted on top, "
            "creating a watercolor painting effect with soft edges. "
            "A small fine mist spray bottle and a handful of washable markers sit nearby on a craft table. "
            "Dreamy sweet child art, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "napkin-bouquet-card.webp",
        "prompt": (
            "A handmade folded greeting card lying flat on a white craft table. The front of the card is pale "
            "cream cardstock with a tight cluster of small pastel paper napkin rosettes (pink, peach, lavender, "
            "soft yellow) glued in a bouquet shape. Hand-drawn green stems extend down from the rosettes "
            "and a tiny pink ribbon bow ties them together. "
            "Mother's Day card, sweet and clearly child-made. "
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
