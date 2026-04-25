#!/usr/bin/env python3
"""Generate all images for paper-rocket-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-rocket-craft"
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
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-rocket-craft.webp",
        "prompt": (
            "A finished handmade paper rocket craft glued onto a dark blue construction paper background. "
            "The rocket has a tall white construction paper body with a rounded top, a bright red triangular "
            "nose cone on top, two red right-angled triangle fins on either side at the bottom, and a small "
            "light blue paper porthole circle in the middle of the body. Wavy orange and yellow paper flame "
            "shapes are glued just below the bottom of the rocket. Silver foil star stickers are scattered "
            "across the dark blue night sky around the rocket. A tiny smiling astronaut face is drawn in marker "
            "inside the porthole. The whole composition fills the frame on a white craft table. "
            "Clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rocket-craft-why-kids-love.webp",
        "prompt": (
            "An American mom in her early thirties and her young child around age four sitting together "
            "at a white craft table, smiling and getting ready to make a paper rocket craft. Sheets of "
            "dark blue, white, red, yellow, and orange construction paper are spread on the table along with "
            "kid-safe scissors, a glue stick, and a sheet of silver foil star stickers. The mom is gently "
            "pointing at the construction paper, the child looks excited and engaged. Warm natural light, "
            "cozy home craft moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rocket-craft-night-sky-background.webp",
        "prompt": (
            "A single sheet of dark blue construction paper laid flat in portrait orientation on a white "
            "craft table. The paper is smooth and empty, ready to become a starry night sky background. "
            "A pair of kid-safe scissors and a glue stick rest just to the side of the dark blue sheet. "
            "Calm, clean composition. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rocket-craft-white-body.webp",
        "prompt": (
            "A tall white construction paper rectangle, roughly twice as tall as it is wide, with the top "
            "two corners rounded smoothly to form the body of a paper rocket. The cut shape is lying flat on "
            "a white craft table next to a pair of blunt-tip kids scissors and a pencil. White paper scraps "
            "are visible to the side. The cut edges are slightly uneven, clearly cut by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rocket-craft-red-nose-cone.webp",
        "prompt": (
            "A bright red construction paper triangle cut as a tall pointed nose cone for a paper rocket, "
            "sitting flat on a white craft table next to the previously cut tall white rocket body shape "
            "with rounded top corners. The base of the red triangle matches the width of the white rocket "
            "body. Red paper scraps and scissors visible at the edge of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rocket-craft-red-fins.webp",
        "prompt": (
            "Two bright red construction paper right-angled triangles cut as mirror-image rocket fins, "
            "arranged on a white craft table so they point outward. Next to them sit the previously cut "
            "tall white rocket body with rounded top corners and the red triangular nose cone. Red paper "
            "scraps and kid-safe scissors visible to the side. Clearly child-made cuts. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rocket-craft-blue-porthole.webp",
        "prompt": (
            "A small light blue construction paper circle, about the size of a bottle cap, cut as a "
            "porthole window for a paper rocket. It is sitting on a white craft table next to the white "
            "rocket body with rounded top corners, the red triangular nose cone, and the two red mirror "
            "image fin triangles arranged together. Light blue paper scraps and scissors at the edge. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rocket-craft-assembled-on-background.webp",
        "prompt": (
            "A handmade paper rocket fully assembled on a dark blue construction paper background. "
            "The white rectangular rocket body with rounded top is glued in the center of the dark blue "
            "background, with the red triangular nose cone glued on top, two red right-angled triangle fins "
            "glued on either side at the bottom of the body pointing outward, and a small light blue paper "
            "circle porthole glued in the middle of the white body. No flames yet, no stars yet. Sitting on "
            "a white craft table. Slightly imperfect, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rocket-craft-orange-yellow-flames.webp",
        "prompt": (
            "The same handmade paper rocket on a dark blue construction paper background as before "
            "(white body with red nose cone, two red fins pointing outward, light blue porthole circle), "
            "now with wavy orange and yellow construction paper flames glued just below the bottom of "
            "the rocket. The orange flame is slightly larger and behind, the yellow flame is layered on "
            "top so the orange peeks out around it. No star stickers yet. On a white craft table. "
            "Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rocket-craft-finished-stars-astronaut.webp",
        "prompt": (
            "The fully finished handmade paper rocket craft on a dark blue construction paper background. "
            "The rocket has a white body with rounded top, a red triangular nose cone, two red right-angled "
            "fins pointing outward at the bottom, and a small light blue porthole circle in the middle. "
            "Wavy orange and yellow paper flames are glued just below the rocket. Many silver foil star "
            "stickers are scattered all across the dark blue night sky around the rocket. A tiny smiling "
            "astronaut face is drawn in marker inside the light blue porthole window. The dark blue paper "
            "fills the frame on a white craft table. Clearly child-made and joyful. "
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
