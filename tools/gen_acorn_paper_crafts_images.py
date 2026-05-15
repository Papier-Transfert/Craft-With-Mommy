#!/usr/bin/env python3
"""Generate all images for acorn-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "acorn-paper-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. Cozy fall atmosphere. "
    "Clean, family-friendly composition. Landscape orientation 4:3. "
    "No cartoon elements. Real paper craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "acorn-paper-crafts.webp",
        "prompt": (
            "A warm flat lay of handmade acorn paper crafts arranged on a light wooden craft table: "
            "several brown paper acorn cutouts in different sizes, an acorn-shaped paper garland made of "
            "brown and tan paper acorns on twine, a small paper plate acorn, a torn-paper acorn mosaic, "
            "and an acorn corner bookmark. Real orange and yellow oak leaves scattered around. "
            "Child-safe scissors and a glue stick visible at the edges. Soft autumn light, cozy fall feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "acorn-cutout-card.webp",
        "prompt": (
            "A handmade folded greeting card standing on a craft table. The front shows a simple brown "
            "construction paper acorn shape glued onto the cream card, topped with a darker brown paper "
            "cap with a tiny stem. The card is slightly imperfect and clearly cut by a child. "
            "A pencil and a small pile of paper scraps sit beside the card. Warm fall light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "torn-paper-acorn-mosaic.webp",
        "prompt": (
            "A handmade torn paper acorn mosaic on a white sheet of paper. An acorn outline is filled with "
            "small irregular pieces of torn brown and tan construction paper glued inside, creating a "
            "textured mosaic look. The darker cap is filled with darker brown torn pieces. Visible torn "
            "paper edges. Glue stick beside it on the craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "acorn-paper-bag-puppet.webp",
        "prompt": (
            "A small brown paper lunch bag standing on a craft table, decorated as an adorable acorn "
            "puppet. The top flap of the bag has two googly eyes and a friendly smile drawn in black "
            "marker. A darker brown construction paper cap with a small stem is glued at the very top "
            "of the bag. Clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "fingerprint-acorn-tree.webp",
        "prompt": (
            "A handmade paper craft showing a simple oak tree drawn on a piece of white paper with a "
            "brown trunk and bare branches. Small brown fingerprint dots are pressed all over the branches "
            "to look like little acorns, each topped with a tiny darker brown dot for the cap. A small "
            "brown ink pad sits beside the paper on the craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "acorn-paper-garland.webp",
        "prompt": (
            "A handmade paper acorn garland draped across a light wooden surface. About ten brown and tan "
            "paper acorn shapes, each with a slightly darker brown cap, are strung onto twine with small "
            "evenly spaced gaps. A few real orange autumn leaves are scattered nearby. Soft daylight, "
            "cozy fall vibe. Charming and slightly uneven, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-plate-acorn.webp",
        "prompt": (
            "A handmade paper plate acorn craft lying on a craft table. The bottom half of a small white "
            "paper plate has been painted or covered with light brown paper to form the acorn body. "
            "A textured crinkled darker brown paper strip is glued across the top as the cap, with a "
            "tiny stem rising from the center. A curled orange paper leaf is attached on one side. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "accordion-acorn-card.webp",
        "prompt": (
            "A handmade pop-up accordion paper acorn card sitting on a craft table. Two brown paper "
            "acorn shapes with darker caps are connected by a folded white paper accordion strip stretching "
            "between them. The front acorn has a simple smiley face drawn in black marker. The accordion "
            "is partially extended, showing visible folds. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "acorn-crown-headband.webp",
        "prompt": (
            "A handmade paper crown headband laid flat on a light wood craft table. A long strip of brown "
            "construction paper forms the band, decorated along the front with several small brown paper "
            "acorns alternating with orange and yellow oak leaf shapes. The two ends of the strip are "
            "taped together. Clearly handmade by a child, slightly uneven. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "acorn-name-banner.webp",
        "prompt": (
            "A handmade paper acorn name banner strung on jute twine across a light wooden background. "
            "Five large brown paper acorn shapes with darker caps hang from the twine, each acorn showing "
            "a single chunky black letter written in marker spelling a child name like 'LIAM'. "
            "Slightly uneven and clearly child-made, warm fall feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-acorn-sun-catcher.webp",
        "prompt": (
            "A handmade acorn-shaped tissue paper sun catcher hanging in a sunny window. The frame is a "
            "black paper acorn outline with the inside cut out and filled with overlapping pieces of "
            "orange, yellow, and red tissue paper that glow as sunlight passes through. The sun catcher "
            "is taped to a window pane against a softly blurred garden background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "3d-paper-acorn-sculpture.webp",
        "prompt": (
            "A handmade three-dimensional paper acorn sculpture hanging from a piece of brown string "
            "against a soft cream background. The acorn is made from four matching brown paper halves "
            "glued together at the center fold so it pops outward in 3D. A darker brown cap sits at the "
            "top with a tiny stem. Clearly handmade by a child, slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "acorn-bookmark-corner.webp",
        "prompt": (
            "A handmade paper corner bookmark shaped like a friendly brown acorn, sliding over the top "
            "corner of an open chapter book. The bookmark has a brown paper body with a darker textured "
            "paper cap at the top and two small googly eyes with a tiny smile drawn in black marker. "
            "The open book sits on a light wood craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "squirrel-acorn-collage.webp",
        "prompt": (
            "A handmade paper collage on a cream sheet of paper showing a chunky brown paper squirrel "
            "with a fluffy curled paper tail standing among several small brown paper acorns. A few small "
            "orange and yellow paper oak leaves are scattered around. The squirrel has a tiny googly eye "
            "and a small black nose. Clearly child-made, slightly uneven cutting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "heart-acorn-paper-craft.webp",
        "prompt": (
            "A handmade paper acorn made from an upside-down brown construction paper heart shape, so the "
            "rounded curves of the heart form the body of the acorn. A darker textured brown paper cap "
            "with a tiny stem sits on top. The craft is glued onto a cream background sheet of paper, "
            "lying flat on a craft table next to scissors. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "acorn-counting-tree.webp",
        "prompt": (
            "A handmade paper oak tree counting activity on a large sheet of paper. A simple brown trunk "
            "with branches has the numbers 1 through 5 written in black marker on different branches. "
            "Small brown paper acorns are placed on each branch in the correct quantity, with some loose "
            "extras at the bottom of the page. Warm fall feel, clearly child-made. "
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
