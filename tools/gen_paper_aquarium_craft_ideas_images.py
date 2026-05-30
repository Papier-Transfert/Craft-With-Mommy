#!/usr/bin/env python3
"""Generate all images for paper-aquarium-craft-ideas.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-aquarium-craft-ideas"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper, tissue paper, paper plates, "
    "and ordinary household craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-aquarium-craft-ideas.webp",
        "prompt": (
            "A colorful flat lay of handmade paper aquarium crafts arranged together on a white craft table: "
            "a paper plate decorated like an aquarium window with cut paper fish inside, "
            "a tissue paper jellyfish with curly streamer tentacles, "
            "a construction paper seahorse, "
            "a paper strip octopus with eight curled legs, "
            "a paper plate crab, an origami tropical fish, "
            "blue and green paper seaweed strips, and a coral reef collage. "
            "Scissors, glue sticks, and colorful construction paper scraps visible at the edges. "
            "Bright underwater colors: blue, orange, yellow, pink, green. "
            "Clearly made by children, cheerful ocean theme. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-aquarium-window.webp",
        "prompt": (
            "A handmade paper plate aquarium craft: a white paper plate with the center cut out, "
            "with blue cellophane or blue tissue paper stretched across the back, "
            "and small construction paper fish in orange, yellow, and red glued to the blue background. "
            "Tiny paper bubbles drawn on. Green paper seaweed strips at the bottom. "
            "Flat lay on a light craft table. Looks like a child made it. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-bag-fish-puppet.webp",
        "prompt": (
            "A handmade paper bag fish puppet: a small brown or white paper lunch bag laid flat, "
            "decorated with overlapping colorful paper scale shapes in pink, orange, and yellow. "
            "A big googly eye glued near the top fold of the bag, "
            "with paper triangle fins and a tail at one end. "
            "Sitting flat on a craft table next to scissors. "
            "Clearly child-made with uneven scales. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-jellyfish.webp",
        "prompt": (
            "A handmade tissue paper jellyfish craft: a rounded pink and purple tissue paper "
            "bell-shaped dome with long curly streamers of pink, purple, and white tissue paper "
            "hanging down as tentacles. Two tiny googly eyes on the dome. "
            "Hanging or laid flat on a light blue paper background to suggest water. "
            "Cheerful and slightly floppy, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cardboard-box-aquarium-diorama.webp",
        "prompt": (
            "A handmade cardboard box aquarium diorama craft: a shoebox stood on its long side "
            "with the inside walls covered in blue construction paper, "
            "and small paper fish in orange, yellow, and pink dangling from strings inside the box. "
            "Sand colored paper at the bottom with small paper rocks and green paper seaweed. "
            "A paper coral and tiny paper bubbles. "
            "Photographed from the open front of the box. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strip-octopus.webp",
        "prompt": (
            "A handmade paper strip octopus craft: a round purple construction paper head shape "
            "with two large googly eyes glued on, and eight long purple paper strips curled into spirals "
            "around the bottom edge as tentacles. The curled strips hang downward. "
            "Sitting flat on a light craft table. Cheerful and clearly handmade by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-seahorse.webp",
        "prompt": (
            "A handmade construction paper seahorse craft: a yellow or orange seahorse shape "
            "cut from construction paper with a curled tail at the bottom, a small fin on the back, "
            "and a googly eye glued on the head. Decorated with small dot stickers or marker spots. "
            "Glued onto a blue construction paper background suggesting water. "
            "Flat lay on a craft table, clearly cut by a child with slightly uneven edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-coral-reef-collage.webp",
        "prompt": (
            "A handmade paper coral reef collage: a blue construction paper background "
            "with colorful torn and cut paper shapes glued on to form a coral reef scene: "
            "branching pink and orange coral, green paper seaweed strips, "
            "yellow paper sea anemones with curled tentacles, and a few small paper fish swimming above. "
            "Bright tropical colors. Clearly child-made with a torn-paper texture. Flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-crab.webp",
        "prompt": (
            "A handmade paper plate crab craft: half of a white paper plate painted bright red, "
            "with the curved side facing up as the crab body. Two large googly eyes glued on top, "
            "two red paper claws cut and glued at the front, and four small red paper legs "
            "on each side. Sitting flat on a light craft table. "
            "Cheerful and lopsided, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-tropical-fish.webp",
        "prompt": (
            "Several handmade origami tropical fish folded from bright square sheets of paper "
            "in orange, yellow, pink, and turquoise. Each fish has clean origami fold lines, "
            "a pointed mouth at one end and a triangular tail fin at the other. "
            "Small black marker dots for eyes. Three or four fish arranged on a light wood craft table. "
            "Charming and slightly imperfect folds. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-roll-shark.webp",
        "prompt": (
            "A handmade paper roll shark craft: an empty toilet paper tube wrapped in grey "
            "construction paper, with a triangle paper fin on top, a tail fin at one end, "
            "and a white paper toothy mouth at the other end. Two googly eyes glued near the mouth. "
            "Standing upright on a light wood craft table. Clearly child-made and cheerful. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "handprint-paper-starfish.webp",
        "prompt": (
            "A handmade handprint paper starfish craft: an orange handprint traced and cut from "
            "construction paper, with the five fingers spread out to form the five arms of a starfish. "
            "Decorated with small yellow dot stickers or marker spots on the surface. "
            "Glued onto a sandy beige paper background. "
            "Flat lay on a light craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-chain-seaweed.webp",
        "prompt": (
            "A handmade paper chain seaweed garland: long strips of green and dark green "
            "construction paper interlocked into a wavy paper chain that mimics swaying seaweed. "
            "The chain trails along a light craft table next to a small paper fish for scale. "
            "Cheerful and slightly uneven, clearly assembled by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-sea-turtle.webp",
        "prompt": (
            "A handmade paper plate sea turtle craft: a paper plate painted green with the bottom "
            "side decorated with darker green hexagon shapes glued on as a turtle shell pattern. "
            "Four small green paper flippers glued underneath the rim, a small green paper head "
            "with two googly eyes peeking out at the front, and a tiny tail at the back. "
            "Flat lay on a light craft table. Charming child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mosaic-goldfish-bowl.webp",
        "prompt": (
            "A handmade paper mosaic goldfish bowl craft: a round fishbowl outline drawn on "
            "white cardstock and filled in with small torn squares of light blue paper for water, "
            "with one or two orange paper goldfish silhouettes glued on top, tiny white paper "
            "bubble circles, and small green paper plants at the bottom. "
            "Glued in mosaic style with visible torn paper edges. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-aquarium-mobile.webp",
        "prompt": (
            "A handmade paper aquarium mobile craft: a small wooden twig or stick with several "
            "colorful paper fish, a paper octopus, and a paper jellyfish hanging from strings "
            "at different lengths below. The fish are cut from bright construction paper "
            "in orange, yellow, blue, and pink. Hanging in front of a light wall. "
            "Clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "folded-paper-stingray.webp",
        "prompt": (
            "A handmade folded paper stingray craft: a grey or pale blue diamond shape of paper "
            "folded gently in the middle to give it a slight wing curve, with two small googly eyes "
            "on the front edge and a long thin paper strip tail trailing behind. "
            "Placed on a blue construction paper background suggesting the ocean floor. "
            "Flat lay, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cup-underwater-diver.webp",
        "prompt": (
            "A handmade paper cup underwater diver craft: a small white paper cup turned upside "
            "down as a diving helmet, with a circle window cut on the front showing a smiling "
            "face drawn on a paper circle inside. A blue paper body shape below the cup, with "
            "tiny paper bubble circles glued near the top. Sitting on a sandy beige paper background. "
            "Cheerful and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-bubble-fish-scene.webp",
        "prompt": (
            "A handmade paper bubble fish scene: a blue construction paper background with three "
            "or four colorful paper fish in orange, yellow, and pink swimming across, and a stream "
            "of small white paper circles glued in a curving line as bubbles rising upward. "
            "Green paper seaweed at the bottom. "
            "Flat lay on a craft table. Cheerful and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-whale.webp",
        "prompt": (
            "A handmade paper plate whale craft: a paper plate painted light blue with a wedge "
            "cut out at one side to form the open mouth of the whale, and a small triangular fin "
            "glued on top, a curled paper water spout above the head, and a googly eye on the side. "
            "A small tail fin attached at the back. "
            "Flat lay on a light craft table. Cheerful and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-treasure-chest.webp",
        "prompt": (
            "A handmade paper treasure chest craft: a small brown construction paper chest shape "
            "with a curved lid lifted open, revealing yellow paper coin circles, a few paper gem shapes "
            "in red, blue, and green, and a string of paper pearls spilling out. "
            "Placed on a sandy beige paper background suggesting an ocean floor. "
            "Flat lay, clearly child-made and cheerful. "
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
