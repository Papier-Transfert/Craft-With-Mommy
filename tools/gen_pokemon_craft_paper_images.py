#!/usr/bin/env python3
"""Generate all images for pokemon-craft-paper.html (Pikachu-style)."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "pokemon-craft-paper"
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
        "filename": "pokemon-craft-paper.webp",
        "prompt": (
            "A finished handmade paper craft of a cute yellow cartoon mouse character "
            "sitting flat on a white craft table, photographed from directly above. "
            "The character is a round bright yellow construction paper face with two "
            "long pointed yellow ears standing tall above the head. The top third of "
            "each ear is colored solid black. Two small red paper circles are glued "
            "as cheeks on the lower half of the yellow face. Two small black googly "
            "eyes are stuck above the cheeks, with a tiny black marker triangle nose "
            "between them and a wide curved smiling mouth drawn below. A small zigzag "
            "yellow lightning-bolt-shaped paper tail sticks out behind the head. "
            "Cheerful, sweet, and clearly child-made. A few yellow paper scraps and a "
            "purple glue stick visible at the edges of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pokemon-craft-paper-mom-child.webp",
        "prompt": (
            "A warm natural photo of an American mom sitting at a light wood craft "
            "table with her young child of about 5 years old, both excited and ready "
            "to start making a yellow paper mouse character craft together. On the "
            "table in front of them: sheets of bright yellow and red construction "
            "paper, kid-safe scissors with rounded handles, a purple Elmer's glue "
            "stick, a packet of small black googly eyes, and a black marker. The "
            "mom is smiling warmly at the child, and the child is reaching for the "
            "yellow paper. Cozy, family-friendly home atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pokemon-craft-paper-yellow-head.webp",
        "prompt": (
            "A single large bright yellow construction paper circle, about the size "
            "of a small saucer, freshly cut out and lying flat on a white craft "
            "table. The circle has slightly imperfect edges that show it was cut by "
            "a child. Next to it: a small white bowl that was used to trace the "
            "circle, a pencil, and a pair of kid-safe scissors with rounded handles. "
            "A few small yellow paper scraps are scattered around the edges. "
            "Top-down photograph. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pokemon-craft-paper-ears-cut.webp",
        "prompt": (
            "A flat lay top-down photo on a white craft table. In the center is a "
            "single large bright yellow construction paper circle for a character "
            "face. To either side of the circle are two long, tall, pointed yellow "
            "construction paper ear shapes freshly cut, each about as long as a "
            "child's hand, with a slightly rounded base and a sharp pointed tip at "
            "the top. Nothing is glued yet, the ears are just laid out next to the "
            "head. A pair of kid-safe scissors and a glue stick rest beside them. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pokemon-craft-paper-black-ear-tips.webp",
        "prompt": (
            "A flat lay top-down photo on a white craft table. Two long pointed "
            "bright yellow construction paper ear shapes lying side by side. The top "
            "third of each yellow ear has been colored solid rich black with a "
            "marker, creating a clear contrast between the yellow base and the "
            "black tips. The black coloring is slightly imperfect, clearly done by "
            "a child. A black broad-line marker rests next to the ears, and a few "
            "yellow paper scraps are visible. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pokemon-craft-paper-ears-glued.webp",
        "prompt": (
            "A handmade paper craft on a white craft table, photographed from "
            "above. The bright yellow round construction paper face is now flipped "
            "right side up with two long pointed yellow ears glued behind it, "
            "standing tall above the top of the round head. The top third of each "
            "ear is solid black. The ears are angled slightly outward into a "
            "friendly V shape. The face is otherwise still completely plain bright "
            "yellow with no cheeks, eyes, or mouth yet, just the basic head and "
            "ears silhouette. A purple glue stick rests nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pokemon-craft-paper-red-cheeks.webp",
        "prompt": (
            "A handmade paper craft on a white craft table, photographed from "
            "above. The bright yellow round paper face has two long pointed yellow "
            "ears with black tips standing tall above it. Two small red paper "
            "circles, each about the size of a quarter, are now glued onto the "
            "lower half of the yellow face, one on each side, with a little space "
            "between them in the middle. No googly eyes or mouth yet, just the "
            "head, ears, and red cheeks. A scrap of red construction paper and a "
            "pair of kid-safe scissors rest next to the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pokemon-craft-paper-face-details.webp",
        "prompt": (
            "A handmade paper craft on a white craft table, photographed from "
            "above. The bright yellow round paper face has long pointed yellow "
            "ears with black tips standing above it and two small red paper cheek "
            "circles on the lower half of the face. The face now has two small "
            "black googly eyes stuck above the cheeks with a small space between "
            "them, a tiny black marker triangular nose drawn between the eyes, and "
            "a wide curved black marker smiling mouth drawn below the nose. "
            "Cheerful and sweet. A black marker rests next to the craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pokemon-craft-paper-finished.webp",
        "prompt": (
            "A finished handmade paper craft of a cute yellow cartoon mouse "
            "character proudly displayed on a white craft table, photographed "
            "slightly from the side at a low angle. The character is complete: "
            "round bright yellow construction paper face, two tall pointed yellow "
            "ears with solid black tips, two red paper cheek circles, two small "
            "black googly eyes, a small black marker triangular nose, a wide "
            "curved smiling mouth, and a yellow zigzag lightning-bolt-shaped paper "
            "tail glued behind the head sticking out to one side. Cheerful, sweet, "
            "and clearly child-made. "
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
