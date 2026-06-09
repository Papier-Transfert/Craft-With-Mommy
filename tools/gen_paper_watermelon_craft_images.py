#!/usr/bin/env python3
"""Generate all images for paper-watermelon-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-watermelon-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-watermelon-craft.webp",
        "prompt": (
            "A finished handmade paper watermelon slice craft lying flat on a white craft table. "
            "It is a half-circle made from layered construction paper: a wide green half-circle rind on the bottom, "
            "a thin white crescent strip above it, and a big red half-circle of fruit on top. "
            "Several small black paper teardrop seeds are scattered across the red fruit. "
            "A small cheerful smiling face is drawn on the red part with marker. "
            "Bright summery colors, clearly cut and glued by a young child, slightly uneven edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-watermelon-craft-mom-child.webp",
        "prompt": (
            "A warm scene of a young mother and her happy preschool child sitting together at a light wood craft table, "
            "about to make a paper watermelon craft. On the table are sheets of red, green, white, and black construction paper, "
            "child-safe scissors, and a glue stick. The mom is smiling and pointing at a red paper half-circle. "
            "Cozy home kitchen background, warm natural light, candid and loving family moment. "
            "The photograph is full bleed and fills the entire image frame edge to edge. "
            "No white border, no frame, no margin, no padding around the photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-watermelon-cut-red-fruit.webp",
        "prompt": (
            "A child's hands using child-safe scissors to cut a large red half-circle shape from a sheet of red construction paper, "
            "on a white craft table. The half-circle is the juicy fruit part of a paper watermelon craft. "
            "A faint pencil line shows the curve being followed. A few red paper scraps lie nearby. "
            "Close, clear view of the single red half-circle being cut. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-watermelon-cut-green-rind.webp",
        "prompt": (
            "A green construction paper half-circle laid flat on a white craft table next to a slightly smaller red paper half-circle, "
            "to show the green rind is a bit bigger than the red fruit for a paper watermelon craft. "
            "Child-safe scissors and a few green paper scraps beside them. "
            "Clear flat lay showing the green rind shape and the red fruit shape side by side. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-watermelon-white-rind-strip.webp",
        "prompt": (
            "A flat lay on a white craft table of three separate paper pieces for a paper watermelon slice craft, not yet glued: "
            "a green half-circle (semicircle with a flat straight top edge and a curved bottom), "
            "a red half-circle (semicircle, slightly smaller, also with a flat top edge and curved bottom), "
            "and a thin white curved crescent strip about a finger wide that follows the same curve. "
            "All three shapes are clearly half-circle slice shapes, not full circles. "
            "Child-safe scissors and a few white paper scraps nearby. Clear top-down view. "
            "The photograph is full bleed and fills the entire image frame edge to edge with no white border or padding. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-watermelon-glue-slice.webp",
        "prompt": (
            "A handmade paper watermelon slice assembled and glued together on a white craft table: "
            "a green half-circle rind on the bottom, a thin white crescent strip in the middle, "
            "and a red half-circle of fruit on top, all edges lined up so the green rim and white band show along the curve. "
            "No seeds yet. A glue stick lies open beside it. Clearly child-made with slightly uneven edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-watermelon-add-seeds.webp",
        "prompt": (
            "A child's hand placing small black paper teardrop seeds onto the red fruit of a glued paper watermelon slice "
            "made of green rind, white strip, and red fruit, on a white craft table. "
            "Several black paper seeds are already scattered across the red, with a few more seeds and scraps nearby. "
            "Clear close view of the seeds being added to the watermelon slice. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-watermelon-finished-slice.webp",
        "prompt": (
            "A finished handmade paper watermelon slice craft displayed on a white craft table: "
            "green rind, thin white inner rind, big red fruit, and many small black paper seeds, "
            "with a cute smiling face drawn on the red part with marker. "
            "Bright, cheerful, summery, clearly made by a child with charming uneven edges. "
            "Scissors and a glue stick rest at the edge of the frame. "
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
