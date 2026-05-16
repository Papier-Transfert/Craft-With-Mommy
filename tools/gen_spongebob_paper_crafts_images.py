#!/usr/bin/env python3
"""Generate all images for spongebob-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "spongebob-paper-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Wooden craft table surface, soft blue table cloth or pale wood. "
    "Clean, cheerful, family-friendly atmosphere. Landscape orientation 4:3. "
    "Bright primary colors with yellow, red, blue, and pink tones. "
    "No copyrighted logos or trademark text. Real handmade construction-paper craft style with simple shapes. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

SPONGE_DESC = (
    "a simple handmade paper character cut from bright yellow construction paper, "
    "shaped like a tall yellow rectangle or square with rounded corners, "
    "with two big round white oval eyes with small black pupils, "
    "a wide goofy smile with two square white teeth, small black freckle dots on the cheeks, "
    "wearing a small white paper shirt with a red paper tie at the bottom"
)

IMAGES = [
    {
        "filename": "spongebob-paper-crafts.webp",
        "prompt": (
            "A bright flat lay of handmade paper crafts featuring an underwater sea world theme on a soft blue craft table: "
            f"in the center, {SPONGE_DESC}; "
            "around it, a pink paper starfish with a silly face, a tall yellow paper pineapple house with green leafy top, "
            "a blue paper snail, and a small paper jellyfish with wiggly paper strip tentacles. "
            "Yellow, pink, blue, and red construction paper scraps, scissors, and a glue stick visible at the edges. "
            "Cheerful underwater mood, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spongebob-paper-plate-face.webp",
        "prompt": (
            "A handmade craft made from a small round paper plate painted bright yellow as the round face, "
            f"in the style of {SPONGE_DESC}. "
            "Big oval white eyes with black dot pupils, a wide goofy smile with two square teeth, "
            "small black freckle dots on the cheeks, and a small red paper tie glued at the bottom. "
            "Lying flat on a soft blue craft table. Charming child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spongebob-paper-doll.webp",
        "prompt": (
            f"A handmade flat paper doll cutout of {SPONGE_DESC}, "
            "a tall yellow square standing figure made from bright yellow construction paper, "
            "with brown paper shorts, a small white paper shirt, and a red paper tie. "
            "Lying flat on a pale wood craft table next to bright construction paper scraps and a glue stick. "
            "Clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spongebob-bookmark.webp",
        "prompt": (
            f"A handmade triangular paper corner bookmark cut from bright yellow paper, in the style of {SPONGE_DESC}. "
            "The face has two big round white eyes with black dot pupils, "
            "a wide goofy smile, and small black freckle dots, sitting on the corner of an open storybook. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pineapple-house-paper-craft.webp",
        "prompt": (
            "A handmade paper pineapple house craft, made from a tall yellow paper oval shape "
            "with crosshatch lines drawn on it with a brown marker, topped with a leafy green paper crown of pointy leaves. "
            "Glued on the front: a small round brown paper door and two small light blue paper windows. "
            "Lying flat on a soft blue craft table next to construction paper scraps. "
            "Cheerful underwater home, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patrick-star-paper-craft.webp",
        "prompt": (
            "A handmade paper starfish craft cut from bright pink construction paper, "
            "shaped like a chubby five-pointed star with rounded points. "
            "Two simple oval white eyes with black dot pupils, thick black eyebrows drawn above, "
            "and a wide silly smile drawn with a black marker. "
            "Below the body, small green paper shorts with little purple flower dots glued on. "
            "Lying flat on a soft blue craft table next to paper scraps. Cheerful and silly. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "squidward-paper-craft.webp",
        "prompt": (
            "A handmade paper craft of a tall light blue or teal oval head shape with a long pointed nose, "
            "two droopy half-closed eyes, and a small frown drawn with a black marker. "
            "Six small tentacle strips at the bottom. A small light brown paper striped shirt glued at the base of the head. "
            "Cut from construction paper, lying flat on a soft blue craft table. "
            "Charming child-made craft with a grumpy expression. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spongebob-paper-bag-puppet.webp",
        "prompt": (
            f"A handmade paper bag puppet made from a small yellow paper lunch bag with the flap forming the face, in the style of {SPONGE_DESC}. "
            "On the flap, big white oval eyes with black dot pupils, a goofy smile with square teeth, and freckle dots. "
            "Small yellow paper arms and legs glued to the sides and bottom of the bag, "
            "and a small red paper tie glued at the bottom front of the bag. "
            "Standing upright on a pale wood craft table next to scissors and paper scraps. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spongebob-paper-crown.webp",
        "prompt": (
            "A wearable handmade paper crown: a long bright yellow construction paper strip sized for a child's head, "
            f"with a row of mini paper sponge faces along the top edge in the style of {SPONGE_DESC}: "
            "each tiny face has two dot eyes, a goofy smile, and a small red tie. "
            "Lying flat on a pale wood craft table or shown displayed standing in a circle. "
            "Cheerful child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "sandy-cheeks-paper-craft.webp",
        "prompt": (
            "A handmade paper craft of a brown squirrel character face with two round cheeks, "
            "two small ears, and a fluffy curved tail behind the head. "
            "Around the head, a round clear circle outlined in light blue marker to look like a glass helmet, "
            "with a small pink paper flower glued on top of the helmet. "
            "Cut from construction paper, lying flat on a soft blue craft table. "
            "Sweet child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "krabby-patty-paper-craft.webp",
        "prompt": (
            "A handmade paper burger craft made of layered paper circles: "
            "a round tan bun on top, a brown round patty layer, a curly green paper lettuce frill, "
            "a yellow paper cheese square corner peeking out, a red paper tomato slice, "
            "and a tan paper bottom bun. Stacked slightly 3D with thin glue dots. "
            "Lying on a pale wood craft table next to paper scraps and a glue stick. "
            "Cheerful, looks good enough to pretend-eat. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spongebob-mini-notebook.webp",
        "prompt": (
            "A small handmade mini notebook, the cover wrapped in bright yellow construction paper, "
            f"with a hand-drawn face in the style of {SPONGE_DESC} on the front along with three small white paper bubble cutouts. "
            "Light blue washi tape borders along the top and bottom edges of the cover. "
            "Sitting flat on a pale wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "jellyfish-paper-craft.webp",
        "prompt": (
            "A handmade paper jellyfish craft: a soft pink half-circle paper dome as the body, "
            "with several thin curly pink paper strips glued underneath as wiggly tentacles. "
            "Two tiny black dot eyes and a small smile drawn on the dome with a marker. "
            "Lying flat on a soft blue craft table next to scissors and bright paper scraps. "
            "Sweet child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spongebob-greeting-card.webp",
        "prompt": (
            "A handmade folded greeting card on bright yellow cardstock standing on a craft table. "
            f"On the front, a glued-on paper face cutout in the style of {SPONGE_DESC}, "
            "with a tiny white paper bubble in the bottom corner. "
            "Sitting upright on a soft blue craft table. Cheerful atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "mr-krabs-paper-craft.webp",
        "prompt": (
            "A handmade paper crab craft cut from bright red construction paper: "
            "a round red oval body with two large red claw shapes on the sides and six small red leg strips at the bottom. "
            "Two googly eyes on tall white paper stalks rising above the body, and a wide friendly smile drawn with a black marker. "
            "Lying flat on a soft blue craft table next to paper scraps. "
            "Cheerful and goofy, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "gary-snail-paper-craft.webp",
        "prompt": (
            "A handmade paper snail craft with a swirly pink paper spiral shell glued on top of a small blue snail body. "
            "The blue body has two tall paper eye stalks with tiny black dot eyes on top, and a small smile drawn with a black marker. "
            "Lying flat on a soft blue craft table next to paper scraps and scissors. "
            "Sweet child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spongebob-origami-face.webp",
        "prompt": (
            f"A simple folded yellow paper origami face in the style of {SPONGE_DESC}, "
            "made from a yellow square folded into a flat face shape with a small fold at the bottom for the red paper tie. "
            "Two big round white eyes with black dot pupils, a wide goofy smile with two square teeth, "
            "and small black freckle dots drawn with marker. "
            "Lying flat on a soft blue craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "bikini-bottom-scene.webp",
        "prompt": (
            "A handmade flat paper collage on a light blue construction paper background, "
            "depicting an underwater sea scene with several glued cutouts: "
            f"in the center, a small yellow paper character in the style of {SPONGE_DESC}; "
            "a pink paper starfish with silly face; a small blue paper snail; "
            "two simple pink paper jellyfish with tentacle strips; "
            "and a tall yellow paper pineapple house in the corner. "
            "Small white paint marker bubble dots scattered across the blue background. "
            "Lying flat on a pale wood craft table, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spongebob-paper-garland.webp",
        "prompt": (
            "A handmade paper garland made from small alternating yellow square sponge faces "
            f"in the style of {SPONGE_DESC} "
            "and small pink paper starfish shapes, strung on bakery twine. "
            "Each yellow square has dot eyes and a goofy smile drawn on it. "
            "Draped loosely on a pale wood craft table. Cheerful and festive, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spongebob-paper-lantern.webp",
        "prompt": (
            "A handmade yellow paper lantern: a tube of bright yellow cardstock with evenly spaced vertical slits cut along the body, "
            f"with a small paper face in the style of {SPONGE_DESC} glued to the front, "
            "and light blue washi tape strips along the top and bottom edges. "
            "Sitting upright on a pale wood craft table. Cheerful decoration. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "spongebob-treat-box.webp",
        "prompt": (
            "A small handmade paper treat box, about the size of a fist, folded from bright yellow cardstock. "
            f"On the front, a glued paper face in the style of {SPONGE_DESC} with a tiny red ribbon bow on top. "
            "The box is closed and sitting upright on a pale wood craft table next to a tiny folded note. "
            "Adorable gift box, clearly child-made. "
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
