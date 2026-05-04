#!/usr/bin/env python3
"""Generate all images for craft-using-paper-cups.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "craft-using-paper-cups"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "craft-using-paper-cups.webp",
        "prompt": (
            "A finished handmade flower bouquet craft using small white paper cups: "
            "five paper cups have been transformed into bright flowers, each with petals cut from the rim "
            "and pressed open in different shapes. The flowers are painted in cheerful spring colors: "
            "pink, golden yellow, soft purple, coral orange, and bright magenta. "
            "Each flower has a small contrasting paper circle glued inside as the bloom center, "
            "and a green pipe cleaner stem with a small green construction paper leaf attached to it. "
            "The entire bouquet is arranged in a small clear glass jar tied with a thin ribbon. "
            "Photographed from above on a white craft table with soft natural light, "
            "scissors and a few extra paper scraps visible at the edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-using-paper-cups-mom-child.webp",
        "prompt": (
            "A mom with shoulder-length hair sitting next to her young child (around five years old) at a white craft table. "
            "Both are smiling and looking at the supplies laid out in front of them: "
            "a small stack of plain white Dixie-style 3 oz paper cups, several small bottles of washable kids paint "
            "in pink, yellow, and purple, two kid-sized paint brushes, a bundle of green pipe cleaners, "
            "a sheet of green construction paper, a glue stick, blunt-tip kid scissors, and a pencil. "
            "The mood is warm and excited, ready to begin a craft using paper cups together. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-using-paper-cups-pencil-lines.webp",
        "prompt": (
            "Three small white paper cups standing upside down on a white craft table, "
            "each cup marked with eight evenly spaced light pencil lines running vertically "
            "from the top rim down toward the closed base, each line stopping about half an inch short of the bottom. "
            "A yellow pencil rests on the table beside the cups. The lines are clearly visible. "
            "Flat overhead photo with soft natural light, no other clutter on the table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-using-paper-cups-cut-slits.webp",
        "prompt": (
            "A single small white paper cup standing upside down on a white craft table, "
            "with eight straight vertical petal slits already cut from the rim down toward the base, "
            "each slit stopping about half an inch from the bottom so the petal strips remain attached at the base. "
            "The cut petal strips are still pointing straight up like a closed tulip bud. "
            "A pair of bright blue blunt-tip kid scissors lies open on the table beside the cup. "
            "Small paper trimmings are scattered nearby. Flat overhead photo, soft daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-using-paper-cups-petals-open.webp",
        "prompt": (
            "Three white paper cups sitting upside down on a white craft table, "
            "each one with its eight cut petal strips now bent outward into a different flower shape: "
            "the first has petals folded flat outward like a wide daisy, "
            "the second has petals curled gently outward at the tips like an open lily, "
            "the third has petals only slightly opened to look like a tulip bud. "
            "All three flowers are still plain white, not yet painted. "
            "Soft natural light, flat overhead photo, no other supplies in frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-using-paper-cups-painted.webp",
        "prompt": (
            "Five paper cup flowers freshly painted in bright cheerful colors: "
            "one pink, one golden yellow, one soft purple, one coral orange, and one magenta, "
            "all sitting upside down on a sheet of white paper towel to dry on a white craft table. "
            "The petals on each cup have been pressed open into flower shapes. "
            "Several small bottles of Crayola-style washable kids paint are visible in the background, "
            "along with a paint brush resting on the edge of a paper plate palette with smudges of paint. "
            "Soft natural daylight, slightly imperfect handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-using-paper-cups-stems-attached.webp",
        "prompt": (
            "A single finished paper cup flower painted bright pink, with petals pressed open into a daisy shape. "
            "A small bright yellow construction paper circle is glued inside the cup as the flower center, "
            "clearly visible from the open side. A long green pipe cleaner has been pushed through "
            "a small hole in the closed bottom of the cup and now extends downward as a green stem. "
            "Beside the flower on the white craft table sit a few extra small paper centers in yellow and orange, "
            "a small purple glue stick, and a bundle of green pipe cleaners. "
            "Flat overhead photo, warm daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-using-paper-cups-finished-bouquet.webp",
        "prompt": (
            "A finished cheerful flower bouquet made entirely from a craft using paper cups, "
            "with five small painted paper cup flowers in pink, yellow, purple, orange, and magenta, "
            "each with a contrasting paper center, a green pipe cleaner stem, and a small green paper leaf "
            "wrapped around each stem. All the stems are gathered into a bunch and tied with a thin pastel ribbon. "
            "The finished bouquet is displayed in a small clear glass jar on a sunny white windowsill, "
            "with soft daylight streaming through and casting gentle shadows. "
            "The handmade, slightly imperfect quality is clearly visible, child-made and joyful. "
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
