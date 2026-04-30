#!/usr/bin/env python3
"""Generate all images for craft-patterned-paper.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "craft-patterned-paper"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood or cream craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "craft-patterned-paper.webp",
        "prompt": (
            "A flat lay of finished craft patterned paper projects on a light wooden craft table: "
            "a heart garland made of layered patterned hearts, a floral pinwheel, a stack of patterned "
            "butterflies, a small triangle bunting banner, a few rolled paper roses, and a tassel bookmark. "
            "Patterned papers in soft florals, polka dots, gingham, and stripes. "
            "Scissors, glue stick, baker's twine, and paper scraps visible at the edges. "
            "Cheerful crafty mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-heart-garland.webp",
        "prompt": (
            "A handmade heart garland with five medium hearts cut from different patterned scrapbook papers: "
            "pink florals, blue polka dots, soft yellow stripes, mint gingham, and white with tiny red dots. "
            "The hearts are strung on a length of natural baker's twine, slightly mismatched and charming. "
            "Laid out flat on a light wooden surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-pinwheel.webp",
        "prompt": (
            "A handmade paper pinwheel made from a single square of double-sided floral patterned paper, "
            "the four points pinned together at the center onto a wooden skewer. The pinwheel sits "
            "on a light wood surface with a few patterned paper scraps and a glue stick beside it. "
            "Pretty soft pink and green floral pattern visible on the blades. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-tassel-bookmark.webp",
        "prompt": (
            "A handmade rectangular bookmark cut from sturdy patterned paper with a soft floral print, "
            "rounded corners, and a small hole punched at the top with a soft pink yarn tassel attached. "
            "Lying on a light wood surface beside a closed book. Slightly imperfect, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-butterflies.webp",
        "prompt": (
            "Three handmade layered patterned paper butterflies, each made from a larger butterfly "
            "silhouette in one print and a smaller butterfly glued on top in a contrasting pattern. "
            "Mix of soft pink florals, blue polka dots, and cream gingham. The middles are pinched "
            "to give a slight three-dimensional fold. Arranged side by side on a cream paper background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-greeting-card.webp",
        "prompt": (
            "A handmade folded greeting card on a light wood surface. The cardstock front is decorated "
            "with three layered horizontal strips of patterned paper, and a single patterned paper heart "
            "is glued on top as the focal point. Soft pastel florals, polka dots, and stripes. "
            "Clearly child-made, charming and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-bunting-banner.webp",
        "prompt": (
            "A handmade triangle bunting banner with eight small triangular pennants in coordinating "
            "patterned papers: florals, gingham, polka dots, and stripes in soft pinks, mint, and cream. "
            "The pennants hang from natural baker's twine, points facing down. "
            "Photographed laid out flat across a light wood craft table. Charming homemade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-origami-bow.webp",
        "prompt": (
            "A single handmade origami bow folded from a soft pink and gold patterned paper rectangle. "
            "The bow has two clean folded loops with a small wrapped center band. "
            "Sitting on a light cream craft table beside a few extra patterned paper squares. "
            "Crisp folds, gentle imperfect handmade quality. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-rolled-roses.webp",
        "prompt": (
            "A small bouquet of five handmade rolled paper roses made from spiraled patterned paper strips. "
            "The roses are in soft pink florals, pale yellow gingham, and white with tiny pink dots. "
            "Arranged together in a small cluster on a cream craft table beside a pair of scissors. "
            "Each rose tightly rolled in the center, looser at the outer petals. Clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-photo-frame.webp",
        "prompt": (
            "A handmade rectangular photo frame made of cream cardstock with the four edges covered in "
            "strips of mixed patterned paper, soft pink florals and tiny polka dots. The center opening "
            "displays a small printed family photo of a smiling child. "
            "Sitting flat on a light wooden craft table. Charming homemade gift quality. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-bird-mobile.webp",
        "prompt": (
            "A handmade mobile featuring five small bird shapes cut from different patterned papers: "
            "soft pink florals, blue polka dots, cream gingham, mint stripes, and pale yellow florals. "
            "Each bird has a contrasting patterned wing layered on top. The birds hang from short strings "
            "tied to a small natural wooden hoop. Photographed against a soft cream wall. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-envelopes.webp",
        "prompt": (
            "Three handmade envelopes folded from different patterned papers: a soft pink floral, "
            "a blue polka dot, and a mint gingham. Each envelope is sealed at the back with a small "
            "strip of decorative washi tape. Arranged in a slight fan on a light wood craft table. "
            "Clean folds, charming handmade quality. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-patchwork-collage.webp",
        "prompt": (
            "A handmade patchwork collage on a large cream cardstock background. Small uniform squares "
            "of patterned paper are glued in a tidy grid arrangement, mixing soft pink florals, "
            "blue polka dots, mint gingham, pale yellow stripes, and white with tiny dots. "
            "Looks like a paper quilt, clearly arranged by a young child. Flat lay on a light wooden surface. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-accordion-fan.webp",
        "prompt": (
            "A handmade accordion paper fan folded from a long rectangle of soft pink floral patterned "
            "paper. The folds form a half circle, pinched at the bottom and taped to a wooden craft stick "
            "as a handle. Held open on a cream craft table beside a few patterned paper scraps. "
            "Clearly handmade, charming and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-star-garland.webp",
        "prompt": (
            "A handmade star garland made from small five-point stars cut from various patterned papers: "
            "pink florals, blue polka dots, mint gingham, cream stripes. The stars are sewn together "
            "down the middle with a single line of cream thread, hanging in a flowing line. "
            "Photographed laid out flat on a light wooden craft table. Pretty handmade quality. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "patterned-paper-notebook-cover.webp",
        "prompt": (
            "A small composition notebook wrapped in soft pink floral patterned paper as a homemade cover. "
            "A strip of coordinating mint gingham washi tape runs along the spine. A small white name label "
            "is glued in the center of the front with hand-written letters. "
            "Sitting on a light wooden craft table beside a pencil. Charming homemade quality. "
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
