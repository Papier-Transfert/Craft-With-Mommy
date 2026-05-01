#!/usr/bin/env python3
"""Generate all images for japanese-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "japanese-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood or cream-colored craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child or a parent and child together. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "japanese-paper-craft.webp",
        "prompt": (
            "A bright flat lay of handmade Japanese paper crafts on a light wood table: "
            "a folded blue origami crane in the center, a small red and yellow paper chochin lantern, "
            "a pink cherry blossom paper garland strung along one edge, a folded accordion paper fan in pink and white, "
            "a bright orange and blue koinobori carp paper streamer, two small puffy origami lucky stars, "
            "a folded green origami jumping frog, and a pink origami tulip. "
            "Origami paper sheets and washi tape rolls visible at the corners. "
            "Cheerful Japanese-inspired craft mood, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-crane.webp",
        "prompt": (
            "A handmade origami paper crane folded from a single square of solid blue origami paper. "
            "The crane has clearly defined head, neck, two wings spread upward, and a pointed tail. "
            "Sitting on a light wood craft table next to one extra square of origami paper. "
            "Crisp folds, slightly imperfect, handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-heart.webp",
        "prompt": (
            "A handmade origami paper heart folded from a single square of solid pink origami paper, "
            "flat puffy heart shape with crisp folds visible. Resting on a light wood table next to "
            "a few more pink and red origami paper squares. Sweet and simple handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-jumping-frog.webp",
        "prompt": (
            "A handmade green origami jumping frog folded from a single square of green origami paper. "
            "Triangular pointed head, accordion-folded back legs ready to spring. "
            "Sitting on a wooden table with another smaller frog beside it. Clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-boat.webp",
        "prompt": (
            "A folded blue origami paper boat with a pointed front and back, "
            "open hollow center, sitting on a light wood craft table. "
            "Crisp clean folds, clearly handmade. A second smaller red boat sits beside it. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-tulip.webp",
        "prompt": (
            "A handmade origami tulip with a pink folded paper bloom and a green folded paper stem with a leaf. "
            "Standing upright on a light wood craft table, with a few extra pink and green origami paper squares scattered nearby. "
            "Sweet handmade look, clearly child-friendly. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-cat.webp",
        "prompt": (
            "A handmade origami cat face folded from a single square of orange origami paper, "
            "with two pointy triangle ears at the top and a small triangle nose. "
            "Decorated with marker-drawn whiskers, two round eyes, and a tiny smile. "
            "Lying flat on a light wood table beside two more origami cat faces in pink and yellow. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-lucky-star.webp",
        "prompt": (
            "A small pile of around fifteen handmade origami lucky stars in pastel pink, mint green, "
            "yellow, and pale blue, gathered together on a light wood surface. "
            "Each star is a small puffy three-dimensional pentagon, clearly folded by hand. "
            "Some are placed inside a small clear glass jar in the background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-butterfly.webp",
        "prompt": (
            "A folded origami butterfly with patterned pink and white origami paper wings, "
            "the wings slightly lifted to suggest flight. Resting on a light wood craft table "
            "beside a few small leftover scraps of origami paper. Clean crisp folds, handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-fish.webp",
        "prompt": (
            "A folded orange origami fish with a forked tail and a small marker-drawn dot eye and a few small scales. "
            "Lying flat on a light wood craft table next to a square of blue origami paper. "
            "Friendly chubby fish shape, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-lantern-chochin.webp",
        "prompt": (
            "A handmade red and yellow paper lantern in the Japanese chochin style: "
            "a cylinder of red paper with a yellow strip top and bottom, with vertical fringe-like cuts visible. "
            "A small paper handle at the top. Hanging from a thin string against a soft cream wall background. "
            "Cheerful and slightly imperfect, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cherry-blossom-garland.webp",
        "prompt": (
            "A handmade cherry blossom garland: a long piece of white twine strung with about ten small "
            "five-petal sakura paper flowers cut from soft pink and pure white paper, each with a tiny yellow center. "
            "Draped loosely on a light wood surface. Soft springtime mood, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "washi-tape-bookmark.webp",
        "prompt": (
            "A handmade cardstock bookmark decorated with horizontal stripes of colorful washi tape "
            "in pink, mint, gold, and pale blue patterns. A thin pink ribbon threaded through a hole at the top. "
            "Lying flat on a light wood craft table next to a stack of three washi tape rolls. "
            "Clearly child-made and cheerful. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "japanese-paper-fan.webp",
        "prompt": (
            "A handmade Japanese paper fan made from a long rectangle of pink and white patterned paper "
            "accordion-folded into neat pleats and pinched at the bottom. The fan is held open on a light wood surface, "
            "showing the full pleated fan shape. A small piece of washi tape secures the base. "
            "Pretty Japanese-inspired craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "koinobori-carp-streamer.webp",
        "prompt": (
            "A handmade koinobori Japanese carp streamer made from rolled blue and orange paper tubes "
            "shaped like fish, with cut V-tails at one end and marker-drawn round scales and a single eye. "
            "Hanging horizontally from white strings against a light wall, billowing slightly. "
            "Cheerful Japanese Children's Day craft, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-house.webp",
        "prompt": (
            "A folded origami paper house with a pointed triangular roof and a square base, "
            "made from one square of pale yellow origami paper. Decorated with small child-drawn windows, "
            "a red door, and a tiny garden of marker flowers in front. Sitting on a light wood craft table "
            "with two more origami houses in pink and blue beside it. Sweet pretend-play craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-daruma-doll.webp",
        "prompt": (
            "A handmade paper daruma doll: a round shape cut from bright red cardstock with a smaller "
            "skin-tone circle face glued in the middle. Big bold black painted eyes (one filled in, one blank), "
            "expressive black painted eyebrows, and a small mouth. Small Japanese characters lightly drawn on the body. "
            "Lying flat on a light wood craft table. Clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-fortune-teller.webp",
        "prompt": (
            "A handmade origami paper fortune teller, also called a cootie catcher, made from "
            "a single square of pink and yellow patterned origami paper folded into the four-pocket shape. "
            "Sitting on a light wood table with the pockets visible from above, fingertips of a child barely visible "
            "at the edges as if about to slip into the pockets. Clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-sumo-wrestlers.webp",
        "prompt": (
            "Two handmade paper sumo wrestler silhouettes cut from cream and tan cardstock, "
            "standing upright facing each other inside a shallow round cardboard box arena. "
            "Each wrestler has a simple painted face, a black belt drawn around the waist, and a small folded base tab. "
            "Photographed from slightly above on a light wood table. Playful Japanese-inspired craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-kokeshi-doll.webp",
        "prompt": (
            "A handmade paper kokeshi doll: a vertical paper tube body wrapped with stripes of pink and white "
            "washi tape forming a kimono pattern, topped by a round paper head with a small painted face "
            "(two black dots for eyes, a tiny red mouth) and short black painted hair. "
            "Standing upright on a light wood craft table beside a few rolls of washi tape. "
            "Cute Japanese-inspired craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-bookmark.webp",
        "prompt": (
            "A handmade origami corner bookmark folded from a small square of green origami paper, "
            "decorated to look like a smiling animal face with two googly eyes, a small triangle nose, "
            "and a child-drawn smile. The bookmark is slipped over the top corner of an open book page, "
            "clearly hugging the corner. Photographed from above on a light wood table. Sweet handmade craft. "
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
