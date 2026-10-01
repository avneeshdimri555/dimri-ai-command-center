import os,json,secrets,base64,hashlib
from datetime import datetime,timezone
from urllib.parse import urlencode
import httpx
from .db import connect

def _mv(): return os.getenv("META_GRAPH_VERSION","v24.0")
def _mu(p): return "https://graph.facebook.com/"+_mv()+p
def _load(t):
    with connect() as c:
        r=c.execute("SELECT token_blob FROM social_tokens WHERE provider=?",(t,)).fetchone()
    return json.loads(r["token_blob"]) if r else None
def _save(t,x):
    with connect() as c:
        c.execute("INSERT INTO social_tokens(provider,token_blob,updated_at) VALUES(?,?,?) ON CONFLICT(provider) DO UPDATE SET token_blob=excluded.token_blob,updated_at=excluded.updated_at",(t,json.dumps(x),datetime.now(timezone.utc).isoformat()))
def init_social():
    with connect() as c:
        c.execute("CREATE TABLE IF NOT EXISTS social_tokens(provider TEXT PRIMARY KEY,token_blob TEXT NOT NULL,updated_at TEXT NOT NULL)")
        c.execute("CREATE TABLE IF NOT EXISTS social_states(state TEXT PRIMARY KEY,provider TEXT NOT NULL,redirect_uri TEXT NOT NULL,verifier TEXT,created_at TEXT NOT NULL)")
def meta_configured(): return bool(os.getenv("META_APP_ID") and os.getenv("META_APP_SECRET"))
def meta_start(redirect_uri):
    if not meta_configured(): raise RuntimeError("META_APP_ID and META_APP_SECRET required")
    state=secrets.token_urlsafe(32)
    with connect() as c: c.execute("INSERT INTO social_states VALUES(?,?,?,?,?)",(state,"meta",redirect_uri,None,datetime.now(timezone.utc).isoformat()))
    scope="pages_show_list,pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish"
    return "https://www.facebook.com/"+_mv()+"/dialog/oauth?"+urlencode({"client_id":os.environ["META_APP_ID"],"redirect_uri":redirect_uri,"state":state,"scope":scope})
async def meta_callback(code,state,redirect_uri):
    with connect() as c: row=c.execute("SELECT * FROM social_states WHERE state=? AND provider='meta'",(state,)).fetchone()
    if not row or row["redirect_uri"]!=redirect_uri: raise ValueError("Invalid Meta OAuth state")
    async with httpx.AsyncClient(timeout=30) as cl:
        r=await cl.get("https://graph.facebook.com/"+_mv()+"/oauth/access_token",params={"client_id":os.environ["META_APP_ID"],"client_secret":os.environ["META_APP_SECRET"],"redirect_uri":redirect_uri,"code":code}); r.raise_for_status()
    _save("meta",r.json())
    with connect() as c: c.execute("DELETE FROM social_states WHERE state=?",(state,))
async def meta_pages():
    t=_load("meta")
    if not t: raise RuntimeError("Meta not connected")
    async with httpx.AsyncClient(timeout=30) as cl:
        r=await cl.get(_mu("/me/accounts"),params={"access_token":t["access_token"],"fields":"id,name,access_token,instagram_business_account"}); r.raise_for_status()
    return r.json().get("data",[])
async def facebook_publish(page_id,message,link=None):
    p=next((x for x in await meta_pages() if x["id"]==page_id),None)
    if not p: raise ValueError("Facebook Page not available")
    data={"message":message,"access_token":p["access_token"]}
    if link: data["link"]=link
    async with httpx.AsyncClient(timeout=30) as cl:
        r=await cl.post(_mu("/"+page_id+"/feed"),data=data); r.raise_for_status(); return r.json()
async def instagram_publish_image(ig_id,image_url,caption=""):
    p=next((x for x in await meta_pages() if x.get("instagram_business_account",{}).get("id")==ig_id),None)
    if not p: raise ValueError("Instagram professional account not available")
    token=p["access_token"]
    async with httpx.AsyncClient(timeout=60) as cl:
        r=await cl.post(_mu("/"+ig_id+"/media"),data={"image_url":image_url,"caption":caption,"access_token":token}); r.raise_for_status()
        r=await cl.post(_mu("/"+ig_id+"/media_publish"),data={"creation_id":r.json()["id"],"access_token":token}); r.raise_for_status(); return r.json()
def x_configured(): return bool(os.getenv("X_CLIENT_ID") and os.getenv("X_CLIENT_SECRET"))
def x_start(redirect_uri):
    if not x_configured(): raise RuntimeError("X_CLIENT_ID and X_CLIENT_SECRET required")
    verifier=base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
    challenge=base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state=secrets.token_urlsafe(32)
    with connect() as c: c.execute("INSERT INTO social_states VALUES(?,?,?,?,?)",(state,"x",redirect_uri,verifier,datetime.now(timezone.utc).isoformat()))
    return "https://twitter.com/i/oauth2/authorize?"+urlencode({"response_type":"code","client_id":os.environ["X_CLIENT_ID"],"redirect_uri":redirect_uri,"scope":"tweet.read tweet.write users.read offline.access","state":state,"code_challenge":challenge,"code_challenge_method":"S256"})
async def x_callback(code,state,redirect_uri):
    with connect() as c: row=c.execute("SELECT * FROM social_states WHERE state=? AND provider='x'",(state,)).fetchone()
    if not row or row["redirect_uri"]!=redirect_uri: raise ValueError("Invalid X OAuth state")
    async with httpx.AsyncClient(timeout=30) as cl:
        r=await cl.post("https://api.x.com/2/oauth2/token",data={"code":code,"grant_type":"authorization_code","client_id":os.environ["X_CLIENT_ID"],"redirect_uri":redirect_uri,"code_verifier":row["verifier"]},auth=(os.environ["X_CLIENT_ID"],os.environ["X_CLIENT_SECRET"])); r.raise_for_status()
    _save("x",r.json())
    with connect() as c: c.execute("DELETE FROM social_states WHERE state=?",(state,))
async def x_publish(text):
    t=_load("x")
    if not t: raise RuntimeError("X not connected")
    async with httpx.AsyncClient(timeout=30) as cl:
        r=await cl.post("https://api.x.com/2/tweets",json={"text":text},headers={"Authorization":"Bearer "+t["access_token"]}); r.raise_for_status(); return r.json()
def status():
    m=_load("meta"); x=_load("x")
    return {"meta":{"configured":meta_configured(),"connected":bool(m)}, "facebook":{"configured":meta_configured(),"connected":bool(m)}, "instagram":{"configured":meta_configured(),"connected":bool(m)}, "x":{"configured":x_configured(),"connected":bool(x)}}
init_social()
