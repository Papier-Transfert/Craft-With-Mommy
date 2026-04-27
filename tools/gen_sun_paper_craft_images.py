#!/usr/bin/env python3
"""Generate all images for sun-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "sun-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood or white craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper, real markers, real glue. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "sun-paper-craft.webp",
        "prompt": (
            "A finished bright yellow sun paper craft displayed flat on a white craft table. "
            "The sun has a round yellow construction paper face with a friendly drawn smile, "
            "two big round eyes, and small rosy pink cheeks. Around the back edge of the circle, "
            "twelve triangular construction paper rays alternate yellow and orange, pointing outward "
            "like a child's drawing of the sun. The whole craft is about 8 inches across. "
            "Markers and glue stick visible slightly out of focus in the background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "sun-paper-craft-mom-child.webp",
        "prompt": (
            "A mom and a young child around age 4 sitting together at a bright craft table, "
            "both smiling, looking down at sheets of yellow and orange construction paper they are about to use. "
            "The child holds a small pair of blunt-tip kid scissors and the mom is pointing to the paper. "
            "A small bowl, a pencil, and a glue stick are also on the table, ready for a sun paper craft. "
            "Warm, cozy, emotionally connected moment with morning light coming through a window. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "sun-paper-craft-trace-circle.webp",
        "prompt": (
            "A child's small hands tracing a circle on a sheet of bright yellow construction paper "
            "using a small white bowl turned upside down as a guide. A pencil rests in the child's hand "
            "drawing along the bowl's edge. The faint pencil line is visible along the curve. "
            "The yellow construction paper fills most of the frame on a light wood craft table. "
            "Flat-lay overhead view. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "sun-paper-craft-cut-rays.webp",
        "prompt": (
            "A flat-lay overhead view of a craft table showing the same yellow construction paper sun face circle "
            "(already cut out, about 5 inches across) and beside it a small pile of freshly cut triangular rays, "
            "six in bright yellow construction paper and six in bright orange construction paper. "
            "The rays are about 2 to 3 inches long, like skinny pizza slices. "
            "A pair of kid blunt-tip scissors and a few paper scraps lie nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "sun-paper-craft-glue-rays.webp",
        "prompt": (
            "A flat-lay overhead view of the same yellow circle, now flipped upside down so the back is facing up. "
            "Yellow and orange triangular paper rays are being glued around the back edge of the circle, "
            "alternating colors and pointing outward, with about half of the rays already attached "
            "and a few more waiting to be added. A child's small hand presses one orange ray firmly in place. "
            "A purple glue stick lies open on the table beside the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "sun-paper-craft-draw-face.webp",
        "prompt": (
            "A flat-lay overhead view of the same sun craft, now flipped right-side up so the smooth yellow face is showing, "
            "with the alternating yellow and orange paper rays clearly visible all around the back edge of the circle. "
            "A child's small hand uses a black marker to draw a happy curved smile and two round eyes "
            "onto the front of the yellow sun face. The eyes and smile are about a third of the way down the circle. "
            "A few markers in different colors lie nearby on the wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "sun-paper-craft-add-details.webp",
        "prompt": (
            "A flat-lay overhead view of the same finished sun paper craft on a light wood craft table. "
            "The yellow circle face now has two round black eyes, a wide curved black smile, "
            "two pink rosy cheeks below the eyes, and small curved black eyebrows above the eyes. "
            "Tiny pink and orange dots have been added near the tips of some of the alternating yellow and orange rays "
            "to look like sparkles. The whole sun looks bright, friendly, and clearly handmade by a child. "
            "Markers and a pink crayon scattered nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "sun-paper-craft-finished.webp",
        "prompt": (
            "A finished bright yellow sun paper craft taped to the inside of a sunny window with morning sunlight "
            "shining around its edges. The sun has a round yellow face with a happy smile, big eyes, "
            "rosy pink cheeks, and twelve alternating yellow and orange construction paper rays around the edge. "
            "The window frame is white and the soft glow of daylight surrounds the craft. "
            "Warm, cozy, kitchen or playroom atmosphere. Photographed at a slight angle so the sun fills the frame. "
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
