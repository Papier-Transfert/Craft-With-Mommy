#!/usr/bin/env python3
"""Generate all images for chinese-lanterns-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "chinese-lanterns-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3, fills the entire frame edge to edge. "
    "No cartoon elements. Real construction paper materials only. "
    "Charming and slightly imperfect, clearly handmade by a child. Pinterest-worthy. "
    "No padding, no white borders, no letterboxing. The photograph fills the whole frame."
)

IMAGES = [
    {
        "filename": "chinese-lanterns-paper-craft.webp",
        "prompt": (
            "A finished handmade Chinese paper lantern made from red construction paper, "
            "shaped like a classic round cylindrical lantern with vertical strips slightly bowed outward, "
            "a flat gold yellow paper band wrapped around the top and another around the bottom, "
            "a red yarn loop attached at the top for hanging, and a small red and gold paper tassel hanging from the bottom. "
            "The lantern stands upright on a light wood craft table. Two more smaller lanterns sit beside it for variety. "
            "Festive but cozy atmosphere, clearly a children's craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "chinese-lanterns-paper-craft-mom-child.webp",
        "prompt": (
            "A warm friendly American mom and her young child around five years old sitting together at a light wood craft table, "
            "smiling, getting ready to make a Chinese paper lantern craft. "
            "On the table: a sheet of red construction paper, a sheet of yellow gold paper, kids scissors, "
            "a purple glue stick, a pencil, a small ruler, and a length of red yarn. "
            "The mom is showing the child how to start. Daylight from a window, very cozy and natural. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "chinese-lanterns-paper-craft-cut-rectangles.webp",
        "prompt": (
            "Two flat rectangular pieces of construction paper laid out on a white craft table: "
            "one large red rectangle about 9 by 6 inches, and one thinner gold yellow strip about 9 inches long and 1 inch tall. "
            "Kids scissors, a pencil, and a ruler are next to the paper. "
            "Nothing has been folded or cut yet, just neatly cut rectangles. "
            "Top down flat lay view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "chinese-lanterns-paper-craft-folded-paper.webp",
        "prompt": (
            "The same red construction paper rectangle, now folded in half lengthwise so it is now half its original height, "
            "laying flat on a white craft table. The fold line is clearly visible at the bottom edge. "
            "Open edge of the fold is at the top. "
            "Pencil and ruler beside it. The gold yellow strip from before still sits next to the folded red paper. "
            "Top down flat lay view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "chinese-lanterns-paper-craft-cut-slits.webp",
        "prompt": (
            "The folded red rectangle of construction paper now has many parallel vertical slits cut from the folded bottom edge "
            "going almost up to the open top edge but stopping about half an inch short. "
            "The cuts are evenly spaced about half an inch apart. The paper is still folded in half. "
            "Kids scissors are placed beside the paper. White craft table. "
            "Top down flat lay view, very clear progression of the lantern body. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "chinese-lanterns-paper-craft-rolled-cylinder.webp",
        "prompt": (
            "The same red construction paper, now unfolded and rolled into a tall vertical cylinder shape, "
            "with the previously cut slits running vertically around the outside of the cylinder. "
            "The two short ends of the paper are joined and held together with a small visible silver staple. "
            "The cylinder stands upright on a white craft table, lantern body shape now clearly visible. "
            "No gold trim added yet. Soft natural daylight, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "chinese-lanterns-paper-craft-gold-trim.webp",
        "prompt": (
            "The same red paper lantern cylinder, now with two flat gold yellow paper bands glued in place: "
            "one wrapped around the top opening, one wrapped around the bottom opening. "
            "The vertical red slits in the middle of the lantern still bow outward slightly. "
            "Lantern stands upright on a white craft table, no string yet, no tassel yet. "
            "Clean, child-made appearance. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "chinese-lanterns-paper-craft-finished.webp",
        "prompt": (
            "The completely finished handmade Chinese paper lantern: a red cylindrical lantern body with vertical slits bowing outward, "
            "gold yellow paper bands at the top and bottom, "
            "a thin red yarn loop attached to the top with a small piece of tape so it can hang, "
            "and a small red and gold paper tassel hanging from the bottom of the lantern. "
            "The lantern is held up by the yarn loop in front of a soft cream wall, gently swaying. "
            "Warm natural daylight, festive cozy mood, clearly a child's handmade craft. "
            f"{STYLE}"
        ),
    },
]


def generate_image(client, prompt, output_path):
    from google.genai import types as genai_types
    from PIL import Image as PILImage
    full_prompt = f"{prompt} Aspect ratio: 4:3. Wide rectangular landscape orientation, image fills the full frame, no white borders."
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
        if img.mode != "RGB":
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
