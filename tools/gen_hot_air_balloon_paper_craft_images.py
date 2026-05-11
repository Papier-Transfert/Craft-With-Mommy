#!/usr/bin/env python3
"""Generate all images for hot-air-balloon-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "hot-air-balloon-paper-craft"
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

BALLOON_DESC = (
    "a handmade flat paper hot air balloon craft on a light blue cardstock sky "
    "background. The balloon is a large rounded teardrop shape covered in horizontal "
    "rainbow stripes of red, orange, yellow, green, blue, and purple construction "
    "paper. A small brown construction paper rectangle hangs below the balloon as a "
    "tiny basket with pencil lines drawn on it to look woven. Two short pieces of "
    "beige yarn connect the bottom of the balloon to the top of the basket as ropes. "
    "Three or four small rounded white paper clouds are glued around the balloon. "
    "A black marker has drawn a cheerful smiling face on the balloon and tiny waving "
    "passengers in the basket."
)

IMAGES = [
    {
        "filename": "hot-air-balloon-paper-craft.webp",
        "prompt": (
            f"A finished {BALLOON_DESC} "
            "Photographed from above as a flat lay on a white craft table with a few "
            "colorful construction paper scraps, a glue stick, and a pair of red kids "
            "scissors beside it. The hot air balloon craft looks cute, friendly, and "
            "clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "hot-air-balloon-paper-craft-mom-child.webp",
        "prompt": (
            "A warm photo of a young American mom and her four year old child sitting "
            "together at a light wood craft table, both smiling and excited. They are "
            "starting a hot air balloon paper craft. On the table in front of them are "
            "sheets of bright red, orange, yellow, green, blue, purple, brown, and light "
            "blue construction paper, a glue stick, red kids safety scissors, a small "
            "ball of beige yarn, and a black marker. Soft natural window light. The mood "
            "is cheerful, calm, and full of connection. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "hot-air-balloon-paper-craft-cut-balloon.webp",
        "prompt": (
            "Top-down photo on a light wood craft table showing a sheet of cardstock. A "
            "child's hand holds red kids safety scissors and has just finished cutting "
            "out a large rounded balloon shape about 7 inches tall and 6 inches wide. "
            "The shape looks like a soft upside-down teardrop with a flat bottom. The "
            "cut balloon shape and the leftover cardstock scraps are clearly visible. "
            "No stripes, basket, ropes, or clouds yet, just the plain cut balloon shape. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "hot-air-balloon-paper-craft-rainbow-stripes.webp",
        "prompt": (
            "Top-down photo on a light wood craft table. A large rounded teardrop "
            "balloon shape from cardstock is now covered in horizontal rainbow stripes "
            "of red, orange, yellow, green, blue, and purple construction paper, glued "
            "across the balloon from top to bottom in rainbow order. The stripes follow "
            "the rounded shape and the extra paper has been trimmed off at the edges. A "
            "purple glue stick is open beside the craft. No basket, ropes, or clouds "
            "yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "hot-air-balloon-paper-craft-cut-basket.webp",
        "prompt": (
            "Top-down photo on a light wood craft table showing a small brown "
            "construction paper rectangle, about 2.5 inches wide and 2 inches tall. "
            "Light pencil or brown marker horizontal and vertical lines have been drawn "
            "across the rectangle to make it look like a woven wicker basket. The "
            "rainbow striped balloon shape from the previous step is visible nearby on "
            "the table but not yet attached to anything. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "hot-air-balloon-paper-craft-glue-on-sky.webp",
        "prompt": (
            "Top-down photo of a light blue cardstock sky background sheet on a craft "
            "table. The rainbow striped paper balloon has been glued near the top "
            "center of the blue sheet. The small brown basket rectangle with woven "
            "pencil lines is glued about 2 inches below the balloon, centered "
            "underneath, with a clear gap between them. No yarn ropes yet and no clouds "
            "yet. The craft is sitting flat on the table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "hot-air-balloon-paper-craft-add-yarn-ropes.webp",
        "prompt": (
            "Top-down photo of the hot air balloon paper craft in progress on a light "
            "blue cardstock sky background. The rainbow striped balloon is at the top "
            "and the small brown woven basket is centered below it. Two short pieces of "
            "beige or natural yarn, each about 3 inches long, are now threaded through "
            "small punched holes connecting the bottom of the balloon to the top of the "
            "basket as ropes. No clouds or face details yet. A blue hole punch and yarn "
            "spool are visible beside the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "hot-air-balloon-paper-craft-add-clouds.webp",
        "prompt": (
            "Top-down photo of the hot air balloon paper craft on a light blue "
            "cardstock sky background. The rainbow striped balloon is connected to a "
            "small brown basket below by two beige yarn ropes. Three or four small "
            "rounded white construction paper cloud shapes with soft bumpy edges have "
            "now been glued around the balloon on the blue sky background. The balloon "
            "is still clearly in the center. No smiling face or passenger details yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "hot-air-balloon-paper-craft-final-details.webp",
        "prompt": (
            "Top-down photo of the nearly finished hot air balloon paper craft on a "
            "light blue cardstock sky background. A child's hand holds a black "
            "fine-tip marker and is drawing a cheerful smiling face on the rainbow "
            "balloon and two tiny waving passenger figures peeking out of the brown "
            "basket. The balloon has rainbow stripes, the basket has woven pencil "
            "lines, beige yarn ropes connect them, and several white paper clouds are "
            "glued around the balloon. The mood is warm and creative. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "hot-air-balloon-paper-craft-finished.webp",
        "prompt": (
            "A cheerful child, about five years old, holding up the finished handmade "
            "hot air balloon paper craft with both hands and smiling proudly at the "
            "camera. The craft shows a rainbow striped paper balloon at the top "
            "connected by short beige yarn ropes to a small brown woven basket below, "
            "with several white paper clouds glued around it on a light blue sky "
            "background. A smiling face is drawn on the balloon and tiny waving "
            "passengers peek out of the basket. Bright joyful expression, soft warm "
            "living room background. "
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
