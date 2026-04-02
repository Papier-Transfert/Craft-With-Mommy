#!/usr/bin/env python3
"""Generate all images for foldable-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "foldable-paper-crafts"
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
        "filename": "foldable-paper-crafts.webp",
        "prompt": (
            "A colorful flat lay of handmade foldable paper crafts on a white craft table: "
            "a small origami boat in blue paper, a paper fortune teller in pink and yellow, "
            "an accordion fan in rainbow colors, a tiny paper jumping frog in green, "
            "a folded paper butterfly in purple, a small origami crane in red, "
            "and a folded paper heart in pink. "
            "Origami paper sheets and a glue stick visible at the edges. "
            "Warm cozy crafting mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-origami-boat.webp",
        "prompt": (
            "A handmade origami paper boat folded from a single sheet of blue origami paper. "
            "The boat has the classic peaked roof shape with two pointed ends. "
            "Small porthole circles drawn on the side with a black marker. "
            "Sitting on a light wood craft table. Charming and slightly imperfect, made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fortune-teller.webp",
        "prompt": (
            "A handmade paper fortune teller cootie catcher made from a square of yellow paper. "
            "Four colored flaps visible on the outside labeled with colors in crayon: red, blue, green, purple. "
            "Numbers written on the triangular panels. The fortune teller is open showing the pinching shape. "
            "Lying flat on a white craft table with crayons nearby. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "accordion-paper-fan.webp",
        "prompt": (
            "A handmade accordion-folded paper fan made from a single sheet of paper decorated with "
            "rainbow stripes in red, orange, yellow, green, and blue marker. "
            "The fan is fanned out fully showing all the crisp accordion pleats. "
            "A small piece of tape secures the pinched handle end. "
            "Lying open on a white craft table. Bright, cheerful, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-jumping-frog.webp",
        "prompt": (
            "A small handmade origami jumping frog folded from a rectangle of bright green cardstock. "
            "The frog has the classic jumping frog shape with two front legs and a folded back section. "
            "Two small black dot eyes drawn on with a marker. "
            "Sitting on a light wood table with a few green paper scraps nearby. "
            "Slightly imperfect folds, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "folded-paper-butterfly.webp",
        "prompt": (
            "A handmade accordion-fold paper butterfly made from a strip of paper decorated with "
            "colorful flower and dot patterns in marker. The paper is pinched in the center to form "
            "two symmetrical wings fanned out on each side. A small twisted piece of paper serves as antennae. "
            "Photographed on a white craft table. Pretty and slightly uneven, made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-cup-craft.webp",
        "prompt": (
            "A small handmade origami paper cup folded from a square of blue origami paper. "
            "The cup is the classic triangular-based drinking cup shape with a small opening at the top. "
            "Sitting upright on a light wood table. A drop of water visible inside the cup. "
            "Neat simple folds, slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-tulip-craft.webp",
        "prompt": (
            "Three handmade origami tulips folded from red and pink origami paper squares. "
            "Each tulip blossom is attached to a green construction paper strip stem. "
            "The flowers are arranged loosely in a small glass jar on a white craft table. "
            "Warm and cheerful, clearly folded by a child with adult help. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pinwheel-craft.webp",
        "prompt": (
            "A handmade paper pinwheel made from a square of paper decorated with bright marker stripes "
            "in red, orange, and yellow. Diagonal cuts reach toward the center, and alternating corners "
            "are folded in and held by a small brad at the center. Attached to a wooden skewer handle. "
            "Sitting on a craft table, ready to spin. Bright and cheerful. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "folded-paper-envelope.webp",
        "prompt": (
            "A small handmade folded paper envelope made from a square of light blue patterned paper. "
            "The four corners are folded to the center forming a neat diamond envelope shape. "
            "A small handwritten note is tucked inside with the corner visible. "
            "Lying flat on a white craft table. Neat and charming, made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-crane-craft.webp",
        "prompt": (
            "A single handmade origami crane folded from a red and white patterned origami paper square. "
            "The crane has two spread wings, a pointed beak, and a small tail. "
            "Sitting on a light wood craft table next to its origami paper square wrapper. "
            "Slightly imperfect folds showing it was made by an older child with help. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "accordion-fold-bookmark.webp",
        "prompt": (
            "A handmade accordion-fold paper bookmark made from a narrow strip of cardstock. "
            "The bookmark is folded into a compact pleated stack with a rainbow drawn on the top panel. "
            "The bookmark is tucked into the corner of an open colorful children's book. "
            "Seen from a slightly angled overhead view on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-dove-craft.webp",
        "prompt": (
            "Three handmade white origami doves folded from white origami paper squares. "
            "Each dove has spread wings and is hung from a thin thread at different heights. "
            "Photographed against a soft pale background showing all three birds in a gentle mobile arrangement. "
            "Simple elegant folded shapes, slightly varied sizes. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "folded-paper-crown.webp",
        "prompt": (
            "A handmade folded paper crown made from a long strip of gold cardstock. "
            "The strip is accordion-folded to create pointed peaks, then shaped into a circle and taped closed. "
            "Small yellow paper star cutouts are glued to the tips of each peak. "
            "Sitting on a white craft table. Regal and slightly wonky, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-popup-card.webp",
        "prompt": (
            "A handmade paper pop-up card open flat on a white craft table. "
            "The card is folded in half from white cardstock and has a small red origami heart "
            "mounted on a rectangular paper tab that pops up from the center fold when opened. "
            "The inside of the card shows a handwritten message around the pop-up. "
            "Photographed open at a slight angle to show the 3D pop-up effect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-dog-face.webp",
        "prompt": (
            "A handmade origami dog face folded from a square of brown origami paper. "
            "Two top corners folded down to form floppy triangular ears, bottom corner folded up for a nose. "
            "Two large black dot eyes and a smile drawn on with a black marker after folding. "
            "Sitting flat on a white craft table. Cute and slightly uneven, made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-ninja-star.webp",
        "prompt": (
            "A handmade origami ninja star shuriken made from two interlocked folded paper tubes, "
            "one blue and one yellow origami paper. The finished star has four sharp points alternating "
            "between blue and yellow. Lying flat on a light wood craft table. "
            "Crisp folds, clearly made by an older child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "folded-paper-box.webp",
        "prompt": (
            "Two handmade folded origami masu boxes sitting side by side on a craft table. "
            "One box is folded from blue origami paper and the other from orange. "
            "Both are open at the top with clean square walls. The slightly larger box acts as a lid "
            "resting beside the smaller one. Neat folds, clearly made with care. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-heart-craft.webp",
        "prompt": (
            "Five small handmade origami hearts folded from red and pink origami paper squares in various sizes. "
            "Arranged in a loose cluster on a white surface. Each heart has the classic pointed bottom and "
            "rounded top formed by folding. A few heart shapes are slightly different in size. "
            "Warm, sweet, Valentine mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "accordion-caterpillar.webp",
        "prompt": (
            "A handmade accordion-fold paper caterpillar made from alternating green and yellow paper strips "
            "accordion-folded and glued end to end to form a wiggly body. "
            "The head section has two small googly eyes and two paper antennae. "
            "The caterpillar is stretched out in a gentle curve on a white craft table. "
            "Cheerful and slightly wobbly, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-fish-craft.webp",
        "prompt": (
            "Five small handmade origami fish folded from orange and blue origami paper squares. "
            "Each fish has a pointed tail and a slightly rounded body, with a small black dot eye "
            "drawn on with marker. Arranged in a loose group on a light wood surface as if swimming. "
            "Fun, bright, ocean-themed craft clearly made by a child. "
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

    from PIL import Image as PILImage
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
