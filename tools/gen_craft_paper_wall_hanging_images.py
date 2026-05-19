#!/usr/bin/env python3
"""Generate all images for craft-paper-wall-hanging.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "craft-paper-wall-hanging"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "Image must fill the entire frame edge to edge with no white borders, no letterboxing, no padding."
)

IMAGES = [
    {
        "filename": "craft-paper-wall-hanging.webp",
        "prompt": (
            "A finished handmade craft paper wall hanging displayed on a soft cream nursery wall. "
            "A 12 inch unfinished wooden dowel forms the top, with five jute twine strands hanging "
            "evenly along it. Each strand carries three or four layered cardstock paper shapes including "
            "small circles, scalloped clouds, and tiny rainbow arches in pastel pink, soft yellow, light blue, "
            "and white, each shape with a contrasting smaller shape glued on top showing a thin ring of color. "
            "A soft pink satin ribbon forms a hanging loop above the dowel, with three small pastel tissue "
            "paper tassels tied along it at the ends and center. The whole hanging sways slightly with a "
            "soft handmade boho feel. Clean photo, no objects in foreground. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-wall-hanging-mom-child.webp",
        "prompt": (
            "A warm overhead view of a young American mom and her four year old child sitting "
            "side by side at a light wood craft table, smiling as they look at the craft supplies "
            "in front of them. On the table are stacks of pastel cardstock in pink, yellow, blue and white, "
            "a 12 inch wooden dowel, a small ball of natural jute twine, a blue single hole punch, "
            "a glue stick, kid scissors with red handles, and a few already cut paper circles and cloud shapes. "
            "The mom is gently helping the child line up paper pieces. Cozy family kitchen feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-wall-hanging-cut-shapes.webp",
        "prompt": (
            "A flat lay close up of about fifteen freshly cut paper shapes on a light wood craft table. "
            "The shapes include small circles, scalloped cloud shapes, and tiny rainbow arches in pastel pink, "
            "soft yellow, light blue, and white cardstock and construction paper. The shapes are arranged "
            "in tidy rows, each about two to three inches wide, with slightly wobbly child-cut edges. "
            "Kid scissors with red handles and a few cardstock scraps are visible at the edge of the frame. "
            "Bright natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-wall-hanging-layered-shapes.webp",
        "prompt": (
            "A flat lay close up of fifteen layered paper shapes arranged in rows on a light wood craft table. "
            "Each piece is a larger pastel cardstock shape (circle, scalloped cloud, or rainbow arch) "
            "in pink, yellow, blue or white with a smaller contrasting shape in a different pastel color "
            "glued centered on top, leaving a thin colored frame visible around the edge. "
            "A purple glue stick lies open on the table next to them and a few finished shapes have tiny "
            "marker dots or simple heart drawings in their centers. Bright natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-wall-hanging-punch-holes.webp",
        "prompt": (
            "A close up of small child hands using a blue handheld single hole punch with a soft grip "
            "to punch a small hole at the top center of a layered pastel pink and yellow paper shape "
            "on a light wood craft table. Around the work area, fifteen layered pastel cardstock shapes "
            "(circles, clouds, rainbow arches) are arranged in five neat columns of three, each shape "
            "showing a small clean punched hole at the very top center. A few tiny paper hole dots are "
            "scattered on the table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-wall-hanging-thread-twine.webp",
        "prompt": (
            "Five lengths of soft natural jute twine laid out side by side on a light wood craft table. "
            "Each strand of twine is threaded through the punched hole of three or four layered pastel "
            "paper shapes (small circles, scalloped clouds, tiny rainbow arches) in pink, yellow, blue "
            "and white. The shapes are slightly staggered at different heights along each strand, with "
            "small simple knots tied in the twine between shapes to hold them in place. A pair of "
            "kid scissors and a small ball of natural jute twine sit at the edge of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-wall-hanging-tie-dowel.webp",
        "prompt": (
            "An overhead view of a 12 inch unfinished wooden dowel lying flat on a light wood craft table. "
            "Five strands of natural jute twine are tied evenly along the dowel with simple double knots, "
            "each spaced about an inch and a half apart. Each twine strand hangs straight down from the dowel "
            "and carries three or four layered pastel cardstock paper shapes (small circles, scalloped clouds, "
            "tiny rainbow arches in pink, yellow, blue and white), forming a soft, even paper curtain. "
            "The composition feels balanced and almost finished. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "craft-paper-wall-hanging-finished-hung.webp",
        "prompt": (
            "The completed handmade craft paper wall hanging proudly displayed on a soft cream nursery wall. "
            "A 12 inch unfinished wooden dowel forms the top crossbar with five jute twine strands tied "
            "evenly along it, each strand carrying three or four layered pastel cardstock paper shapes "
            "(small circles, scalloped clouds, tiny rainbow arches in pink, yellow, blue and white). "
            "A soft pink satin ribbon ties to both tips of the dowel and forms a hanging loop above. "
            "Three small handmade tissue paper tassels in pastel pink, yellow, and blue hang along the "
            "ribbon at the two ends and center. Soft warm daylight, gentle nursery feel, the hanging "
            "fills the frame as the focal point. "
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
