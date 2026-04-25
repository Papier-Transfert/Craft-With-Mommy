#!/usr/bin/env python3
"""Generate all images for pumpkin-construction-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "pumpkin-construction-paper-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly autumn atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "pumpkin-construction-paper-crafts.webp",
        "prompt": (
            "A colorful flat lay of handmade pumpkin construction paper crafts on a light wood craft table: "
            "an orange paper jack-o-lantern with black triangle eyes, a small paper pumpkin chain garland, "
            "a 3D paper strip loop pumpkin, an orange paper pumpkin treat bag with a green ribbon handle, "
            "a few tiny pumpkin place cards, and a stacked paper pumpkin tower. "
            "Brown stems and small green leaves. Scissors, glue stick, and orange and brown construction paper scraps "
            "visible at the edges. Cozy autumn mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "classic-construction-paper-pumpkin.webp",
        "prompt": (
            "A handmade classic round orange construction paper pumpkin shape lying flat on a wooden craft table. "
            "Small brown rectangle stem on top, tiny green paper leaf, and a curly green vine drawn with marker. "
            "Slightly imperfect cut edges, clearly child-made. Single pumpkin centered in the frame. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-strip-3d-pumpkin.webp",
        "prompt": (
            "A handmade 3D pumpkin made from six orange construction paper strips fanned out into a round dimensional shape. "
            "The strips are joined at the top and bottom with a small brown paper stem on top "
            "and a green paper leaf attached. Standing on a wooden craft table. "
            "Clearly handmade by a child, slightly wobbly shape. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-jack-o-lantern.webp",
        "prompt": (
            "A handmade orange construction paper jack-o-lantern: a large round pumpkin shape "
            "with two black paper triangle eyes, a black triangle nose, and a jagged black paper smile glued on. "
            "Small brown stem and tiny green leaf on top. Lying flat on a craft table with paper scraps around it. "
            "Charming and clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-pumpkin-patch.webp",
        "prompt": (
            "A handmade construction paper pumpkin patch collage: a half sheet of brown construction paper background "
            "with green grass strips along the bottom, five orange paper pumpkin shapes of different sizes, "
            "curly green vines, a yellow paper sun in the corner, and small green leaves. "
            "Clearly cut and glued by a child. Flat lay on a craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-pumpkin-garland.webp",
        "prompt": (
            "A handmade pumpkin chain garland with eight small orange construction paper pumpkin shapes "
            "and tiny green paper leaves threaded onto a piece of brown twine, draped along a white shelf or mantel. "
            "Each pumpkin slightly different, clearly cut by a child. Festive autumn decoration. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "accordion-paper-pumpkin.webp",
        "prompt": (
            "A handmade accordion-folded orange construction paper pumpkin: a square of orange paper folded "
            "with narrow even accordion pleats, pinched in the middle to form a fan-like rounded pumpkin shape. "
            "A small brown paper stem on top and a curly green paper vine attached. "
            "Standing upright on a wooden craft table. Clearly child-made, slightly uneven folds. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-pumpkin-lantern.webp",
        "prompt": (
            "A handmade construction paper pumpkin lantern: an orange construction paper cylinder with vertical slits cut "
            "along the side and pushed gently outward to form a rounded pumpkin shape. "
            "A brown paper stem on top and a friendly black jack-o-lantern face drawn on the front. "
            "A small battery tealight glows softly inside. Sitting on a wooden craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pumpkin-mosaic.webp",
        "prompt": (
            "A handmade torn paper pumpkin mosaic: a large pumpkin outline drawn on white construction paper, "
            "filled in with small torn pieces of orange, yellow, and red construction paper glued like a mosaic. "
            "A brown torn paper stem on top and torn green paper leaves. "
            "The mosaic pieces have rough irregular edges. Clearly handmade by a young child. Flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pumpkin-trick-or-treat-bag.webp",
        "prompt": (
            "A handmade pumpkin trick-or-treat bag made from a folded sheet of orange construction paper "
            "stapled at the sides to form a small pouch. A black paper jack-o-lantern face glued on the front, "
            "and a green ribbon handle threaded through two punched holes at the top. "
            "Sitting upright on a craft table with paper scraps around it. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pumpkin-greeting-card.webp",
        "prompt": (
            "A handmade folded cream construction paper greeting card lying open on a wooden table. "
            "On the front of the card, a small orange paper pumpkin shape with a brown paper stem and a green leaf glued on, "
            "with the words 'Happy Fall' written below in brown marker by a child's hand. "
            "Slightly wobbly handwriting. Charming and warm. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "construction-paper-pumpkin-wreath.webp",
        "prompt": (
            "A handmade construction paper pumpkin wreath: a brown paper ring base with a dozen small orange paper "
            "pumpkin shapes glued around it, overlapping at points. Small green paper leaves tucked between the pumpkins. "
            "A brown ribbon bow at the top. Hanging on a white wall or door. Clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pumpkin-crown.webp",
        "prompt": (
            "A handmade orange construction paper crown: a long strip of orange paper stapled into a band, "
            "with five small paper pumpkin shapes glued along the front like jewels, each with a tiny brown stem. "
            "Lying flat on a wooden craft table next to scissors and orange paper scraps. "
            "Slightly uneven, clearly made by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pumpkin-family.webp",
        "prompt": (
            "A handmade construction paper pumpkin family portrait: four orange paper pumpkin shapes of graduated sizes "
            "from large to small in a row on a cream background, each with a different friendly face drawn on with marker "
            "and a name handwritten beneath each pumpkin. Small brown stems on top of each. "
            "Clearly child-made and personal. Flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "pumpkin-corner-bookmark.webp",
        "prompt": (
            "A handmade orange construction paper pumpkin corner bookmark slipped over the corner of an open book. "
            "The triangular pocket bookmark is decorated with a friendly black drawn jack-o-lantern face on the front "
            "and a tiny brown paper stem at the top. The book is open to a children's storybook page. "
            "Cozy reading scene on a wooden table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "stacked-paper-pumpkin-tower.webp",
        "prompt": (
            "A handmade construction paper stacked pumpkin tower: three orange paper pumpkin shapes in graduated sizes "
            "stacked vertically on a cream paper background, with the largest at the bottom and smallest on top. "
            "A brown paper stem at the very top and curling green paper vines on both sides. "
            "Farmhouse-style fall decoration, clearly handmade by a child. Flat lay. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cat-on-pumpkin.webp",
        "prompt": (
            "A handmade construction paper craft: a small black paper cat silhouette with two pointy ears, a curved tail, "
            "and two tiny yellow eyes, glued on top of a large round orange paper pumpkin shape. "
            "Small brown stem on the pumpkin. Lying flat on a light wood craft table. "
            "Cute Halloween-adjacent mood, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pumpkin-mobile.webp",
        "prompt": (
            "A handmade hanging pumpkin mobile: six small orange construction paper pumpkin shapes of different sizes "
            "tied at varying lengths from white strings, attached to a small wooden twig or dowel. "
            "Hanging in front of a white wall, gently swaying. Each pumpkin has a tiny brown stem. "
            "Calm, cozy autumn decoration. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pumpkin-place-cards.webp",
        "prompt": (
            "Several handmade folded cream construction paper tent place cards arranged on a Thanksgiving table setting. "
            "Each card has a small orange paper pumpkin shape glued to the front and a guest name handwritten in marker. "
            "Tiny brown stems on each pumpkin. The cards sit beside white plates. "
            "Warm and welcoming family table. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pumpkin-vine-mural.webp",
        "prompt": (
            "A handmade construction paper pumpkin vine wall mural: a long brown paper vine taped horizontally across a "
            "white wall, with curly green paper tendrils branching off, several orange paper pumpkin shapes of different sizes "
            "taped along the vine, and small green paper leaves tucked between them. "
            "Looks like a temporary autumn room transformation. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pumpkin-door-hanger.webp",
        "prompt": (
            "A handmade orange construction paper pumpkin door hanger hanging on a wooden bedroom door. "
            "Long oval pumpkin shape with a circular hole cut at the top to fit over the doorknob. "
            "Decorated with a brown paper stem, a small green paper leaf, a friendly black jack-o-lantern face, "
            "and the words 'Welcome Fall' written along the bottom in marker. Clearly child-made. "
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
