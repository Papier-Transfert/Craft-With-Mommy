#!/usr/bin/env python3
"""Generate all images for paper-turtle-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-turtle-craft"
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
        "filename": "paper-turtle-craft.webp",
        "prompt": (
            "A finished handmade paper turtle craft sitting flat on a white craft table, "
            "photographed from directly above. The turtle has a large round bright green "
            "construction paper shell decorated with about ten small dark green hexagon "
            "spots glued in a honeycomb pattern. A small green oval head peeks out at the "
            "top with two small googly eyes and a tiny black marker smile. Four short "
            "rectangular green legs poke out from the sides at four-and-eight, two-and-ten "
            "clock positions. A tiny green triangle tail at the bottom. Cheerful, sweet, "
            "and clearly child-made. Construction paper scraps and a glue stick visible at "
            "the edges of the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-turtle-craft-mom-child.webp",
        "prompt": (
            "A warm natural photo of an American mom sitting at a light wood craft table "
            "with her young child of about 4 years old, both excited and ready to start "
            "making a paper turtle craft together. On the table in front of them: sheets "
            "of bright green and dark green construction paper, kid-safe scissors with "
            "rounded handles, a purple Elmer's glue stick, a small bowl for tracing "
            "circles, a packet of googly eyes, and a black marker. The mom is smiling "
            "warmly at the child, and the child is reaching for the green paper. Cozy, "
            "family-friendly home atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-turtle-craft-shell-circle.webp",
        "prompt": (
            "A single large bright green construction paper circle, about the size of a "
            "small saucer, freshly cut out and lying flat on a white craft table. The "
            "circle has slightly imperfect edges that show it was cut by a child. Next "
            "to it: a small white bowl that was used to trace the circle, a pencil, and "
            "a pair of kid-safe scissors with rounded handles. A few small green paper "
            "scraps are scattered around the edges. Top-down photograph. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-turtle-craft-cut-body-parts.webp",
        "prompt": (
            "A flat lay top-down photo on a white craft table. In the center is a single "
            "large bright green construction paper circle for the turtle shell. Around it "
            "are five smaller bright green construction paper pieces freshly cut: one "
            "small oval the size of a walnut for the head placed at the top of the circle, "
            "four short rectangular shapes with rounded ends placed at the sides like four "
            "little legs, and one tiny green triangle placed at the bottom for the tail. "
            "Nothing is glued yet, the pieces are just laid out around the shell. "
            "A pair of kid-safe scissors and a glue stick rest beside them. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-turtle-craft-assembled-body.webp",
        "prompt": (
            "A handmade paper turtle craft on a white craft table, photographed from "
            "above. The bright green round construction paper shell is now complete with "
            "the head, four legs, and a tail glued behind it so they peek out around the "
            "edges. The head is at the top, the tail is at the bottom, and the four legs "
            "are at four-and-eight, two-and-ten clock positions. The shell is still "
            "completely plain bright green with no hexagon decoration yet. No googly eyes "
            "or smile yet either, just the basic turtle silhouette taking shape. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-turtle-craft-cut-hexagons.webp",
        "prompt": (
            "A flat lay top-down photo of a small loose pile of about ten freshly cut "
            "dark green construction paper hexagons, each roughly the size of a quarter, "
            "scattered on a white craft table. The hexagons are slightly imperfect and "
            "wonky, clearly cut by a child. A pair of kid-safe scissors with rounded "
            "handles and a sheet of dark green construction paper with hexagon-shaped "
            "holes cut out of it sit next to the pile. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-turtle-craft-shell-pattern.webp",
        "prompt": (
            "A handmade paper turtle craft on a white craft table, photographed from "
            "above. The bright green round shell now has about ten small dark green "
            "hexagon paper shapes glued onto it in a honeycomb pattern, with a little "
            "space between each piece so the bright green base shows through. The head, "
            "four legs, and tail are still in place behind the shell. No googly eyes or "
            "smile yet. The hexagon spots are slightly wonky and clearly placed by a "
            "child. A purple glue stick is visible nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-turtle-craft-face-details.webp",
        "prompt": (
            "A handmade paper turtle craft on a white craft table, photographed from "
            "above. The bright green round shell is decorated with dark green hexagon "
            "spots in a honeycomb pattern. The small green oval head at the top now has "
            "two small googly eyes stuck onto it and a tiny curved black marker smile "
            "drawn underneath. The face looks cheerful and sweet. Four green legs and a "
            "tail still peek out around the shell. A black marker rests next to the "
            "turtle. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-turtle-craft-finished.webp",
        "prompt": (
            "A finished handmade paper turtle craft proudly displayed on a white craft "
            "table, photographed slightly from the side at a low angle. The turtle is "
            "complete: bright green round construction paper shell decorated with about "
            "ten dark green hexagon spots glued in a honeycomb pattern, a small green "
            "oval head with two googly eyes and a small black marker smile, four short "
            "green rectangular legs poking out from the sides, and a tiny green triangle "
            "tail at the back. The turtle sits on a small blue construction paper pond "
            "shape for display. Cheerful, sweet, and clearly child-made. "
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
