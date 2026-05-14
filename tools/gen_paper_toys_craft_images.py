#!/usr/bin/env python3
"""Generate all images for paper-toys-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-toys-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-toys-craft.webp",
        "prompt": (
            "A bright flat lay of handmade paper toys on a light wood craft table: "
            "a folded white paper airplane, a folded paper boat with a sail, "
            "a colorful paper fortune teller cootie catcher, "
            "two paper finger puppets shaped like animals, "
            "a multi-color paper pinwheel on a wooden stick, "
            "a green origami jumping frog, and a small paper crown with zig-zag points. "
            "Scissors, glue stick, and assorted construction paper scraps visible at the edges. "
            "Cheerful homemade toy mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-airplane-toy.webp",
        "prompt": (
            "A colorful folded paper airplane made from a single sheet of bright blue origami paper, "
            "classic dart style design with sharp pointed nose and triangular wings, "
            "resting on a light wood craft table next to a few extra folded paper airplanes "
            "in red and yellow. Clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-boat-toy.webp",
        "prompt": (
            "A folded paper boat made from white origami paper in classic origami sailboat style "
            "with a flat hull and triangular sail shape on top, "
            "sitting on a wooden craft table with small torn blue paper waves around it. "
            "Charming handmade folded toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fortune-teller-toy.webp",
        "prompt": (
            "A folded paper fortune teller cootie catcher made from a square sheet of paper, "
            "with four colored outer flaps in red, blue, yellow, and green, "
            "and numbers written in marker on the inner flaps. "
            "Two hands holding it open above a light wood craft table, "
            "fingers inserted into the four pockets. Classic kids paper toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-finger-puppets-toy.webp",
        "prompt": (
            "Five small paper finger puppets in a row on a light wood craft table, "
            "each made from rolled paper tubes about an inch tall. "
            "One brown bear, one green frog, one grey mouse, one white rabbit with paper ears, "
            "and one orange fox. Each has small googly eyes and tiny paper details. "
            "Clearly child-made, slightly uneven cuts. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spinner-top-toy.webp",
        "prompt": (
            "A handmade paper spinning top made from a circle of patterned cardstock "
            "decorated with bright rainbow stripes and spirals, "
            "with a small brass brad fastener pushed through the very center as the spinning point. "
            "Resting on a smooth light wood surface with another spinner nearby. "
            "Charming child-made paper toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-whirligig-helicopter-toy.webp",
        "prompt": (
            "A handmade paper whirligig helicopter made from a long narrow rectangle of white paper "
            "with two folded paper blades at the top spread outward like helicopter rotors, "
            "and a small silver paper clip clipped at the bottom for weight. "
            "Resting on a light wood craft table with a few more whirligigs in the background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-jumping-frog-toy.webp",
        "prompt": (
            "A green origami jumping frog made from folded bright green paper, "
            "with two small googly eyes glued to the head and a clear hinged back fold visible. "
            "Sitting on a light wood craft table with two more small folded paper frogs in different "
            "shades of green nearby. Classic kids origami toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pinwheel-toy.webp",
        "prompt": (
            "A handmade paper pinwheel with four pointed petals folded inward toward the center, "
            "decorated in bright multi-color stripes of pink, yellow, and blue, "
            "attached to a small wooden stick handle with a brass brad fastener through the middle. "
            "Resting on a light wood craft table. Cheerful and playful. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-binoculars-toy.webp",
        "prompt": (
            "A handmade pair of toy binoculars made from two empty toilet paper rolls taped together "
            "side by side, the outside covered in bright blue construction paper "
            "with a thin yellow yarn neck strap threaded through two holes. "
            "Resting on a light wood craft table. Clearly child-made and slightly uneven. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crown-toy.webp",
        "prompt": (
            "A handmade wearable paper crown made from a yellow cardstock strip "
            "with triangular zig-zag points cut along the top edge, decorated with "
            "colorful marker scribbles and red and blue paper jewels glued to the front. "
            "Resting flat on a light wood craft table. Charming handmade kids royal toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-sword-toy.webp",
        "prompt": (
            "A handmade rolled paper sword for kids, with the blade made from tightly rolled white "
            "cardstock covered in shiny silver paper for a metallic look, and a brown paper "
            "cross-shaped hilt at the base with a small handle wrap. "
            "Lying flat on a light wood craft table. Clearly child-made toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-animal-mask-toy.webp",
        "prompt": (
            "A handmade paper lion mask cut from yellow cardstock with two round eye holes, "
            "a fringed orange paper mane glued around the edge, two small rounded paper ears, "
            "and a small black triangle nose. A natural wooden craft stick taped to one side as a "
            "handle. Resting on a light wood craft table. Cute imperfect handmade toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-telescope-toy.webp",
        "prompt": (
            "A handmade paper telescope made from a single sturdy paper tube wrapped in dark "
            "navy blue construction paper, decorated with small yellow and silver star and moon "
            "stickers down the sides, with a small paper ring at one end as the eyepiece. "
            "Lying on a light wood craft table. Charming kids astronomy toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rocket-toy.webp",
        "prompt": (
            "A small handmade paper rocket about four inches tall, made from a thin paper tube "
            "with a pointed paper nose cone glued on the top and three red triangular paper fins "
            "around the bottom. Resting next to a yellow drinking straw on a light wood craft table. "
            "Clearly child-made toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-doll-toy.webp",
        "prompt": (
            "A handmade paper dress up doll cut from cream cardstock, with a simple drawn face "
            "and hair, lying on a light wood craft table next to four paper outfits with "
            "small fold-over tabs at the shoulders. The outfits include a pink dress, a yellow shirt "
            "with blue pants, a winter coat, and a striped t-shirt. Charming child-made paper toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-race-car-toy.webp",
        "prompt": (
            "Two handmade flat paper race cars cut from cardstock, one in bright red with the "
            "number 3 written on the side, one in blue with the number 7. Both have small "
            "round black paper wheels glued underneath and racing stripe details. "
            "Resting side by side on a light wood craft table as if at a starting line. "
            "Clearly child-made and slightly uneven cuts. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-glider-toy.webp",
        "prompt": (
            "A handmade paper glider with wide flat horizontal paper wings and a small narrow "
            "paper fuselage taped together at an angle for lift. Resting on a light wood craft "
            "table with another smaller glider in the background. Simple, light, child-made paper toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-snake-spiral-toy.webp",
        "prompt": (
            "A green spiral paper snake made from a paper circle cut into a wide spiral, "
            "lifted by the center so it dangles and unwinds, with a small triangular green head "
            "at the bottom of the spiral, a red paper tongue, and two googly eyes. "
            "Photographed against a light wood craft table background. Charming silly kids paper toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-kazoo-toy.webp",
        "prompt": (
            "A handmade paper kazoo made from a thin paper tube about five inches long, "
            "decorated with colorful washi tape and small marker stars, with one end covered by "
            "wax paper held in place by a brown rubber band. A small hole punched near the covered end. "
            "Resting on a light wood craft table. Clearly child-made music toy. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-castle-playset-toy.webp",
        "prompt": (
            "A handmade paper castle playset standing on a light wood craft table, made from "
            "grey cardstock with three tall round towers topped with red cone roofs, "
            "connected by short cardstock walls with crenellations along the top. "
            "Small triangular paper flags glued on the tops of the towers, and a brown paper "
            "drawbridge in the center wall. Clearly child-made, slightly imperfect and charming. "
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
