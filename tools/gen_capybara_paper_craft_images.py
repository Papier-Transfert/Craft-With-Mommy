#!/usr/bin/env python3
"""Generate all images for capybara-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "capybara-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

CAPYBARA_DESC = (
    "a handmade paper capybara made from warm light-brown construction paper, with "
    "a chunky rounded oval body about 6 inches wide, a smaller rounded head shape "
    "attached to the front, two small rounded ears on top, four short stubby legs "
    "underneath, a tiny rounded tail, two small round black paper eyes, and a tiny "
    "black nose. The capybara has a soft friendly smile drawn with a black marker."
)

IMAGES = [
    {
        "filename": "capybara-paper-craft.webp",
        "prompt": (
            f"A finished {CAPYBARA_DESC} "
            "Photographed from above as a flat lay on a white craft table with a few brown "
            "and pink construction paper scraps beside it, a glue stick, and a pair of kids "
            "scissors. The capybara looks cute, friendly, and clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "capybara-paper-craft-mom-child.webp",
        "prompt": (
            "A warm photo of a young American mom and her four year old child sitting together "
            "at a light wood craft table, both smiling and excited. They are starting a paper "
            "capybara craft. On the table in front of them are sheets of warm light-brown, "
            "darker brown, pink, and black construction paper, a glue stick, kids safety "
            "scissors, and a few cut paper shapes. Soft natural window light. The mood is "
            "cheerful, calm, and full of connection. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "capybara-paper-craft-cut-body.webp",
        "prompt": (
            "Top-down photo on a craft table showing a sheet of warm light-brown construction "
            "paper. A child's hand holds red kids safety scissors and has just finished cutting "
            "out a chunky rounded oval body shape about 6 inches wide and 4 inches tall for the "
            "capybara body. The cut oval body and the leftover paper scraps are clearly visible. "
            "No head, ears, or legs yet, just the oval body. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "capybara-paper-craft-attach-head.webp",
        "prompt": (
            "Top-down photo on a light wood craft table. The chunky rounded oval brown body of "
            "a paper capybara is on the table. A smaller rounded brown paper head shape, about "
            "3 inches wide, has just been glued onto the front-left edge of the body so the "
            "capybara is shown in profile. The head slightly overlaps the body. A purple glue "
            "stick is open beside the craft. No ears, eyes, or legs yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "capybara-paper-craft-add-ears.webp",
        "prompt": (
            "Top-down photo of the same paper capybara in progress: chunky brown oval body with "
            "a smaller round brown head attached at the front. Two small rounded brown paper "
            "ears, each about 1 inch wide, have been glued to the top of the head. Each ear has "
            "a tiny pink construction paper inner-ear shape glued on top. No eyes, legs, or tail "
            "yet. A glue stick lies next to the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "capybara-paper-craft-add-legs.webp",
        "prompt": (
            "Top-down photo of the same paper capybara in progress: brown oval body with a round "
            "brown head, two small rounded ears with pink inner ears. Four short stubby brown "
            "paper leg shapes, each about 1 inch tall and 1 inch wide, have been glued under the "
            "bottom edge of the body. The legs are barely peeking out from under the body. No "
            "eyes, nose, tail, or face details yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "capybara-paper-craft-add-face.webp",
        "prompt": (
            "Top-down photo of the same paper capybara in progress on a craft table: brown oval "
            "body, round brown head with two small ears, four short stubby legs. Two small round "
            "black paper circles have been glued onto the head as the eyes, and a tiny black "
            "paper oval has been glued at the front tip of the head as the nose. Still no smile "
            "or tail. The craft is sitting flat on the wood table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "capybara-paper-craft-add-tail.webp",
        "prompt": (
            "Top-down photo of the paper capybara in progress: brown oval body, round brown head "
            "with ears, four legs, two black eyes, and a tiny black nose. A small rounded brown "
            "paper tail shape, about half an inch wide, has just been glued onto the back-right "
            "end of the body. The tail is small and short. The craft is on a light wood table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "capybara-paper-craft-decorate.webp",
        "prompt": (
            "Top-down photo of the nearly finished paper capybara. A child's hand holds a black "
            "fine-tip marker and is drawing a tiny soft smile under the nose, plus little "
            "whiskers and small toe lines on the legs. The capybara has its brown oval body, "
            "round head, ears with pink inner ears, four legs, two black eyes, a black nose, "
            "and a small tail. Markers and paper scraps are scattered around. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "capybara-paper-craft-finished.webp",
        "prompt": (
            "A cheerful child, about five years old, holding up the finished handmade paper "
            "capybara craft with both hands and smiling proudly at the camera. The capybara is "
            "a chunky brown oval body with a rounded head, two small ears with pink inner ears, "
            "four short legs, two black eyes, a tiny black nose, a soft marker smile, and a "
            "small tail. Bright joyful expression, soft warm living room background. "
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
