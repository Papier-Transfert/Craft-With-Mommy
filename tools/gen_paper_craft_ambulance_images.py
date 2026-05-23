#!/usr/bin/env python3
"""Generate all images for paper-craft-ambulance.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-craft-ambulance"
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
        "filename": "paper-craft-ambulance.webp",
        "prompt": (
            "A handmade paper ambulance craft fully assembled and lying flat on a white craft table. "
            "The ambulance body is a wide white construction paper rectangle for the back box with a smaller "
            "white square attached as the front cab. A small bright red paper cross is glued in the center of "
            "the back box and a long thin red paper stripe runs across the side just under the cross. "
            "A light blue paper windshield is on the front cab and a smaller light blue paper window on the "
            "back box. Two round black paper wheels with smaller grey paper hubcaps sit under the body. "
            "A small red rectangle and a small blue rectangle are glued side by side on top of the roof as "
            "siren lights. The ambulance sits on a long grey paper road strip with tiny yellow paper dashes "
            "down the middle. Clearly child-made with slightly uneven edges, soft pastel colors, scissors and "
            "a glue stick visible at the edge. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ambulance-mom-child.webp",
        "prompt": (
            "A warm photo of a young American mom in a cozy beige sweater sitting next to her smiling preschool "
            "aged child at a white wooden craft table. Spread out on the table in front of them are sheets of "
            "white, bright red, light blue, black, and yellow construction paper, a pair of small kid scissors "
            "with blue handles, a purple glue stick, a black marker, and a small bag of googly eyes. "
            "Both are looking at the paper with bright happy faces, clearly about to start making a paper ambulance "
            "craft together. Warm natural daylight from a side window. Cozy family-friendly atmosphere. "
            "Landscape 4:3. Realistic photo style. No cartoon elements."
        ),
    },
    {
        "filename": "paper-craft-ambulance-cut-body.webp",
        "prompt": (
            "A close-up flat lay photo of two freshly cut shapes of plain white construction paper resting on a "
            "white wooden craft table: one larger wide rectangle for the back box of an ambulance and one smaller "
            "square for the front cab, lying side by side so together they form one long ambulance silhouette. "
            "A pair of blue-handled kid scissors and a yellow pencil are placed neatly next to the shapes. "
            "Edges are slightly uneven, clearly cut by a child. Nothing else assembled yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ambulance-red-cross.webp",
        "prompt": (
            "A close-up flat lay photo showing the same simple white paper ambulance body from the previous step "
            "now with a small bright red paper cross glued in the center of the wider back rectangle and a long "
            "thin red paper stripe glued horizontally across the side just below the red cross. "
            "No windows yet, no wheels yet, no siren yet. A purple glue stick sits next to the paper. "
            "Slightly uneven child cut edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ambulance-windows.webp",
        "prompt": (
            "A close-up flat lay photo of the same simple white paper ambulance from the previous step (white "
            "rectangle back box plus a smaller white square cab, with a small red cross and a thin red stripe "
            "already on the side) now with two light blue construction paper windows added: a larger light blue "
            "rounded square as the windshield on the front cab and a smaller light blue square as a back window on "
            "the back box. Still no wheels yet, no siren yet. Clearly child made with slightly uneven edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ambulance-wheels.webp",
        "prompt": (
            "A close-up flat lay photo of the same paper ambulance from the previous step (white body with red "
            "cross, red stripe, light blue windshield, and light blue back window already in place) now with two "
            "round black construction paper wheels glued under the ambulance body, one near the front cab and one "
            "near the back, each black wheel showing a smaller round grey paper circle inside as the hubcap. "
            "The bottom of each black wheel peeks slightly below the body. No siren lights or face details yet. "
            "Slightly uneven child cut edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ambulance-siren-lights.webp",
        "prompt": (
            "A close-up flat lay photo of the same paper ambulance from the previous step (white body with red "
            "cross, red stripe, light blue windshield, light blue back window, two round black wheels with grey "
            "hubcaps) now with two small paper rectangles glued side by side on the top of the back box roof, "
            "one bright red and one bright blue, as the siren light bar. Two small googly eyes are stuck on the "
            "front of the cab as headlight eyes and a small black marker drawn smile is under the windshield, "
            "giving the ambulance a sweet little face. Slightly uneven child cut edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-craft-ambulance-road-scene.webp",
        "prompt": (
            "A finished handmade paper ambulance craft mounted onto a pale blue cardstock background. "
            "The ambulance has a white rectangle back box with a smaller white cab, a small red cross and a thin "
            "red stripe on the side, a light blue windshield and a smaller back window, two round black wheels "
            "with grey hubcaps, a small red and blue siren rectangle on the roof, two googly eye headlights, and "
            "a marker drawn smile. It is glued on top of a long grey paper road strip running across the cardstock, "
            "with several small bright yellow paper rectangles glued in a dashed line down the middle of the road. "
            "Tiny black marker drawn speed lines and a small puff of exhaust are behind the ambulance to suggest "
            "movement. Cheerful and clearly child made. "
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
