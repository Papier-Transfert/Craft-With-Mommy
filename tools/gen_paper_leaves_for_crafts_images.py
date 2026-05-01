#!/usr/bin/env python3
"""Generate all images for paper-leaves-for-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-leaves-for-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-leaves-for-crafts.webp",
        "prompt": (
            "A beautiful flat lay collection of about a dozen handmade paper leaves "
            "in autumn colors arranged on a light wood craft table. The leaves are made "
            "from red, orange, yellow, brown, and deep green construction paper. "
            "Each leaf has a soft center fold crease, hand-drawn black branching veins, "
            "and gently curled edges. The leaves are different shapes (pointed oval, "
            "five-lobed maple, wavy oak) and slightly different sizes. Scissors, a pencil, "
            "a black marker, and a few paper scraps visible at the edges. "
            "Cozy autumn mood, clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-leaves-for-crafts-mom-child.webp",
        "prompt": (
            "A warm photo of a young mom and her young child (around 5 years old) sitting "
            "side by side at a craft table, smiling and excited to start a paper leaves craft. "
            "On the table in front of them: a small stack of red, orange, yellow, brown, "
            "and green construction paper, a pair of kids scissors, a pencil, a black marker, "
            "and a glue stick. They are looking down at the paper supplies, happy and engaged. "
            "Cozy home atmosphere, soft natural light from a window. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-leaves-for-crafts-choose-colors.webp",
        "prompt": (
            "A neat overhead shot of a small stack of construction paper sheets in autumn "
            "colors fanned out on a light wood craft table: one red sheet, one orange, "
            "one yellow, one brown, and one deep mossy green. A pair of kids scissors and "
            "a sharpened pencil sit beside the stack. No leaves cut yet, just the fresh "
            "supplies waiting to be used. Clean, calm, and inviting composition. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-leaves-for-crafts-templates.webp",
        "prompt": (
            "A flat lay of three handmade leaf templates cut from off-white cardstock, "
            "lying on a light wood craft table. The templates are: one simple pointed oval "
            "leaf shape, one five-lobed maple leaf shape, and one wavy oak leaf shape. "
            "Each template is around four inches tall. Pencil lines from the original "
            "drawing are slightly visible. A pencil and a small pair of scissors rest next "
            "to them. Clearly hand-drawn and child-friendly. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-leaves-for-crafts-trace-cut.webp",
        "prompt": (
            "Close-up overhead shot of a child's hands tracing around a cardstock leaf "
            "template onto a sheet of orange construction paper with a sharpened pencil. "
            "Beside the orange sheet, three already-cut paper leaves in red, yellow, and "
            "brown are arranged on the wood craft table. A pair of kids scissors lies "
            "open nearby. Process clearly visible, warm and homey. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-leaves-for-crafts-fold-vein.webp",
        "prompt": (
            "Close-up of a child's small fingers folding a single red paper leaf in half "
            "down the middle, with the two pointed ends meeting, to create a soft center "
            "crease. The leaf is being folded gently on a light wood craft table. Around it, "
            "two or three other already-cut paper leaves in orange and yellow lie flat, "
            "waiting for their crease. A pencil rests to one side. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-leaves-for-crafts-draw-veins.webp",
        "prompt": (
            "Close-up overhead shot of a child carefully drawing branching black veins "
            "with a fine black marker onto a yellow paper leaf that has a clear soft fold "
            "down the middle. The main vein runs along the fold line, and four smaller "
            "diagonal veins branch out toward the edges. A few finished leaves with veins "
            "in red and orange lie nearby on the wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-leaves-for-crafts-finished.webp",
        "prompt": (
            "A finished collection of about ten handmade paper leaves spread artfully on "
            "a light wood craft table. The leaves are in autumn colors (red, orange, yellow, "
            "brown), each with hand-drawn black branching veins and gently curled edges that "
            "make them look like they just fell from a tree. They overlap softly in a loose "
            "pile, with a few pieces of jute twine winding through. The composition is warm, "
            "cozy, and ready for a fall craft project. "
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
