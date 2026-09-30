"""Secure YouTube OAuth and AI image generation helpers. Secrets are configured only as server environment variables."""
import os, json, secrets
from datetime import datetime, timezone
from urllib.parse import urlencode
import httpx
from cryptography.fernet import Fernet
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from .db import connect
AUTH_ENDPOINT="https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT="https://oauth2.googleapis.com/token"
YT_CHANNELS="https://www.googleapis.com/youtube/v3/channels"
YT_SCOPE="https://www.googleapis.com/auth/youtube.readonly"
FRONTEND_URL=os.getenv("YOUTUBE_FRONTEND_URL","https://dimri-youtube-studio.onrender.com/youtube.html")
def _serializer():
    secret=os.getenv("DIMRI_OAUTH_STATE_SECRET")
    if not secret: raise RuntimeError("DIMRI_OAUTH_STATE_SECRET is not configured")
    return URLSafeTimedSerializer(secret,salt="dimri-youtube-oauth")
def _fernet():
    key=os.getenv("DIMRI_TOKEN_ENCRYPTION_KEY")
    if not key: raise RuntimeError("DIMRI_TOKEN_ENCRYPTION_KEY is not configured")
    return Fernet(key.encode())
def init_oauth_table():
    with connect() as c:
        c.execute("CREATE TABLE IF NOT EXISTS youtube_oauth (id INTEGER PRIMARY KEY CHECK(id=1), token_blob TEXT NOT NULL, connected_at TEXT NOT NULL)")
def oauth_start_url(redirect_uri):
    client=os.getenv("GOOGLE_CLIENT_ID")
    if not client or not os.getenv("GOOGLE_CLIENT_SECRET"): raise RuntimeError("Google OAuth credentials are not configured on the backend")
    state=_serializer().dumps({"nonce":secrets.token_urlsafe(24)})
    params={"client_id":client,"redirect_uri":redirect_uri,"response_type":"code","scope":YT_SCOPE,"access_type":"offline","include_granted_scopes":"true","prompt":"consent select_account","state":state}
    return AUTH_ENDPOINT+"?"+urlencode(params)
async def oauth_callback(code,state,redirect_uri):
    try: _serializer().loads(state,max_age=600)
    except (BadSignature,SignatureExpired) as e: raise ValueError("OAuth state expired or invalid") from e
    async with httpx.AsyncClient(timeout=30) as client:
        r=await client.post(TOKEN_ENDPOINT,data={"code":code,"client_id":os.environ["GOOGLE_CLIENT_ID"],"client_secret":os.environ["GOOGLE_CLIENT_SECRET"],"redirect_uri":redirect_uri,"grant_type":"authorization_code"},headers={"Accept":"application/json"})
        r.raise_for_status(); tokens=r.json()
    old=get_token_payload()
    if not tokens.get("refresh_token") and old: tokens["refresh_token"]=old.get("refresh_token")
    encrypted=_fernet().encrypt(json.dumps(tokens).encode()).decode()
    with connect() as c: c.execute("INSERT INTO youtube_oauth(id,token_blob,connected_at) VALUES(1,?,?) ON CONFLICT(id) DO UPDATE SET token_blob=excluded.token_blob,connected_at=excluded.connected_at",(encrypted,datetime.now(timezone.utc).isoformat()))
    return tokens
def get_token_payload():
    with connect() as c: row=c.execute("SELECT token_blob FROM youtube_oauth WHERE id=1").fetchone()
    if not row: return None
    return json.loads(_fernet().decrypt(row["token_blob"].encode()).decode())
def oauth_status():
    with connect() as c: row=c.execute("SELECT connected_at FROM youtube_oauth WHERE id=1").fetchone()
    return {"connected":bool(row),"connected_at":row["connected_at"] if row else None,"oauth_configured":bool(os.getenv("GOOGLE_CLIENT_ID") and os.getenv("GOOGLE_CLIENT_SECRET"))}
async def youtube_access_token():
    t=get_token_payload()
    if not t: raise RuntimeError("Google account is not connected")
    if t.get("expires_at",0)>datetime.now(timezone.utc).timestamp()+60 and t.get("access_token"): return t["access_token"]
    if not t.get("refresh_token"): raise RuntimeError("No refresh token; reconnect Google account")
    async with httpx.AsyncClient(timeout=30) as client:
        r=await client.post(TOKEN_ENDPOINT,data={"client_id":os.environ["GOOGLE_CLIENT_ID"],"client_secret":os.environ["GOOGLE_CLIENT_SECRET"],"refresh_token":t["refresh_token"],"grant_type":"refresh_token"},headers={"Accept":"application/json"})
        r.raise_for_status(); fresh=r.json()
    t.update(fresh); t["expires_at"]=datetime.now(timezone.utc).timestamp()+int(fresh.get("expires_in",3600))
    encrypted=_fernet().encrypt(json.dumps(t).encode()).decode()
    with connect() as c: c.execute("UPDATE youtube_oauth SET token_blob=? WHERE id=1",(encrypted,))
    return t["access_token"]
async def fetch_my_channels():
    token=await youtube_access_token()
    async with httpx.AsyncClient(timeout=30) as client:
        r=await client.get(YT_CHANNELS,params={"part":"snippet,statistics","mine":"true"},headers={"Authorization":"Bearer "+token})
        r.raise_for_status(); data=r.json()
    found=[]
    with connect() as c:
        for item in data.get("items",[]):
            snippet=item.get("snippet",{}); cid=item["id"]
            row={"channel_id":cid,"name":snippet.get("title","YouTube Channel"),"handle":snippet.get("customUrl",""),"channel_url":"https://www.youtube.com/channel/"+cid,"connection_state":"oauth","created_at":datetime.now(timezone.utc).isoformat()}
            c.execute("INSERT INTO youtube_channels(channel_id,name,handle,channel_url,connection_state,created_at) VALUES(:channel_id,:name,:handle,:channel_url,:connection_state,:created_at) ON CONFLICT(channel_id) DO UPDATE SET name=excluded.name,handle=excluded.handle,channel_url=excluded.channel_url,connection_state='oauth'",row)
            found.append({**row,"statistics":item.get("statistics",{})})
    return found
async def generate_image(prompt):
    key=os.getenv("OPENAI_API_KEY")
    if not key: raise RuntimeError("OPENAI_API_KEY is not configured on the backend")
    async with httpx.AsyncClient(timeout=120) as client:
        r=await client.post("https://api.openai.com/v1/images/generations",headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},json={"model":os.getenv("OPENAI_IMAGE_MODEL","gpt-image-1"),"prompt":prompt,"size":"1024x1024","n":1})
        r.raise_for_status(); data=r.json()
    first=data.get("data",[{}])[0]
    return {"b64_json":first.get("b64_json"),"url":first.get("url"),"revised_prompt":first.get("revised_prompt")}
init_oauth_table()
