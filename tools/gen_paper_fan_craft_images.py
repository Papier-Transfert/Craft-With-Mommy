#!/usr/bin/env python3
"""Generate all images for paper-fan-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-fan-craft"
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
        "filename": "paper-fan-craft.webp",
        "prompt": (
            "A flat lay of three finished handmade paper fan crafts on a white craft table: "
            "one bright pink fan, one sky blue fan, and one yellow fan, all opened into full "
            "semicircle shapes. Each fan is accordion-folded from construction paper with crisp "
            "pleats. One fan has colorful washi tape stripes across the pleats. A craft stick "
            "handle is visible on one fan. Scattered construction paper scraps and a glue stick "
            "at the edges. Warm, cheerful, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fan-craft-why-kids-love.webp",
        "prompt": (
            "A young mom and her preschool-aged child sitting together at a bright white craft table, "
            "both smiling and looking excited. Several colorful sheets of construction paper in pink, "
            "blue, and yellow are spread on the table in front of them. A glue stick and scissors "
            "are visible. The atmosphere is warm, cozy, and cheerful. Realistic family photo feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fan-craft-cut-paper.webp",
        "prompt": (
            "A long rectangle of bright pink construction paper lying flat on a white craft table, "
            "approximately 4.5 inches by 12 inches. A ruler and pencil are placed neatly next to "
            "the paper. A small pile of colored construction paper sheets is visible in the background. "
            "Clean, simple, well-lit craft table setup. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fan-craft-accordion-fold.webp",
        "prompt": (
            "Close-up of a child's small hands accordion-folding a bright yellow sheet of "
            "construction paper on a white craft table. The first three back-and-forth folds are "
            "clearly visible, showing the pleated accordion pattern beginning to form. The folds "
            "are about 1 inch wide each. The paper is half-folded with the unfolded end visible. "
            "Warm natural light, hands look small and child-like. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fan-craft-full-fold.webp",
        "prompt": (
            "A fully accordion-folded strip of blue construction paper lying flat on a white craft "
            "table. All the folds are complete from one end to the other, making a long narrow "
            "pleated strip with crisp, even creases. The folds are clearly visible as alternating "
            "ridges. The strip is about 12 inches long and 1 inch wide when fully folded. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fan-craft-fold-in-half.webp",
        "prompt": (
            "A fully accordion-folded strip of red construction paper being held in a child's "
            "small hands, pinched at the center and folded in half so both ends meet. "
            "The folded fan shape is beginning to appear. The layers are fanned slightly apart "
            "at the top while the base is pinched together tightly. White craft table background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fan-craft-secure-base.webp",
        "prompt": (
            "A pinched accordion-folded paper fan base being secured with a strip of clear tape "
            "wrapped tightly around the bottom where all the layers meet. A wooden craft stick "
            "popsicle stick is tucked inside the tape wrap as a handle. The fan layers spread "
            "upward above the tape. The tape is clearly visible and neatly applied. "
            "White craft table background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fan-craft-open-fan.webp",
        "prompt": (
            "A finished accordion-folded paper fan opened into a full semicircle shape, held "
            "upright on a white craft table. The orange construction paper pleats fan out evenly "
            "in a perfect half-circle. The taped base with a craft stick handle is visible at "
            "the bottom. The fan is crisp and clean with no decorations yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fan-craft-decorate.webp",
        "prompt": (
            "A young child's hands pressing colorful washi tape strips across the pleats of "
            "a finished paper fan craft on a white craft table. Several rolls of colorful "
            "washi tape in pink, blue, and gold patterns are nearby. Small star stickers are "
            "scattered on the table. The fan is propped open and partially decorated with "
            "two washi tape stripes already applied. Cheerful and creative craft moment. "
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
