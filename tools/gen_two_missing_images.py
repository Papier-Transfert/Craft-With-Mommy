#!/usr/bin/env python3
"""Generate folded-paper-fish.webp and paper-helicopter-spinner.webp for paper-arts-and-crafts."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-arts-and-crafts"
TARGET_W, TARGET_H = 1200, 900

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "The craft is clearly handmade by a child, charming and imperfect. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "folded-paper-fish.webp",
        "prompt": (
            "A handmade folded paper fish craft on a white craft table. "
            "A square sheet of orange construction paper folded into a triangle fish shape "
            "with a small triangular tail flap folded back to form the tail fin. "
            "A large googly eye glued on one side, and blue paper strips cut and glued "
            "as fin details along the top. The fish lies flat on the table. "
            "Scissors and leftover orange paper scraps sit nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-helicopter-spinner.webp",
        "prompt": (
            "A handmade paper helicopter spinner craft held between a child's fingers. "
            "A single strip of white cardstock about 15cm long, folded near one end so the "
            "two ends fan out like helicopter blades in opposite directions. "
            "A small metal paper clip attached at the bottom as a weight. "
            "The child's hand holds it at arm's length, ready to let it drop and spin. "
            "A white craft table is visible below. The strip is decorated with red and blue "
            "marker stripes. "
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
    client = genai.Client(api_key=api_key)

    for img in IMAGES:
        out = IMG_DIR / img["filename"]
        log.info(f"Generating {img['filename']}...")
        for attempt in range(1, 4):
            if attempt > 1:
                log.info(f"  Retry {attempt}/3...")
                time.sleep(3)
            try:
                if generate_image(client, img["prompt"], out):
                    break
            except Exception as e:
                log.warning(f"  Error: {e}")
            time.sleep(2)
        else:
            log.error(f"  FAILED after 3 attempts: {img['filename']}")

    log.info("Done.")


if __name__ == "__main__":
    main()
