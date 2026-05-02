#!/usr/bin/env python3
"""Generate all images for paper-weave-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-weave-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-weave-craft.webp",
        "prompt": (
            "A finished handmade paper weave craft mat made from a dark blue construction paper loom "
            "with rainbow strips of red, orange, yellow, green, blue, and purple construction paper "
            "woven through it in a clear over and under pattern. The woven mat sits flat on a white craft table. "
            "The strips are about one inch wide and lie snug against each other. Charming, clearly child-made, "
            "slightly imperfect rectangular woven design. Bright cheerful colors. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-weave-craft-mom-child.webp",
        "prompt": (
            "A young American mom and her child around five years old sitting together at a light wood craft table, "
            "smiling and getting ready to make a paper weave craft. On the table in front of them are several sheets "
            "of bright construction paper in red, orange, yellow, green, blue, and dark blue, "
            "a pair of kid-safe scissors, a wooden ruler, and a pencil. Warm cozy family atmosphere. "
            "Both look happy and engaged. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-weave-craft-loom-base.webp",
        "prompt": (
            "A single sheet of dark blue construction paper folded in half on a white craft table, "
            "with a series of evenly spaced parallel pencil lines drawn straight across from the folded edge, "
            "stopping about an inch before the open edge. A wooden ruler and a pencil sit next to the paper. "
            "Clean overhead flat lay photo. The pencil marks are clearly visible but light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-weave-craft-cut-slits.webp",
        "prompt": (
            "A single sheet of dark blue construction paper unfolded flat on a white craft table, "
            "showing a row of evenly spaced vertical slits cut across the middle of the paper, "
            "framed by a one-inch border of solid dark blue paper at the top and bottom. "
            "The paper has been cut and unfolded to form a paper weaving loom. "
            "Kid-safe scissors lie next to it. Clean overhead flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-weave-craft-cut-strips.webp",
        "prompt": (
            "Several stacks of long one-inch-wide construction paper strips in red, orange, yellow, green, blue, "
            "and purple, neatly cut and arranged on a white craft table. About five strips of each color. "
            "A wooden ruler, pencil, and kid-safe scissors sit beside the strips. "
            "Bright cheerful rainbow colors. Clean overhead flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-weave-craft-first-strip.webp",
        "prompt": (
            "A child's small hands threading a single yellow construction paper strip through the slits of a "
            "dark blue paper weaving loom in an over and under pattern. The strip is partway through, "
            "showing the over and under sections clearly. The yellow strip is pushed up snug against the top of the loom. "
            "Other colorful strips wait on the table beside the loom. Clean overhead flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-weave-craft-second-strip.webp",
        "prompt": (
            "A dark blue paper weaving loom on a white craft table with two woven strips visible: "
            "a yellow construction paper strip woven over and under the slits at the top of the loom, "
            "and a red construction paper strip woven below it under and over the slits in the opposite pattern. "
            "Both strips sit snug against each other. A few more colorful strips wait beside the loom. "
            "Clean overhead flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-weave-craft-full-loom.webp",
        "prompt": (
            "A dark blue construction paper weaving loom completely filled with rainbow strips of "
            "red, orange, yellow, green, blue, and purple construction paper woven over and under in a clear pattern. "
            "All strips sit snug against each other with no visible gaps. The woven rectangle looks like a tiny handmade rug. "
            "Charming, clearly child-made. Lying flat on a white craft table. Clean overhead flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-weave-craft-finished.webp",
        "prompt": (
            "A finished paper weave craft mat with rainbow construction paper strips woven into a dark blue paper loom. "
            "The strip ends at the back have been trimmed flush with the loom edge and glued down so the front "
            "shows a clean rectangular woven design with neat edges. Sits proudly on a white craft table. "
            "Bright cheerful colors. A glue stick lies beside it. Clean overhead flat lay photo. "
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
