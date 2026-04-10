#!/usr/bin/env python3
"""Generate all images for paper-star-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-star-craft"
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
        "filename": "paper-star-craft.webp",
        "prompt": (
            "A beautiful finished paper star craft hanging from a pink ribbon near a bright window. "
            "The star is cut from yellow cardstock and decorated with bold rainbow marker colors "
            "and sparkly gold and silver glitter glue along the edges and points. "
            "The star is large, about 9 inches wide, and clearly handmade with slightly uneven edges. "
            "Warm sunlight catches the glitter and makes it shimmer. "
            "A craft table surface is visible in the background with a glue stick and markers nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-star-craft-why-kids-love.webp",
        "prompt": (
            "A warm, joyful scene of a mom and her young child (around age 5) sitting together "
            "at a light wood craft table, smiling and excited. "
            "The table has colorful sheets of cardstock, washable markers, and a pencil laid out. "
            "The mom is pointing at a pencil-drawn star outline on a yellow cardstock sheet. "
            "The child is looking at it with wide, happy eyes. "
            "Cozy home environment, natural window light, warm and authentic family moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-star-craft-gather-trace.webp",
        "prompt": (
            "A flat lay of craft supplies neatly arranged on a white craft table: "
            "a large yellow cardstock sheet with a pencil-drawn five-pointed star outline in the center, "
            "a pencil lying beside it, a pair of child-safe scissors, "
            "a set of colorful washable markers, and a small bottle of glitter glue. "
            "The star outline is large, about 8 to 10 inches wide. "
            "Clean and organized setup, ready to begin crafting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-star-craft-cut-out.webp",
        "prompt": (
            "Close-up of a young child's small hands holding child-safe scissors "
            "and carefully cutting along a large pencil-drawn star outline on bright yellow cardstock. "
            "The paper is on a white craft table. "
            "The scissors are clearly child-sized with soft grip handles. "
            "The star shape is large and the cutting is in progress, showing the inward angle between two points. "
            "Slightly uneven cut edges, natural handmade look. Warm natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-star-craft-color.webp",
        "prompt": (
            "A large cut-out paper star lying flat on a white craft table, "
            "being colored with washable markers. "
            "Each of the five points is a different bright color: red, orange, blue, purple, and green. "
            "The center of the star has a swirl of yellow marker. "
            "Several uncapped markers are arranged around the star. "
            "A child's hand is visible adding color to one of the points. "
            "Bold, bright, clearly handmade coloring style. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-star-craft-glitter.webp",
        "prompt": (
            "A brightly colored paper star lying flat on a white craft table. "
            "A child is squeezing gold glitter glue along the outer edge of one of the star points, "
            "creating a thin sparkly border. "
            "Silver glitter glue trails are already visible along two other points. "
            "The glitter glue bottle is visible in the child's hand. "
            "The star colors beneath are vivid rainbow markers. "
            "The glitter catches the light beautifully. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-star-craft-add-ribbon.webp",
        "prompt": (
            "A fully decorated paper star lying flat on a white craft table. "
            "The star has colorful marker decorations and dried sparkly glitter glue along the edges. "
            "A small hole has been punched near the top point of the star. "
            "A piece of soft pink ribbon is being threaded through the hole by a child's fingers. "
            "A single hole punch tool is visible nearby. "
            "The star looks finished and beautiful, ready to hang. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-star-craft-display.webp",
        "prompt": (
            "A finished paper star craft hanging from a pink ribbon tied to a small wooden peg "
            "on a bright white wall near a sunny window. "
            "The star is large and colorful with rainbow marker coloring and gold and silver glitter "
            "glue accents along the points and edges that sparkle in the sunlight. "
            "The background is soft and light, giving a warm and cheerful atmosphere. "
            "The star hangs at a slight angle, swaying gently, clearly handmade and beautiful. "
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
