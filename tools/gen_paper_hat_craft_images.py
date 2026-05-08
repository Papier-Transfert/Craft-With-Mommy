#!/usr/bin/env python3
"""Generate all images for paper-hat-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-hat-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-hat-craft.webp",
        "prompt": (
            "A finished handmade paper cone party hat made from bright pink cardstock, "
            "decorated with horizontal washi tape stripes in turquoise, yellow, and white, "
            "small star stickers, and a fluffy yellow pom pom glued at the top point. "
            "A thin white elastic chin cord runs from one side to the other through "
            "two small punched holes near the bottom rim. The hat sits upright on a "
            "light wood craft table next to a few washi tape rolls and a glue stick. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-hat-craft-mom-child.webp",
        "prompt": (
            "A young American mother with shoulder length brown hair sitting at a light "
            "wood craft table next to her cheerful 5 year old child, both smiling and "
            "starting a paper hat craft. On the table are a sheet of bright pink "
            "cardstock half circle, a roll of turquoise washi tape, a green roll of "
            "washi tape, a small stack of star stickers, blunt-tip kid scissors, and "
            "a glue stick. Warm natural light from a window. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-hat-craft-cut-half-circle.webp",
        "prompt": (
            "A child's small hand using blunt-tip kid scissors to cut along a straight "
            "pencil line across a large bright pink cardstock circle, separating it into "
            "two half circles. A round white dinner plate sits next to the paper as the "
            "tracing guide that was used to draw the circle. A pencil rests on the table. "
            "Light wood craft table surface. The half circle clearly visible, ready to "
            "become a paper cone party hat. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-hat-craft-decorate-flat.webp",
        "prompt": (
            "A flat bright pink cardstock half circle laid on a light wood craft table, "
            "decorated with several horizontal washi tape stripes in turquoise, yellow, "
            "and white, scattered small yellow and silver star stickers, and a few "
            "drawn marker dots in blue and green. The half circle is not yet rolled, "
            "still completely flat. Markers, washi tape rolls, and a sheet of stickers "
            "lie next to it. Cheerful and slightly imperfect, clearly child-decorated. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-hat-craft-roll-cone.webp",
        "prompt": (
            "Two adult hands rolling a decorated bright pink cardstock half circle into "
            "a tall pointed cone shape on a light wood craft table. The cardstock has "
            "horizontal washi tape stripes in turquoise, yellow, and white, plus small "
            "star stickers visible on the curved outside surface. The two straight edges "
            "of the half circle overlap by about an inch along a clear vertical seam. "
            "The point of the cone is at the top. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-hat-craft-staple-seam.webp",
        "prompt": (
            "A small black mini stapler being pressed against the vertical seam of a tall "
            "bright pink cone shaped paper hat to fasten the overlap. The cone hat stands "
            "upright on a light wood craft table. The hat is decorated with horizontal "
            "washi tape stripes in turquoise, yellow, and white, plus small star stickers. "
            "The seam is clearly visible. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-hat-craft-add-string.webp",
        "prompt": (
            "A bright pink cone shaped paper party hat standing upright on a light wood "
            "craft table, with two small holes punched at the bottom rim on opposite sides. "
            "A thin white elastic cord is threaded through both holes from one side of the "
            "cone to the other to form a chin strap, with small visible knots inside. The "
            "hat is decorated with horizontal washi tape stripes in turquoise, yellow, "
            "and white, plus small star stickers. A hole punch lies on the table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-hat-craft-pom-pom.webp",
        "prompt": (
            "A close up view of a fluffy yellow pom pom being glued onto the very top "
            "point of a tall bright pink paper cone party hat resting on a light wood "
            "craft table. A small dab of clear glue is visible at the contact point. "
            "The hat is decorated with horizontal washi tape stripes in turquoise, yellow, "
            "and white, plus small star stickers. The chin strap of thin white elastic "
            "cord is visible at the bottom. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-hat-craft-finished.webp",
        "prompt": (
            "A cheerful 5 year old child wearing a finished bright pink cone shaped paper "
            "party hat with horizontal washi tape stripes in turquoise, yellow, and white, "
            "small star stickers on the front, a fluffy yellow pom pom at the top point, "
            "and a thin white elastic chin strap holding the hat in place. The child is "
            "smiling brightly and sitting at a light wood craft table in a cozy room "
            "with warm natural light from a window. "
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
