#!/usr/bin/env python3
"""Generate all images for paper-craft-monkey.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-craft-monkey"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

MONKEY = (
    "The monkey is a flat paper craft face: a large brown construction paper circle for the head, "
    "two round brown paper ears glued sticking out on the sides each with a small tan circle inside, "
    "a tan or cream peanut-shaped face area on the lower part of the head, two googly eyes near the top "
    "of the tan face, two small black marker nostril dots, and a wide black marker smile. "
)

IMAGES = [
    {
        "filename": "paper-craft-monkey.webp",
        "prompt": (
            "A finished handmade paper craft monkey face lying flat on a white craft table. "
            + MONKEY +
            "A little tuft of curled brown paper strips stands up on top of the head as hair. "
            "Cheerful and cute, clearly made by a young child with slightly uneven edges. "
            "A few brown and tan paper scraps and a glue stick visible at the edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-monkey-why-kids-love.webp",
        "prompt": (
            "A warm scene of an American mom and her young child sitting together at a light wood craft table, "
            "smiling and excited, about to make a paper craft monkey. On the table are sheets of brown and tan "
            "construction paper, child-safe scissors, a glue stick, and a couple of googly eyes. "
            "A partly finished brown paper monkey head is on the table between them. "
            "Cozy, joyful, real family moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-monkey-cut-head.webp",
        "prompt": (
            "A child's hands cutting a large brown construction paper circle with child-safe scissors on a craft table, "
            "to make the head of a paper monkey. A round lid used for tracing and a pencil line are visible on the brown paper. "
            "Brown paper scraps around. Only the plain brown circle so far, no face yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-monkey-ears.webp",
        "prompt": (
            "A large brown construction paper circle for a monkey head lying flat on a light wood craft table, "
            "with two round brown paper ears freshly glued onto the left and right sides, sticking out past the edge. "
            "The ears are plain brown with nothing inside them yet. No face, no eyes yet. "
            "A glue stick sits beside it. Clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-monkey-face-muzzle.webp",
        "prompt": (
            "A brown paper monkey head with round side ears, now with a tan cream peanut-shaped face area glued "
            "onto the lower two thirds of the head, and a small tan circle glued inside each ear. "
            "Still no eyes and no drawn face yet, just the tan paper shapes added. "
            "Lying flat on a craft table with paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-monkey-googly-eyes.webp",
        "prompt": (
            "A brown paper monkey face with round ears and a tan peanut-shaped face area, now with two googly eyes "
            "pressed onto the top of the tan face, sitting a little apart. "
            "No nose or mouth drawn yet, just the googly eyes added. "
            "Lying flat on a white craft table. Cute and expressive, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-monkey-nose-smile.webp",
        "prompt": (
            "A brown paper monkey face with round ears, a tan peanut face area, and two googly eyes, now with "
            "two small black marker nostril dots in the middle of the tan face and a wide curved black marker smile "
            "drawn underneath. No paper hair tuft on top yet. "
            "Lying flat on a craft table, cheerful and clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-monkey-finished.webp",
        "prompt": (
            "A completely finished handmade paper craft monkey face on a white craft table. "
            + MONKEY +
            "A tuft of curled thin brown paper strips is glued standing up on top of the head as hair. "
            "Bright, cheerful, and full of personality, clearly made by a young child. "
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
