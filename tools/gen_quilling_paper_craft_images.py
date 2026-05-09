#!/usr/bin/env python3
"""Generate all images for quilling-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "quilling-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and slightly imperfect, clearly handmade. Pinterest-worthy. "
    "Image fills the full frame edge to edge with no white borders or padding."
)

IMAGES = [
    {
        "filename": "quilling-paper-craft.webp",
        "prompt": (
            "A finished handmade quilling paper craft flower card placed on a light wood craft table. "
            "On the front of a white folded greeting card, a delicate five petal quilled flower is glued: "
            "five soft pink teardrop shaped paper coils form the petals, a small tight yellow paper coil "
            "sits as the flower center, and two small green marquise (eye-shaped) leaf coils sit just below. "
            "Around the card, several thin colorful quilling paper strips in pink, yellow, blue, and green are "
            "scattered loosely. A small slotted quilling tool with a blue handle and a tan cork board are "
            "visible at the edge of the frame. The whole composition is bright, cheerful, and clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "quilling-paper-craft-mom-child.webp",
        "prompt": (
            "A warm, candid photo of a young American mom and her smiling 6 year old child sitting together "
            "at a light wood kitchen craft table working on a quilling paper craft. "
            "The child is rolling a thin pink paper strip onto a small blue handled slotted quilling tool. "
            "Assorted thin colorful quilling paper strips in pink, yellow, blue, and green are spread on the table. "
            "A small white folded greeting card and a tan cork board sit nearby. "
            "Both faces are visible and gentle natural sunlight comes from a window. "
            "Cozy, real moment, not staged. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "quilling-paper-craft-supplies.webp",
        "prompt": (
            "A flat lay overhead photo of quilling paper craft supplies neatly arranged on a light wood table. "
            "Visible: a small bundle of thin quilling paper strips in pink, yellow, blue, and green; "
            "a single blue handled slotted quilling tool; a tan square cork board; a small bottle of clear glue; "
            "a pair of fine point silver tweezers; a folded white blank greeting card; "
            "a wooden pencil; and a single wooden toothpick. "
            "The supplies are arranged cleanly with a little space between each item. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "quilling-paper-craft-pencil-outline.webp",
        "prompt": (
            "A blank white folded 5 by 7 inch greeting card lying flat on a light wood craft table. "
            "On the front of the card, a very faint pencil sketch shows a simple five petal flower in the center, "
            "with a small circle in the middle for the flower center, and two small leaf shapes drawn at the bottom. "
            "The pencil lines are light gray and barely visible. A sharpened wooden pencil rests beside the card. "
            "Clean, simple, beginner friendly composition. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "quilling-paper-craft-rolling-coil.webp",
        "prompt": (
            "A close up overhead photo of a child's small hands rolling a thin pink paper quilling strip "
            "on a blue handled slotted quilling tool. The paper strip is wrapping neatly around the tool tip "
            "into a small tidy spiral coil. Other unrolled colorful paper strips lay in soft scatter on the "
            "light wood craft table beside a tan cork board. The shot focuses on the rolling action. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "quilling-paper-craft-teardrop-petals.webp",
        "prompt": (
            "An overhead close up of five small pink quilling paper coils that have been pinched into "
            "teardrop shapes on one side, arranged in a circular flower petal pattern on a tan square cork board. "
            "Each teardrop has a sharp pointed tip facing toward the empty center of the circle and a rounded "
            "outer edge. The paper coils show visible spiral lines inside. The cork board sits on a light wood table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "quilling-paper-craft-center-leaves.webp",
        "prompt": (
            "An overhead close up of three small finished quilling shapes arranged on a tan cork board: "
            "one tiny tight yellow paper coil that looks like a small wound spiral, "
            "and two green marquise (eye shaped) leaf coils with both ends pinched into points. "
            "Five pink teardrop petal coils sit nearby in a partial circle. "
            "All shapes are clearly handmade with visible paper spirals inside. "
            "Light wood craft table beneath the cork board. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "quilling-paper-craft-gluing-coils.webp",
        "prompt": (
            "An overhead close up photo of a child's hand using small fine point silver tweezers to place "
            "a pink teardrop shaped quilling paper petal onto a white folded greeting card. "
            "Three other pink teardrop petals are already glued onto the card around a small yellow center coil, "
            "forming most of a flower. A small bottle of clear glue and a wooden toothpick sit beside the card. "
            "The card lies on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "quilling-paper-craft-finished.webp",
        "prompt": (
            "A small smiling 6 year old child holding up a finished handmade quilling paper craft flower card "
            "toward the camera with both hands. The white folded greeting card features a sweet quilled flower "
            "made of five pink teardrop petals around a small yellow center coil, with two green leaf coils "
            "near the bottom. The child wears a casual t-shirt and is photographed in a cozy light home kitchen "
            "with warm natural light. The full card and the child's proud smile are clearly visible. "
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
