#!/usr/bin/env python3
"""Generate all images for paper-airplane-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-airplane-craft"
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
        "filename": "paper-airplane-craft.webp",
        "prompt": (
            "A finished classic dart-style paper airplane craft resting on a white craft table. "
            "The airplane is folded from bright blue paper and decorated with colorful washi tape "
            "stripes along the wings and small star stickers near the nose. "
            "The airplane is sharp and crisp with clean folds, lying flat with wings spread open. "
            "Markers and sticker sheets visible slightly out of focus in the background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-airplane-craft-why-kids-love.webp",
        "prompt": (
            "A mom and a young child aged around 4 sitting together at a bright craft table, "
            "both smiling and looking at a sheet of colorful paper they are about to fold into a paper airplane. "
            "The child is reaching toward the paper with small hands. "
            "Colorful paper sheets in red, blue, yellow, and green are spread on the table. "
            "Warm, cozy, emotionally connected moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-airplane-craft-center-crease.webp",
        "prompt": (
            "A single sheet of bright blue paper lying flat on a white craft table. "
            "A sharp center crease runs from top to bottom down the middle of the paper, "
            "clearly visible as the paper is unfolded and lying flat. "
            "Small child's hands visible at the edge pressing the crease. "
            "Clean, simple, bright photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-airplane-craft-corner-folds.webp",
        "prompt": (
            "A sheet of bright blue paper lying on a white craft table with both top corners "
            "folded diagonally inward to the center crease, forming a triangular pointed nose at the top. "
            "The folds are neat and crisp. The paper still lies flat. "
            "The center crease is clearly visible. "
            "Child's small fingers visible lightly touching the edge of one fold. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-airplane-craft-second-folds.webp",
        "prompt": (
            "A sheet of bright blue paper on a white craft table where the slanted edges "
            "have been folded inward a second time to the center crease. "
            "The nose is now much longer and sharper than before, like an elongated dart point. "
            "Both sides are symmetrical and pressed flat with clean creases. "
            "Viewed from directly above in a flat-lay style. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-airplane-craft-fold-in-half.webp",
        "prompt": (
            "A blue paper airplane dart being held up sideways against a light background. "
            "The airplane has been folded in half along the center crease, showing a slim "
            "triangular dart profile with a sharp point at the front and a flat spine along the bottom. "
            "The airplane is clearly recognizable as a classic paper dart. "
            "One hand holding it gently at the back. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-airplane-craft-wings-folded.webp",
        "prompt": (
            "A completed blue paper dart airplane held up with both wings folded down flat and symmetrical, "
            "wings spread open at a slight angle like a real airplane ready to fly. "
            "Viewed from a front-angle perspective so both wings are clearly visible. "
            "Sharp, crisp folds. Clean white background or craft table surface. "
            "The nose points forward and the wings are level and even on both sides. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-airplane-craft-decorated.webp",
        "prompt": (
            "A beautifully decorated paper airplane craft lying on a white craft table. "
            "The airplane is folded from bright red paper and decorated with rainbow washi tape "
            "stripes running along both wings, yellow and gold star stickers near the nose, "
            "and the name 'ROCKET' written in chunky marker letters on one wing. "
            "Sticker sheets, washi tape rolls, and markers scattered artistically nearby. "
            "Wings spread open flat, airplane ready to launch. "
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

    from PIL import Image as PILImage
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
