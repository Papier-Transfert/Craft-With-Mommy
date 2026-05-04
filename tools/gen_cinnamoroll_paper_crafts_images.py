#!/usr/bin/env python3
"""Generate all images for cinnamoroll-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "cinnamoroll-paper-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or pale wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "Pastel color palette with soft sky blue, soft pink, and white tones. "
    "No copyrighted logos. Real handmade paper craft style with simple shapes. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

CINNAMOROLL_DESC = (
    "a simple handmade paper puppy character with a round white face, "
    "two long droopy white floppy ears, tiny black dot eyes, soft pink rosy cheeks, "
    "and a small black smile, in the style of a cute kawaii white puppy"
)

IMAGES = [
    {
        "filename": "cinnamoroll-paper-crafts.webp",
        "prompt": (
            "A pastel flat lay of handmade paper crafts featuring a cute white puppy character "
            f"({CINNAMOROLL_DESC}) on a soft blue wooden craft table: "
            "a paper doll, a folded greeting card with a white puppy face, a corner bookmark, "
            "a small paper donut with pink frosting, and a paper plate with a white puppy face. "
            "Pastel pink and blue construction paper scraps, scissors, and a glue stick visible at the edges. "
            "Soft cute kawaii mood, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-paper-doll.webp",
        "prompt": (
            f"A handmade flat paper doll cutout of {CINNAMOROLL_DESC}, "
            "a chubby standing white puppy figure made from white cardstock with two long droopy ears, "
            "a small pastel blue paper collar with a yellow paper star button. "
            "Lying flat on a pale wood craft table next to pastel paper scraps and a glue stick. "
            "Clearly child-made and slightly imperfect. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-greeting-card.webp",
        "prompt": (
            "A handmade folded greeting card on pastel sky blue cardstock standing on a craft table. "
            f"On the front, a glued-on paper face cutout of {CINNAMOROLL_DESC}, "
            "with a tiny pink paper heart in the bottom corner. "
            "Sitting upright on a white wooden craft table. Soft pastel atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-corner-bookmark.webp",
        "prompt": (
            f"A handmade triangular paper corner bookmark shaped like {CINNAMOROLL_DESC}, "
            "made from folded white paper, sitting on the corner of an open storybook. "
            "The face has tiny black dot eyes, pink cheeks, and a small smile drawn on it. "
            "Two long ears flop over the top edge. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-origami-face.webp",
        "prompt": (
            f"A simple folded white paper origami face of {CINNAMOROLL_DESC}, "
            "made from a square of white paper folded into a puppy face shape with two long folded-down ear flaps. "
            "Tiny black dot eyes, soft pink cheek dots, and a small mouth drawn with marker. "
            "Lying flat on a soft pastel pink craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-paper-donut.webp",
        "prompt": (
            f"A handmade paper donut craft with a light brown ring base, a fluffy pink paper frosting layer on top, "
            "and small colorful paper sprinkles glued to the frosting. "
            f"A small paper face of {CINNAMOROLL_DESC} is peeking out from one side as if sneaking a bite. "
            "Lying flat on a pale wood craft table. Cheerful and cute. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-bunting-garland.webp",
        "prompt": (
            "A handmade pastel bunting garland made from small triangular flags of pale pink, sky blue, and white paper, "
            f"strung on bakery twine. Every other flag has a tiny paper face of {CINNAMOROLL_DESC} glued to it. "
            "Draped loosely on a white wooden table. Festive and cheerful, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-paper-headband.webp",
        "prompt": (
            "A wearable handmade paper headband: a long white cardstock strip sized for a child's head, "
            f"with two tall floppy white paper ears glued at the top in the style of {CINNAMOROLL_DESC}, "
            "and a small pink paper heart in the middle. The headband is being worn by a young child seen from behind, "
            "or displayed on a craft table. Cute kawaii style. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-paper-plate-face.webp",
        "prompt": (
            "A handmade craft made from a small white paper plate as the round face, with two long droopy white paper ears "
            f"glued at the top in the style of {CINNAMOROLL_DESC}. "
            "Tiny black dot eyes, soft pink crayon cheek blush, and a small pink mouth. "
            "Lying flat on a pastel blue craft table. Charming child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-pencil-holder.webp",
        "prompt": (
            "A handmade desk pencil holder made from a clean small paper cup wrapped in white paper. "
            f"On the front, a glued paper face of {CINNAMOROLL_DESC} with two long ears that flop over the top edge. "
            "Filled with several pastel pink, blue, and yellow pencils sticking out of the top. "
            "Sitting upright on a soft wooden desk. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-mini-notebook.webp",
        "prompt": (
            "A small handmade mini notebook, the cover wrapped in white paper, "
            f"with a hand-drawn pastel face of {CINNAMOROLL_DESC} on the front along with three small white paper cloud cutouts. "
            "Soft sky blue washi tape borders along the top and bottom edges of the cover. "
            "Sitting flat on a pastel pink craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-paper-bag-puppet.webp",
        "prompt": (
            "A handmade paper bag puppet made from a small white paper lunch bag with the flap forming the face. "
            f"On the flap, a paper face of {CINNAMOROLL_DESC} with two long droopy ears glued on top, "
            "and a small fluffy white paper tail glued to the back. "
            "Standing upright on a pale wood craft table next to scissors and paper scraps. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-window-cling.webp",
        "prompt": (
            f"A handmade window decoration shaped like the silhouette of {CINNAMOROLL_DESC}, "
            "made from torn pastel pink, sky blue, and white tissue paper pieces pressed inside a contact paper outline. "
            "Stuck on a sunny window with soft daylight glowing through the colored tissue. "
            "Photographed against a softly blurred home interior background. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-paper-lantern.webp",
        "prompt": (
            "A handmade white paper lantern: a tube of white cardstock with evenly spaced vertical slits cut along the body, "
            f"a small paper face of {CINNAMOROLL_DESC} glued to the front, "
            "and pastel sky blue washi tape strips along the top and bottom edges. "
            "Sitting upright on a pastel pink craft table. Cute kawaii decoration. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-paper-fan.webp",
        "prompt": (
            "A handmade accordion-folded paper fan made from a wide white cardstock rectangle, "
            f"decorated on one side with a paper face of {CINNAMOROLL_DESC} and a few small pastel pink hearts. "
            "The fan is open and resting on a soft sky blue craft table next to washi tape rolls. "
            "Cheerful child-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-standing-card.webp",
        "prompt": (
            "A handmade standing card folded from white cardstock so it stands like a small tent on a desk. "
            f"At the fold, a paper cutout of {CINNAMOROLL_DESC} pops above the top edge so the head and ears stick up. "
            "Pastel pink and sky blue accents around the figure. "
            "Sitting upright on a pale wood craft table next to a thank-you note. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-cloud-mobile.webp",
        "prompt": (
            f"A handmade hanging paper mobile with a paper figure of {CINNAMOROLL_DESC} in the center "
            "and several small white paper cloud cutouts hanging at varying lengths from a thin wooden dowel. "
            "Hanging in front of a softly blurred sunny window with pastel sky blue tones. "
            "Charming nursery-style decoration. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-birthday-banner.webp",
        "prompt": (
            "A handmade pastel birthday banner with large scallop-shaped flags of pale pink, sky blue, and white paper. "
            "Each flag has one letter of HAPPY BIRTHDAY written in marker. "
            f"In the gaps between the words, small paper faces of {CINNAMOROLL_DESC} are glued. "
            "The banner is strung across a pastel wall above a small table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-paper-stickers.webp",
        "prompt": (
            "A flat lay of handmade paper stickers on a pastel pink craft table. "
            f"Several small cutouts of {CINNAMOROLL_DESC} faces, small pink paper hearts, and tiny white paper clouds, "
            "all colored with soft pastel markers. Some are arranged in a rough sticker sheet pattern, "
            "others lie scattered around scissors and a glue stick. Cute kawaii craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-fortune-teller.webp",
        "prompt": (
            "A handmade paper fortune teller cootie catcher folded from a square of white paper, "
            f"with the four outer flaps decorated with small paper faces of {CINNAMOROLL_DESC}, "
            "tiny pink hearts, and small pastel stars. "
            "Sitting flat on a soft sky blue craft table next to pastel markers. Cheerful kid-made craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cinnamoroll-treat-box.webp",
        "prompt": (
            "A small handmade paper treat box, about the size of a fist, folded from white cardstock. "
            f"On the front, a glued paper face of {CINNAMOROLL_DESC} with a tiny pastel pink ribbon bow on top. "
            "The box is closed and sitting upright on a pale wood craft table next to a tiny folded note. "
            "Adorable kawaii gift box, clearly child-made. "
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
