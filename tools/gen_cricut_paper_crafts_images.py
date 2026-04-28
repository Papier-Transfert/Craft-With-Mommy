#!/usr/bin/env python3
"""Generate all images for cricut-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "cricut-paper-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real cardstock paper craft materials only. "
    "Charming and slightly imperfect, clearly handmade. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "cricut-paper-crafts.webp",
        "prompt": (
            "A bright flat lay of finished handmade Cricut paper crafts on a white craft table: "
            "a layered pastel 3D birthday card with foam-tape depth, three giant paper rosettes in pink and peach, "
            "a rainbow paper name banner spelling LILY, a cluster of pastel paper butterflies, "
            "a small bouquet of rolled paper roses in a glass jar, a Happy Birthday cake topper on skewers, "
            "a small Cricut cutting machine partially visible at the edge of the frame, "
            "and scattered colorful cardstock scraps. Cheerful, organized, family-friendly atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-layered-3d-birthday-card.webp",
        "prompt": (
            "A handmade layered 3D birthday card with three layers of cardstock in pastel pink, mint green, "
            "and pale yellow. Each layer is held apart by foam tape creating dimension. "
            "On top, hand-lettered cursive script reads 'Happy Birthday' cut from gold cardstock. "
            "Card sits at an angle on a white craft table. Charming and slightly imperfect, handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-paper-name-banner.webp",
        "prompt": (
            "A handmade paper name banner spelling LILY in tall block letters cut from rainbow cardstock: "
            "L in red, I in orange, L in yellow, Y in blue. Each letter has two small holes punched at the top "
            "and is strung together with rustic baker's twine. The banner hangs across a soft white wall above "
            "a small play table. Cheerful nursery decoration. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-paper-rosettes.webp",
        "prompt": (
            "Three handmade paper rosettes in different sizes mounted on a white wall: "
            "a large 12-inch rosette in soft pink cardstock, a medium 8-inch rosette in peach, "
            "and a small 5-inch rosette in metallic gold. Each rosette has clean accordion folds radiating "
            "from a center button. Bright, photogenic, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-mandala-wall-art.webp",
        "prompt": (
            "A delicate intricate handmade white paper mandala with circular geometric cutouts and lacy details, "
            "mounted on a deep navy blue cardstock background. The whole piece is displayed in a simple wooden "
            "picture frame on a light shelf. Lacework-like beauty, clearly cut by a craft machine. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-butterfly-wall-decals.webp",
        "prompt": (
            "About a dozen handmade paper butterflies in soft pastel cardstock (pink, lavender, peach, mint, white), "
            "their wings bent slightly upward to give a 3D mid-flight look. Taped to a soft white bedroom wall "
            "in a swooping flying pattern that arches upward. Decorative children's room wall art. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-3d-paper-flowers.webp",
        "prompt": (
            "A handmade 3D paper rose bouquet of about seven rolled spiral roses in shades of pink, peach, "
            "and pale yellow cardstock. Each rose was rolled from a spiral template. Small green paper leaves "
            "tucked between the blooms. The bouquet sits in a small clear glass jar on a wooden craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-paper-favor-boxes.webp",
        "prompt": (
            "Five handmade mini cardstock favor boxes in coordinating pastel colors (mint, pink, peach, "
            "pale yellow, lavender), each about 2 inches square. Crisp clean fold lines. A few are open "
            "showing small candies inside. A few are closed with tiny paper tab tops. Arranged in a cluster "
            "on a wooden craft table. Sweet party favor look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-paper-cake-topper.webp",
        "prompt": (
            "A handmade gold glittery 'Happy Birthday' paper cake topper in fancy script, cut from gold "
            "metallic cardstock and mounted on two thin wooden skewers. The topper is stuck into a small "
            "round white frosted birthday cake on a cake stand. Soft natural light. Birthday party feeling. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-heart-gift-tags.webp",
        "prompt": (
            "Six handmade small heart-shaped paper gift tags arranged on a white craft table: "
            "two red, two pink, two white. Each has a small hole punched at the top with rustic baker's "
            "twine threaded through, and a hand-lettered name written on it ('Mom', 'Dad', 'Grace'). "
            "Sweet handmade gift wrapping. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-paper-snowflake-garland.webp",
        "prompt": (
            "A handmade white paper snowflake garland with about eight intricate snowflakes in different "
            "designs strung on clear thread across a sunny window. Soft afternoon sunlight passes through "
            "the cutouts. Cozy winter window decoration. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-mini-paper-pumpkins.webp",
        "prompt": (
            "Three handmade mini paper pumpkins arranged on a wooden fall-themed table: each pumpkin is "
            "made from layered curved orange cardstock strips that wrap around to form a 3D pumpkin shape. "
            "Each has a small twisted brown paper stem and a tiny green paper leaf. "
            "Soft autumn lighting. Cozy fall centerpiece. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-paper-bookmark.webp",
        "prompt": (
            "Three handmade decorative paper bookmarks lying flat on a wooden craft table: "
            "a long pink rectangle with a heart cutout at the top, a blue rectangle with a star cutout, "
            "and a yellow rectangle with a flower cutout. Each has a small punched hole and a coordinating "
            "tassel hanging from the top. Pretty handmade gift idea. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-layered-easter-eggs.webp",
        "prompt": (
            "Five large handmade paper Easter eggs hanging from a slim bare branch in a tall vase: "
            "each egg is a base color (pastel pink, mint, blue, lavender, peach) with smaller patterned "
            "paper layers stacked on top in stripes, dots, and zigzag designs. Eggs hang on baker's twine "
            "loops. Spring centerpiece on a kitchen table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-paper-crown.webp",
        "prompt": (
            "A handmade gold cardstock paper crown with a tall pointed band and several diamond and "
            "circle-shaped cutouts along the top. Behind each cutout, colorful tissue paper (red, blue, "
            "green) is glued so the openings look like jewels glowing in the light. The crown is being "
            "worn by a smiling young child looking off camera. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-geometric-animal-faces.webp",
        "prompt": (
            "Three handmade geometric paper animal faces arranged on a light wood surface: "
            "a fox face made from orange and white triangles, an owl face made from brown and cream "
            "circles and triangles, and a bear face made from brown rounded shapes. Each animal is "
            "assembled from about six to seven simple geometric cardstock pieces. Friendly, modern "
            "nursery wall art look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-holiday-tree-ornaments.webp",
        "prompt": (
            "Several handmade paper holiday tree ornaments hanging on a small green Christmas tree: "
            "star shapes in red, gold, and white cardstock; heart shapes in matching colors; "
            "small tree shapes too. Each ornament is decorated with subtle metallic marker swirls and "
            "hangs from baker's twine. Cozy holiday tree close-up shot. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-paper-lantern-trio.webp",
        "prompt": (
            "Three handmade paper lanterns hanging together from string above a windowsill: "
            "one pink, one yellow, one turquoise. Each lantern is a tube of cardstock with vertical slits "
            "down the middle that bow outward to form a classic lantern shape. Soft natural light comes "
            "through the slits. Cheerful nursery or play kitchen decoration. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-watercolor-flowers-card.webp",
        "prompt": (
            "A handmade folded greeting card on a white craft table. The front of the card features "
            "a layered 3D paper flower made from soft watercolor-printed cardstock: a large blossom shape, "
            "a smaller blossom on top, and a tiny round center. The layers are stacked with foam tape "
            "between each one for visible dimension. Pink and peach colors. Boutique-quality handmade card. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-paper-star-garland.webp",
        "prompt": (
            "A handmade paper star garland with about twelve small stars in white, gold, and pale blue "
            "cardstock, sewn onto a long thin thread with a few stitches in the middle of each star so the "
            "stars hang freely. The garland is draped along a soft white wall above a child's reading nook. "
            "Magical and delicate. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cricut-paper-photo-frames.webp",
        "prompt": (
            "Three handmade decorative paper photo frames in pastel colors (pink, mint, yellow) magnetically "
            "stuck to a white refrigerator door. Each frame has scalloped or floral cutouts around the edges "
            "and shows a small family photo of children behind the opening. Charming homemade keepsakes. "
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
