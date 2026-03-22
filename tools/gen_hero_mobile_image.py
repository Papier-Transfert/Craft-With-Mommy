#!/usr/bin/env python3
import io, os, sys, time, logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path("/var/www/craft-with-mommy")
OUTPUT_PATH = BASE_DIR / "images" / "hero-mobile.webp"
TARGET_W, TARGET_H = 900, 900   # square, ideal for mobile portrait block

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")

PROMPT = (
    "A warm, natural lifestyle photograph for a mobile website hero. "
    "A young American mother, late 20s to early 30s, casual relaxed style, hair down or loosely pulled back, "
    "wearing a soft cozy top, sitting close at a light wooden table with her young daughter, around 3-4 years old. "
    "They are doing a simple, colorful paper craft together — making a paper rainbow with colorful strips of "
    "construction paper, glue sticks, and simple craft supplies. The finished craft is bright and cheerful. "
    "The mother and daughter are both smiling and laughing naturally, fully engaged and happy. "
    "Close, intimate framing — we see their faces, hands, and the craft clearly. "
    "The composition should feel warm and close, not wide or distant. "
    "Table surface is clean and inviting with a few colorful paper strips, a glue stick, and the cute rainbow craft. "
    "Background: warm, softly blurred cozy home interior — a sofa or shelves visible, nothing distracting. "
    "Lighting: soft, warm golden natural light from the side, warm color temperature, gentle and flattering. "
    "Mood: cozy, joyful, low-stress, genuine family connection. "
    "Square composition 1:1 ratio. Close and intimate framing. "
    "No AI artifacts, no distorted hands or fingers, no plastic skin texture. "
    "True photographic realism, premium quality, natural and heartfelt expressions."
)

def generate_image(client, prompt, output_path):
    try:
        from google.genai import types as genai_types
        from PIL import Image as PILImage
        full_prompt = f"{prompt} Aspect ratio 1:1. Square format."
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
            log.warning("No image data returned.")
            return False
        with PILImage.open(io.BytesIO(image_bytes)) as img:
            resized = img.resize((TARGET_W, TARGET_H), PILImage.LANCZOS)
            resized.save(output_path, "WEBP", quality=85, method=6)
        log.info(f"Saved: {output_path} ({TARGET_W}x{TARGET_H}px, {output_path.stat().st_size // 1024}KB)")
        return True
    except Exception as exc:
        log.warning(f"Failed: {exc}")
        return False

def main():
    from google import genai
    from PIL import Image
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        log.error("GOOGLE_API_KEY not set"); sys.exit(1)
    client = genai.Client(api_key=api_key)
    for attempt in range(1, 4):
        if attempt > 1:
            log.info(f"Retry {attempt}/3..."); time.sleep(4)
        if generate_image(client, PROMPT, OUTPUT_PATH):
            log.info("Done."); return
    log.error("All attempts failed."); sys.exit(1)

if __name__ == "__main__":
    main()
