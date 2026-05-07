#!/usr/bin/env python3
"""Generate all images for paper-car-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "blog" / "images" / "paper-car-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper and cardstock only. "
    "Charming and slightly imperfect, clearly handmade by a child. Pinterest-worthy."
)

CAR_DESCRIPTION = (
    "A handmade flat paper car craft made from layered construction paper: "
    "a long red rectangle body with rounded corners, a smaller rounded red cabin "
    "glued on top in the middle, a light blue rectangle window glued on the cabin, "
    "two large round black cardstock wheels with smaller grey hubcap circles "
    "sitting under each end of the body, a small yellow circle headlight glued at the front, "
    "a tiny red circle tail light at the back, and a black marker drawn door line on the side."
)

IMAGES = [
    {
        "filename": "paper-car-craft.webp",
        "prompt": (
            f"{CAR_DESCRIPTION} The car is photographed flat on a light wood craft table, "
            "with a few colored paper scraps, scissors, and a glue stick visible at the edges. "
            "The car looks finished, cheerful, and very child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-car-craft-mom-child.webp",
        "prompt": (
            "A warm, candid photo of a young American mom and her young child, around age 4, "
            "sitting together at a light wood craft table starting a paper car craft project. "
            "On the table are sheets of red, blue, yellow, white, and grey construction paper, "
            "a black sheet of cardstock, child-safe scissors, a purple glue stick, and crayola markers. "
            "Both are smiling and looking down at the materials with happy anticipation. "
            "The mom is gently helping the child place a piece of red paper. "
            "Soft natural daylight. No finished car visible yet, just the materials laid out. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-car-craft-cut-body.webp",
        "prompt": (
            "Close-up photo of a child's small hand using blunt-tip kid scissors "
            "to cut a long rectangle from a sheet of red construction paper, "
            "about 6 inches wide and 2.5 inches tall, on a light wood craft table. "
            "The cut rectangle is visible alongside the leftover red paper scraps. "
            "Pencil guide lines are faintly visible. Only the body rectangle is shown so far, "
            "no cabin, no wheels, no window. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-car-craft-add-roof.webp",
        "prompt": (
            "Top-down photo on a light wood craft table showing a long red construction paper rectangle "
            "(the car body, about 6 inches wide and 2.5 inches tall, with rounded corners), "
            "with a smaller rounded red paper cabin shape (about 4 inches wide and 1.5 inches tall, "
            "with a softly curved top) being glued onto the top middle of the rectangle. "
            "A purple glue stick and a small hand pressing the cabin flat are visible. "
            "No window, no wheels yet, just the two stacked red paper pieces. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-car-craft-add-window.webp",
        "prompt": (
            "Top-down photo on a light wood craft table showing the in-progress paper car craft: "
            "a long red rectangle body with a smaller rounded red cabin on top, "
            "and a child's hand gluing a small light blue paper rectangle window "
            "onto the rounded red cabin. The window is centered on the cabin "
            "with a thin red border showing around it. No wheels yet, no headlights yet. "
            "A purple glue stick is visible nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-car-craft-cut-wheels.webp",
        "prompt": (
            "Top-down photo on a light wood craft table showing two large round black cardstock circles "
            "(about 1.5 inches across) and two smaller round grey paper circles "
            "(about three quarters of an inch across) cut and laid out neatly side by side. "
            "Blunt-tip kid scissors and a few black paper scraps are visible at the edges. "
            "No car body shown in this photo, just the wheel pieces ready to be assembled. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-car-craft-attach-wheels.webp",
        "prompt": (
            "Top-down photo on a light wood craft table showing the in-progress paper car craft: "
            "a long red rectangle body with a smaller rounded red cabin on top, a light blue rectangle "
            "window on the cabin, and two large black cardstock circle wheels with smaller grey hubcap circles "
            "glued in the center of each wheel. The wheels are glued under each end of the body so "
            "the bottom half of each circle peeks out below the rectangle. "
            "No headlights yet, no door line yet, no decorations yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-car-craft-add-headlights.webp",
        "prompt": (
            "Top-down photo on a light wood craft table showing the in-progress paper car craft: "
            "a long red rectangle body with a rounded red cabin on top, a light blue rectangle window, "
            "two black wheels with grey hubcaps under each end, plus a small yellow circle headlight "
            "glued at the front of the car and a tiny red circle tail light at the back. "
            "A simple curved black marker drawn door line is visible on the side of the body, "
            "with a small dot for the door handle. No racing stripes yet, no license plate yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-car-craft-decorate.webp",
        "prompt": (
            "Top-down photo on a light wood craft table showing the finished decorated paper car craft: "
            "a long red rectangle body with a rounded red cabin, a light blue rectangle window with a "
            "tiny black steering wheel drawn inside, two black wheels with grey hubcaps, a yellow front "
            "headlight, a red rear tail light, plus marker decorations including two thin black racing "
            "stripes down the side, a tiny white paper rectangle license plate near the back, "
            "and a small playful brand name written in marker on the door. "
            "Crayola broad line markers and a black fine-tip Sharpie are visible nearby. Cheerful and finished. "
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
