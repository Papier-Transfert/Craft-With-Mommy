#!/usr/bin/env python3
"""Generate all images for shredded-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "shredded-paper-crafts"
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
        "filename": "shredded-paper-crafts.webp",
        "prompt": (
            "A colorful flat lay of handmade shredded paper crafts on a white craft table: "
            "a brown shredded paper bird's nest with pastel paper eggs, a yellow lion face with an "
            "orange shredded paper mane, a black sheep covered in white shredded paper wool, "
            "a smiling sun with yellow shredded paper rays, and rainbow shredded paper strips "
            "arranged in stripes. Scissors, a glue bottle, and small piles of shredded paper "
            "in red, yellow, blue, green visible at the edges. Cheerful warm mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-bird-nest.webp",
        "prompt": (
            "A handmade bird's nest collage made from a thick ring of brown shredded paper "
            "glued in a circle on cream cardstock, with three small pale-blue construction paper "
            "egg shapes nestled in the center. Flat lay on a light wood craft table. "
            "Cozy springtime feel, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-sensory-bin.webp",
        "prompt": (
            "A shallow rectangular plastic tub on a wooden table filled with a generous pile of "
            "colorful shredded paper in pink, yellow, green, and blue. Two small wooden scoops, "
            "a few rainbow pom poms, and small toy animals are partially buried in the shreds. "
            "A child's hand reaches into the bin. Bright, cheerful, sensory play scene. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-lion-mane.webp",
        "prompt": (
            "A handmade lion craft: a round yellow construction paper face with a friendly "
            "drawn smile, two small black paper triangle ears, a brown nose, and dot eyes. "
            "Around the entire edge of the face is a thick fluffy mane made from orange and yellow "
            "shredded paper glued in a ring. Lying flat on a white craft table. Charming and "
            "playful, clearly a child's craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-easter-basket.webp",
        "prompt": (
            "A small handmade paper Easter basket sitting on a white craft table, filled with "
            "fluffy green shredded paper grass and topped with three pastel cardstock egg cutouts "
            "in pink, blue, and yellow. The basket is decorated with a simple paper handle. "
            "Soft springtime atmosphere, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-sheep.webp",
        "prompt": (
            "A handmade sheep craft on cream cardstock: a black construction paper sheep body shape "
            "with a small black face, two googly eyes, and four short legs, completely covered "
            "with fluffy white shredded paper to look like wool. The shreds bunch and curl naturally "
            "across the body. Lying flat on a craft table. Cute springtime craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-santa-beard.webp",
        "prompt": (
            "A handmade Santa face craft: a round pink-beige construction paper face with a red "
            "triangle cardstock hat at the top, two small black dot eyes, a tiny pink nose, "
            "and a thick fluffy puffy beard made from white shredded paper covering the bottom of the face. "
            "A white pom pom or paper circle decorates the tip of the hat. Lying flat on a craft table. "
            "Festive holiday craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-scarecrow.webp",
        "prompt": (
            "A handmade scarecrow face craft on green cardstock: a circular tan construction paper face "
            "with two button eyes, a stitched smile drawn in marker, a small triangle nose, and a wide "
            "brown paper hat on top. Yellow shredded paper sticks out from under the hat brim and along "
            "the cheeks like straw hair. Charming fall craft, lying flat on a craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-hedgehog.webp",
        "prompt": (
            "A handmade hedgehog craft: a brown teardrop body shape on cream cardstock with "
            "a small triangular black nose, two small googly eyes, a tiny smile, and four small feet. "
            "The rounded back is covered in clumps of brown and tan shredded paper to look like prickly spines. "
            "Lying flat on a craft table. Sweet woodland craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-fireworks.webp",
        "prompt": (
            "A handmade fireworks picture on dark blue cardstock: three bursts of bright shredded paper "
            "in red, yellow, and white arranged radiating outward from center points to look like exploding fireworks "
            "in the night sky. The strips form starburst patterns. Flat lay photo on a craft table. "
            "Festive Fourth of July craft, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-sun-rays.webp",
        "prompt": (
            "A handmade smiling sun craft: a large yellow cardstock circle face with a happy smile, "
            "two simple eyes, and rosy cheeks, surrounded by a fluffy ring of yellow and orange "
            "shredded paper sun rays curling outward in all directions. The shreds look soft and bright. "
            "Lying flat on a white craft table. Bright, cheerful summer craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-self-portrait.webp",
        "prompt": (
            "A handmade child's self-portrait on cream cardstock: a simple oval face shape drawn in "
            "marker with two eyes, a small nose, and a smiling mouth, topped with a generous tuft of "
            "brown curly shredded paper glued on as hair. Charming and slightly silly. Lying flat on a "
            "craft table. Clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-turkey.webp",
        "prompt": (
            "A handmade turkey craft: a round brown construction paper body shape with two googly eyes, "
            "an orange triangle beak, and a small red wattle. Behind the body fans out a wide spray of "
            "red, orange, yellow, and brown shredded paper feathers radiating outward. Lying flat on a "
            "white craft table. Festive Thanksgiving craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-snowman.webp",
        "prompt": (
            "A handmade snowman craft on light blue cardstock: three stacked white fluffy circles "
            "made from white shredded paper, with a black paper top hat at the top, two black dot eyes, "
            "an orange triangle carrot nose, three black button dots down the middle, and two simple "
            "brown paper twig arms. Lying flat on a craft table. Cozy winter craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-mache-bowl.webp",
        "prompt": (
            "A handmade paper mache bowl drying upside down on a craft table. The bowl is made from "
            "layered strips of white and tan shredded paper coated in flour-water paste, with a "
            "rough lumpy texture clearly visible. The bowl is small, slightly imperfect, and obviously "
            "handmade by a child. Photographed on a wooden surface with a small dish of paste nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-rainbow.webp",
        "prompt": (
            "A handmade rainbow craft on white cardstock: curving stripes of red, orange, yellow, "
            "green, blue, and purple shredded paper glued in arching bands across the page. "
            "At each end of the rainbow is a fluffy white shredded paper cloud. A few blue raindrops "
            "fall below the clouds. Lying flat on a craft table. Bright cheerful craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-confetti-card.webp",
        "prompt": (
            "A handmade greeting card on a craft table, opened slightly. The front of the card is "
            "completely covered in tiny pieces of bright multicolor shredded paper confetti glued in place "
            "to form a celebration texture. A simple word like 'Hooray' is visible somewhere on the front "
            "in handwritten marker. Festive birthday or party craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-haystack.webp",
        "prompt": (
            "A handmade farm scene on green cardstock: three rounded mounds of yellow shredded paper "
            "glued in haystack shapes across the foreground, a small red paper barn with a triangle roof "
            "in the background, two simple cardstock farm animals (a cow and a sheep), and a strip of "
            "blue paper sky across the top with a yellow paper sun. Lying flat on a craft table. "
            "Charming countryside craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-fluffy-dog.webp",
        "prompt": (
            "A handmade fluffy dog craft: a cardstock dog body shape with floppy paper ears, a small "
            "black triangle nose, two googly eyes, a smiling mouth, and a stuck-out pink tongue. "
            "The body, head, and tail are completely covered in tan and cream shredded paper to look "
            "like soft fluffy dog fur. Lying flat on a white craft table. Sweet pet craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-underwater.webp",
        "prompt": (
            "A handmade underwater scene on blue cardstock: tall green shredded paper seaweed standing "
            "upright across the bottom half of the page, a few cardstock fish in orange and yellow "
            "swimming above, an orange paper starfish, and a smiling red paper crab on the ocean floor. "
            "A sprinkle of tan shredded paper sand at the very bottom. Lying flat on a craft table. "
            "Peaceful ocean craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "shredded-paper-mosaic-heart.webp",
        "prompt": (
            "A handmade mosaic heart on white cardstock: a large heart shape outline filled completely "
            "with small clumps of red, pink, and white shredded paper glued in a textured mosaic pattern. "
            "The shades are layered in a soft gradient from light pink at the top to deep red at the bottom. "
            "Lying flat on a craft table. Sweet Valentine's Day craft, clearly child-made. "
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
