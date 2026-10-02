"""Persona media generation for DIMRI AI. Provider calls are server-side only."""
import os
import base64
import binascii
import httpx

OPENAI_IMAGES_URL = "https://api.openai.com/v1/images/generations"

def persona_prompt(profile: dict, scene: str = "") -> str:
    fields = [
        f"adult {profile.get('gender','androgynous')} creator, age range {profile.get('age','Adult 25–34')}",
        f"face shape: {profile.get('face','Soft oval')}",
        f"skin tone: {profile.get('skin','Warm medium')}",
        f"eyes: {profile.get('eyes','Large almond')}, iris {profile.get('iris','Hazel')}",
        f"hair: {profile.get('hair','Long wavy')}, {profile.get('hairColor','Dark brown')}",
        f"body type: {profile.get('body','Balanced')}",
        f"wardrobe: {profile.get('outfit','Modern casual')}",
        f"expression: {profile.get('expression','Warm smile')}",
        f"pose: {profile.get('pose','3/4 portrait')}",
        f"background: {profile.get('background','Studio teal')}",
        f"lighting: {profile.get('lighting','Cinematic soft')}",
    ]
    scene_text = scene.strip() or "premium social-media creator portrait"
    return (
        "Create a photorealistic, original adult AI persona image for a creator brand. "
        "Preserve every listed identity attribute consistently. Natural human anatomy, realistic skin texture, "
        "realistic eyes and hair, premium commercial photography, no text, no watermark. "
        + "; ".join(fields) + f". Scene: {scene_text}."
    )

async def generate_persona_image(profile: dict, scene: str = "", size: str = "1024x1536") -> dict:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not configured on the backend")
    model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2.5-sunburst")
    prompt = persona_prompt(profile, scene)
    headers = {"Authorization": "Bearer " + key}
    reference = profile.get("reference_image_b64")
    timeout = httpx.Timeout(240.0, connect=20.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        if reference:
            raw = reference.strip()
            mime = "image/jpeg"
            if raw.startswith("data:"):
                header, sep, raw = raw.partition(",")
                if not sep:
                    raise ValueError("Invalid reference image data URL")
                mime = header[5:].split(";", 1)[0] or mime
            if mime not in {"image/jpeg", "image/png", "image/webp"}:
                raise ValueError("Reference must be JPEG, PNG or WebP")
            try:
                image_bytes = base64.b64decode(raw, validate=True)
            except (binascii.Error, ValueError) as exc:
                raise ValueError("Reference image is not valid base64 data") from exc
            if not image_bytes or len(image_bytes) > 12 * 1024 * 1024:
                raise ValueError("Reference image must be under 12 MB")
            ext = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}[mime]
            response = await client.post(
                "https://api.openai.com/v1/images/edits",
                headers=headers,
                data={"model": model, "prompt": prompt, "size": size, "n": "1"},
                files={"image": (f"persona-reference.{ext}", image_bytes, mime)},
            )
        else:
            response = await client.post(
                "https://api.openai.com/v1/images/generations",
                headers={**headers, "Content-Type": "application/json"},
                json={"model": model, "prompt": prompt, "size": size, "n": 1},
            )
        if response.status_code >= 400:
            raise RuntimeError(f"OpenAI image request failed ({response.status_code}). Check model access, billing, and image input requirements.")
        data = response.json()

    item = (data.get("data") or [{}])[0]
    image_data = item.get("b64_json")
    if not image_data:
        raise RuntimeError("Image provider returned no image data")
    return {
        "model": model,
        "prompt": prompt,
        "b64_json": image_data,
        "revised_prompt": item.get("revised_prompt"),
        "mode": "edit" if reference else "generate",
    }
