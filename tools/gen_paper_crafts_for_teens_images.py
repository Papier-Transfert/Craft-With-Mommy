#!/usr/bin/env python3
"""Generate all images for paper-crafts-for-teens.html."""
import io, os, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "paper-crafts-for-teens"
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
    "Charming and imperfect, clearly handmade. Pinterest-worthy."
)

IMAGES = [
    {
        "filename": "paper-crafts-for-teens.webp",
        "prompt": (
            "A flat lay of colorful handmade paper crafts for teens on a white craft table: "
            "a glass jar filled with tiny origami lucky stars in pink, blue, and gold; "
            "a paper bead bracelet in warm colors; a washi tape geometric art piece on cardstock; "
            "a few folded origami cranes in pastel colors; a small handmade mini zine booklet; "
            "and a shimmery 3D paper star in gold. Scissors, washi tape rolls, and colorful cardstock "
            "sheets visible at the edges. Creative, teen-friendly vibe. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-lucky-stars.webp",
        "prompt": (
            "A clear glass mason jar filled to the brim with dozens of tiny five-pointed 3D origami "
            "lucky stars folded from narrow paper strips in pink, blue, yellow, green, purple, "
            "and gold. A few extra stars scattered on the white wooden surface around the jar. "
            "The jar sits on a light wood craft table with a few colorful paper strips nearby. "
            "Warm cozy lighting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-bead-bracelet.webp",
        "prompt": (
            "A handmade paper bead bracelet laid flat on a white surface. The bracelet is made from "
            "tightly rolled triangular paper strips in warm tones including terracotta, coral, cream, "
            "mustard, and rust, all strung on elastic cord. Each bead has a slightly tapered shape "
            "and a visible paper grain pattern. A few loose paper strip beads sit beside the finished "
            "bracelet. Natural daylight, craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-washi-wall-art.webp",
        "prompt": (
            "A piece of white A4 cardstock decorated with bold geometric washi tape art. "
            "Multiple colored washi tape strips in blue, pink, gold, and teal form sharp diagonal "
            "lines and triangular sections across the paper. Some sections between the tape lines "
            "are filled in with watercolor washes in light purple and peach. "
            "The finished piece sits on a light wood desk. Modern and graphic look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-quilling-art.webp",
        "prompt": (
            "A handmade quilling art greeting card open on a wooden table. On the front is a "
            "detailed flower bouquet design made from tightly coiled and pinched paper strips in "
            "pink, purple, green, and white. The coils form rose-like spirals, leaf teardrops, "
            "and stem shapes. The background is clean white cardstock. The quilling work is "
            "intricate and precise, clearly done by a skilled teen. Beautiful detail. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-decoupage-journal.webp",
        "prompt": (
            "A plain hardcover journal with a beautifully decorated decoupage cover. The cover "
            "is covered in overlapping pieces of colorful torn paper, magazine clippings with "
            "floral and abstract patterns, and strips of patterned washi tape. The whole surface "
            "is sealed with a smooth glossy Mod Podge finish. The journal sits open at a slight "
            "angle on a white craft table with a small brush and Mod Podge jar beside it. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-crane-mobile.webp",
        "prompt": (
            "A handmade origami crane mobile hanging against a soft white wall. A thin wooden "
            "dowel holds twelve origami cranes of varying sizes in pink, lavender, white, gold, "
            "and sage green hanging from thin thread at different heights. The cranes are neatly "
            "folded with visible crisp creases. Light from a nearby window catches the paper folds "
            "creating a delicate, airy display. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-silhouette-art.webp",
        "prompt": (
            "A handmade paper cut silhouette artwork mounted and displayed. A detailed tree silhouette "
            "with branching arms and small leaves is precisely cut from black cardstock and mounted "
            "on a bright warm orange background paper. The piece is framed inside a simple white frame "
            "leaning against a light wall. The silhouette has clean, slightly imperfect hand-cut edges. "
            "Striking graphic contrast. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-weaving-hanging.webp",
        "prompt": (
            "A handmade paper weaving wall hanging mounted on a wooden dowel. The woven panel is "
            "made from interlaced horizontal and vertical strips of cardstock in warm earth tones: "
            "terracotta, cream, mustard, and olive green. The over-under weave pattern is clearly "
            "visible. Fringe strips of the same colors hang from the bottom edge. "
            "Displayed against a white wall with soft natural lighting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-mini-zine.webp",
        "prompt": (
            "A small handmade mini zine booklet open on a light wooden desk. The folded white paper "
            "booklet has 8 pages, each filled with hand-drawn black ink illustrations of plants, "
            "geometric shapes, and small handwritten text in a personal journaling style. "
            "A few colored pencils, a fine-tip pen, and loose paper sheets are scattered nearby. "
            "Cozy desk creative atmosphere. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-3d-star.webp",
        "prompt": (
            "A cluster of handmade 3D paper stars in three different sizes arranged on a white "
            "wooden surface. Each star is made from two interlocking cardstock star shapes slotted "
            "together. The stars are made in gold metallic, silver metallic, and rose gold cardstock. "
            "The largest star is in the center, flanked by two smaller ones. Clean, elegant holiday "
            "decor look. Warm side lighting. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-geo-lantern.webp",
        "prompt": (
            "A handmade geometric paper lantern sitting on a wooden surface glowing warmly from inside. "
            "The lantern is folded from white cardstock with scored triangular facets creating a "
            "multi-sided icosahedron-like shape. A small battery-powered LED tea light inside casts "
            "a warm amber glow through the paper faces. Photographed in a slightly dim setting to "
            "show the glow effect. Clean, modern design aesthetic. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-fan-bookmark.webp",
        "prompt": (
            "Three handmade paper accordion fan bookmarks in different colors peeking out from the "
            "top of an open hardcover book. Each bookmark has a tightly pleated fan portion in "
            "colorful patterned paper and a washi tape-wrapped base handle that clips over the page. "
            "The fans are spread open at the top showing the accordion folds. Cheerful and practical. "
            "Photographed on a light wood desk. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-stationery-set.webp",
        "prompt": (
            "A matching DIY stationery set laid out flat on a white surface. The set includes "
            "four notecards in cream cardstock each with a different washi tape border in blush, "
            "sage, and gold, plus three folded envelopes made from light floral patterned paper. "
            "Small hand-lettered details and a tiny hand-drawn floral illustration appear on each "
            "notecard. The set is arranged neatly on a white desk with a fine-point pen alongside. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-mosaic-art.webp",
        "prompt": (
            "A handmade paper mosaic artwork on a white background. The mosaic shows a large butterfly "
            "outline filled in with tiny squares of colorful paper in a rainbow gradient from warm "
            "reds and oranges on one wing to cool blues and purples on the other. Each small paper "
            "square is glued with small gaps between them like traditional mosaic tiles. "
            "The finished piece lies flat on a craft table. Colorful and graphic. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-pinwheel.webp",
        "prompt": (
            "Five colorful handmade paper pinwheels mounted on wooden skewer sticks arranged "
            "together in a small terracotta pot filled with dried beans. The pinwheels are made "
            "from double-sided decorative paper in pink and gold, blue and white, and coral and "
            "cream. Each pinwheel has a brad fastener at the center. The pot sits on a light wood "
            "table with soft natural light. Cheerful, playful display. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-desk-organizer.webp",
        "prompt": (
            "A handmade desk organizer made from paper tubes wrapped in coordinating washi tape "
            "and patterned paper. Five tubes of different heights are glued together in a cluster: "
            "three tall ones holding colored pencils, markers, and pens, and two shorter ones "
            "holding erasers and small supplies. The tubes are covered in matching blush and gold "
            "patterns. Photographed on a light wood desk from a slightly above angle. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-ninja-star.webp",
        "prompt": (
            "Two handmade origami ninja stars (shurikens) on a light wooden surface. "
            "Each star is made from two interlocking pieces of square paper without glue. "
            "One star uses royal blue and crisp white paper, the other uses burgundy and gold paper. "
            "The flat geometric star shapes show clean crisp folds and the interlocking mechanism "
            "is clearly visible. Photographed from slightly above on a wooden craft table. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-fortune-teller.webp",
        "prompt": (
            "A handmade paper fortune teller (cootie catcher) partially opened on a white wooden "
            "desk showing hand-written text on the inside flaps. The fortune teller is made from "
            "a decorated square sheet with colorful hand-drawn stars and doodles on the outer faces. "
            "The four inner sections are open showing short fun handwritten messages in different "
            "colors. A fine-point marker lies beside it. Friendly and creative look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-shadow-box.webp",
        "prompt": (
            "A handmade layered paper shadow box framed and photographed slightly from the front. "
            "Inside the white frame are five layers of cut paper silhouettes creating a 3D forest "
            "scene: the back layer is deep navy blue, then progressively lighter blue-grey layers "
            "show silhouetted pine trees and rolling hills, getting lighter toward the front. "
            "The depth between layers creates a beautiful shadow effect. "
            "Clean white frame, displayed on a light wall. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "paper-crafts-teens-letter-art.webp",
        "prompt": (
            "A handmade paper letter art piece showing a large capital letter A cut from thick "
            "white cardstock and completely covered in a colorful collage of torn washi tape strips, "
            "small patterned paper pieces, and magazine clippings in pink, gold, teal, and coral. "
            "Each section has a different pattern creating a mosaic-like surface. "
            "The finished letter leans against a white wall on a craft table. "
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
