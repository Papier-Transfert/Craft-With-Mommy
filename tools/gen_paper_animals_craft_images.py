#!/usr/bin/env python3
"""Generate all images for paper-animals-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-animals-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "The image should fill the entire 4:3 frame edge to edge with no white borders, no padding, no letterboxing."
)

IMAGES = [
    {
        "filename": "paper-animals-craft.webp",
        "prompt": (
            "A cheerful flat lay of handmade paper animal crafts spread across a light wood craft table: "
            "a yellow paper lion with an orange strip mane, a brown layered paper owl with big googly eyes, "
            "a black-and-white paper penguin with an orange beak, a gray paper elephant with a curling trunk, "
            "a green paper frog, a bright paper butterfly, a red paper ladybug, and a pink paper pig. "
            "Construction paper scraps, scissors, and a glue stick scattered around the edges. "
            "Cheerful, colorful, and clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-lion-craft.webp",
        "prompt": (
            "A handmade paper lion craft made from construction paper: a large yellow circle face with two googly eyes, "
            "a small black triangle nose, and a smile drawn with marker. "
            "Around the edge of the face is a thick mane made of many short orange and yellow paper strips, "
            "some curled gently with a pencil, glued in a sunburst pattern around the head. "
            "Two small round ears poke out the top. Lying flat on a white craft table with paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-owl-craft.webp",
        "prompt": (
            "A handmade paper owl craft from layered construction paper: a large brown round head and body, "
            "two cream-colored circles for the eye patches with big googly eyes glued in the centers, "
            "a small orange triangle beak, and two pointed brown ear tufts on top of the head. "
            "A cream paper belly oval is glued on the body. Lying flat on a wooden craft table with paper scraps and scissors nearby. "
            "Slightly imperfect and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-penguin-craft.webp",
        "prompt": (
            "A handmade paper penguin craft made from construction paper: a large black oval body, "
            "a smaller white oval glued on the front for the belly, two small black wing shapes on the sides, "
            "an orange triangle beak, two small orange paper feet at the bottom, "
            "and two large googly eyes. Standing upright on a white craft table. "
            "Cute and clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-elephant-craft.webp",
        "prompt": (
            "A handmade paper elephant craft made from gray construction paper: a large rounded gray body and head, "
            "two big rounded fan-shaped gray ears glued on the sides of the head, "
            "a long curving gray paper trunk strip curled with a pencil, "
            "a small white tusk, four short legs, a tiny tail, and one big googly eye. "
            "Glued onto a white background paper, lying flat on a wooden craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-frog-jumping-craft.webp",
        "prompt": (
            "A handmade origami jumping frog folded from a single square of bright green paper. "
            "The frog has a triangular head with two small googly eyes glued on top, folded back legs ready to spring, "
            "and a folded body with visible accordion-style pleats. Sitting on a wooden craft table next to "
            "a green square of paper and a marker. Slightly imperfect folds, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-bunny-craft.webp",
        "prompt": (
            "A handmade paper bunny craft made from construction paper: a round white head, "
            "two long white teardrop-shaped ears with smaller pink inner ear shapes glued on top, "
            "a tiny pink triangle nose, two big googly eyes, and thin paper whiskers on each cheek. "
            "A small white cotton ball glued on the chin like a fluffy puff. "
            "Lying flat on a white craft table with paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cat-face-craft.webp",
        "prompt": (
            "A handmade paper cat face made from orange construction paper: a round orange face, "
            "two small orange triangle ears with pink inner triangles glued on top, "
            "a tiny pink triangle nose, two big yellow circle eyes with black pupils, "
            "and three thin black paper whisker strips on each cheek. A small smile drawn with marker. "
            "Lying flat on a wooden craft table with paper scraps and scissors nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-puppy-craft.webp",
        "prompt": (
            "A handmade paper puppy craft made from brown construction paper: a round brown head, "
            "two long floppy darker brown ears hanging on either side of the head, "
            "a small dark brown muzzle oval glued on the lower face, a tiny black triangle nose, "
            "two big googly eyes, and a smile drawn with marker. "
            "Lying flat on a wooden craft table next to brown paper scraps and a glue stick. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fish-animal-craft.webp",
        "prompt": (
            "A handmade colorful paper fish craft: a large oval body covered with overlapping rows of small "
            "semicircle paper scales in rainbow colors (red, orange, yellow, green, blue, purple). "
            "A pointed orange triangle tail at the back, a smaller blue triangle fin on top, "
            "and one large googly eye near the front. Lying flat on a white craft table with colorful paper scraps nearby. "
            "Charming and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-butterfly-animal-craft.webp",
        "prompt": (
            "A handmade symmetrical paper butterfly craft made from construction paper: large bright pink and purple wings "
            "cut from a folded paper so they are perfectly symmetrical, decorated with small yellow and blue paper circles "
            "and dot stickers in a pattern across both wings. A thin black paper body strip down the middle, "
            "two thin curled black antennae at the top. Lying flat on a craft table with paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-bee-craft.webp",
        "prompt": (
            "A handmade paper bee craft made from construction paper: a yellow oval body with three black paper stripes "
            "glued horizontally across it, two white teardrop-shaped wings on top, two thin black antennae, "
            "two large googly eyes, and a small smile drawn with marker. Lying flat on a wooden craft table next to "
            "yellow and black paper scraps and a glue stick. Cheerful and clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-ladybug-craft.webp",
        "prompt": (
            "A handmade paper ladybug craft made from construction paper: a large red circle body with several "
            "small black paper dots glued on, a thin black line down the center to suggest the wings, "
            "a small black half-circle head at the front with two tiny googly eyes and short antennae. "
            "Lying flat on a bright craft table with red and black paper scraps nearby. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-turtle-craft.webp",
        "prompt": (
            "A handmade paper turtle craft made from green construction paper: a large green oval shell "
            "decorated with small green and yellow paper hexagon shapes glued in a patchwork pattern. "
            "A small green head poking out the front with two googly eyes, four short green legs at the corners, "
            "and a tiny green tail at the back. Lying flat on a wooden craft table with green paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-snake-accordion-craft.webp",
        "prompt": (
            "A handmade accordion-folded paper snake craft made from a long strip of green construction paper "
            "folded back and forth in tight pleats, stretched out across a wooden craft table. "
            "A green triangle head at one end with two small googly eyes and a small red forked tongue paper strip. "
            "Green and red paper scraps and scissors visible near the edges. Friendly and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-giraffe-craft.webp",
        "prompt": (
            "A handmade paper giraffe craft made from yellow construction paper: a tall yellow body with a long rectangular "
            "neck connecting to a small yellow head, four straight yellow legs, two tiny brown horn nubs on top of the head, "
            "two small ear shapes, and a swishy paper tail with a brown tuft. Many brown spots glued or drawn across "
            "the body and neck. One large googly eye on the head. Lying flat on a craft table with yellow and brown paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cow-craft.webp",
        "prompt": (
            "A handmade paper cow craft made from white construction paper: a white oval body with several "
            "irregular black paper spot shapes glued randomly across it, a white head with a pink oval snout, "
            "two black dot nostrils drawn on, two small white horn shapes on top, big sweet eyes, "
            "four short black legs, and a small pink udder shape. Lying flat on a wooden craft table with paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pig-craft.webp",
        "prompt": (
            "A handmade paper pig craft made from pink construction paper: a round pink body, "
            "a smaller pink oval snout glued on the face with two black dot nostrils drawn on, "
            "two small pink triangle ears flopping forward, four short pink legs at the bottom, "
            "and a thin curly pink paper tail at the back curled tightly with a pencil. "
            "Two big googly eyes on the face. Lying flat on a wooden craft table with pink paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-sheep-craft.webp",
        "prompt": (
            "A handmade paper sheep craft: a black oval head with two small black ears and four short black paper legs, "
            "and a fluffy white woolly body made from many small white cotton balls glued densely onto a white circle base. "
            "Two googly eyes on the face and a tiny pink triangle nose. Lying flat on a wooden craft table with white "
            "cotton balls and black paper scraps scattered around. Charming and clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mouse-craft.webp",
        "prompt": (
            "A handmade paper mouse craft made from gray construction paper: a small gray semicircle body, "
            "two round gray ears with small pink inner circles glued on top, a tiny pink triangle nose, "
            "two small black dot eyes, and a long thin curled gray paper tail at the back. "
            "Lying flat on a wooden craft table with gray and pink paper scraps nearby. Tiny and irresistibly cute, "
            "clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-peacock-craft.webp",
        "prompt": (
            "A handmade paper peacock craft made from construction paper: a teal blue body with a small head "
            "and a tiny yellow triangle beak, with a large fan of overlapping teardrop-shaped paper feathers "
            "behind the body in alternating colors of bright blue, emerald green, purple, and gold. "
            "Each feather has a small contrasting dot near the tip suggesting the peacock's eye pattern. "
            "One small googly eye on the head. Lying flat on a white craft table with colorful paper scraps nearby. "
            "Show-stopping and clearly child-made. "
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
