"""Persona media generation for DIMRI AI. Provider calls are server-side only."""
import os
import base64
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
    model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2")
    payload = {"model": model, "prompt": persona_prompt(profile, scene), "size": size, "n": 1}
    async with httpx.AsyncClient(timeout=180) as client:
        r = await client.post(
            OPENAI_IMAGES_URL,
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            json=payload,
        )
        if r.status_code >= 400:
            raise RuntimeError(f"Image provider error {r.status_code}: {r.text[:1200]}")
        data = r.json()
    item = (data.get("data") or [{}])[0]
    return {
        "model": model,
        "prompt": payload["prompt"],
        "b64_json": item.get("b64_json"),
        "url": item.get("url"),
        "revised_prompt": item.get("revised_prompt"),
    }
