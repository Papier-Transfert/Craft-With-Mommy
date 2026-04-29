#!/usr/bin/env python3
"""Generate all images for owl-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "owl-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper craft only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

OWL_DESCRIPTION = (
    "The owl is built from flat construction paper layered shapes: "
    "a tall rounded brown body with two small pointed ear tufts at the top, "
    "a smaller cream oval glued onto the front as a tummy panel, "
    "two large white circle eyes with black paper pupils, a small orange triangle beak, "
    "two brown teardrop wings glued on each side curving inward, "
    "three rows of cream scalloped feather strips overlapping across the tummy, "
    "and two small orange feet at the bottom."
)

IMAGES = [
    {
        "filename": "owl-paper-craft.webp",
        "prompt": (
            "A finished handmade owl paper craft lying flat on a white craft table. "
            f"{OWL_DESCRIPTION} "
            "A few brown, cream, white, and orange paper scraps and a glue stick visible at the edges. "
            "The owl looks friendly, cozy, and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "owl-paper-craft-why-kids-love.webp",
        "prompt": (
            "A warm photo of an American mom in her early thirties and her young child (around four years old) "
            "sitting together at a light wood craft table. "
            "Brown, cream, white, black, and orange construction paper sheets, "
            "blunt-tip kids scissors, and a purple glue stick are spread on the table in front of them. "
            "They are smiling and starting to make an owl paper craft together. "
            "The mom is gently helping the child arrange paper shapes. "
            "No finished owl yet, just supplies. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "owl-paper-craft-body-shape.webp",
        "prompt": (
            "Step 1 of a paper owl craft tutorial. A tall rounded brown construction paper body shape "
            "that looks like a soft egg, with two small pointed ear tufts at the top, just cut out and "
            "lying flat on a white craft table. A pencil and a pair of blunt-tip kids scissors lie next "
            "to the brown body. Brown paper scraps around the edges. No other owl features yet, "
            "just the plain brown body shape. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "owl-paper-craft-belly-panel.webp",
        "prompt": (
            "Step 2 of a paper owl craft tutorial. The same brown construction paper owl body shape "
            "(tall rounded shape with two pointed ear tufts at the top) now has a smaller cream oval "
            "glued onto the front as a tummy panel, leaving a brown border all the way around. "
            "No eyes, no beak, no wings, no feet yet. Lying flat on a white craft table. "
            "A glue stick lies nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "owl-paper-craft-eye-circles.webp",
        "prompt": (
            "Step 3 of a paper owl craft tutorial. The brown construction paper owl body with cream "
            "tummy panel now has two large plain white paper circle eyes glued side by side near the "
            "top of the body, just below the ear tufts, slightly overlapping the cream tummy panel. "
            "The white circles do not have pupils yet. No beak, no wings, no feet yet. "
            "Lying flat on a white craft table next to a pair of blunt-tip kids scissors. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "owl-paper-craft-pupils-beak.webp",
        "prompt": (
            "Step 4 of a paper owl craft tutorial. The brown construction paper owl body with cream "
            "tummy panel and two large white eye circles now has small black paper pupils glued in "
            "the center of each white eye, plus a small orange triangle beak glued between and slightly "
            "below the eyes pointing downward. Still no wings, no feet, no chest feathers. "
            "Lying flat on a white craft table. The owl now has a clear face and personality. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "owl-paper-craft-side-wings.webp",
        "prompt": (
            "Step 5 of a paper owl craft tutorial. The brown construction paper owl with cream tummy "
            "panel, two big white eyes with black pupils, and an orange triangle beak now also has "
            "two brown teardrop-shaped wings glued along the sides of the body, curving gently inward "
            "and slightly overlapping the cream tummy panel. The wings sit slightly below the eye "
            "level. Still no chest feathers or feet yet. Lying flat on a white craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "owl-paper-craft-feather-scallops.webp",
        "prompt": (
            "Step 6 of a paper owl craft tutorial. The brown construction paper owl with white eyes, "
            "black pupils, orange triangle beak, and brown side wings now also has three rows of cream "
            "scalloped paper feather strips glued in overlapping layers across the cream tummy panel "
            "from the bottom upward, giving the chest a soft fluffy textured look. Still no orange "
            "feet at the bottom yet. Lying flat on a white craft table next to small cream scalloped "
            "paper scraps. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "owl-paper-craft-feet-finished.webp",
        "prompt": (
            "Final step of a paper owl craft tutorial. The completely finished owl paper craft. "
            f"{OWL_DESCRIPTION} "
            "All elements are now in place: brown body with ear tufts, cream tummy panel, white eyes "
            "with black pupils, orange triangle beak, brown side wings, three rows of cream scalloped "
            "tummy feathers, and two small orange feet glued at the bottom of the body so they peek "
            "out below the owl. Lying flat on a white craft table. The owl looks complete and friendly. "
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
