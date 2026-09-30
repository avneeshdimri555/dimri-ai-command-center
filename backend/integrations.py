import os

INTEGRATIONS = [
    {"id":"youtube","name":"YouTube Data + Analytics","pillar":"DIMRI Media","mode":"oauth","configured_keys":["YOUTUBE_CLIENT_ID","YOUTUBE_CLIENT_SECRET","YOUTUBE_REFRESH_TOKEN"]},
    {"id":"instagram","name":"Instagram / Meta","pillar":"DIMRI Media","mode":"oauth","configured_keys":["INSTAGRAM_ACCESS_TOKEN"]},
    {"id":"pinterest","name":"Pinterest API","pillar":"DIMRI Digital Commerce","mode":"oauth","configured_keys":["PINTEREST_ACCESS_TOKEN"]},
    {"id":"google-play","name":"Google Play Developer","pillar":"DIMRI Apps","mode":"service-account","configured_keys":["GOOGLE_PLAY_SERVICE_ACCOUNT_JSON"]},
    {"id":"app-store-connect","name":"Apple App Store Connect","pillar":"DIMRI Apps","mode":"api-key","configured_keys":["APPLE_APP_STORE_CONNECT_KEY_ID","APPLE_APP_STORE_CONNECT_ISSUER_ID","APPLE_APP_STORE_CONNECT_PRIVATE_KEY"]},
    {"id":"affiliate","name":"Affiliate Networks","pillar":"DIMRI Digital Commerce","mode":"partner-api-or-feed","configured_keys":["AFFILIATE_NETWORK_TOKEN"]},
    {"id":"stripe","name":"Stripe","pillar":"Shared Commerce","mode":"api","configured_keys":[]},
]

def integration_status():
    out=[]
    for item in INTEGRATIONS:
        configured=all(bool(os.getenv(k)) for k in item["configured_keys"]) if item["configured_keys"] else False
        out.append({**item,"configured":configured})
    return out
