#!/usr/bin/env python3
"""Generate all images for paper-cones-for-crafts.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-cones-for-crafts"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "White or light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and imperfect, clearly handmade by a child. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-cones-for-crafts.webp",
        "prompt": (
            "A bright flat lay of handmade paper cone crafts arranged together on a white craft table: "
            "a brown paper cone holding a pink tissue paper ice cream scoop with sprinkles, "
            "a tall green construction paper Christmas tree cone decorated with colorful paper ornaments, "
            "two paper cone birthday party hats in pink and blue with pom-poms on top, "
            "a gold paper cone unicorn horn on a headband, "
            "two paper cone fairy dolls in pastel pink and lavender with bead heads. "
            "Scissors, glue stick, tape, and colored cardstock scraps visible at the edges. "
            "Cheerful family craft mood, clearly made by children. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-ice-cream-treats.webp",
        "prompt": (
            "Three handmade paper cone ice cream crafts standing upright on a light wood table. "
            "Each cone is rolled from tan or light brown cardstock and topped with crinkled tissue paper "
            "scoops in pink, mint green, and pale yellow. Tiny marker dots on the scoops look like sprinkles. "
            "Charming and slightly uneven, clearly made by a young child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-christmas-trees.webp",
        "prompt": (
            "A row of three handmade paper cone Christmas tree crafts on a light wood table. "
            "Each tree is rolled from green construction paper into a tall cone shape and decorated with "
            "small paper circle ornaments in red, gold, and blue. A small yellow paper star sits at the top "
            "of each tree. Tape visible at the seams. Cozy holiday craft mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-birthday-hats.webp",
        "prompt": (
            "Three handmade paper cone birthday party hats arranged on a white table. "
            "Each hat is rolled from bright cardstock in pink, light blue, and yellow, "
            "decorated with paper polka dots and a fluffy tissue paper pom-pom on top. "
            "Thin ribbon chin straps attached at the base of each hat. "
            "Cheerful party craft mood, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-unicorn-horn.webp",
        "prompt": (
            "A handmade paper cone unicorn horn headband lying on a craft table. "
            "A short narrow cone made from shimmery gold cardstock is taped onto a white fabric headband. "
            "A small fringe of pastel pink and lavender tissue paper sits behind the horn like a mane. "
            "Simple and slightly imperfect, clearly handmade. Magical and dreamy mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-witch-hats.webp",
        "prompt": (
            "Three handmade paper cone witch hat crafts on a craft table with Halloween scraps around them. "
            "Each hat is made from a tall black cardstock cone glued to a flat black paper circle brim. "
            "An orange paper band wraps the base of each cone with a small paper buckle. "
            "Slightly lopsided and charming, clearly child-made. Festive Halloween mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-princess-crown.webp",
        "prompt": (
            "A handmade paper cone princess crown lying on a craft table. "
            "A tall slim cone is rolled from pastel pink cardstock with the top edge cut into soft scallops. "
            "Decorated with small adhesive gem stickers and colorful paper dots. "
            "A long pink and white tulle ribbon trails from the top point of the crown. "
            "Sweet and dreamy mood, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-easter-carrots.webp",
        "prompt": (
            "A bundle of five handmade paper cone Easter carrot crafts on a light wood table. "
            "Each carrot is rolled from bright orange construction paper into a narrow pointed cone "
            "with a tuft of green tissue paper fringe poking out of the open top to look like carrot leaves. "
            "Slightly imperfect and charming, clearly child-made. Springtime Easter mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-rocket-ships.webp",
        "prompt": (
            "Two handmade paper cone rocket ship crafts standing on a craft table. "
            "Each rocket has a white paper cone nose taped to the top of a cardboard paper towel tube body. "
            "Red cardstock triangle fins are glued at the bottom and a round paper window in the middle. "
            "Marker stars and stripes decorate the body. Slightly uneven, clearly child-made. Playful space mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-garden-gnomes.webp",
        "prompt": (
            "Three handmade paper cone gnome crafts standing on a wooden shelf. "
            "Each gnome has a beige paper cone body with a red, blue, or green cardstock pointed hat cone on top. "
            "A fluffy white cotton ball beard covers most of the body where the hat ends, and a small round paper "
            "nose peeks out where the hat meets the beard. Storybook cozy mood, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-pencil-holders.webp",
        "prompt": (
            "A handmade paper cone pencil holder sitting on a wooden desk. "
            "A wide cone is rolled from floral patterned cardstock and taped inside a small flat paper plate base. "
            "Several colored pencils, markers, and a paint brush are tucked inside the cone. "
            "Slightly imperfect and charming, clearly child-made. Calm desk craft mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-candy-treat-cups.webp",
        "prompt": (
            "Four handmade paper cone candy treat cup crafts arranged on a party table. "
            "Each cone is rolled from pastel cardstock in pink, mint, yellow, and lavender, sealed with tape, "
            "and has a thin ribbon handle taped near the top rim. Each cone is filled with a small handful "
            "of colorful candies. Cheerful birthday party mood, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-megaphone-toy.webp",
        "prompt": (
            "A handmade paper cone megaphone toy held by a small child's hand on a craft table. "
            "The megaphone is a wide cone rolled from bright orange cardstock, taped firmly, with a small "
            "opening at the narrow end. Decorated with thick marker stripes and a child's printed name on the side. "
            "Cheerful and playful mood, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-fairy-dolls.webp",
        "prompt": (
            "Two handmade paper cone fairy dolls standing on a wooden shelf. "
            "Each fairy has a slim cone-shaped dress in pastel pink or lavender cardstock and a small wooden bead "
            "or paper circle head on top. Tiny paper wings are glued to the back of each cone, and a pipe cleaner "
            "wraps around as arms. Delicate, whimsical handmade craft mood. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-christmas-ornaments.webp",
        "prompt": (
            "Five handmade paper cone Christmas ornaments hanging from a small evergreen branch. "
            "Each cone is small, rolled from gold, red, or green patterned paper, with a thin ribbon loop at the "
            "top for hanging. Small paper snowflakes and marker doodles decorate the sides. "
            "Cozy festive mood, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-volcano-model.webp",
        "prompt": (
            "A handmade paper cone volcano model standing on a paper plate base on a craft table. "
            "The volcano is a wide brown cardstock cone with the tip cut off to form an opening. "
            "Strips of orange and red tissue paper run down the sides like lava, and yellow tissue paper "
            "is crumpled inside the opening to look like erupting lava. Playful science-craft mood, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-bird-beak-mask.webp",
        "prompt": (
            "A handmade paper cone bird beak mask lying on a craft table. "
            "A short yellow paper cone is taped onto the center of a brown paper bird mask shape that covers the "
            "eye area. Small paper feather cutouts in brown and orange are glued around the edges. "
            "Elastic ear straps attached at each side. Playful role-play mood, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-hanging-lanterns.webp",
        "prompt": (
            "Three handmade paper cone hanging lanterns strung along a sunlit window. "
            "Each cone is rolled from soft cream or pastel blue cardstock with small star and moon shaped "
            "cutouts on the sides so light shines through. A thin ribbon hangs each lantern from the closed pointed end "
            "upward. Dreamy bedtime mood, clearly handmade. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-castle-turrets.webp",
        "prompt": (
            "A cluster of four handmade paper cone castle turret crafts arranged as a small castle scene on a craft table. "
            "Each tower is a tall rectangle of grey or stone-colored cardstock with crenellated tops, topped with a "
            "small bright cone roof in red or blue cardstock. Towers stand close together to form a tiny fairy-tale castle. "
            "Storybook handmade mood, clearly child-made. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-mini-pumpkins.webp",
        "prompt": (
            "A row of five handmade paper cone mini pumpkin crafts on a fall table runner. "
            "Each pumpkin is a short squat cone rolled from orange cardstock with the tip pinched down to look "
            "like the top of a pumpkin. A small green paper stem and a curly green pipe cleaner vine sit at the top of each. "
            "Cozy autumn mood, clearly handmade by a child. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-cone-snowmen.webp",
        "prompt": (
            "Three handmade paper cone snowmen standing on a wooden windowsill. "
            "Each snowman is a short wide cone rolled from white cardstock with a small black paper top hat at the tip, "
            "two black paper button dots on the body, a tiny orange triangle paper nose, and a marker-drawn smile. "
            "Cheerful wintertime mood, clearly child-made. "
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
