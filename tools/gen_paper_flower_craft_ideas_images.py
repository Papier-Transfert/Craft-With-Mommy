#!/usr/bin/env python3
"""Generate all images for paper-flower-craft-ideas.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-flower-craft-ideas"
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
        "filename": "paper-flower-craft-ideas.webp",
        "prompt": (
            "A colorful flat lay of handmade paper flower craft ideas on a white craft table: "
            "an accordion-folded pink paper flower, a fluffy yellow tissue paper pom pom bloom, "
            "a coffee filter flower painted in soft watercolors, a paper plate sunflower with yellow petals, "
            "a small toilet paper roll tulip in red, and a paper strip spiral rose in pink. "
            "Scissors, glue stick, and colorful paper scraps visible at the edges. "
            "Warm spring mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "accordion-fold-paper-flower.webp",
        "prompt": (
            "A handmade accordion-folded paper flower: a long strip of pink construction paper "
            "folded into narrow pleats across its full length, then fanned open and pinched at the center "
            "to form a full round bloom. A green pipe cleaner twisted around the center serves as a stem. "
            "The flower sits on a light wood craft table with leftover paper strips nearby. "
            "Charming and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-pom-pom-flower.webp",
        "prompt": (
            "Several fluffy tissue paper pom pom flowers in pink, yellow, and lavender arranged together "
            "on a light craft table. Each pom pom is made from multiple accordion-folded tissue paper layers "
            "with individual sheets pulled apart and fluffed outward into a full round bloom. "
            "Green pipe cleaners act as stems. Soft pastel spring colors, sweet and decorative. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "coffee-filter-flower.webp",
        "prompt": (
            "Three handmade coffee filter flowers on a craft table: each basket-style coffee filter "
            "has been painted with soft watercolors in pink, orange, and purple, allowed to dry, "
            "then pinched at the center and wrapped with a green pipe cleaner stem. "
            "The filters create ruffled, soft petal shapes. Small watercolor pan set and brush visible nearby. "
            "Delicate and pretty, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-sunflower.webp",
        "prompt": (
            "A handmade paper plate sunflower on a craft table: a full paper plate painted yellow "
            "with long oval yellow construction paper petals glued all around the rim, "
            "and the center filled with torn brown paper scraps to mimic sunflower seeds. "
            "A wide green paper strip serves as the stem with two simple leaf cutouts attached. "
            "Cheerful and bright, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cupcake-liner-daffodil.webp",
        "prompt": (
            "Several handmade cupcake liner daffodils on a craft table: yellow cupcake liners "
            "with small triangle notches cut around the edge forming petal shapes, "
            "and a smaller orange liner pushed through the center to create the classic daffodil trumpet. "
            "Each flower is glued onto a green paper strip stem. "
            "Five daffodils in a cluster, bright yellow and orange, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "toilet-paper-roll-tulip.webp",
        "prompt": (
            "Several handmade toilet paper roll tulips standing in a small mason jar on a craft table: "
            "empty toilet paper rolls with the tops pinched and folded into rounded tulip shapes, "
            "wrapped in red and pink construction paper. Wide green paper strips serve as stems "
            "attached below each tulip bloom. Three to four tulips of different heights in the jar. "
            "Sweet spring craft, clearly handmade by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strip-spiral-rose.webp",
        "prompt": (
            "A handmade paper spiral rose sitting on a craft table next to the red cardstock square it was cut from: "
            "the rose is made from a single red paper square cut into a continuous spiral strip, "
            "rolled from the outside inward and glued at the base to hold a three-dimensional rose shape. "
            "The finished rose sits beside scissors and the remaining paper square with the spiral cut visible. "
            "Elegant and realistic-looking handmade rose. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-paper-tulip.webp",
        "prompt": (
            "A finished origami paper tulip in bright pink with a green origami stem and leaf standing upright "
            "on a wooden craft table. The tulip bloom is three-dimensional with visible fold lines creating "
            "the characteristic rounded tulip shape. The green stem piece connects neatly below the bloom. "
            "Two more completed origami tulips in yellow and purple stand nearby. "
            "Clean, beautiful origami folding, clearly crafted with care. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "crepe-paper-carnation.webp",
        "prompt": (
            "Handmade crepe paper carnations in pink and white standing in a small vase on a craft table: "
            "each carnation is made from multiple crepe paper circles cut into petal shapes and layered together, "
            "with each layer fluffed and ruffled upward to create the dense, layered look of a real carnation. "
            "Green pipe cleaner stems hold each flower. Three carnations of different heights in the vase. "
            "Beautifully textured and romantic-looking handmade flowers. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-daisy.webp",
        "prompt": (
            "A handmade construction paper daisy on a craft table: a large yellow circle center "
            "with eight to ten white oval petal shapes glued evenly around the back so they radiate outward. "
            "A green construction paper strip forms the stem below the daisy, with two simple leaf cutouts "
            "attached at the sides. The flower is laid flat on a wooden surface. "
            "Simple, cheerful, and clearly cut by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fan-flower.webp",
        "prompt": (
            "A handmade paper fan flower on a craft table: two sheets of orange and yellow construction paper "
            "accordion-folded and joined at both ends to form a full round fan flower shape. "
            "A small contrasting red circle is glued to the center of the flower. "
            "The finished flower is laid flat on a light wood surface next to two more fan flowers "
            "in purple and blue. Cheerful and graphic, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-loop-flower-wreath.webp",
        "prompt": (
            "A handmade paper wreath covered in small loop paper flowers on a craft table: "
            "a large cardstock ring base covered in dozens of small flowers, each made from "
            "paper strip loops arranged in a circle around a small paper circle center. "
            "Flowers in pink, yellow, orange, and green cover the entire ring. "
            "The wreath lies flat on a white surface showing the full cheerful design. "
            "Colorful spring decoration, clearly handmade with care. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "wax-paper-flower-suncatcher.webp",
        "prompt": (
            "A handmade wax paper flower suncatcher taped to a sunny window: "
            "two sheets of wax paper sealed together with an iron, with small tissue paper squares "
            "inside arranged in a flower pattern with pink and orange petals and a yellow center. "
            "Warm sunlight shines through the tissue paper creating a glowing stained glass effect. "
            "The flower shape is cut from the wax paper panel with clean edges. "
            "Beautiful translucent colors against the bright window. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-heart-petal-flower.webp",
        "prompt": (
            "A handmade paper heart petal flower on a craft table: six pink construction paper hearts "
            "of the same size arranged in a circle with the pointed tips meeting at the center, "
            "glued flat so the rounded tops face outward as petals. A small yellow circle covers "
            "the center point where all the hearts meet. A green paper strip stem is attached below. "
            "Sweet and simple, laid flat on a white craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pinwheel-flower.webp",
        "prompt": (
            "A colorful handmade paper pinwheel flower mounted on a straw: a square of bright striped paper "
            "with four diagonal cuts from the corners toward the center, with alternating corner points "
            "folded to the center and secured with a small brad, creating a pinwheel shape. "
            "The pinwheel sits on a white paper straw. Two more pinwheels in different colors "
            "stand nearby in a small cup. Bright and playful craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "egg-carton-flower.webp",
        "prompt": (
            "Handmade egg carton flowers in a bundle on a craft table: individual cardboard egg carton cups "
            "trimmed into petal shapes all around the edge and painted in bright pink, yellow, and orange. "
            "Each flower has a green pipe cleaner stem poked through the base and a small yellow pom pom "
            "glued to the center. Five flowers held together as a bouquet. "
            "Dimensional and sculptural, clearly handmade by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mosaic-flower-card.webp",
        "prompt": (
            "A handmade paper mosaic flower card on a craft table: a white cardstock background "
            "with a large flower outline filled in with dozens of small torn and cut paper squares "
            "in purple, pink, and lilac petals and yellow center pieces, glued closely together "
            "in a mosaic pattern. The background around the flower is left white. "
            "Detailed and colorful, clearly made by a child with small paper scraps and glue. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-straw-flower.webp",
        "prompt": (
            "A handmade paper straw flower on a craft table: short segments of colorful paper straws "
            "arranged in a flower pattern on a blue paper background, with straw pieces radiating outward "
            "from a circular cluster of straw segments at the center to form petals. "
            "A green paper stem is glued below the straw flower shape. "
            "The hollow round ends of each straw segment face upward. Geometric and unusual craft look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-chain-flower-garland.webp",
        "prompt": (
            "A handmade paper chain flower garland draped across a light-colored wall: "
            "small paper loop flowers in pink, yellow, orange, and red connected along a ribbon or paper strip chain. "
            "Each flower is made from small paper loops arranged around a circle center. "
            "The garland stretches across the wall showing about ten flowers at different sizes. "
            "Colorful spring decoration, cheerful and clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-bag-flower-bouquet.webp",
        "prompt": (
            "A handmade paper bag flower bouquet on a craft table: a small white paper gift bag "
            "decorated with marker drawings of hearts and dots, holding seven colorful paper flowers "
            "on green paper strip stems. The flower heads, in pink, orange, yellow, and red, "
            "fan out above the bag opening like a real gift bouquet. "
            "Sweet and gift-worthy, clearly made by a young child. "
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
