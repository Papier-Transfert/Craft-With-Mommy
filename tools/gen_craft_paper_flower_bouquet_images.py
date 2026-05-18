#!/usr/bin/env python3
"""Generate all images for craft-paper-flower-bouquet.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "craft-paper-flower-bouquet"
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
        "filename": "craft-paper-flower-bouquet.webp",
        "prompt": (
            "A finished handmade paper flower bouquet on a light wood craft table. "
            "Seven layered cardstock flowers in bright pink, yellow, purple, and orange "
            "with contrasting circle centers, each on a green pipe cleaner stem with "
            "small green paper leaves halfway down the stems. The whole bouquet is "
            "wrapped in soft pink tissue paper that flares out at the top and gathers "
            "at the base, tied with a pink satin ribbon in a tidy bow. The bouquet lies "
            "at a slight angle, photographed from above. Cardstock scraps and a glue "
            "stick visible at the edge of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-flower-bouquet-mom-child.webp",
        "prompt": (
            "A warm photo of a young American mom and her preschool age child sitting "
            "side by side at a light wood craft table, both smiling and engaged. "
            "On the table in front of them: sheets of bright pink, yellow, purple, and "
            "orange cardstock, a bundle of green pipe cleaners, kid scissors, an "
            "Elmer's glue stick, and a few partially cut paper flower shapes. The mom "
            "is helping the child shape a flower petal. Warm cozy lighting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-flower-bouquet-cut-petals.webp",
        "prompt": (
            "A flat lay of seven cardstock flower cutouts on a light wood craft table. "
            "Each flower has rounded petals (some with five petals, some with six), in "
            "bright pink, lemon yellow, lavender purple, and orange. The flowers vary "
            "slightly in size. Around them: kid scissors, a few small cardstock scraps, "
            "and a folded square of cardstock showing how they were cut. Clean and tidy "
            "composition. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-flower-bouquet-layered-blooms.webp",
        "prompt": (
            "Several handmade two-layer paper flowers on a light wood craft table. "
            "Each bloom has a larger flower shape on the bottom in one color (pink, "
            "yellow, purple, or orange) and a smaller flower shape on top in a "
            "contrasting color, glued in the center with the petals offset so both "
            "layers are visible. No stems yet. A glue stick lies beside the flowers. "
            "Clean flat lay, child-made look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-flower-bouquet-add-centers.webp",
        "prompt": (
            "Several handmade two-layer cardstock paper flowers on a light wood craft "
            "table, each now featuring a small contrasting circle glued in the very "
            "center: yellow circles on pink and purple flowers, pink circles on yellow "
            "flowers. The flower faces look cheerful and complete. A glue stick and "
            "small circle cutouts visible at the edge of the frame. Top down view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-flower-bouquet-attach-stems.webp",
        "prompt": (
            "Close up top down photo on a light wood craft table showing the back of "
            "a handmade pink cardstock paper flower. A green pipe cleaner is laid flat "
            "against the back behind the flower center, pointing down like a stem. A "
            "small square of clear tape secures the tip of the pipe cleaner to the "
            "cardstock. Several other completed paper flowers with stems already "
            "attached lie nearby. Real craft materials. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-flower-bouquet-add-leaves.webp",
        "prompt": (
            "Three or four finished handmade paper flowers lying side by side on a "
            "light wood craft table. Each flower is in bright cardstock (pink, yellow, "
            "purple, or orange) with a green pipe cleaner stem. About halfway down each "
            "stem, one or two small pointed oval green cardstock leaves are attached "
            "and bent slightly outward. The composition is calm and clean, with green "
            "paper scraps visible at the edge. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-flower-bouquet-gather-stems.webp",
        "prompt": (
            "A small child's hand holding a gathered bundle of seven handmade paper "
            "flowers in pink, yellow, purple, and orange cardstock with green pipe "
            "cleaner stems twisted tightly together near the base. The flower heads "
            "sit at slightly different heights, like a real bouquet. Small green "
            "paper leaves are visible halfway down the stems. Light wood craft table "
            "in the background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-flower-bouquet-wrapped-bouquet.webp",
        "prompt": (
            "A finished handmade paper flower bouquet lying flat on a light wood craft "
            "table. Seven colorful cardstock flowers in pink, yellow, purple, and "
            "orange with green pipe cleaner stems are bundled together and wrapped in "
            "soft pink tissue paper that flares out around the flower heads and "
            "gathers at the base. A pink satin ribbon is tied in a tidy bow around the "
            "tissue paper near the bottom of the stems. Photographed from above at a "
            "slight angle. Ready to be given as a sweet handmade gift. "
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
