#!/usr/bin/env python3
"""Generate all images for food-crafts-with-paper.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "food-crafts-with-paper"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper and cardstock only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "The craft fills the frame edge to edge with no white borders or letterboxing."
)

IMAGES = [
    {
        "filename": "food-crafts-with-paper.webp",
        "prompt": (
            "A colorful flat lay of handmade paper food crafts on a white craft table: "
            "a triangular paper pizza slice with red sauce and pepperoni, a paper ice cream cone "
            "with three colorful scoops, a pink frosted paper cupcake with sprinkles, "
            "a pink paper watermelon slice, a chocolate paper donut with sprinkles, "
            "a red paper apple, and a stack of paper banana shapes. "
            "Scissors, glue stick, and bright construction paper scraps visible at the edges. "
            "Cheerful pretend food spread, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pizza-slice.webp",
        "prompt": (
            "A handmade paper pizza slice craft: a large triangle cut from tan cardstock for the "
            "crust base, with a curved red construction paper edge for the tomato sauce, "
            "and a smaller cream-colored paper layer on top for the cheese. "
            "Decorated with several small red paper circles for pepperoni, tiny green paper squares "
            "for peppers, and a few small brown paper mushroom shapes. "
            "Lying flat on a white craft table, clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-ice-cream-cone.webp",
        "prompt": (
            "A handmade paper ice cream cone craft: a brown paper triangle cone with a marker-drawn "
            "crosshatch waffle pattern at the bottom, topped with three round paper scoops stacked "
            "on top of each other in pink (strawberry), pale green (mint), and dark brown (chocolate). "
            "A tiny red paper cherry sits on top. "
            "Lying flat on a light wood craft table. Charming, child-made paper food craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cupcake-craft.webp",
        "prompt": (
            "A handmade paper cupcake craft: a striped pink and brown paper cupcake liner at the bottom, "
            "topped with a swirling pastel pink paper frosting shape. "
            "Tiny rainbow paper sprinkles dot the frosting and a small red paper cherry sits on top. "
            "Lying flat on a white craft table with paper scraps around it. "
            "Cheerful child-made bakery craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-hamburger-craft.webp",
        "prompt": (
            "A handmade paper hamburger craft: two tan rounded paper bun shapes with tiny black marker "
            "sesame seed dots on the top bun. Between them is a brown paper patty, "
            "a ruffled green paper lettuce leaf, a round red paper tomato slice, "
            "and a yellow paper square of cheese with the corners poking out. "
            "Layered like a tall cheeseburger and lying flat on a craft table. "
            "Clearly child-made, slightly uneven paper layers. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-sushi-roll.webp",
        "prompt": (
            "Handmade paper sushi roll craft pieces: several small round pieces each made from a "
            "black paper strip wrapped around a white paper rectangle (rice). "
            "Inside each, tiny strips of orange paper (salmon) and green paper (avocado) are visible. "
            "Six pieces are arranged in a neat row on a small white paper plate on a craft table. "
            "Charming pretend food craft, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-apple-craft.webp",
        "prompt": (
            "A handmade paper apple craft: a round shape cut from bright red cardstock with a small "
            "brown paper stem attached at the top and a single small green paper leaf glued on the side. "
            "A soft pale pink crayon shading on one cheek of the apple. "
            "Lying flat on a white craft table with paper scraps and scissors nearby. "
            "Clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-donut-craft.webp",
        "prompt": (
            "Three handmade paper donut crafts: each donut is a tan paper ring with a hole in the middle, "
            "topped with a glossy frosting paper layer. One donut has pink frosting, "
            "one has chocolate brown frosting, and one has pastel blue frosting. "
            "Each donut is decorated with tiny rainbow paper sprinkles. "
            "Arranged in a small triangle on a white craft table. Charming child-made bakery craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-hot-dog-craft.webp",
        "prompt": (
            "A handmade paper hot dog craft: a long oval tan paper bun shape with a brown paper sausage "
            "tucked along the middle so it peeks out at both ends. "
            "On top, a wavy yellow paper strip represents mustard and a wavy red paper strip represents ketchup. "
            "Lying flat on a craft table next to a paper plate. Cheerful pretend food craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-banana-craft.webp",
        "prompt": (
            "A handmade paper banana craft: a long curved banana shape cut from bright yellow cardstock, "
            "with small brown paper tips at each end for the stem and the blossom point. "
            "Two faint vertical marker lines run down the side as the banana ridges, and tiny brown "
            "marker specks dot the surface for a ripe look. "
            "Lying flat on a white craft table with paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strawberry-craft.webp",
        "prompt": (
            "A handmade paper strawberry craft: a heart shape cut from bright red paper, with the bottom "
            "trimmed to a soft point, forming a classic strawberry silhouette. "
            "A small green leafy crown is glued at the top. "
            "Tiny black marker dots are scattered evenly across the red surface to represent seeds. "
            "Lying flat on a white craft table with red paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-watermelon-slice.webp",
        "prompt": (
            "A handmade paper watermelon slice craft: a half-circle of green paper at the bottom, "
            "topped with a slightly smaller half-circle of white paper, "
            "and finished with an even smaller bright pink half-circle on top for the juicy fruit. "
            "Several small black paper teardrop seeds are glued onto the pink section. "
            "Lying flat on a white craft table with paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-birthday-cake.webp",
        "prompt": (
            "A handmade paper birthday cake craft: three pastel cardstock rectangles (pink, mint, "
            "and pale yellow) stacked from largest at the bottom to smallest at the top, forming "
            "tiered cake layers. A wavy white paper strip on top represents the frosting. "
            "Three thin paper candle shapes stand upright on top, each with a small yellow paper "
            "flame. Tiny polka dots and small paper drips decorate the sides. "
            "Lying flat on a craft table. Cheerful, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-sandwich-craft.webp",
        "prompt": (
            "A handmade paper sandwich craft cut diagonally in half: two square slices of tan paper "
            "for the bread, with a yellow paper square of cheese, a small ruffled green lettuce shape, "
            "and a round red paper tomato slice layered between them. "
            "The diagonal cut shows all the colorful layers from the side. "
            "Lying flat on a craft table on a small paper napkin. "
            "Charming pretend food craft, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-carrot-craft.webp",
        "prompt": (
            "A handmade paper carrot craft: a rolled cone shape made from bright orange paper, "
            "tapered to a point at the bottom. "
            "Several thin green paper strips are tucked into the wide top to look like leafy carrot greens. "
            "Faint horizontal marker lines run along the orange body for carrot ridges. "
            "Lying flat on a white craft table with green paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-popcorn-bucket.webp",
        "prompt": (
            "A handmade paper popcorn bucket craft: a small folded paper container in classic red and "
            "white vertical stripes. The bucket overflows with crinkled small balls of white tissue paper "
            "that look like fluffy popcorn pieces. A few small yellow paper bits sprinkle across "
            "the popcorn for a buttery look. "
            "Standing upright on a white craft table. Playful pretend food craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-taco-craft.webp",
        "prompt": (
            "A handmade paper taco craft: a yellow paper semicircle folded into a taco shell shape, "
            "with green ruffled paper lettuce, a red paper tomato strip, brown paper meat squiggles, "
            "and small yellow paper cheese sprinkles tucked inside. "
            "Standing upright on a small paper plate on a craft table. "
            "Cheerful pretend food craft, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pineapple-craft.webp",
        "prompt": (
            "A handmade paper pineapple craft: a tall oval body cut from golden yellow paper, "
            "with a black marker crisscross diamond pattern drawn across the surface for the texture. "
            "A spiky green crown made from several pointed paper leaf strips is glued at the top. "
            "Lying flat on a white craft table with green paper scraps nearby. "
            "Tropical pretend food craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-lemon-craft.webp",
        "prompt": (
            "Two handmade paper lemon crafts side by side: on the left, a small bright yellow paper "
            "oval lemon shape with a tiny green paper stem and a single green leaf at one end. "
            "On the right, a sliced lemon version: a yellow paper circle with a smaller white circle "
            "inside, and thin marker lines drawn from the center outward to look like citrus segments. "
            "Both lying flat on a white craft table with yellow paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-french-fries.webp",
        "prompt": (
            "A handmade paper french fries craft: a small folded red paper pouch shaped like a fries cup, "
            "with seven long thin yellow paper rectangles poking out at slightly different heights "
            "to represent the fries. "
            "Standing upright on a white craft table. Playful pretend fast food craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rainbow-lollipop.webp",
        "prompt": (
            "A handmade paper rainbow lollipop craft: a round white cardstock circle covered in "
            "spiraling strips of colorful paper (red, orange, yellow, green, blue, purple) glued in a "
            "swirl from the center outward. A paper straw stick is taped to the back as the lollipop handle. "
            "Lying flat on a white craft table with colorful paper scraps nearby. "
            "Cheerful candy-shop pretend food craft, clearly child-made. "
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
        if resized.mode != "RGB":
            resized = resized.convert("RGB")
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
