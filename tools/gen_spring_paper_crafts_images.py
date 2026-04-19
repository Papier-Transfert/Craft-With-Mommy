#!/usr/bin/env python3
"""Generate all images for spring-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "spring-paper-crafts"
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
        "filename": "spring-paper-crafts.webp",
        "prompt": (
            "A colorful flat lay of handmade spring paper crafts on a white craft table: "
            "a paper butterfly with decorated wings, a paper tulip bouquet in pink and red, "
            "a paper rainbow with cotton ball clouds, a paper ladybug in red with black spots, "
            "a paper bunny in white with tall ears, and a small paper flower wreath. "
            "Scissors, glue stick, and colorful construction paper scraps visible at the edges. "
            "Bright cheerful spring mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-butterfly.webp",
        "prompt": (
            "A handmade paper butterfly craft on a white craft table. "
            "Two large symmetrical wings cut from a single folded sheet of bright pink and yellow construction paper, "
            "decorated with marker polka dots and swirls. "
            "The center is pinched together and wrapped with a green pipe cleaner that forms the body and two antennae with small dot tips. "
            "Wings open flat showing colorful patterns. Charming, child-made look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-tulip.webp",
        "prompt": (
            "Three handmade paper tulips standing in a small mason jar on a craft table. "
            "Each tulip has four rounded petal shapes cut from red, pink, and purple construction paper "
            "gathered at the base around a long green paper strip stem, with two small green leaf shapes attached. "
            "The tulips look slightly different from each other, clearly child-made. "
            "Warm spring atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-rainbow.webp",
        "prompt": (
            "A handmade paper rainbow craft lying flat on a white craft table. "
            "Six arched strips of construction paper in red, orange, yellow, green, blue, and purple "
            "are layered concentrically to form a full rainbow arch. "
            "Two small fluffy white cotton ball clouds are glued at each end of the rainbow. "
            "Bright, cheerful spring craft, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-chick.webp",
        "prompt": (
            "A handmade paper Easter chick craft on a white craft table. "
            "A large yellow construction paper circle body with a smaller yellow circle head on top. "
            "An orange triangle beak, two small orange feet cut from paper at the bottom, "
            "and two small black googly eyes on the face. "
            "Small yellow tissue paper fringe pieces tucked around the body like fluffy feathers. "
            "Adorable and simple, clearly made by a toddler. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-bee.webp",
        "prompt": (
            "A handmade paper bee craft on a white craft table. "
            "A fat yellow construction paper oval body with three thin black paper strips glued across it as stripes. "
            "Two small white tissue paper wings attached symmetrically on the sides. "
            "A tiny black triangle stinger at the back end, two googly eyes at the front. "
            "A loop of white thread at the top for hanging. Cute and cheerful, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-caterpillar.webp",
        "prompt": (
            "A handmade paper caterpillar craft on a white craft table. "
            "A long green construction paper strip accordion-folded into a zigzag body. "
            "A large bright green circle glued at one end as the head, with two small googly eyes, "
            "a tiny red smile drawn with marker, and two short green pipe cleaner antennae curling upward. "
            "The accordion body looks springy. Simple and charming, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-kite.webp",
        "prompt": (
            "A handmade paper kite craft lying on a light wood craft table. "
            "A large diamond shape cut from bright orange cardstock decorated with red and yellow crayon stripes. "
            "A long colorful ribbon tail attached at the bottom corner with several small bow ties tied along it. "
            "A piece of white string attached at the top corner. "
            "Fresh and cheerful spring craft, clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-ladybug.webp",
        "prompt": (
            "A handmade paper ladybug craft on a white craft table. "
            "A large red construction paper circle with a fold down the center creating two open wing halves. "
            "A smaller black semicircle glued at the top for the head with two small googly eyes. "
            "Five or six black paper circle spots glued on the red wings. "
            "A thin black marker line drawn down the center fold. Cheerful and simple, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-bird-nest.webp",
        "prompt": (
            "A handmade paper bird nest craft on a white craft table. "
            "A small bowl-shaped piece of brown cardstock filled with torn strips of brown and tan paper "
            "layered inside to look like nest material. "
            "Three small oval paper eggs in pale blue and white sit nestled inside the paper strips. "
            "Some paper strips hang slightly over the edge. Sweet and realistic-looking, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-frog.webp",
        "prompt": (
            "A handmade paper frog craft on a white craft table. "
            "A large bright green construction paper circle body with a smaller green oval head attached at the top. "
            "Two large white circle eyes with black paper pupils sitting on top of the head. "
            "Two pairs of rounded green legs folded at the ends to create flat feet. "
            "A wide smile and red tongue drawn with marker. Friendly and cute, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-umbrella.webp",
        "prompt": (
            "A handmade paper umbrella craft on a white craft table. "
            "A large semicircle of bright teal construction paper with colorful polka dots drawn on it, "
            "folded into a gentle dome shape and glued. "
            "A thin rolled brown paper tube attached underneath as the handle with a small curl at the bottom. "
            "The umbrella stands upright on its handle tip. Cheerful spring craft, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-dragonfly.webp",
        "prompt": (
            "A handmade paper dragonfly craft on a white craft table. "
            "A thin rolled blue construction paper tube as the elongated body. "
            "Four large translucent-looking wings made from light blue tissue paper attached symmetrically, "
            "two on each side, with delicate vein lines drawn in light marker. "
            "Two small googly eyes at the front of the body. "
            "Elegant and delicate-looking, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-bunny.webp",
        "prompt": (
            "A handmade paper bunny craft on a white craft table. "
            "A large white construction paper circle body and a smaller white oval head. "
            "Two tall narrow white ear shapes with pink centers, a tiny pink triangle nose, "
            "three thin marker-drawn whiskers on each side, and two small dot eyes. "
            "A small white cotton ball tail at the back. "
            "Sweet and simple, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-sunflower.webp",
        "prompt": (
            "A handmade paper sunflower craft in a small mason jar on a white craft table. "
            "A large brown paper circle center surrounded by fourteen bright yellow construction paper petal shapes. "
            "Small black marker dots drawn on the brown center to look like seeds. "
            "A long green paper strip stem with two green leaf shapes attached on each side. "
            "Cheerful and bright, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-duck.webp",
        "prompt": (
            "A handmade paper duck craft standing upright on a white craft table. "
            "Two identical yellow construction paper duck shapes glued back-to-back with a small folded base tab "
            "so the duck stands on its own. "
            "An orange triangle beak folded and attached, a small dot eye drawn with marker, "
            "and a small white tissue paper wing detail on the side. "
            "Cute and simple, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-snail.webp",
        "prompt": (
            "A handmade paper snail craft on a white craft table. "
            "A long multicolored paper strip rolled tightly into a flat spiral shell with the end glued. "
            "A small light green paper oblong attached underneath as the body and head. "
            "Two short green pipe cleaner antennae curling upward from the head with tiny paper dots at the tips. "
            "The spiral shell shows colorful marker decorations that were added before rolling. "
            "Charming and creative, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-cloud-mobile.webp",
        "prompt": (
            "A handmade paper cloud mobile hanging against a light wall. "
            "A small wooden twig or dowel with five white cardstock cloud shapes hanging at different lengths "
            "on white string. Several small light blue paper teardrop raindrop shapes hang below some of the clouds. "
            "The clouds have slightly uneven edges, clearly cut by a child. "
            "Soft, dreamy spring decoration look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-raindrop-garland.webp",
        "prompt": (
            "A handmade paper raindrop garland draped across a light wood shelf. "
            "About twelve teardrop-shaped paper cutouts in shades of sky blue and light lavender, "
            "each with a small hole punched at the narrow top, threaded onto a long piece of natural twine. "
            "The raindrops hang at slightly different angles. "
            "Simple and charming spring decoration, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-strawberry.webp",
        "prompt": (
            "A handmade paper strawberry craft on a white craft table. "
            "A large red construction paper heart shape as the strawberry body covered in small yellow marker dots as seeds. "
            "Three small bright green paper leaf shapes glued at the rounded top and a short green paper stem. "
            "Three strawberries of slightly different sizes arranged together. "
            "Cheerful and sweet, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spring-paper-flower-wreath.webp",
        "prompt": (
            "A handmade paper flower wreath on a white craft table. "
            "A large paper plate ring with the center cut out, covered in overlapping handmade paper flower shapes "
            "in pink, yellow, and white construction paper with yellow centers. "
            "Small green paper leaf shapes tucked between the flowers around the ring. "
            "A pink ribbon bow tied at the top. "
            "Colorful and impressive-looking, clearly child-made and slightly imperfect. "
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

    from PIL import Image as PILImage
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
