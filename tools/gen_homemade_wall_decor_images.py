#!/usr/bin/env python3
"""Generate all images for homemade-paper-craft-ideas-for-wall-decoration.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
SLUG = "homemade-paper-craft-ideas-for-wall-decoration"
IMG_DIR  = BASE_DIR / "blog" / "images" / SLUG
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight. Cozy, family-friendly atmosphere. "
    "Landscape orientation 4:3. No cartoon elements. Real paper craft materials only. "
    "Charming and slightly imperfect, clearly handmade by a child or by a parent and child together. "
    "Soft Pinterest-worthy mood, but realistic, not over-styled."
)

IMAGES = [
    {
        "filename": "homemade-paper-craft-ideas-for-wall-decoration.webp",
        "prompt": (
            "A bright cheerful flat lay of homemade paper craft wall decorations arranged on a light wood craft table: "
            "a paper flower garland with layered pink, peach and yellow paper flowers on twine, "
            "several folded paper butterflies in pastel colors with wings lifted, "
            "a small handmade paper rainbow with cotton ball clouds, "
            "three small 3D paper stars in gold and cream, "
            "a fluffy tissue paper pom-pom, and a leaf garland strand. "
            "Scissors, glue sticks, and small piles of colored construction paper visible at the edges. "
            "Top-down photo. Soft, warm daylight. Clearly a real DIY paper crafting scene for kids. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-flower-wall-garland.webp",
        "prompt": (
            "A handmade paper flower wall garland strung along a piece of natural twine and draped along a soft "
            "off-white wall. The garland has nine paper flowers in soft pink, peach, and pale yellow, "
            "each made from two layered five-petal paper flowers glued together with a small yellow paper center. "
            "The flowers are clearly cut by hand with slightly uneven edges. Photographed in soft daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "layered-heart-paper-wreath.webp",
        "prompt": (
            "A handmade layered paper heart wreath hanging on a light wall. The wreath is a paper plate ring "
            "completely covered in layered paper hearts in three sizes, in shades of pink, red, and white. "
            "Each heart slightly overlaps the next for a full fluffy look. A small red ribbon bow is tied at the top "
            "as a hanger. The cut edges look clearly handmade. Photographed in soft natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-butterfly-wall-display.webp",
        "prompt": (
            "A handmade paper butterfly wall display on a clean white wall. About eight paper butterflies "
            "in pastel pink, lilac, mint, peach, and soft yellow paper are arranged in a flowing diagonal pattern "
            "rising upward. Each butterfly is folded gently down the middle so the wings lift up in a 3D way, "
            "casting tiny soft shadows. Different sizes for visual interest. Clearly hand-cut. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pinwheel-wall-cluster.webp",
        "prompt": (
            "A cluster of three handmade paper pinwheels mounted together on a light wall. "
            "The pinwheels are made from squares of patterned and solid cardstock in pink polka dots, "
            "soft blue stripes, and mustard yellow. Each pinwheel is fixed to a wooden skewer with a small button "
            "in the center. Photographed in soft natural daylight. Playful, child-made feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "geometric-paper-triangle-bunting.webp",
        "prompt": (
            "A handmade geometric paper triangle bunting strung on natural twine along a light wall. "
            "The bunting has seven cardstock triangle pennants in a modern color palette of cream, dusty pink, "
            "terracotta, sage green, and mustard yellow. Each triangle is decorated with simple marker stripes, dots, "
            "or small shapes drawn by a child. The tops are taped onto the twine. Clean and warm look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-sunburst-wall-decor.webp",
        "prompt": (
            "A handmade paper sunburst wall decoration on a clean light wall. A small yellow cardstock circle "
            "forms the center of the sun, surrounded by about sixteen long thin paper rays in golden yellow, "
            "warm orange, and red, alternating in length. Everything is glued onto a cream backing sheet "
            "to hold its shape. Clearly child-made, slightly imperfect. Warm cheerful atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "tissue-paper-pom-pom-garland.webp",
        "prompt": (
            "A handmade tissue paper pom-pom garland with four fluffy round pom-poms in soft pink, mint green, "
            "peach, and white tissue paper, strung on natural twine along a light wall. Each pom-pom is made "
            "by accordion-folding stacked tissue paper and fluffing out the layers. Soft, dreamy, party-like feel. "
            "Photographed in warm natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "3d-paper-star-cluster.webp",
        "prompt": (
            "A handmade 3D paper star cluster mounted on a soft white wall above a child's wooden bed. "
            "Six small folded paper stars are arranged in a loose constellation shape, in a calm dreamy palette: "
            "metallic gold, cream, and soft dusty blue. Each star has a gentle 3D pyramid lift, casting tiny shadows. "
            "Cozy bedroom atmosphere. Photographed in warm soft light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cloud-raindrop-mobile.webp",
        "prompt": (
            "A handmade paper cloud and raindrop mobile hanging near a sunny nursery window. "
            "A fluffy puffy white cardstock cloud shape hangs from a piece of natural twine. From the bottom "
            "of the cloud, five thin strings dangle small paper raindrops in pale blue and silver paper at "
            "different lengths. The raindrops twirl gently in soft daylight. Calm, nursery-friendly mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-rainbow-wall-hanging.webp",
        "prompt": (
            "A handmade paper rainbow wall hanging mounted on a soft pastel wall. The rainbow is made of six "
            "arched paper strips in red, orange, yellow, green, blue, and purple, glued onto a cream cardstock "
            "backing. A fluffy white cotton ball cloud is attached at each end of the rainbow, and a small "
            "natural twine loop sits at the top for hanging. Clearly child-made with slightly uneven edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cherry-blossom-branch.webp",
        "prompt": (
            "A handmade paper cherry blossom branch mounted horizontally on a light wall. A slim real twig "
            "is covered along its length with small soft pink tissue paper blossoms made by pinching squares "
            "of pink tissue around a pencil tip and gluing them to the branch. The blossoms are uneven and "
            "charming, clearly handmade. Elegant, peaceful feel. Soft natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "honeycomb-paper-wall-pops.webp",
        "prompt": (
            "Three handmade tissue paper honeycomb balls in soft pink, peach, and mint green hanging at different "
            "heights against a clean light wall using small thread loops. The honeycomb balls are partially "
            "open into 3D rounded shapes with delicate paper folds visible. Soft, party-like decorative feel "
            "without being over the top. Warm daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-picture-frames-display.webp",
        "prompt": (
            "A row of four handmade paper picture frames arranged along a soft hallway wall. The frames are "
            "cut from colorful cardstock in soft pink, sky blue, mint green, and butter yellow, each with a "
            "square window cut from the center. The borders are decorated with child's marker doodles and "
            "sticker dots. Each frame holds a small piece of children's artwork or a family photo inside. "
            "Charming and personal. Warm light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-leaf-garland-wall-art.webp",
        "prompt": (
            "A handmade paper leaf garland made from cut paper leaves in green, ochre, and warm red, attached "
            "to a long piece of natural twine with small glue dots. The garland is draped along a doorway and "
            "trailing across a light wall. The leaves vary slightly in shape and size, clearly hand-cut. "
            "Cozy autumn family home feel. Warm natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-doily-mandala-wall-art.webp",
        "prompt": (
            "A handmade paper doily mandala mounted on a wall. Three or four white paper doilies in different "
            "sizes are layered onto a pastel pink cardstock square, with smaller doilies glued on top of larger "
            "ones to form a soft mandala pattern. The cardstock is in a simple thin frame. Delicate, lacy texture. "
            "Photographed in soft natural daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-fan-wall-display.webp",
        "prompt": (
            "A handmade paper fan wall display on a clean cream wall, above a small wooden sideboard. "
            "Five accordion-folded paper fans in coordinating patterns of soft pink, blush, gold polka dot, "
            "and cream, in half-circle and full-circle shapes, are arranged in an artful cluster. Each fan is "
            "secured at the bottom with a small dab of glue. Elegant, dressy decorative effect. Warm natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "family-handprint-tree-wall-art.webp",
        "prompt": (
            "A handmade family handprint paper tree mounted on a soft cream wall. A large brown paper tree trunk "
            "and bare branches form the structure. Several colorful paper handprints in green, ochre yellow, "
            "and warm orange are glued onto the branches like leaves, including different sizes from adult to "
            "toddler. A few extra paper leaves are tucked in to fill it out. Personal, warm family feel. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-name-letter-wall-art.webp",
        "prompt": (
            "A handmade paper name wall art hanging above a child's small wooden bed. Five large letters "
            "spelling a child's name (for example E M M I E) are cut from patterned scrapbook paper and "
            "hand-decorated cardstock in coordinating soft pink, mint, and cream tones. The letters are mounted "
            "in a clean horizontal line on the wall. Cozy children's bedroom atmosphere. Soft daylight. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "quilled-paper-initial-frame.webp",
        "prompt": (
            "A handmade quilled paper initial wall art in a small wooden frame hanging on a light wall. "
            "A large outlined letter (for example a capital A) on cream cardstock is filled in with tiny tight "
            "coils of rolled colored paper strips in soft pink, peach, and gold tones. The quilling is intricate "
            "and clearly handmade. Charming and delicate. Photographed in warm natural light. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "origami-crane-wall-hanging.webp",
        "prompt": (
            "A handmade origami crane wall hanging with two vertical strings of small folded paper cranes "
            "in soft pink, white, and gold paper hanging side by side along a light wall. Each string has "
            "four or five cranes attached at different heights, gently rotating in space. The cranes are clearly "
            "folded by hand. Graceful, calming decorative effect. Warm soft daylight. "
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
