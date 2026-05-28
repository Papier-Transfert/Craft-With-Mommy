#!/usr/bin/env python3
"""Generate all images for lettuce-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "lettuce-paper-craft"
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
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "lettuce-paper-craft.webp",
        "prompt": (
            "A finished handmade paper lettuce craft sitting on a light wood craft table. "
            "A rounded head of lettuce made from layered green construction paper leaves, "
            "each leaf with crinkled wavy edges, the lighter green leaves placed inside "
            "and the darker green outer leaves curling slightly outward like a real lettuce head. "
            "The whole craft is about the size of a small bowl. Round and full and cute. "
            "A few small green paper scraps and a glue stick visible at the edges of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lettuce-paper-craft-mom-child.webp",
        "prompt": (
            "A mom and a young child around 4 years old sitting together at a light wood craft table, "
            "smiling, getting ready to make a paper lettuce craft. "
            "Several sheets of light green and dark green construction paper, "
            "kid safety scissors, a glue stick, and a pencil laid out on the table. "
            "The mom holds a green paper leaf shape, the child reaches for the scissors. "
            "Warm bonding moment, soft natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lettuce-paper-craft-draw-leaves.webp",
        "prompt": (
            "A close up of a child's hand drawing a wavy curvy leaf shape with a pencil "
            "onto a sheet of light green construction paper on a light wood craft table. "
            "Several other green construction paper sheets stacked beside it. "
            "The leaf shape is rounded and floppy, like a lettuce leaf. "
            "A pencil and kid safety scissors are visible. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lettuce-paper-craft-cut-leaves.webp",
        "prompt": (
            "Several wavy lettuce-shaped leaves cut from light green and dark green "
            "construction paper, laid out flat on a light wood craft table. "
            "About eight to ten leaves of slightly different sizes, the larger leaves are darker green "
            "and the smaller inner leaves are paler yellow-green. "
            "Edges are wavy and slightly uneven, clearly cut by a child. "
            "Kid safety scissors and small green paper scraps visible around the leaves. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lettuce-paper-craft-crinkle-edges.webp",
        "prompt": (
            "A child's hands gently crinkling the wavy edges of a light green paper lettuce leaf "
            "to give it texture and a ruffled look, sitting at a light wood craft table. "
            "Several other green paper leaves laid flat beside the hands, "
            "some already crinkled along the edges, some still smooth. "
            "Close-up view showing the soft ruffled paper texture clearly. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lettuce-paper-craft-glue-outer-leaves.webp",
        "prompt": (
            "A child's hand pressing a darker green wavy lettuce leaf onto a round circular "
            "green paper base, with glue stick glue visible at the base of the leaf. "
            "Three darker green outer leaves already attached to the round base, forming the start "
            "of a paper lettuce head on a light wood craft table. "
            "A purple Elmer's glue stick is sitting beside the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lettuce-paper-craft-add-inner-leaves.webp",
        "prompt": (
            "A paper lettuce craft in progress with the darker outer green leaves "
            "already glued in a layered ring around the base, and a child's hand now placing "
            "smaller paler yellow-green inner leaves toward the center. "
            "The lettuce head is taking on a real rounded shape with overlapping ruffled paper leaves. "
            "Sitting on a light wood craft table with a glue stick nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lettuce-paper-craft-finished-head.webp",
        "prompt": (
            "A completed handmade paper lettuce craft on a light wood craft table. "
            "Layered light green and dark green construction paper leaves with wavy crinkled edges "
            "form a beautiful rounded head of lettuce. The smaller pale leaves are tucked in the "
            "center and the larger darker leaves curl outward around the bottom. "
            "Looks like a real fresh head of lettuce but clearly made from paper, child handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "lettuce-paper-craft-display-basket.webp",
        "prompt": (
            "A finished paper lettuce craft displayed in a small woven kitchen basket "
            "alongside two other paper vegetables like a small paper tomato and a paper carrot, "
            "sitting on a light wood kitchen counter near a window with warm natural sunlight. "
            "The paper lettuce is the star, round and full with layered green ruffled leaves. "
            "Cheerful pretend-play kitchen scene clearly made by a child. "
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
