#!/usr/bin/env python3
"""Generate all images for ladybug-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "ladybug-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "ladybug-paper-craft.webp",
        "prompt": (
            "A finished handmade ladybug paper craft displayed flat on a light wood craft table. "
            "The ladybug has a large round red construction paper body about the size of a small saucer, "
            "a smaller black construction paper half-circle glued at the top as the head, "
            "a clean black marker line drawn straight down the center of the red body to divide the wings, "
            "six round black paper spots glued evenly across the red body (three on each side of the line), "
            "two large self-adhesive googly eyes pressed onto the black head, a tiny drawn smile between the eyes, "
            "and two short black pipe cleaner antennae with small curls at the tips poking out from the top of the head. "
            "Scissors, glue stick, and a few red and black paper scraps visible at the edges of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ladybug-paper-craft-mom-child.webp",
        "prompt": (
            "A warm photograph of an American mom in her thirties and her young child (about four years old) "
            "sitting side by side at a light wood craft table, both smiling and excited to start a ladybug paper craft. "
            "On the table in front of them: a sheet of bright red construction paper, a sheet of black construction paper, "
            "a glue stick, a pair of child-safe pointed-tip scissors, a small pile of self-adhesive googly eyes, "
            "and two short black pipe cleaners. No finished craft yet, just the materials laid out. "
            "Soft natural daylight, cozy living room atmosphere. The mom is gently looking at the child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ladybug-paper-craft-cut-body.webp",
        "prompt": (
            "Close-up of a child's small hands using child-safe scissors to cut out a large round circle "
            "from a sheet of bright red construction paper on a light wood craft table. "
            "A faint pencil line shows the circle outline, and a few red paper scraps are scattered next to the work. "
            "No finished ladybug yet, only the red body in progress, half cut out. "
            "The black construction paper sheet sits unused beside the work. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ladybug-paper-craft-attach-head.webp",
        "prompt": (
            "Close-up of a child's small hands pressing a small black construction paper half-circle onto the top "
            "of a fully cut large round red construction paper body, gluing it down with a glue stick. "
            "The flat edge of the black half-circle is lined up along the top curve of the red body. "
            "No spots yet, no eyes yet, no antennae yet, no wing line yet. Just the red round body and the black head. "
            "A glue stick rests on the light wood craft table beside the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ladybug-paper-craft-wing-line.webp",
        "prompt": (
            "Close-up of a ladybug paper craft in progress on a light wood craft table: "
            "a large round red construction paper body with a small black half-circle head glued at the top, "
            "and a freshly drawn straight black marker line running down the center of the red body from just under the head to the bottom edge. "
            "No spots yet, no googly eyes yet, no antennae yet. A black washable marker rests on the table beside the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ladybug-paper-craft-spots.webp",
        "prompt": (
            "Close-up of a child's small hands gluing small round black construction paper circles "
            "as spots onto the red round body of a ladybug paper craft. "
            "The craft already shows the small black half-circle head at the top and a clear black marker line down the center of the red body. "
            "Three black spots are already glued on one side of the wing line, and the child is pressing on another spot on the other side. "
            "A few extra black paper circle spots wait on the light wood craft table. "
            "No googly eyes yet and no pipe cleaner antennae yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ladybug-paper-craft-eyes-face.webp",
        "prompt": (
            "Close-up of a child's small hands pressing two large self-adhesive googly eyes onto the small black half-circle head "
            "of a ladybug paper craft. The craft already has a round red body with a clear black marker wing line down the center "
            "and six small black paper circle spots glued evenly across the red body. A small drawn smile is visible between the eyes. "
            "No pipe cleaner antennae yet. The light wood craft table holds a black marker and a strip of googly eye stickers nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "ladybug-paper-craft-finished.webp",
        "prompt": (
            "A fully finished handmade ladybug paper craft photographed on a light wood craft table from a slightly angled view. "
            "Round red construction paper body, small black half-circle head at the top, a clear black marker line down the center of the body, "
            "six round black paper spots evenly placed across the red body, two large googly eyes on the black head, "
            "a tiny drawn smile, and two short black pipe cleaner antennae with curled tips poking out from the top of the head. "
            "A glue stick, scissors, and a few black and red paper scraps are visible at the edges of the photo. "
            "Cheerful, sweet, clearly child-made spring craft. "
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
