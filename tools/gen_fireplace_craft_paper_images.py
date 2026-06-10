#!/usr/bin/env python3
"""Generate all images for fireplace-craft-paper.html."""
import io, os, time, logging
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv(*a, **k):
        return False

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "fireplace-craft-paper"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper and craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

# A flat paper fireplace built on white cardstock: red brick paper front,
# black firebox opening, brown paper mantel and hearth, brown paper logs,
# layered red/orange/yellow paper flames. Continuity across all step images.

IMAGES = [
    {
        "filename": "fireplace-craft-paper.webp",
        "prompt": (
            "A finished handmade paper fireplace craft made flat on white cardstock: "
            "a red construction paper brick front with marker brick lines, a black paper "
            "firebox opening in the center, a brown paper mantel shelf across the top and a "
            "brown paper hearth strip at the bottom, two or three brown paper logs with marker "
            "bark, and layered red, orange and yellow paper flames glowing above the logs. "
            "A tiny colorful paper stocking hangs from the mantel. Scissors, a glue stick and "
            "paper scraps at the edges. Cozy and cheerful, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fireplace-craft-paper-mom-child.webp",
        "prompt": (
            "A mom and her young child sitting together at a light wood craft table, smiling, "
            "getting ready to make a paper fireplace craft. On the table are sheets of red, "
            "brown, orange and yellow construction paper, child-safe scissors, and a glue stick. "
            "A partly started red brick paper fireplace front sits between them. "
            "Warm, loving, candid family moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fireplace-craft-paper-brick-front.webp",
        "prompt": (
            "Step one of a paper fireplace craft: a single large red construction paper "
            "rectangle glued flat onto a sheet of white cardstock, with simple horizontal and "
            "vertical brick lines drawn across it in black marker to look like rows of bricks. "
            "Nothing else added yet, no opening, no logs, no flames. A marker and ruler lie "
            "beside it on the craft table. Clearly child-made with slightly wobbly lines. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fireplace-craft-paper-firebox-opening.webp",
        "prompt": (
            "Step two of a paper fireplace craft: the same red brick paper front on white "
            "cardstock now has a black construction paper rectangle with a gently rounded top "
            "glued onto the center toward the bottom, forming a dark firebox opening. "
            "The red bricks with marker brick lines are still visible around the black opening. "
            "No mantel, logs or flames yet. Flat lay on a craft table with paper scraps nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fireplace-craft-paper-mantel-hearth.webp",
        "prompt": (
            "Step three of a paper fireplace craft: the red brick paper fireplace with its black "
            "firebox opening now has a long brown construction paper strip glued flat across the "
            "very top as a mantel shelf, sticking out slightly on each side, and a thinner brown "
            "paper strip glued along the bottom edge as the hearth. The dark firebox opening is "
            "still empty, no logs or flames yet. Flat lay on white cardstock on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fireplace-craft-paper-paper-logs.webp",
        "prompt": (
            "Step four of a paper fireplace craft: two or three brown construction paper log "
            "shapes, each decorated with short marker bark lines and small circles on the ends, "
            "glued stacked at the bottom inside the black paper firebox opening of the red brick "
            "paper fireplace. The brown mantel and hearth are in place. No flames yet, just the "
            "logs sitting in the dark opening. Flat lay on white cardstock, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fireplace-craft-paper-flames.webp",
        "prompt": (
            "Step five of a paper fireplace craft: layered paper flames glued rising up from the "
            "brown paper logs inside the black firebox opening. A large red paper flame at the "
            "back, a medium orange flame in the middle, and a small yellow flame in front, each "
            "with a wavy pointed top and slightly different height, so the paper fire looks like "
            "it is glowing. The red brick front, brown mantel and hearth are all in place. "
            "Flat lay on white cardstock on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fireplace-craft-paper-finished.webp",
        "prompt": (
            "The finished paper fireplace craft on white cardstock: red brick paper front with "
            "marker brick lines, a black firebox opening, brown paper logs with bark details, "
            "and glowing layered red, orange and yellow paper flames. A small colorful paper "
            "stocking hangs from the brown paper mantel, with little yellow marker glow dots "
            "around the flames. Cozy, complete and cheerful, clearly made by a child. "
            "Flat lay on a craft table with a few paper scraps and a glue stick nearby. "
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
        img = img.convert("RGB")
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
