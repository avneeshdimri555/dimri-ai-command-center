APPS = [
    {"name":"VANI","type":"AI app","status":"building","pillar":"DIMRI Apps","department":"Product","description":"AI voice/language companion product."},
    {"name":"DermaVeda","type":"AI app","status":"planned","pillar":"DIMRI Apps","department":"Product","description":"AI skin/face analysis and personalized skincare experience."},
    {"name":"YOU AI","type":"AI app","status":"planned","pillar":"DIMRI Apps","department":"Product","description":"Personal AI assistant / consumer AI product concept."},
]

PILLARS = [
    {"id":"media","name":"DIMRI Media","icon":"🎬","focus":"YouTube + Instagram + Ghost Mode + automated content operations"},
    {"id":"commerce","name":"DIMRI Digital Commerce","icon":"🛍️","focus":"E-books, stickers, digital goods, blogging, Pinterest, affiliate and marketplaces"},
    {"id":"apps","name":"DIMRI Apps","icon":"📱","focus":"Build, monitor, market and grow VANI, DermaVeda, YOU AI and future apps"},
    {"id":"games","name":"DIMRI Games","icon":"🎮","focus":"Game development, publishing, UA, monetization, analytics and live ops"},
    {"id":"products","name":"DIMRI Products & Services","icon":"🚀","focus":"50 productized AI offers and commercial services"},
]

def list_apps(): return APPS
def list_pillars(): return PILLARS
