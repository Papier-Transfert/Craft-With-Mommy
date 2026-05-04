#!/usr/bin/env python3
"""Generate all images for colorful-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "colorful-paper-crafts"
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
        "filename": "colorful-paper-crafts.webp",
        "prompt": (
            "A cheerful flat lay of bright handmade colorful paper crafts on a white craft table: "
            "a rainbow paper plate arch with cotton ball clouds, a tissue paper stained glass square, "
            "a long colorful paper chain garland, a tissue paper flower bouquet in pink, yellow and blue, "
            "a colorful paper pinwheel, and a paper mosaic heart in rainbow colors. "
            "Scissors, glue stick, and bright construction paper scraps visible at the edges. "
            "Joyful colorful mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "rainbow-paper-plate-arch.webp",
        "prompt": (
            "A handmade rainbow paper plate arch craft: a paper plate cut in half "
            "with strips of red, orange, yellow, green, blue, and purple construction paper "
            "glued in a curved arch shape across the half-circle. Two small white cotton ball "
            "clouds glued at each end of the rainbow. Lying flat on a light wood craft table. "
            "Clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-stained-glass.webp",
        "prompt": (
            "A handmade tissue paper stained glass craft: a square frame of black construction paper "
            "with the inside filled with overlapping torn pieces of bright tissue paper "
            "in red, orange, yellow, green, blue, and purple. Sunlight glowing through from behind. "
            "The frame sits on a light wood table. Translucent, glowing colors, child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "colorful-paper-chain-garland.webp",
        "prompt": (
            "A long handmade colorful paper chain garland made from looped construction paper rings "
            "in red, orange, yellow, green, blue, and purple, repeating in rainbow order. "
            "The chain is draped loosely on a white craft table showing about twenty rings. "
            "Cheerful and bright, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-color-wheel.webp",
        "prompt": (
            "A handmade paper plate color wheel craft: a paper plate divided into six wedge-shaped "
            "sections, each one filled with a different color (red, orange, yellow, green, blue, purple) "
            "using thick marker or paint. The wedges are slightly uneven, clearly drawn by a child. "
            "Lying flat on a light wood table next to a black marker. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "rainbow-hot-air-balloon-card.webp",
        "prompt": (
            "A handmade rainbow hot air balloon card: white cardstock with six colored paper strips "
            "(red, orange, yellow, green, blue, purple) stacked in a rounded balloon shape. "
            "A small brown paper rectangle basket hangs below the balloon, connected by thin marker strings. "
            "Lying open on a light wood craft table. Cheerful child-made greeting card. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "colorful-paper-pinwheels.webp",
        "prompt": (
            "Three handmade colorful paper pinwheels with rainbow-striped paper, each folded "
            "into a classic four-blade pinwheel and pinned in the center with a brad. "
            "Each pinwheel is attached to a wooden skewer stick. Standing upright in a small jar "
            "on a light wood craft table. Bright spinning toys, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mosaic-heart.webp",
        "prompt": (
            "A handmade paper mosaic heart craft: a large heart shape on white cardstock "
            "filled with small torn squares of bright construction paper in red, orange, yellow, "
            "green, blue, and purple, glued in an overlapping mosaic pattern. The squares are "
            "slightly uneven, clearly torn by a child. Flat on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-flower-bouquet.webp",
        "prompt": (
            "A handmade tissue paper flower bouquet: five fluffy accordion-folded tissue paper flowers "
            "in pink, yellow, blue, orange, and purple, each with a green pipe cleaner stem. "
            "Bundled together with a white ribbon and resting in a small white vase on a light wood table. "
            "Soft warm daylight. Clearly handmade and charming. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "rainbow-paper-fan.webp",
        "prompt": (
            "A handmade rainbow paper fan: six paper strips in red, orange, yellow, green, blue, "
            "and purple glued together side by side, then accordion-folded into a fan shape, "
            "with one end taped together so the other side fans open. Lying flat on a light wood "
            "craft table next to scissors. Bright cheerful child-made fan. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "colorful-tissue-paper-butterfly.webp",
        "prompt": (
            "A handmade tissue paper butterfly craft: a square of brightly colored tissue paper "
            "(pink, yellow, and blue layered) pinched in the middle with a green pipe cleaner "
            "twisted to form the body, with two pipe cleaner antennae at the top. "
            "Wings fan out colorfully on either side. Resting on a light wood craft table. "
            "Cheerful and magical, child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "rainbow-handprint-tree.webp",
        "prompt": (
            "A handmade rainbow handprint tree craft: a brown paper handprint and forearm shape "
            "glued onto white cardstock as the tree trunk and branches. Small circles of construction "
            "paper in red, orange, yellow, green, blue, and purple are glued around the branches "
            "as colorful leaves. Charming child-made keepsake, lying flat on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strip-peacock.webp",
        "prompt": (
            "A handmade paper peacock craft: a teardrop blue paper body with a small orange beak "
            "and two googly eyes, surrounded by a fan of teardrop loops made from paper strips "
            "in red, orange, yellow, green, blue, and purple as feathers. Lying flat on a "
            "light wood craft table. Bright, child-made, colorful peacock. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "colorful-paper-lantern.webp",
        "prompt": (
            "Three handmade colorful paper lanterns hanging side by side: one pink, one yellow, "
            "one teal blue. Each lantern is a rolled cylinder of bright cardstock with vertical "
            "slits along its body. A paper strip handle attaches at the top. Hanging from a "
            "string against a white wall in soft daylight. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-fruit-slices.webp",
        "prompt": (
            "Four handmade paper plate fruit slices arranged on a white craft table: "
            "a pink watermelon slice with green rind and black seed dots, a green kiwi slice "
            "with brown rim and black seeds, an orange slice with white wedge lines, "
            "and a yellow lemon slice with white wedge lines. Cheerful summer craft, "
            "clearly painted by a child, slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "rainbow-paper-plate-caterpillar.webp",
        "prompt": (
            "A handmade rainbow paper plate caterpillar craft: six paper plate ring sections "
            "painted red, orange, yellow, green, blue, and purple, connected together in a wavy "
            "row by brass fasteners. The first ring has a smiley marker face and two pipe cleaner "
            "antennae. Lying on a light wood craft table. Cheerful and slightly wobbly. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "confetti-paper-collage.webp",
        "prompt": (
            "A handmade confetti paper collage card: a folded white cardstock card with "
            "the front entirely covered in tiny round paper hole-punch dots in pink, yellow, "
            "green, blue, orange, and purple. The dots overlap slightly and are densely packed. "
            "Lying flat on a light wood craft table next to a paper hole punch. Bright child-made card. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "colorful-paper-fish-aquarium.webp",
        "prompt": (
            "A handmade colorful paper fish aquarium scene: blue construction paper background "
            "with five paper fish cut from bright pink, yellow, green, orange, and purple paper. "
            "Each fish has a googly eye and marker scale lines. Long green wavy seaweed strips "
            "and small white circle bubbles surround the fish. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cupcake-liner-flowers.webp",
        "prompt": (
            "Three handmade cupcake liner flowers on green paper stems with leaves: "
            "a pink flower, a yellow flower, and a purple flower, each made from layered "
            "flattened cupcake liners with a button center. The flowers are glued onto a white "
            "cardstock background. Cheerful spring craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "colorful-paper-mobile.webp",
        "prompt": (
            "A handmade colorful paper mobile: a small wooden hoop with strings of varying lengths "
            "hanging down. Each string has a paper shape attached: rainbow circles, bright stars, "
            "and pink and red hearts in a mix of vibrant colors. Hanging in front of a white wall. "
            "Soft warm daylight. Charming child-made decoration. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "colorful-quilling-paper-art.webp",
        "prompt": (
            "A handmade colorful paper quilling craft: a flower shape made from rolled paper "
            "spirals in red, orange, yellow, green, blue, and purple. Each spiral is a thin paper "
            "strip rolled tightly and slightly loosened. The spirals are glued onto white "
            "cardstock in the shape of a flower with petals. Lying flat on a light wood craft table. "
            "Slightly uneven, clearly child-made but pretty. "
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
