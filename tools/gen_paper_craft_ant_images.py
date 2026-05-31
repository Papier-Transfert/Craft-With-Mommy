#!/usr/bin/env python3
"""Generate all images for paper-craft-ant.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-craft-ant"
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

IMAGES = [
    {
        "filename": "paper-craft-ant.webp",
        "prompt": (
            "A finished handmade paper ant craft made from three black construction paper circles "
            "glued in a row from small to large to form the head, middle, and back body. "
            "Six thin black paper strip legs, three on each side, bent in a zigzag. "
            "Two thin black paper antennae curled at the tips on top of the head. "
            "Two googly eyes and a small drawn smile on the head circle. "
            "Lying flat on a white craft table with a few black paper scraps nearby. "
            "Clearly child-made and cheerful. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ant-mom-child.webp",
        "prompt": (
            "A mom and her young child sitting together at a light wood craft table, "
            "smiling and getting ready to make a paper ant craft. "
            "On the table are sheets of black construction paper, a small pile of googly eyes, "
            "blunt safety scissors, and a purple glue stick. "
            "Warm, loving, real family moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ant-cut-circles.webp",
        "prompt": (
            "Three black construction paper circles in small, medium, and large sizes, "
            "freshly cut out and resting in a loose row on a white craft table. "
            "A pair of blunt kid safety scissors and a round cup for tracing lie next to them. "
            "The circle edges are slightly uneven, clearly cut by a child. "
            "This is the very first stage of a paper ant craft, only the three plain circles, "
            "no legs, no eyes, no antennae yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ant-glued-body.webp",
        "prompt": (
            "Three black construction paper circles glued together in a straight row from "
            "smallest to largest, forming the connected body of a paper ant. "
            "The small head circle is on one end and the larger back circle on the other, "
            "edges just touching. Lying flat on a white craft table. "
            "No legs yet, no antennae yet, no eyes yet, just the plain three-circle body. "
            "Clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ant-legs.webp",
        "prompt": (
            "A paper ant craft made of three black paper circles in a row, now with six thin "
            "black construction paper strip legs added, three glued to each side of the middle "
            "circle, each leg bent into a little zigzag so the ant looks ready to march. "
            "Lying flat on a white craft table. Still no antennae and no eyes yet. "
            "Clearly child-made with slightly uneven legs. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ant-antennae.webp",
        "prompt": (
            "A paper ant craft of three black paper circles with six zigzag paper legs, now "
            "with two thin black construction paper antennae added to the top of the small head "
            "circle, pointing up in a V shape and gently curled at the tips. "
            "Lying flat on a white craft table. No googly eyes yet. "
            "Clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ant-face.webp",
        "prompt": (
            "A close up of the head of a handmade paper ant craft: a small black construction "
            "paper circle with two plastic googly eyes stuck on and a small smile drawn in black "
            "marker underneath. Two curled black paper antennae rise from the top of the head. "
            "The rest of the black paper ant body and legs are visible behind it on a white craft table. "
            "Friendly, cheerful face. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ant-finished-display.webp",
        "prompt": (
            "A finished handmade paper ant craft made from three black construction paper circles "
            "with six zigzag paper legs, two curled antennae, two googly eyes, and a drawn smile, "
            "carrying a small green paper leaf in front of it. "
            "Displayed standing on a white craft table, cheerful and proud. "
            "A couple of black paper scraps nearby. Clearly made by a child. "
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
