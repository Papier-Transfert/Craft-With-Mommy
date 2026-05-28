#!/usr/bin/env python3
"""Generate all images for helicopter-paper-craft.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "helicopter-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "The craft photo fills the entire frame edge to edge with no white borders, no letterboxing, no padding."
)

IMAGES = [
    {
        "filename": "helicopter-paper-craft.webp",
        "prompt": (
            "A finished handmade paper helicopter craft made for kids displayed on a light blue cardstock "
            "sky background with three small fluffy white paper cloud shapes glued around it. "
            "The helicopter has a bright red cardstock body with a rounded cockpit on the left, "
            "a thick mid body, and a long thin tail boom extending to the right that ends in a small white circle tail rotor. "
            "A rounded blue paper window is glued on the front cabin and shows a smiling pilot drawn inside. "
            "Two long thin white paper rotor blades crossed into an X shape are attached on top of the cabin "
            "with one visible gold brass brad fastener in the center. Black marker landing skids are drawn underneath. "
            "Photographed straight on as a flat lay on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "helicopter-paper-craft-mom-child.webp",
        "prompt": (
            "A young American mom in her early thirties and her four year old child sitting side by side at a "
            "light wood craft table together, both smiling at each other, getting ready to make a paper helicopter craft. "
            "On the table in front of them are sheets of red blue and white construction paper, "
            "a pair of green Fiskars kid safety scissors, a purple Elmer's glue stick, a small pile of gold brass brad fasteners, "
            "Crayola markers, and a pencil. Warm cozy family kitchen atmosphere. Natural daylight from a window. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "helicopter-paper-craft-cut-body.webp",
        "prompt": (
            "A child's small hands holding up a freshly cut bright red cardstock helicopter body shape. "
            "The shape has a rounded cockpit bubble on the left side, a thick mid body, and a long thin tail boom "
            "extending to the right that ends in a small disk at the tip. About 9 inches long total. "
            "The edges are slightly wobbly and clearly cut by a young child. "
            "On the light wood craft table around the hands are small red paper scraps, a pencil, and a pair of "
            "green Fiskars kid safety scissors. Flat lay photo from above. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "helicopter-paper-craft-cut-blades-tail.webp",
        "prompt": (
            "Two long thin white construction paper strips about six inches long laid out into a crossed X shape "
            "on a light wood craft table representing the spinning rotor blades for a paper helicopter craft. "
            "Next to the crossed blades is one small white paper circle the size of a quarter for the tail rotor. "
            "The freshly cut red cardstock helicopter body shape with its rounded cockpit and long tail boom "
            "is waiting to the side along with a pair of green kid safety scissors and a pencil. "
            "Clean composition. Flat lay photo from above. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "helicopter-paper-craft-glued-tail-window.webp",
        "prompt": (
            "The red cardstock paper helicopter body shape now upgraded with a small round white paper tail rotor circle "
            "glued at the very tip of its long tail boom on the right side, and a rounded blue paper cockpit window shape "
            "glued onto the front cabin area on the left. The window is plain and clean with no face drawn on it yet. "
            "The body lies flat on a light wood craft table next to a purple Elmer's disappearing glue stick "
            "with the cap off. Small red and blue paper scraps around the edges. Flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "helicopter-paper-craft-decorated-details.webp",
        "prompt": (
            "The red cardstock paper helicopter body now fully decorated with markers. Inside the rounded blue cockpit window "
            "a smiling cartoon pilot face is drawn with a small headset. Black marker outlines trace the edges of the cabin. "
            "Small black rivet dots are drawn around the cabin and along the body. Two curved black landing skids are drawn "
            "underneath the body. A bold flight number 01 is written on the side of the helicopter body in black marker. "
            "The decorated helicopter body lies flat on a light wood craft table next to a black Sharpie marker and a red Crayola marker. "
            "Still no rotor blades attached yet on top. Flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "helicopter-paper-craft-attach-rotor.webp",
        "prompt": (
            "A child's small hands attaching two long thin white paper rotor blades crossed into an X shape "
            "onto the top center of a fully decorated red cardstock paper helicopter body. "
            "A single gold brass brad fastener is being pushed down through the center of both blades and through "
            "the helicopter body just above the blue cockpit window. The shiny gold round head of the brad is clearly visible. "
            "The helicopter has a smiling pilot drawn in the blue cockpit window, a flight number 01 on the side, "
            "and a small white tail rotor at the end of the long tail boom. Light wood craft table underneath. "
            "Flat lay close up photo from above. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "helicopter-paper-craft-finished-display.webp",
        "prompt": (
            "A young child smiling proudly holding up the finished red paper helicopter craft mounted on a light blue cardstock "
            "sky background with three fluffy white paper cloud shapes glued around it. "
            "The helicopter has a rounded cockpit with a smiling pilot drawn inside a blue window, a flight number on the side, "
            "two long crossed white rotor blades held on by a gold brass brad fastener, and a small white tail rotor "
            "at the back. The child stands in front of a clean refrigerator door in a sunny family kitchen. "
            "Warm cozy atmosphere. Centered composition. "
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
