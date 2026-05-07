#!/usr/bin/env python3
"""Generate all images for paper-craft-banners.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-craft-banners"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood or white craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-craft-banners.webp",
        "prompt": (
            "A finished handmade paper craft banner hanging gently along a light cream wall above a cozy wooden mantel. "
            "Eight colorful triangle flags strung on natural cotton baker's twine: pink, yellow, mint green, "
            "sky blue, coral, and lavender cardstock triangles. Each flag is decorated with a simple painted or "
            "marker pattern of polka dots, stripes, hearts, or a single bold black letter, spelling a cheerful word. "
            "The banner droops in a gentle curve in the middle. "
            "Cardstock and a glue stick visible on a craft table below. Warm natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-banners-mom-child.webp",
        "prompt": (
            "An American mom in her early thirties sitting at a light wood craft table with her young child, "
            "around 5 years old, both smiling and starting a paper craft banner project together. "
            "On the table: stacks of pink, yellow, blue, and green construction paper, child-safe scissors, "
            "a glue stick, a single hole punch, and a spool of red and white baker's twine. "
            "A few triangle flags already cut out are visible. "
            "Soft warm natural light from a window. Casual, candid, family-friendly atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-banners-cut-triangles.webp",
        "prompt": (
            "A child's hands holding child-safe scissors and cutting matching triangle flags from colored "
            "construction paper on a light wood craft table. Several already-cut triangle flags lie in a small "
            "stack nearby in pink, yellow, mint green, and sky blue cardstock. Each triangle is roughly 5 inches "
            "wide at the top and 6 inches tall. A pencil and a clear ruler sit at the edge of the frame. "
            "Bright natural light, slightly imperfect handmade cuts. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-banners-decorate-flags.webp",
        "prompt": (
            "Six colorful triangle paper flags laid out flat on a light wood craft table being decorated. "
            "Each flag has different child-drawn marker patterns: black polka dots on a yellow flag, "
            "pink stripes on a white flag, small drawn hearts on a green flag, simple stars on a blue flag, "
            "zigzags on a coral flag, and a flower on a lavender flag. "
            "A small handful of broad line markers in many colors lies beside the flags. "
            "Charming child-made decorations, slightly uneven and imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-banners-add-letters.webp",
        "prompt": (
            "Six decorated triangle paper flags lined up in a row on a light wood craft table, each flag with "
            "one large bold black paper letter glued in the center, together spelling a simple cheerful word "
            "like HELLO or HAPPY. The letters are cut from black cardstock and clearly child-cut with slightly "
            "uneven edges. The triangle flags are pink, yellow, mint green, sky blue, coral, and lavender. "
            "A glue stick and small black paper scraps visible at the edge. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-banners-punch-holes.webp",
        "prompt": (
            "A child's hands using a small handheld single-hole punch to punch a hole near the top corner of a "
            "decorated triangle paper flag on a light wood craft table. The flag is sky blue cardstock with a "
            "bold black letter glued in the center. Several other decorated triangle flags lie in a tidy stack "
            "next to the work area, each already showing two small holes near the top corners. "
            "Tiny paper circle confetti scattered on the table. Cozy, focused craft moment. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-banners-thread-twine.webp",
        "prompt": (
            "A close-up of a child's small hand carefully threading a length of red and white baker's twine "
            "through the punched holes of a decorated triangle paper flag. Three other colorful triangle flags "
            "are already threaded along the same string, hanging in order. The flags are pink, yellow, "
            "mint green, and sky blue cardstock with simple marker patterns and bold black letters. "
            "On a light wood craft table. Warm natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-banners-space-flags.webp",
        "prompt": (
            "A finished paper craft banner laid flat across a light wood craft table, ready to be hung. "
            "Eight colorful triangle paper flags strung evenly along a length of red and white baker's twine, "
            "in pink, yellow, mint green, sky blue, coral, lavender, peach, and white cardstock. "
            "Each flag has a bold black letter and small marker decorations. "
            "Plenty of extra string left untied at each end of the banner. "
            "Soft natural daylight. Cute, neat, handmade arrangement. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-banners-hang-banner.webp",
        "prompt": (
            "A finished handmade paper craft banner hanging on a light cream wall in a cozy living room. "
            "Eight colorful triangle paper flags strung on red and white baker's twine, drooping gently in a "
            "soft curve in the middle, taped at each end above the wall. The flags are pink, yellow, mint green, "
            "sky blue, coral, lavender, peach, and white cardstock, each with a bold black letter and simple "
            "child-drawn marker patterns. A small wooden mantel or shelf with a few homey decor items below. "
            "Bright, joyful, family living room atmosphere. "
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
