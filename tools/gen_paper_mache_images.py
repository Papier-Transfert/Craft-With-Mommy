#!/usr/bin/env python3
"""Generate idea images for paper-mache-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-mache-crafts"
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
        "filename": "paper-mache-balloon-globe.webp",
        "prompt": (
            "A handmade paper mache globe made from a round balloon covered in newspaper strips, "
            "painted with blue oceans and green continents by a child. Sitting on a wooden craft table "
            "with a small paintbrush and acrylic paint pots nearby. "
            "Cheerful homemade look with slightly uneven painted continents. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-dinosaur-egg.webp",
        "prompt": (
            "A handmade paper mache dinosaur egg: a rounded oval shape made from a balloon covered "
            "in dried newspaper strips, painted in mottled earthy greens and browns with speckled dots. "
            "Sitting in a small nest of crumpled brown paper on a craft table. "
            "Charming handmade look, slightly lumpy surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-caterpillar.webp",
        "prompt": (
            "A handmade paper mache caterpillar made from five small spheres lined up in a row, "
            "each one a different bright color (red, orange, yellow, green, blue). "
            "Two pipe cleaner antennae on the head and two googly eyes. "
            "Lying on a light wood craft table. Cheerful and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-rainbow-bowl.webp",
        "prompt": (
            "A handmade paper mache bowl shaped over a round mixing bowl mold, now free-standing. "
            "Painted in wide rainbow stripes of red, orange, yellow, green, and blue on the inside. "
            "Sitting on a wooden craft table with paintbrushes beside it. "
            "Slightly uneven edges, clearly child-made and charming. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-cat.webp",
        "prompt": (
            "A handmade paper mache cat with a round balloon body and a smaller round head, "
            "cardboard triangle ears, painted orange with black stripes. "
            "Googly eyes, a small black button nose, and black marker whiskers. "
            "Sitting upright on a craft table, adorable and slightly lopsided. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-volcano.webp",
        "prompt": (
            "A handmade paper mache volcano built around a small plastic bottle, "
            "covered in dried newspaper strips and painted with rocky browns and grays on the outside, "
            "fiery red and orange at the crater rim. Sitting on a wooden board on a craft table. "
            "Clearly child-made with charming imperfections. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-penguin.webp",
        "prompt": (
            "A handmade paper mache penguin made from a balloon base, painted black and white "
            "with an orange triangle beak and small orange felt feet. "
            "Round roly-poly shape sitting upright on a light wood craft table. "
            "Two googly eyes. Adorable and slightly lumpy, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-sun-moon.webp",
        "prompt": (
            "A handmade paper mache wall hanging: a round flat disc painted half as a bright yellow sun "
            "with pointed cardboard rays around the edge, and half as a pale blue crescent moon. "
            "Hanging from a loop of yarn. Lying flat on a light wood surface for the photo. "
            "Cheerful and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-ladybug.webp",
        "prompt": (
            "A handmade paper mache ladybug: a dome-shaped half-sphere painted bright red "
            "with black spots and a black stripe down the middle to separate the wings. "
            "A small round black head with two googly eyes. "
            "Sitting on a craft table, charming and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-treasure-chest.webp",
        "prompt": (
            "A handmade paper mache treasure chest made from a cardboard box base covered in newspaper strips, "
            "painted brown with gold metallic paint details around the edges and a small clasp. "
            "Lid slightly open revealing gold paper coins inside. "
            "Sitting on a craft table, clearly child-made with charming imperfections. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-fish.webp",
        "prompt": (
            "A handmade paper mache fish with a cardboard tail fin, covered in newspaper strips and "
            "painted in tropical colors: bright orange body with yellow and white stripe details "
            "and a purple tail fin. One googly eye. "
            "Hanging from a string against a light background. Cheerful and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-piggy-bank.webp",
        "prompt": (
            "A handmade paper mache piggy bank: a balloon body with four toilet paper roll legs, "
            "a paper cup snout, and cardboard ears, all covered in dried newspaper strips and "
            "painted bright pink with a curly paper tail. A coin slot cut in the top. "
            "Sitting on a craft table, adorable and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-butterfly.webp",
        "prompt": (
            "A handmade paper mache butterfly with large cardboard wings and a toilet paper roll body, "
            "all covered in newspaper strips. Wings painted in purple, blue, and yellow with "
            "black marker outline details. Displayed flat on a light wood craft table. "
            "Bright and cheerful, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-fruit-bowl.webp",
        "prompt": (
            "A handmade paper mache fruit display: newspaper-stuffed apple, banana, and orange shapes "
            "covered in dried strips and painted in realistic colors, arranged together on a craft table. "
            "The apple is red, the banana yellow, the orange bright orange. "
            "Each piece slightly lumpy and clearly child-made, charming handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-elephant.webp",
        "prompt": (
            "A handmade paper mache elephant: a balloon body, paper towel roll trunk, and large "
            "cardboard circle ears, all covered in newspaper strips and painted gray. "
            "Pink inside the ears, two googly eyes, and a cheerful expression. "
            "Sitting on a craft table, adorable and slightly lumpy, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mache-maracas.webp",
        "prompt": (
            "Two handmade paper mache maracas: each one made from a small balloon on a paper towel roll handle, "
            "covered in dried newspaper strips and painted in bright colors (one red with yellow dots, "
            "one blue with orange stars). "
            "Lying side by side on a craft table. Cheerful and clearly child-made. "
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
