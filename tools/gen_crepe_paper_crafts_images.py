#!/usr/bin/env python3
"""Generate all images for crepe-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "crepe-paper-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood or white craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real crepe paper materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "crepe-paper-crafts.webp",
        "prompt": (
            "A bright flat lay of handmade crepe paper crafts on a light wood craft table: "
            "a small bouquet of pink and yellow twisted crepe paper tissue flowers in a glass jar, "
            "two fluffy pastel crepe paper pom-poms, a colorful pink and purple crepe paper butterfly with a pipe cleaner body, "
            "a pastel tassel garland in mint, peach, and pink, and a few rolled crepe paper streamers on the side. "
            "Scissors, a glue stick, and pipe cleaners scattered at the edges. "
            "Bright cheerful spring mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-tissue-flowers.webp",
        "prompt": (
            "A handmade bouquet of three twisted crepe paper tissue flowers in pink, peach, and yellow, "
            "made by stacking and accordion-folding crepe paper squares and twisting a green pipe cleaner around the middle. "
            "The fluffy layered petals are gently fanned out. "
            "The bouquet is sitting in a small clear glass jar on a wooden table. "
            "Charming and slightly imperfect, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-rainbow-garland.webp",
        "prompt": (
            "A handmade rainbow crepe paper streamer garland with six long flat strips in red, orange, yellow, green, blue, and purple "
            "taped together at the top to form an arched rainbow shape. "
            "The garland is hanging on a plain white wall above a wooden side table. "
            "Cheerful and colorful, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-pom-poms.webp",
        "prompt": (
            "Three handmade fluffy crepe paper pom-poms in pastel pink, pale yellow, and mint green, "
            "each made from accordion-folded layered crepe paper tied in the middle with string and fluffed into round balls. "
            "They are hanging from white string against a soft neutral background, at slightly different heights. "
            "Soft and dreamy, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-butterfly.webp",
        "prompt": (
            "A handmade crepe paper butterfly made from a square of pink and purple crepe paper pinched in the middle "
            "with a black pipe cleaner twisted around the center to form the body. "
            "Two curled antennae point up at the top. The wings are gently fanned out. "
            "The butterfly is sitting on a white craft table next to a few crepe paper scraps. "
            "Cheerful and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-jellyfish.webp",
        "prompt": (
            "A handmade hanging crepe paper jellyfish: a round pink crepe paper head stuffed with crumpled paper, "
            "tied at the bottom with string, and several long wavy pink and white crepe paper streamer legs hanging underneath. "
            "Hanging from a string against a soft pale blue background. "
            "Whimsical under-the-sea look, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-cherry-blossom.webp",
        "prompt": (
            "A handmade cherry blossom branch made from a real brown twig with about ten small pale pink crepe paper "
            "five-petal blossoms scrunched and glued along its length. "
            "The branch is standing in a tall thin clear glass vase on a wooden table near a window. "
            "Soft spring lighting, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-tassel-garland.webp",
        "prompt": (
            "A handmade pastel tassel garland with about eight crepe paper tassels in soft pink, mint green, peach, and pale yellow, "
            "each made from rolled fringed crepe paper strips and tied onto a length of white string. "
            "The garland is strung horizontally above a craft table with a few crepe paper scraps below. "
            "Sweet party-shop look, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-sunflower-card.webp",
        "prompt": (
            "A handmade folded white card lying open on a wooden table, decorated on the front with a single large sunflower: "
            "a brown cardstock circle in the center surrounded by a ring of fringed yellow crepe paper petals. "
            "A green crepe paper leaf is glued to the side. "
            "Charming and slightly imperfect, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-rosettes.webp",
        "prompt": (
            "A handmade cluster of about six small rolled crepe paper rosette flowers in shades of pink and red, "
            "each made by folding and rolling a long strip of crepe paper into a tight rose shape, "
            "glued together onto a piece of white cardstock. "
            "Sweet and feminine, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-octopus.webp",
        "prompt": (
            "A handmade hanging crepe paper octopus with a round purple head stuffed with crumpled tissue and tied with string, "
            "eight long wavy purple crepe paper streamer legs dangling underneath, "
            "and two large googly eyes glued to the front of the head. "
            "Hanging from a string against a soft pale background. "
            "Playful and clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-birthday-backdrop.webp",
        "prompt": (
            "A handmade birthday party backdrop made from long vertical crepe paper streamer strips in pink, gold, and white, "
            "taped to a plain wall above a small wooden side table. "
            "On the table sits a small frosted birthday cake with a single candle. "
            "Some streamers are flat, others are gently twisted for movement. "
            "Cheerful and warm, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-crown.webp",
        "prompt": (
            "A handmade carnival paper crown sitting on a white craft table: a strip of white cardstock formed into a circular crown, "
            "with tall fringed crepe paper streamer spikes in red, yellow, blue, and green standing up along the top edge. "
            "The crown is slightly lopsided and clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-daffodils.webp",
        "prompt": (
            "A handmade bunch of three crepe paper daffodils in a small white vase on a wooden table: "
            "each daffodil has six pointed yellow crepe paper petals around a small orange crepe paper trumpet center, "
            "with a green floral wire stem and a single green leaf. "
            "Spring garden look, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-easter-eggs.webp",
        "prompt": (
            "Three handmade Easter eggs wrapped in bright pink, sky blue, and pale yellow crepe paper, "
            "each one twisted at both ends like a candy wrapper with a small ribbon bow tied at each twist. "
            "The wrapped eggs are nestled together on a white craft table with a few green paper grass pieces around them. "
            "Festive and clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-ribbon-wand.webp",
        "prompt": (
            "A handmade ribbon dancer wand made from a wooden dowel with five long crepe paper streamers in red, orange, "
            "yellow, green, and blue taped to one end. A small child's hand is holding the dowel mid-motion, "
            "with the streamers flowing out to the side. "
            "Bright daylight in a living room, joyful movement, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-watermelon-garland.webp",
        "prompt": (
            "A handmade watermelon slice garland with about six watermelon half-circle slices on a length of brown twine. "
            "Each slice is built from a green crepe paper rind, a thin white crepe paper strip, "
            "and a red crepe paper inside with several small black paper seed dots glued on. "
            "Hanging horizontally above a kitchen counter. Cheerful summer look, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-spider-web.webp",
        "prompt": (
            "A handmade Halloween spider web made from long stretched strips of black crepe paper "
            "taped across an interior doorway in a radial web pattern. "
            "Two small black paper spiders with eight thin legs are attached to the web. "
            "Soft warm hallway lighting in the background. Playful Halloween mood, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-ice-cream.webp",
        "prompt": (
            "A handmade ice cream cone mobile hanging from white string in a child's bedroom: "
            "three brown paper triangle cones, each topped with three crumpled pastel crepe paper balls "
            "in pink, mint, and pale yellow that look like ice cream scoops. "
            "Hanging at different heights against a soft pale wall. Sweet summer mood, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-confetti-shaker.webp",
        "prompt": (
            "A handmade confetti shaker made from a small clear plastic bottle filled about a third of the way with tiny snipped "
            "crepe paper bits in red, yellow, blue, green, and pink. The bottle is sealed at the top with washi tape. "
            "A small child's hand is holding the bottle mid-shake on a craft table. "
            "Cheerful and bright, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-pinwheel.webp",
        "prompt": (
            "A handmade pinwheel made from a square of pink and blue crepe paper folded into the classic four-blade pinwheel shape "
            "and pinned to a wooden stick with a small pin. The pinwheel is being held up against a sunny window, "
            "with the stick angled so the blades catch the light. Sweet, clearly handmade by a child. "
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
