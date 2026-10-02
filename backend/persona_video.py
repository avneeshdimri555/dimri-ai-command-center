"""Sora 2 video adapter for DIMRI AI Persona Studio."""
import os, base64, httpx

VIDEOS_URL="https://api.openai.com/v1/videos"

def video_prompt(profile: dict, scene: str="") -> str:
    attrs=[
        f"adult {profile.get('gender','androgynous')} creator",
        f"face {profile.get('face','Soft oval')}",
        f"skin {profile.get('skin','Warm medium')}",
        f"eyes {profile.get('eyes','Large almond')} {profile.get('iris','Hazel')} irises",
        f"hair {profile.get('hair','Long wavy')} {profile.get('hairColor','Dark brown')}",
        f"body {profile.get('body','Balanced')}",
        f"wardrobe {profile.get('outfit','Modern casual')}",
        f"expression {profile.get('expression','Warm smile')}",
    ]
    return "Photorealistic premium social creator video. Maintain the same adult persona identity attributes throughout the clip. Natural movement, realistic anatomy, realistic skin and hair, commercial cinematography, no text or watermark. "+"; ".join(attrs)+". Scene: "+(scene.strip() or "creator walking toward camera and smiling naturally.")

async def create_persona_video(profile: dict, scene: str="", seconds: str="4", reference_b64: str|None=None, size: str="720x1280") -> dict:
    key=os.getenv("OPENAI_API_KEY")
    if not key: raise RuntimeError("OPENAI_API_KEY is not configured on the backend")
    model=os.getenv("OPENAI_VIDEO_MODEL","sora-2")
    data={"model":model,"prompt":video_prompt(profile,scene),"seconds":seconds,"size":size}
    headers={"Authorization":"Bearer "+key}
    async with httpx.AsyncClient(timeout=60) as client:
        if reference_b64:
            raw=reference_b64.split(",",1)[-1]
            try: image_bytes=base64.b64decode(raw)
            except Exception as exc: raise RuntimeError("Invalid reference image") from exc
            files={"input_reference":("persona-reference.png",image_bytes,"image/png")}
            r=await client.post(VIDEOS_URL,headers=headers,data=data,files=files)
        else:
            r=await client.post(VIDEOS_URL,headers=headers,data=data)
        if r.status_code>=400: raise RuntimeError(f"Video provider error {r.status_code}: {r.text[:1200]}")
        return r.json()

async def get_persona_video(video_id: str) -> dict:
    key=os.getenv("OPENAI_API_KEY")
    if not key: raise RuntimeError("OPENAI_API_KEY is not configured on the backend")
    async with httpx.AsyncClient(timeout=30) as client:
        r=await client.get(f"{VIDEOS_URL}/{video_id}",headers={"Authorization":"Bearer "+key})
        if r.status_code>=400: raise RuntimeError(f"Video status error {r.status_code}: {r.text[:1200]}")
        return r.json()
