#!/usr/bin/env python3
"""Generate all images for spooky-paper-crafts.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "spooky-paper-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real construction paper materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy. "
    "Cute spooky vibe, never scary."
)

IMAGES = [
    {
        "filename": "spooky-paper-crafts.webp",
        "prompt": (
            "A colorful flat lay of handmade spooky paper crafts spread across a white craft table: "
            "a friendly white paper ghost, several small black paper bats with googly eyes, "
            "an orange paper jack-o-lantern with a smile, a paper black cat silhouette on an orange moon, "
            "a tiny black witch hat, a paper spider with bent strip legs, and a paper Boo banner letter. "
            "Scissors, glue stick, and assorted paper scraps visible at the edges of the frame. "
            "Cheerful Halloween mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-ghost-lantern.webp",
        "prompt": (
            "A handmade folded paper ghost lantern made from a sheet of white cardstock rolled "
            "into a soft cylinder, with two small black dot eyes and a tiny round mouth drawn "
            "in marker on the front. A small battery tea light glows softly from inside, lighting "
            "the ghost up with a warm yellow glow. Sitting on a wooden craft table in soft evening light. "
            "Friendly and cute, never scary. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-bat-mobile.webp",
        "prompt": (
            "A handmade paper bat mobile with three black construction paper bat shapes "
            "hanging on white strings from a small wooden twig. Each bat has two small white "
            "googly eyes glued on. The bats hang at three different heights against a "
            "light beige wall. Strings are clearly visible. Charming handmade kid craft look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-boo-banner.webp",
        "prompt": (
            "A handmade paper Boo banner: three large bubble letters B, O, O cut from bright "
            "orange cardstock with marker decorations and small ghost doodles, each letter "
            "strung along a length of brown yarn through punched holes at the top corners. "
            "The banner is hanging across a light cream wall. Cheerful, child-made appearance. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spider-crawler.webp",
        "prompt": (
            "A handmade paper spider craft with a round black paper body, smaller round head, "
            "two large white googly eyes, and eight thin black paper strip legs bent so the spider "
            "looks like it is mid-crawl. The spider is taped to a soft cream-colored wall as if "
            "it is climbing up. Clearly cut and assembled by a child, slightly imperfect edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "black-cat-moon-silhouette.webp",
        "prompt": (
            "A handmade paper black cat silhouette sitting in front of a large bright orange "
            "paper moon. The cat shape has two pointed ears and a curved tail, all cut from "
            "black construction paper. Glued onto a dark navy blue cardstock background to look "
            "like a moonlit night sky. Bold, graphic Halloween look. Edges slightly uneven, "
            "clearly cut by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-tombstone-standees.webp",
        "prompt": (
            "Three handmade grey paper tombstone standees with rounded tops, each labeled with "
            "silly white chalk marker messages like 'RIP Bedtime' and 'Boo!'. Each tombstone has "
            "a small folded paper tab at the bottom so it stands upright on a wooden shelf. "
            "Lined up in a row to look like a tiny graveyard scene. Cheerful, child-made vibe. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-mummy-bookmark.webp",
        "prompt": (
            "A handmade paper mummy corner bookmark: a folded white paper triangle pocket "
            "with thin white paper bandage strips wrapped diagonally across the front, "
            "and two googly eyes peeking out from between the bandages. The bookmark is "
            "tucked over the corner of an open storybook on a wooden table. Cute, kid-made appearance. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-witch-finger-puppet.webp",
        "prompt": (
            "Three tiny handmade paper witch finger puppets lined up on a child's hand. "
            "Each one is a small black paper cone with a wide circular black brim, a tiny "
            "marker face with a friendly grin and dot eyes, and a thin orange paper band "
            "around the base. Photographed against a soft light background, showing the "
            "child's small hand. Charming, playful kid craft. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cauldron-pouch.webp",
        "prompt": (
            "A handmade paper cauldron treat pouch: a black folded paper rectangle glued "
            "into a small pocket, with a green paper bubbling potion shape peeking out the "
            "top, decorated with marker bubble doodles. The pouch sits on a wooden craft table "
            "next to a few small wrapped candies. Clearly child-made, slightly wonky edges. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-pumpkin-lantern.webp",
        "prompt": (
            "A handmade three-dimensional paper pumpkin lantern: orange cardstock folded "
            "and slit along the edges, then rolled into a cylinder so the cuts puff out "
            "into a rounded pumpkin shape. A small green paper stem on top and a friendly "
            "jack-o-lantern face glued on the front with triangle eyes and a smiling mouth. "
            "Sitting on a wooden craft table. Cheerful and clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-skeleton-friend.webp",
        "prompt": (
            "A handmade paper skeleton: white paper bone shapes including a round skull, "
            "a ribcage rectangle with cut lines, arm and leg bone strips, all carefully "
            "arranged on a black construction paper background to look like a complete "
            "friendly skeleton figure. Brass paper fasteners visible at the joints of the "
            "arms and legs. Edges slightly uneven, clearly child-made. Flat lay photo. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-vampire-bookmark.webp",
        "prompt": (
            "A handmade paper vampire bookmark: a small black paper cape shape, a flesh-toned "
            "paper face circle on top with red marker dot eyes and two tiny white paper "
            "triangle fangs, all glued onto a long white paper strip that slides between "
            "the pages of an open storybook. Sitting on a wooden craft table. Cute, friendly, "
            "child-made appearance. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-frankenstein-mask.webp",
        "prompt": (
            "A handmade wearable paper Frankenstein mask: a wide light green construction "
            "paper rectangle for the face with a black paper hair strip across the top, "
            "two small grey square neck bolts on the sides, two googly eyes, and marker stitches "
            "drawn across the forehead. Two small holes punched on the sides with elastic "
            "string for wearing. Lying flat on a craft table. Friendly silly appearance, child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-werewolf-headband.webp",
        "prompt": (
            "A handmade paper werewolf headband: a long brown paper strip sized for a child's "
            "head, with two pointy brown paper ears glued on top and short brown paper fringe "
            "tufts attached to mimic fur. The headband is laid out flat on a wooden craft "
            "table next to scissors and glue. Charming, slightly wonky, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-owl-silhouette.webp",
        "prompt": (
            "A handmade paper night owl scene: a teardrop-shaped brown paper owl body with "
            "two large white circle eyes and black paper pupils, a small orange triangle beak, "
            "and small accordion-folded brown paper wings, perched on a bright yellow paper "
            "moon. The whole scene is glued onto a dark blue cardstock background to look "
            "like a moonlit night sky. Sweet, kid-made charm. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-eyeball-garland.webp",
        "prompt": (
            "A handmade paper eyeball garland: about a dozen small white paper circles "
            "decorated with different colored paper irises (blue, green, brown) and small "
            "black paper pupils so each eye looks unique. The eyes are glued along a length "
            "of brown ribbon, draped across a bookshelf. Silly, cheerful, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spider-web-wreath.webp",
        "prompt": (
            "A handmade paper spider web wreath: a circular cardstock ring with the center "
            "cut out, white yarn woven across the opening in a spider web pattern, and a small "
            "black paper spider with googly eyes glued on the side of the web. Hanging on a "
            "white wall. Charming, slightly imperfect, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-trick-or-treat-sign.webp",
        "prompt": (
            "A handmade paper Trick or Treat sign: a large rectangle of bright orange cardstock "
            "with the words 'Trick or Treat' written in big chunky black marker letters across "
            "the center, and small marker doodles of ghosts, bats, and pumpkins decorating "
            "the edges. Taped to a front door at child-eye level. Cheerful, welcoming, kid-made appearance. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-spooky-tree-scene.webp",
        "prompt": (
            "A handmade paper spooky tree scene: a tall bare tree shape cut from black paper "
            "with crooked branches, glued onto a soft purple cardstock background. A small yellow "
            "paper crescent moon in the upper corner, two tiny black paper bats hanging from "
            "the branches, and two small white paper ghost shapes peeking from behind the tree. "
            "Storybook-style, sweet rather than scary. Clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-witch-hat-garland.webp",
        "prompt": (
            "A handmade mini paper witch hat garland: a row of about six tiny black paper "
            "witch hats, each made from a small triangle rolled into a cone with a circular "
            "brim, decorated with thin orange or purple paper bands. The hats are glued or "
            "tied along a length of brown twine and hung across a white doorway frame. "
            "Cute, festive, clearly child-made. "
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
