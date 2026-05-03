#!/usr/bin/env python3
"""Generate all images for caterpillar-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "caterpillar-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "The image must fill the entire 4:3 frame edge to edge with no white borders, "
    "no padding, no letterboxing, and no blank background bands."
)

IMAGES = [
    {
        "filename": "caterpillar-paper-craft.webp",
        "prompt": (
            "A finished handmade caterpillar paper craft on a white cardstock background. "
            "The caterpillar body is made of six round green construction paper circles in slightly different shades of green, "
            "glued in a slightly curving overlapping row across a hand-cut dark green paper leaf. "
            "At one end of the body row sits a slightly larger yellow paper circle as the caterpillar's head, "
            "with two big plastic googly eyes pressed onto it and a small smile drawn in black marker. "
            "Two short curled green pipe cleaner antennae stick up from the top of the yellow head. "
            "Each green body circle has a small marker dot or pattern in the middle. "
            "Photographed flat from above on a white craft table with warm natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "caterpillar-paper-craft-mom-child.webp",
        "prompt": (
            "An American mom in her early thirties and her young child around age four sitting together at a white craft table, "
            "smiling and getting ready to make a caterpillar paper craft. "
            "On the table in front of them: green construction paper sheets, a yellow construction paper sheet, "
            "kid scissors, a purple glue stick, a small pile of plastic googly eyes, "
            "and a few green pipe cleaners. A piece of white cardstock is laid out in front of the child. "
            "Warm natural daylight from a window. The mom is leaning in attentively, pointing to the paper. "
            "Cozy real-life family kitchen setting. Authentic, candid moment, not posed. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "caterpillar-paper-craft-cut-circles.webp",
        "prompt": (
            "Six freshly cut green construction paper circles, each about two inches across, "
            "in slightly different shades of green (light green and darker green mixed together), "
            "laid out in a casual loose row on a white craft table. "
            "Beside the circles: a pair of kid scissors with red handles, a sharpened pencil, "
            "and a small round bottle cap that was used as a tracing template. "
            "A few green paper scraps are visible at the edges. "
            "Flat lay photograph from directly above. Charming, clearly child-cut with slightly uneven edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "caterpillar-paper-craft-yellow-head-leaf.webp",
        "prompt": (
            "A craft table top showing a single large yellow construction paper circle (slightly larger than a green body circle) "
            "and a hand-cut dark green construction paper leaf shape (a wide oval with a pointed tip), "
            "laid out beside the previously cut six green circles in slightly different shades of green. "
            "The arrangement is loose and casual. Kid scissors and a pencil sit nearby. "
            "Flat lay photograph from directly above on a white craft table. "
            "Clearly child-cut shapes with charming uneven edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "caterpillar-paper-craft-body-row.webp",
        "prompt": (
            "A piece of white cardstock laid out in landscape orientation on a craft table. "
            "On the cardstock, a hand-cut dark green paper leaf shape is glued near the bottom-center. "
            "Across the leaf, six green construction paper circles in slightly different shades of green "
            "are glued in a slightly curving, slightly wavy overlapping row, each circle slightly overlapping the previous one. "
            "There is no caterpillar head yet, no eyes, no antennae, only the row of green body circles on the leaf. "
            "Flat lay photograph from directly above. Clearly handmade and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "caterpillar-paper-craft-head-eyes.webp",
        "prompt": (
            "The caterpillar paper craft from the previous step continues here. "
            "A piece of white cardstock with a hand-cut dark green paper leaf glued to it, "
            "and six green construction paper circles glued in a slightly curving overlapping row across the leaf. "
            "Now a slightly larger yellow construction paper circle has been glued to one end of the green body row as the head, "
            "slightly overlapping the first body circle. Two large plastic googly eyes are pressed onto the yellow head. "
            "There are no antennae yet and no marker dots on the body. "
            "Flat lay photograph from directly above on a craft table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "caterpillar-paper-craft-antennae.webp",
        "prompt": (
            "The caterpillar paper craft continues. "
            "A piece of white cardstock with a hand-cut dark green paper leaf, "
            "six green paper body circles in a slightly curving overlapping row across the leaf, "
            "and a slightly larger yellow paper head circle glued at one end with two large googly eyes pressed onto it. "
            "Now two short green pipe cleaner antennae have been added at the very top of the yellow head, "
            "each curled into a small loose spiral at the tip and pointing upward and slightly outward. "
            "There are no marker dots on the body yet. "
            "Flat lay photograph from directly above on a white craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "caterpillar-paper-craft-finished.webp",
        "prompt": (
            "The completed caterpillar paper craft on a white cardstock background, photographed flat from above on a craft table. "
            "A hand-cut dark green paper leaf glued near the bottom-center of the cardstock. "
            "Six green construction paper body circles in slightly different shades of green, glued in a curving overlapping row across the leaf, "
            "each one decorated with a small marker dot or simple pattern in the middle. "
            "A slightly larger yellow paper circle as the head at one end, with two big googly eyes "
            "and a small smile drawn in black marker. Two short curled green pipe cleaner antennae stick up from the top of the head. "
            "A small yellow marker sun is drawn in the upper corner of the cardstock. "
            "The whole craft fills the frame edge to edge, warm natural daylight, charming and clearly child-made. "
            f"{STYLE}"
        ),
    },
]


def generate_image(client, prompt, output_path):
    from google.genai import types as genai_types
    from PIL import Image as PILImage
    full_prompt = f"{prompt} Aspect ratio: 4:3. Wide rectangular landscape orientation. Fill the entire frame, no borders, no padding."
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
