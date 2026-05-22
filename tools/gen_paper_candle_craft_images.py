#!/usr/bin/env python3
"""Generate all images for paper-candle-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-candle-craft"
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
    "Fill the full frame edge to edge, no white borders or padding."
)

IMAGES = [
    {
        "filename": "paper-candle-craft.webp",
        "prompt": (
            "A finished handmade paper candle craft standing upright on a light wood craft table. "
            "The candle body is an empty toilet paper roll completely wrapped in deep red construction paper. "
            "A wavy white construction paper drip strip is glued around the top edge, with soft round bumps "
            "and dips hanging over the rim like melted wax. A tall teardrop yellow construction paper flame "
            "rises from inside the top of the candle, with a smaller orange construction paper teardrop flame "
            "glued and centered on top of it, leaving a halo of yellow showing around the orange. "
            "Soft warm natural daylight, a few paper scraps and a glue stick visible at the edges of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-candle-craft-why-kids-love.webp",
        "prompt": (
            "A warm cozy scene of an American mom in her early thirties sitting at a light wood craft table "
            "next to her smiling young child around age 4. On the table in front of them are an empty toilet paper roll, "
            "sheets of red, white, yellow, and orange construction paper, a pair of blunt-tip kid scissors, "
            "and a purple glue stick. The mom is showing the toilet paper roll to the child, both looking happy "
            "and engaged, about to start a paper candle craft together. "
            "Soft natural daylight from a side window, cozy family kitchen atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-candle-craft-wrap-body.webp",
        "prompt": (
            "Close-up of a young child's small hands wrapping a sheet of deep red construction paper around "
            "an empty cardboard toilet paper roll on a light wood craft table. The paper is partially rolled "
            "around the tube, with a purple Elmer's glue stick lying open next to it ready to seal the seam. "
            "A pair of blunt-tip kid scissors and a few extra colored construction paper sheets sit nearby. "
            "The action is mid-wrap, showing the red paper curving around the tube. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-candle-craft-cut-drips.webp",
        "prompt": (
            "Flat lay on a light wood craft table showing a long white construction paper strip about one and a half "
            "inches wide, with a wavy bumpy snipped edge along the top that looks like melted candle wax drips. "
            "Each bump along the wavy edge is slightly different in shape and clearly child-cut. "
            "Next to the white drip strip on the table sits the previously made red wrapped paper candle body "
            "(an empty toilet paper roll covered in deep red construction paper), a pair of blunt-tip kid scissors, "
            "and a few small white paper scraps from the cutting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-candle-craft-glue-drips.webp",
        "prompt": (
            "A handmade paper candle craft in progress on a light wood craft table. The candle body is an empty "
            "toilet paper roll wrapped in deep red construction paper, standing upright. A white construction paper "
            "drip strip with a wavy bumpy top edge is now glued all the way around the top of the candle, with the "
            "wavy edge pointing upward and slightly hanging over the rim like melted wax dripping down. "
            "The candle does not yet have a flame on top. A purple glue stick lies open next to the candle. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-candle-craft-cut-flames.webp",
        "prompt": (
            "Flat lay close-up on a light wood craft table showing two teardrop shaped construction paper flames "
            "laid side by side: one large teardrop cut from bright yellow construction paper, about two fingers tall, "
            "and one smaller teardrop cut from bright orange construction paper, about two thirds the size of the yellow one. "
            "Both flame shapes are clearly cut by a child with slightly uneven edges. A pencil and a pair of blunt-tip kid "
            "scissors sit next to the flames along with a few small yellow and orange paper scraps. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-candle-craft-layered-flame.webp",
        "prompt": (
            "Close-up flat lay on a light wood craft table showing a layered paper candle flame: a large bright yellow "
            "teardrop shape cut from construction paper, with a smaller bright orange teardrop construction paper shape "
            "glued and centered on top of it, sitting a little above the bottom edge so a halo of yellow still shows "
            "all around the orange. The two-tone flame looks warm and glowy. A small dot of dried glue is visible "
            "between the layers. A purple glue stick lies open nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-candle-craft-finished.webp",
        "prompt": (
            "A completed handmade paper candle craft standing tall on a light wood craft table. The candle body is "
            "an empty toilet paper roll fully wrapped in deep red construction paper. A wavy white paper drip strip "
            "is glued around the top edge, hanging slightly over the rim like dripping melted wax. A tall two-tone "
            "teardrop flame rises straight up from inside the top of the candle: a large yellow construction paper "
            "teardrop with a smaller centered orange teardrop layered on top. The flame stands proud and slightly "
            "tilted, clearly child-made. A few colorful paper scraps and a glue stick rest near the base of the candle. "
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
