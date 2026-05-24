#!/usr/bin/env python3
"""Generate all images for paper-poinsettia-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-poinsettia-craft"
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
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "The photo fills the full frame edge to edge with no white borders, "
    "no letterboxing, no padding, no blank canvas."
)

IMAGES = [
    {
        "filename": "paper-poinsettia-craft.webp",
        "prompt": (
            "A handmade finished paper poinsettia craft displayed flat on a white craft table. "
            "Five long pointed dark green construction paper leaves are layered underneath, "
            "arranged in a star pattern with their tips pointing outward. "
            "Six bright red pointed paper petals are layered on top of the green leaves, "
            "slightly rotated so the red points peek out between the green points. "
            "A cluster of five small yellow paper dots is glued in the very center. "
            "Soft marker veins are drawn down the middle of each petal and leaf. "
            "Clearly child-made with charming slightly uneven edges. Cozy Christmas mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poinsettia-craft-mom-child.webp",
        "prompt": (
            "A warm cozy photo of a young American mom in her early thirties and her four year old child "
            "sitting together at a light wood craft table, both smiling and looking happy. "
            "On the table in front of them: bright red construction paper sheets, dark green construction "
            "paper sheets, a yellow construction paper sheet, a pair of blue Fiskars kid scissors, "
            "a purple Elmer's glue stick, and a yellow pencil. "
            "The mom is showing her child a small green paper leaf shape she just cut. "
            "Bright warm natural light from a nearby window. Real homey kitchen craft scene. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poinsettia-green-leaves.webp",
        "prompt": (
            "Five long pointed dark green construction paper leaves, each about hand-sized, "
            "cut and laid out in a neat row on a white craft table. "
            "Each leaf is teardrop shaped with a sharp pointed tip. "
            "The edges are slightly uneven and clearly cut by a child with kid scissors. "
            "Next to the leaves on the table: a yellow pencil, blue Fiskars kid scissors, "
            "and a small green paper scrap. Top-down flat lay shot, natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poinsettia-red-petals.webp",
        "prompt": (
            "Six pointed bright red construction paper petals, slightly shorter than green leaves, "
            "arranged in a small cluster on a white craft table. "
            "Next to the red petals are the previously cut five long pointed green paper leaves "
            "in a row for comparison. The red petals are clearly smaller and a bit narrower than the green leaves. "
            "Edges are slightly uneven and child-cut. A yellow pencil and blue kid scissors sit on the table. "
            "Top-down flat lay shot, soft natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poinsettia-yellow-centers.webp",
        "prompt": (
            "Five or six small bright yellow construction paper circles, each about the size of a pea, "
            "arranged in a tiny cluster on a white craft table. "
            "Next to the yellow dots: a small scrap of yellow construction paper with several "
            "tiny circular holes punched through it, and a small hole punch tool. "
            "Top-down flat lay shot, soft natural light. Charming child-made craft scene. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poinsettia-glue-green.webp",
        "prompt": (
            "Five long pointed dark green construction paper leaves glued in a star shape "
            "on a white cardstock background, sitting on a white craft table. "
            "The wide bases of the leaves meet in the center and the pointed tips fan outward "
            "evenly around the center, like the petals of a flower. "
            "No red petals yet, just the green leafy base. "
            "A purple Elmer's glue stick lies open next to the cardstock. "
            "Top-down flat lay shot, warm natural light. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poinsettia-add-red.webp",
        "prompt": (
            "A paper poinsettia craft in progress on a white cardstock background. "
            "Five long pointed dark green construction paper leaves are glued in a star shape "
            "as the base. Six slightly shorter bright red pointed paper petals are layered on top, "
            "rotated so the red points peek out between the green points, forming a bright red "
            "and green poinsettia bloom. No yellow center yet, just the red petals over green leaves. "
            "Sitting on a light wood craft table. A purple glue stick is open nearby. "
            "Top-down flat lay shot, warm natural light. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-poinsettia-finished.webp",
        "prompt": (
            "A finished paper poinsettia craft on white cardstock displayed on a light wood craft table. "
            "Five long pointed dark green paper leaves form the base in a star pattern. "
            "Six pointed bright red paper petals are layered on top, slightly rotated so red points "
            "peek between the green. In the very center is a cheerful cluster of five small yellow "
            "paper dots glued together. Soft marker pen veins are visible down the middle of each "
            "red petal and green leaf, giving the flower a realistic poinsettia look. "
            "Charming child-made craft, slightly uneven edges. Cozy holiday Christmas mood. "
            "Top-down flat lay shot, warm natural light. "
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
