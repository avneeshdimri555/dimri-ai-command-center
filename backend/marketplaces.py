import os

class MarketplaceAdapter:
    def __init__(self, name: str): self.name=name
    def status(self): return {"marketplace":self.name,"configured":False,"mode":"adapter-ready"}

class EbayAdapter(MarketplaceAdapter):
    def __init__(self): super().__init__("eBay")
    def status(self):
        return {"marketplace":"eBay","configured":bool(os.getenv("EBAY_CLIENT_ID") and os.getenv("EBAY_CLIENT_SECRET")),
                "mode":"oauth-required","publish_requires_founder_approval":True}

class GumroadAdapter(MarketplaceAdapter):
    def __init__(self): super().__init__("Gumroad")
    def status(self):
        return {"marketplace":"Gumroad","configured":bool(os.getenv("GUMROAD_ACCESS_TOKEN")),
                "mode":"token-required","publish_requires_founder_approval":True}

class ShopifyAdapter(MarketplaceAdapter):
    def __init__(self): super().__init__("Shopify")
    def status(self):
        return {"marketplace":"Shopify","configured":bool(os.getenv("SHOPIFY_STORE_DOMAIN") and os.getenv("SHOPIFY_ACCESS_TOKEN")),
                "mode":"admin-api-required","publish_requires_founder_approval":True}

def marketplace_status():
    return [EbayAdapter().status(),GumroadAdapter().status(),ShopifyAdapter().status()]
