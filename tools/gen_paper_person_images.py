#!/usr/bin/env python3
"""Generate all images for paper-person-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-person-craft"
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
        "filename": "paper-person-craft.webp",
        "prompt": (
            "A finished handmade paper person craft lying flat on a light wood craft table. "
            "The figure has a peach-colored construction paper oval head, a bright blue construction paper "
            "rectangular body, two thin yellow paper strip arms sticking out at the sides, "
            "two thin red paper strip legs at the bottom, two small googly eyes on the face, "
            "a tiny drawn nose and a smiling mouth, short pieces of brown yarn glued on the head as hair, "
            "small circle hands at the ends of the arms, and oval shoes at the ends of the legs. "
            "Some small marker buttons drawn on the body. "
            "A glue stick and child-safe scissors visible at the edge of the table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-person-craft-mom-child.webp",
        "prompt": (
            "A warm overhead photo of a young American mom and her 5-year-old child sitting together "
            "at a light wood craft table. The mom is helping the child cut construction paper shapes "
            "with child-safe scissors. Several pieces of colorful construction paper, a glue stick, "
            "and a few yarn skeins are on the table. The mom is smiling warmly. Both are focused and happy. "
            "Cozy family moment, soft natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-person-craft-head-body.webp",
        "prompt": (
            "Two construction paper shapes lying flat on a light wood craft table, ready to assemble "
            "a paper person craft. One large peach-colored oval shape for the head, and one tall blue "
            "rectangle for the body, lying side by side. A pencil and child-safe scissors next to the shapes. "
            "Both pieces are clearly cut by a child with slightly uneven edges. "
            "Soft natural lighting, close-up flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-person-craft-cut-arms-legs.webp",
        "prompt": (
            "Four long thin construction paper strips lying on a light wood craft table, "
            "ready to become the arms and legs of a paper person craft. "
            "Two yellow strips for the arms and two red strips for the legs, "
            "with the leg strips slightly longer and wider than the arm strips. "
            "Child-safe scissors and a pencil next to the strips. "
            "Slightly uneven edges showing clearly child-cut paper. Flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-person-craft-assembled-body.webp",
        "prompt": (
            "An assembled paper person craft body on a light wood craft table. "
            "A peach oval head glued on top of a blue rectangle body, with two yellow paper "
            "strip arms attached behind the body sticking out at the sides, "
            "and two red paper strip legs attached behind the body sticking out at the bottom. "
            "No face details yet, no hair yet. Plain blank face. "
            "A glue stick next to the figure. Flat lay, soft natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-person-craft-face-eyes.webp",
        "prompt": (
            "Close-up of a paper person craft face on a light wood craft table. "
            "A peach oval head with two small black-and-white googly eyes stuck on with a small space "
            "between them, a tiny brown marker dot for a nose, and a simple curved smiling mouth "
            "drawn with marker. Two small pink cheek dots. The body of the paper person is partly visible "
            "below the head. No hair yet. Soft natural light, close-up flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-person-craft-yarn-hair.webp",
        "prompt": (
            "A paper person craft on a light wood craft table with short pieces of brown yarn "
            "glued to the top of the peach oval head to form messy charming hair. "
            "The face has two googly eyes, a small marker nose, and a smiling mouth. "
            "The blue rectangle body with yellow paper arms and red paper legs is visible below. "
            "Some yarn scraps and small scissors next to the figure. Flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-person-craft-hands-shoes.webp",
        "prompt": (
            "A paper person craft on a light wood craft table with two small peach paper circles "
            "glued as hands to the ends of the yellow paper arms, and two larger red paper oval shoes "
            "glued to the ends of the red paper legs. The figure has a peach oval head with two googly eyes, "
            "a smiling mouth, brown yarn hair, and a blue rectangle body. "
            "Flat lay, soft natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-person-craft-finished.webp",
        "prompt": (
            "The fully finished decorated paper person craft on a piece of white cardstock "
            "displayed on a light wood craft table. The peach oval head has googly eyes, "
            "a smiling mouth, pink cheeks, and short brown yarn hair. The blue rectangle body "
            "has small drawn marker buttons down the front, small stripes, and a tiny red paper heart "
            "glued on the chest. Yellow paper strip arms with small peach circle hands at the ends. "
            "Red paper legs with oval red paper shoes at the ends. Cheerful and complete. "
            "Marker pens and paper scraps next to the figure. Flat lay. "
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
