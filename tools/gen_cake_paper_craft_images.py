#!/usr/bin/env python3
"""Generate all images for cake-paper-craft.html."""
import io, os, time, logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR  = BASE_DIR / "blog" / "images" / "cake-paper-craft"
TARGET_W, TARGET_H = 1200, 900
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

STYLE = (
    "Realistic photo style. Warm natural daylight from a window. "
    "Light wood craft table surface. "
    "Clean, cozy, family-friendly atmosphere. Landscape orientation 4:3. "
    "No cartoon elements. Real craft materials only. "
    "Charming and slightly imperfect, clearly handmade. Pinterest-worthy. "
    "The image must fill the full frame edge to edge with no white borders or letterboxing."
)

IMAGES = [
    {
        "filename": "cake-paper-craft.webp",
        "prompt": (
            "A finished three tier handmade paper birthday cake standing on a light wood craft table. "
            "Bottom tier is pastel pink cardstock about 4 inches wide, middle tier mint green cardstock about 3 inches wide, "
            "top tier pale yellow cardstock about 2 inches wide. Each tier is a cylinder with a flat circular cardstock top "
            "slightly overhanging the sides like frosting. A delicate floral washi tape band wraps around the bottom of each tier. "
            "Tiny pink, red and white pom poms are glued around the top edge of each tier like cherries and sprinkles. "
            "A small yellow rolled paper candle with an orange teardrop paper flame stands in the center of the top tier. "
            "Clean cozy hero shot. Cardstock construction is clearly visible. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cake-paper-craft-mom-child.webp",
        "prompt": (
            "A young American mom in her early thirties and her happy young child about 5 years old sitting together "
            "at a light wood craft table. Spread on the table are flat pastel cardstock sheets in pink, mint green and pale yellow, "
            "child-safe scissors with pointed tips, a roll of floral washi tape, a small pile of tiny pom poms, "
            "and a glue stick. They are smiling, just starting to roll a strip of pink cardstock into a tube "
            "to begin building a tiered paper birthday cake. Warm sunlit kitchen feel. Real human faces, natural skin tones. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cake-paper-craft-cut-strips.webp",
        "prompt": (
            "A flat overhead photo on a light wood craft table of exactly three rectangle cardstock strips laid out side by side. "
            "Each strip is 3 inches tall. The largest strip is pastel pink cardstock about 12 inches wide on the left. "
            "The medium strip is mint green cardstock about 9 inches wide in the middle. "
            "The smallest strip is pale yellow cardstock about 6 inches wide on the right. "
            "Beside the strips are a clear acrylic ruler, a sharp pencil, and a pair of child safe scissors with pointed tips. "
            "The strips are clearly cut by hand, slightly imperfect edges. No rolled tubes yet, only flat strips. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cake-paper-craft-rolled-tiers.webp",
        "prompt": (
            "Three pastel cardstock cylinders standing upright on a light wood craft table. "
            "The largest cylinder on the left is pastel pink, about 4 inches wide and 3 inches tall. "
            "The medium cylinder in the middle is mint green, about 3 inches wide and 3 inches tall. "
            "The smallest cylinder on the right is pale yellow, about 2 inches wide and 3 inches tall. "
            "Each cylinder has a vertical seam closed with a thin piece of patterned washi tape running top to bottom. "
            "No tops on them yet, the cylinder openings are visible from above. No decorations yet. "
            "A pencil and three flat cardstock sheets sit beside them, ready to become the tops. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cake-paper-craft-cut-circles.webp",
        "prompt": (
            "A flat overhead photo on a light wood craft table showing the three pastel cardstock cylinders "
            "still empty and standing nearby, alongside three flat cardstock circles in matching colors. "
            "The largest circle is pastel pink about 4.5 inches across, the medium circle is mint green about 3.5 inches across, "
            "the smallest circle is pale yellow about 2.5 inches across. "
            "Each circle is slightly larger than its matching cylinder's top opening. "
            "A pencil sits beside the circles. The edges of the circles are clearly hand cut, slightly imperfect. "
            "No decorations yet, no candle, no pom poms, no washi tape on the tiers. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cake-paper-craft-tops-glued.webp",
        "prompt": (
            "Three short pastel cardstock cylinders standing upright on a light wood craft table, "
            "each one now topped with a matching slightly larger flat circle glued flat on top. "
            "The largest pink cylinder has a pink circle on top with a small overhang all around. "
            "The medium mint green cylinder has a mint circle on top. "
            "The smallest pale yellow cylinder has a yellow circle on top. "
            "They look like three separate small cake tiers, NOT stacked, side by side from largest to smallest. "
            "Vertical washi tape seam still visible on each cylinder side. No pom poms, no candle, no frosting bands yet. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cake-paper-craft-stacked-tiers.webp",
        "prompt": (
            "A plain three tier handmade paper cake assembled and standing on a light wood craft table. "
            "Bottom tier is pastel pink cylinder topped with a pink circle, about 4 inches wide. "
            "Middle tier is mint green cylinder topped with a mint circle, about 3 inches wide, centered on top of the pink tier. "
            "Top tier is pale yellow cylinder topped with a pale yellow circle, about 2 inches wide, centered on top of the mint tier. "
            "All three tiers stacked centered and aligned, standing upright. "
            "No decorations yet at all. No washi tape bands wrapping the tiers, no pom poms, no candle. "
            "Just the plain stacked cardstock tiers. Clean, simple, slightly imperfect handmade look. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cake-paper-craft-decorated.webp",
        "prompt": (
            "A three tier handmade paper birthday cake standing on a light wood craft table, now decorated. "
            "Bottom tier pastel pink, middle tier mint green, top tier pale yellow. "
            "A delicate floral washi tape band wraps around the bottom of each tier just where each cylinder meets the circle below it. "
            "Tiny pink, red, and white pom poms are glued around the top edge of every tier like cherries and sprinkles. "
            "Slightly imperfect placement, clearly child decorated. "
            "No candle on top yet. The cake is decorated but unlit. "
            f"{STYLE}"
        ),
    },
    {
        "filename": "cake-paper-craft-finished-candle.webp",
        "prompt": (
            "A completed three tier handmade paper birthday cake on a light wood craft table. "
            "Bottom tier pastel pink, middle tier mint green, top tier pale yellow. "
            "Washi tape frosting bands wrap each tier. Tiny pink, red, and white pom poms glued around each tier edge. "
            "A small yellow rolled paper candle stands upright in the very center of the top tier, with a "
            "small orange teardrop paper flame glued to its top. "
            "Final celebratory shot, ready for pretend play. Warm cozy kitchen lighting. "
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
