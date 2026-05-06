#!/usr/bin/env python3
"""Generate all images for miniature-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "miniature-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White craft table surface. Clean, cozy, family-friendly atmosphere. "
    "Landscape orientation 4:3. No cartoon elements. Real construction paper materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "The image fills the entire frame edge to edge with no white borders or padding."
)

IMAGES = [
    {
        "filename": "miniature-paper-craft.webp",
        "prompt": (
            "A finished miniature paper craft of three tiny standing toadstool mushrooms in small, "
            "medium, and large sizes lined up side by side on a long green construction paper "
            "grass strip with snipped pointed grass blades along the top edge. Each mushroom has a "
            "bright red half-dome cap covered in five or six small white paint marker dots, and a "
            "rounded white construction paper stem with two tiny black dot eyes and a small curved "
            "smile drawn on. Each mushroom stands upright thanks to a small folded base tab under "
            "the stem glued to the green grass strip. Photographed slightly from above on a white "
            "craft table with a few small red and white paper scraps nearby. Clearly handmade by a "
            "young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "miniature-paper-craft-mom-child.webp",
        "prompt": (
            "A young American mom in a soft cream sweater sitting beside her four year old daughter "
            "with light brown hair at a bright white craft table, both looking happy and engaged. "
            "On the table in front of them: small stacks of red, white, and green construction "
            "paper sheets, blunt tip kid scissors with red handles, an open purple Elmer's glue "
            "stick, a fine white paint marker, a fine black marker, and a pencil. They are about "
            "to start a miniature paper craft project of tiny toadstool mushrooms. Warm natural "
            "daylight, cozy family atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "miniature-paper-craft-red-caps.webp",
        "prompt": (
            "Three tiny red construction paper mushroom cap dome shapes in three different sizes "
            "(small, medium, and large, each one a half-circle), freshly cut out by a child and "
            "lying side by side on a white craft table. The largest is about the size of a bottle "
            "cap. A pair of blunt tip kid scissors with red handles, a pencil, and small red paper "
            "scraps and a sheet of red construction paper sit nearby. Slightly wobbly handmade "
            "edges visible on each dome. Top-down flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "miniature-paper-craft-white-stems.webp",
        "prompt": (
            "Three small white construction paper mushroom stem shapes in short, medium, and tall "
            "heights, each one a narrow rectangle with gently rounded bottom corners, just cut out "
            "and lying in a row next to three previously cut tiny red mushroom cap dome shapes on "
            "a white craft table. Blunt tip kid scissors and small white paper scraps visible. "
            "Top-down flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "miniature-paper-craft-glued-shapes.webp",
        "prompt": (
            "Three tiny paper toadstool mushroom shapes assembled by gluing a red half-dome cap "
            "onto the very top of each white rectangular stem, in small, medium, and large sizes "
            "side by side. Each red cap slightly overhangs the white stem on each side, creating "
            "a chubby toadstool silhouette. Lying flat on a white craft table next to an open "
            "purple Elmer's glue stick. The red caps are still plain with no dots yet. Top-down "
            "flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "miniature-paper-craft-white-dots.webp",
        "prompt": (
            "Three tiny paper toadstool mushrooms with red half-dome caps freshly decorated with "
            "five or six small round white paint marker dots scattered across each red cap in a "
            "classic toadstool pattern. The white rectangular stems remain plain. Lying flat side "
            "by side in small, medium, and large sizes on a white craft table with an open white "
            "Sharpie oil-based paint marker beside them. Top-down flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "miniature-paper-craft-faces.webp",
        "prompt": (
            "Three tiny paper toadstool mushrooms with red dotted caps and white rectangular "
            "stems, each stem now decorated with two small black dot eyes and a tiny curved smile "
            "drawn near the top with a fine black marker. Lying flat side by side in small, "
            "medium, and large sizes on a white craft table with a fine black Sharpie marker "
            "beside them. The mushrooms look like cute little smiling friends. Top-down flat lay "
            "photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "miniature-paper-craft-standing.webp",
        "prompt": (
            "Three tiny paper toadstool mushrooms with red dotted caps and white smiling stems "
            "standing upright on a white craft table thanks to a small folded paper tab at the "
            "bottom of each stem bent backward at a ninety degree angle. The three mushrooms "
            "stand in a row in small, medium, and large sizes. Photographed at table eye level so "
            "the standing mushrooms are clearly visible from the side. Soft warm window light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "miniature-paper-craft-finished.webp",
        "prompt": (
            "A finished handmade miniature paper craft of three tiny toadstool mushrooms standing "
            "in a row on a long green construction paper grass strip with snipped pointed grass "
            "blades along the top edge, gently held up by small child hands at a craft table. "
            "Each mushroom has a bright red half-dome cap covered in white paint marker dots and "
            "a white rounded stem decorated with tiny black dot eyes and a small curved smile. "
            "The mushrooms are in small, medium, and large sizes. Warm afternoon light. Pride and "
            "joy in the moment. "
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
