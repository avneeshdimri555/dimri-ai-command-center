from datetime import datetime, timezone
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .brain import memory, create_workflow, route_command
from .task_queue import queue
from .db import audit_events
from .app_registry import list_apps, list_pillars
from .digital_products import create_product, list_products, publish_plan
from .marketplaces import marketplace_status
from .integrations import integration_status
from .youtube_studio import list_channels, add_channel, list_content, create_content, update_content
from .youtube_oauth import oauth_start_url, oauth_callback, oauth_status, fetch_my_channels, generate_image

app = FastAPI(title="DIMRI AI Company OS", version="0.4.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class Command(BaseModel):
    command: str
    priority: str = "normal"

class Workflow(BaseModel):
    name: str
    objective: str
    department: str | None = None

class TaskUpdate(BaseModel):
    status: str
    result: str | None = None

class YouTubeChannel(BaseModel):
    name: str
    handle: str = ""
    channel_url: str = ""

class YouTubeContent(BaseModel):
    channel_id: str | None = None
    content_type: str = "short"
    topic: str
    title: str
    description: str = ""
    script: str = ""
    visual_prompt: str = ""

class YouTubeContentUpdate(BaseModel):
    status: str

class DigitalProduct(BaseModel):
    title: str
    product_type: str = "digital-sticker"
    description: str = ""
    price: float | None = None
    currency: str = "USD"
    asset_path: str | None = None
    marketplaces: str = "gumroad"

@app.get("/api/health")
def health() -> dict[str, Any]:
    return {"ok": True, "service": "dimri-ai-company-os", "version":"0.4.0", "time": datetime.now(timezone.utc).isoformat()}

@app.get("/api/brain")
def brain() -> dict[str, Any]:
    return {"name":"DIMRI Company Brain","state":"persistent-memory","memory":memory.context(),"routing_capabilities":8}

@app.post("/api/brain/route")
def brain_route(command: Command) -> dict[str, Any]:
    return {"accepted":True,"command":command.command,"priority":command.priority,"routes":route_command(command.command)}

@app.post("/api/workflows")
def create_company_workflow(workflow: Workflow) -> dict[str, Any]:
    result = create_workflow(workflow.objective)
    result["name"] = workflow.name
    result["department"] = workflow.department
    task = queue.enqueue(workflow.objective, "normal", result["routes"][0]["agent"] if result["routes"] else "ceo")
    result["task"] = task
    return result

@app.post("/api/commands")
def create_command(command: Command) -> dict[str, Any]:
    result = create_workflow(command.command, command.priority)
    agent = result["routes"][0]["agent"] if result["routes"] else "ceo"
    task = queue.enqueue(command.command, command.priority, agent)
    return {"accepted": True, "status": "queued", "workflow": result, "task": task}

@app.get("/api/tasks")
def tasks(status: str | None = None) -> dict[str, Any]:
    return {"tasks": queue.list(status), "count": len(queue.list(status))}

@app.patch("/api/tasks/{task_id}")
def task_update(task_id: str, update: TaskUpdate) -> dict[str, Any]:
    task = queue.update(task_id, update.status, update.result)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/api/memory")
def remember(kind: str, content: str, source: str = "founder") -> dict[str, Any]:
    return memory.remember(kind, content, source)

@app.get("/api/memory")
def get_memory() -> dict[str, Any]:
    return memory.context()

@app.get("/api/audit")
def audit(limit: int = 50) -> dict[str, Any]:
    return {"events": audit_events(limit)}

@app.get("/api/apps")
def apps() -> dict[str, Any]:
    return {"apps": list_apps()}

@app.get("/api/pillars")
def pillars() -> dict[str, Any]:
    return {"parent_company":"Aishani Enterprises","operating_studio":"DIMRI Studio","pillars":list_pillars()}

@app.get("/api/marketplaces")
def marketplaces() -> dict[str, Any]:
    return {"marketplaces": marketplace_status()}

@app.get("/api/integrations")
def integrations() -> dict[str, Any]:
    return {"integrations": integration_status()}

@app.get("/api/digital-products")
def digital_products() -> dict[str, Any]:
    return {"products": list_products()}

@app.post("/api/digital-products")
def digital_product_create(product: DigitalProduct) -> dict[str, Any]:
    return create_product(**product.model_dump())

@app.post("/api/digital-products/{product_id}/publish-plan")
def digital_product_publish_plan(product_id: str) -> dict[str, Any]:
    result = publish_plan(product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Digital product not found")
    return result

@app.get("/api/company")
def company() -> dict[str, Any]:
    return {"name":"DIMRI AI","mode":"Founder Controlled","departments":8,"planned_agents":90,"products_services":50,
        "platforms":["web","mobile","telegram"],
        "state":{"persistent_memory":True,"durable_task_queue":True,"real_agent_execution":False},
        "principles":{"ghost_mode_real_info_first":True,"source_verification":True,"founder_approval_for_consequential_actions":True,"no_impersonation":True,"no_bulk_spam":True}}


@app.get("/api/youtube/status")
def youtube_status() -> dict[str, Any]:
    channels = list_channels()
    return {"workspace": "ready", "oauth_configured": False, "channel_count": len(channels),
            "note": "Channels are manual registry entries until Google OAuth is implemented and authorized."}

@app.get("/api/youtube/channels")
def youtube_channels() -> dict[str, Any]:
    return {"channels": list_channels()}

@app.post("/api/youtube/channels")
def youtube_add_channel(channel: YouTubeChannel) -> dict[str, Any]:
    try:
        return {"channel": add_channel(**channel.model_dump())}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/api/youtube/content")
def youtube_content() -> dict[str, Any]:
    return {"content": list_content()}

@app.post("/api/youtube/content")
def youtube_create_content(content: YouTubeContent) -> dict[str, Any]:
    try:
        return {"content": create_content(**content.model_dump())}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.patch("/api/youtube/content/{content_id}")
def youtube_update_content(content_id: str, update: YouTubeContentUpdate) -> dict[str, Any]:
    try:
        result = update_content(content_id, update.status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not result:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"content": result}


@app.get("/api/youtube/oauth/status")
def youtube_oauth_status() -> dict[str, Any]:
    return oauth_status()

@app.get("/api/youtube/oauth/start")
def youtube_oauth_start(request):
    from fastapi.responses import RedirectResponse
    try:
        redirect_uri=str(request.base_url).rstrip("/")+"/api/youtube/oauth/callback"
        return RedirectResponse(oauth_start_url(redirect_uri),status_code=302)
    except RuntimeError as exc:
        raise HTTPException(status_code=503,detail=str(exc))

@app.get("/api/youtube/oauth/callback")
async def youtube_oauth_finish(request):
    from fastapi.responses import RedirectResponse
    code=request.query_params.get("code"); state=request.query_params.get("state")
    if request.query_params.get("error"):
        return RedirectResponse("https://dimri-youtube-studio.onrender.com/youtube.html?google=denied")
    if not code or not state: raise HTTPException(status_code=400,detail="Missing OAuth code/state")
    redirect_uri=str(request.base_url).rstrip("/")+"/api/youtube/oauth/callback"
    try:
        await oauth_callback(code,state,redirect_uri)
        await fetch_my_channels()
        return RedirectResponse("https://dimri-youtube-studio.onrender.com/youtube.html?google=connected")
    except Exception:
        return RedirectResponse("https://dimri-youtube-studio.onrender.com/youtube.html?google=error")

@app.post("/api/youtube/oauth/sync")
async def youtube_oauth_sync() -> dict[str, Any]:
    try: return {"channels":await fetch_my_channels()}
    except Exception as exc: raise HTTPException(status_code=503,detail=str(exc))

@app.post("/api/youtube/images/generate")
async def youtube_image_generate(payload: dict[str,str]) -> dict[str, Any]:
    prompt=(payload.get("prompt") or "").strip()
    if not prompt: raise HTTPException(status_code=400,detail="Prompt is required")
    try: return await generate_image(prompt)
    except Exception as exc: raise HTTPException(status_code=503,detail=str(exc))
