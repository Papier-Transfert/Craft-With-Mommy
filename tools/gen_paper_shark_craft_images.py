#!/usr/bin/env python3
"""Generate all images for paper-shark-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-shark-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-shark-craft.webp",
        "prompt": (
            "A finished handmade paper shark craft lying flat on a light wood craft table. "
            "The shark body is cut from bright blue cardstock in a long horizontal shape "
            "about eight inches long with a pointed snout on the left and a pointed tail on the right. "
            "A curved white cardstock belly piece is glued along the lower half of the body. "
            "A narrow zigzag strip of white paper teeth is glued across the front of the face like a wide grin, "
            "with small triangle points facing outward. A tall triangular blue dorsal fin is glued on top of the body, "
            "and two smaller blue triangular side fins are glued on the lower body. "
            "One large round googly eye is stuck near the front of the head, above the teeth. "
            "Three small curved black gill lines are drawn behind the eye. "
            "Cheerful, charming, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-shark-craft-mom-child.webp",
        "prompt": (
            "A warm, realistic photo of a young American mom and her four or five year old child sitting "
            "together at a light wood craft table, just starting to make a paper shark craft. "
            "On the table in front of them: a sheet of bright blue cardstock, a sheet of bright white cardstock, "
            "small blue-handled kid scissors, a purple glue stick, a packet of googly eyes, a black fine point marker, "
            "and a pencil. Both are smiling and looking down at the supplies, ready to begin. "
            "No shark cutouts yet, only the raw materials laid out. Cozy family-friendly summer atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-shark-craft-cut-body.webp",
        "prompt": (
            "A child's hands using small blue-handled kid scissors to cut a long horizontal shark body shape "
            "out of a sheet of bright blue cardstock. The shape is about eight inches long with a small pointed snout "
            "on one end and a pointed tail on the other. A faint pencil outline is partly visible along the edge. "
            "The cut is partway done, showing one finished curve. Light wood craft table in the background. "
            "No fins, no belly, no teeth visible yet, just the plain blue shark body being cut out. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-shark-craft-cut-belly-teeth.webp",
        "prompt": (
            "Close-up flat lay on a light wood craft table. To the left, a long blue cardstock shark body "
            "shape already cut out, lying horizontally with the snout on the left and tail on the right. "
            "To the right, a long curved white cardstock belly piece freshly cut, and a narrow strip of white paper "
            "with a row of small triangle zigzags snipped along one edge to look like shark teeth. "
            "Small blue-handled kid scissors lie next to the white pieces. No fins, no glue, no eye yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-shark-craft-cut-fins.webp",
        "prompt": (
            "Flat lay on a light wood craft table showing a plain blue cardstock shark body shape lying horizontally "
            "with the snout on the left and pointed tail on the right. Next to the body, three triangular blue cardstock "
            "fins are arranged: one tall pointed dorsal fin and two smaller side fin triangles. "
            "Small blue cardstock scraps from the cutting are visible around the edges. "
            "The white belly piece and zigzag white teeth strip from the previous step are also lying nearby but not glued on yet. "
            "No googly eye, no marker lines, no glue applied yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-shark-craft-glue-parts.webp",
        "prompt": (
            "A child's hands pressing a tall triangular blue dorsal fin onto the top of a blue cardstock shark body. "
            "The white curved belly piece is already glued along the lower half of the body, and the zigzag white paper "
            "teeth strip is already glued across the front of the face with the points facing outward. "
            "Two small blue side fin triangles are glued onto the lower body. No googly eye yet and no marker gill lines yet. "
            "An open purple glue stick lies beside the craft. Lying flat on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-shark-craft-add-eye.webp",
        "prompt": (
            "A close-up of a child's small hands placing one large round googly eye onto the front of a finished "
            "blue paper shark body. The shark already has a white belly piece, a row of zigzag white paper teeth, "
            "a tall triangular dorsal fin on top, and two side fins. A black fine point marker lies nearby, "
            "and three small curved black gill lines are visible just behind where the eye is being placed. "
            "Lying flat on a light wood craft table. Charming handmade quality. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-shark-craft-finished-display.webp",
        "prompt": (
            "A finished handmade blue paper shark craft taped to the front of a white refrigerator door at child height. "
            "The shark has a curved white belly piece, a row of zigzag white paper teeth, a tall triangular blue "
            "dorsal fin, two side fins, one large googly eye, and three small curved black gill lines drawn behind the eye. "
            "Next to it on the fridge is a child's marker drawing of a blue ocean scene with simple wavy lines and fish. "
            "Warm kitchen light, cheerful family-friendly mood. "
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
