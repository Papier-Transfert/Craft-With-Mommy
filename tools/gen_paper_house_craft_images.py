#!/usr/bin/env python3
"""Generate all images for paper-house-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-house-craft"
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
        "filename": "paper-house-craft.webp",
        "prompt": (
            "A finished handmade paper house craft displayed on a white craft table: "
            "a bright blue construction paper rectangle for the house walls decorated with "
            "horizontal white marker stripes, topped with a bold red triangle roof, "
            "with two small yellow square windows glued on the upper walls and an orange "
            "rectangle door centered at the bottom. Small marker-drawn flower boxes under "
            "the windows, a green marker garden at the base, and a curling chimney drawn "
            "on the roof. Cheerful, colorful, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-house-craft-mom-child.webp",
        "prompt": (
            "A warm and cozy scene of a mother and her young child (around age 5) sitting "
            "together at a light wood craft table, smiling and ready to start a paper house "
            "craft. Sheets of colorful construction paper (red, blue, yellow, orange) spread "
            "on the table, a glue stick, and a pair of child-safe scissors nearby. "
            "The mom and child look happy and excited. Warm, natural indoor lighting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-house-craft-cut-shapes.webp",
        "prompt": (
            "A large blue construction paper rectangle and a bright red construction paper "
            "triangle laid flat side by side on a white craft table. The rectangle is about "
            "6 inches tall, the triangle slightly wider. Child-safe scissors, a pencil, and "
            "colorful paper scraps visible nearby. The two shapes are the main pieces for a "
            "paper house craft, clearly just cut out. Clean flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-house-craft-cut-details.webp",
        "prompt": (
            "Small paper pieces for a paper house craft laid out on a white craft table: "
            "two small yellow construction paper squares for windows, one taller orange "
            "rectangle with a gently rounded top for the door, and one tiny green circle. "
            "Scissors and the main blue house rectangle and red triangle visible at the edges. "
            "Flat lay, warm daylight. Simple and clear. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-house-craft-decorate-walls.webp",
        "prompt": (
            "A young child (around age 5) using bright washable markers to decorate a large "
            "blue construction paper rectangle on a white craft table. The child is drawing "
            "horizontal white and yellow stripes and colorful polka dots to create a house "
            "pattern. The red triangle roof piece waits nearby. The child looks focused and "
            "delighted. Warm natural lighting, clearly a fun craft moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-house-craft-assemble-roof.webp",
        "prompt": (
            "A pair of small hands pressing a bright red construction paper triangle onto "
            "the top edge of a decorated blue paper rectangle on a white craft table. "
            "The triangle overhangs evenly on both sides to form a roof shape. "
            "A glue stick is visible nearby. The assembly of a handmade paper house craft "
            "in progress, warm daylight, family-friendly atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-house-craft-add-windows.webp",
        "prompt": (
            "A child's hands pressing small yellow construction paper square windows and "
            "an orange rounded-top door onto the assembled blue and red paper house on "
            "a white craft table. The glue stick is visible. The paper house body already "
            "has the red triangle roof attached at the top. The windows go on the upper "
            "walls, the door at the lower center. Mid-assembly, charming handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-house-craft-finished-details.webp",
        "prompt": (
            "A fully finished handmade paper house craft on a white craft table seen up close: "
            "blue rectangle walls decorated with white stripes, red triangle roof, two yellow "
            "square windows with marker-drawn black frames, an orange rounded door with a "
            "small marker doorknob, pink marker flowers in window boxes, a green marker "
            "garden along the base, and a grey swirl chimney drawn on the roof. "
            "A few construction paper scraps and a marker cap visible at the edges. "
            "Charming, colorful, clearly child-made. "
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
