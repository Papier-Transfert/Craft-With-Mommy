#!/usr/bin/env python3
"""Generate all images for paper-pizza-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-pizza-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood or white craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-pizza-craft.webp",
        "prompt": (
            "A finished handmade paper pizza craft sitting on a light wood craft table, viewed from slightly above. "
            "The base is a round white paper plate with the rim colored light golden brown with marker to look like baked pizza crust. "
            "Inside the rim is a red construction paper circle representing tomato sauce. "
            "Across the red sauce are several thin yellow paper strips arranged criss-cross to look like melted mozzarella cheese. "
            "Six small darker red construction paper circles are spread evenly across the cheese as pepperoni. "
            "Three green construction paper rings sit on top as green pepper slices, "
            "and two small wavy brown shapes represent mushrooms. "
            "A pair of kids' scissors and small paper scraps lie next to the plate. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pizza-craft-mom-child.webp",
        "prompt": (
            "A warm photo of a young American mom in her thirties and a small child around four years old "
            "sitting side by side at a light wood craft table, smiling and getting ready to start a paper pizza craft. "
            "On the table in front of them: a plain white paper plate, sheets of red, yellow, brown and green construction paper, "
            "a glue stick, and a pair of small kids scissors. "
            "Soft natural daylight from a window. Cozy, calm, real-life family moment, not staged. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pizza-craft-cut-crust.webp",
        "prompt": (
            "A child's hands using a light brown marker to color around the raised rim of a plain white paper plate, "
            "creating a baked pizza crust look. The center of the plate is still plain white. "
            "The plate sits on a light wood craft table. A few markers in different shades of brown lie next to the plate. "
            "Close, focused shot of the action of coloring the crust. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pizza-craft-tomato-sauce.webp",
        "prompt": (
            "A child's hands gluing a large red construction paper circle inside the brown-colored rim of a white paper plate "
            "to create the tomato sauce layer of a paper pizza craft. "
            "The red circle slightly smaller than the inside of the plate, leaving the brown crust rim visible all around. "
            "An open glue stick lies next to the plate on the light wood craft table. "
            "Charming, clearly child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pizza-craft-cheese-strands.webp",
        "prompt": (
            "A paper pizza craft on a white paper plate with a brown-colored crust rim and a red construction paper sauce circle inside. "
            "Several thin yellow construction paper strips, about three inches long and a quarter inch wide, "
            "are arranged criss-cross in random directions across the red sauce circle to look like melted mozzarella cheese. "
            "A child's hand is shown placing one more yellow strip on top of the red. "
            "Light wood craft table background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pizza-craft-pepperoni.webp",
        "prompt": (
            "A paper pizza craft on a white paper plate with a brown crust rim, red sauce circle, and yellow paper strip cheese already on it. "
            "Now six small darker red or burgundy construction paper circles, about one inch wide each, "
            "are spread evenly across the cheese as pepperoni. "
            "A child's hand presses one of the pepperoni circles down. "
            "A few extra small red circles wait on the craft table. Light wood surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pizza-craft-veggie-toppings.webp",
        "prompt": (
            "A paper pizza craft on a white paper plate with a brown crust rim, red sauce, yellow cheese strips, and red pepperoni circles already in place. "
            "Now three thin green construction paper rings shaped like green pepper slices "
            "and two small wavy brown construction paper mushroom shapes are added on top. "
            "A few small black paper olive circles are also arranged on the pizza. "
            "A child's hand glues one mushroom in place. Light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pizza-craft-sliced.webp",
        "prompt": (
            "A finished paper pizza craft that has been carefully cut into eight triangular pizza slices, "
            "still arranged together on a light wood craft table to form the full pizza shape. "
            "Each slice clearly shows the white paper plate base, brown crust rim, red sauce, yellow cheese strips, "
            "red pepperoni circles, green pepper rings, and brown mushroom shapes. "
            "A pair of small kids' scissors lies next to the sliced pizza. "
            "Top-down view, charming and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pizza-craft-finished.webp",
        "prompt": (
            "A completed paper pizza craft on a white paper plate displayed proudly on a light wood craft table. "
            "The plate has a brown-colored crust rim, a red construction paper tomato sauce layer, "
            "thin yellow paper strips for melted cheese, six small red pepperoni circles, "
            "three green pepper rings, two brown mushroom shapes, and a few black olive circles. "
            "Bright, cheerful, clearly handmade by a child. Top-down view, slightly imperfect and charming. "
            "A few construction paper scraps and a glue stick visible at the edge of the frame. "
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
