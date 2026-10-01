#!/usr/bin/env python3
"""Static QA checks for the single-repository DIMRI AI Persona Studio demo."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

FILE = Path(__file__).resolve().parents[1] / "persona-studio.html"

class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.nav_targets = []
        self.page_ids = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
            if a["id"].startswith("page-"):
                self.page_ids.append(a["id"][5:])
        if a.get("data-page"):
            self.nav_targets.append(a["data-page"])

def fail(message):
    print("FAIL:", message)
    return False

def main():
    html = FILE.read_text(encoding="utf-8")
    parser = Markup()
    parser.feed(html)
    ok = True

    duplicates = sorted({x for x in parser.ids if parser.ids.count(x) > 1})
    if duplicates:
        ok = fail("duplicate HTML ids: " + ", ".join(duplicates)) and ok
    else:
        print("PASS: HTML ids are unique")

    missing = sorted(set(parser.nav_targets) - set(parser.page_ids))
    if missing:
        ok = fail("navigation target without page: " + ", ".join(missing)) and ok
    else:
        print(f"PASS: {len(set(parser.nav_targets))} navigation targets map to pages")

    required_functions = [
        "renderStep", "collect", "stepMove", "savePersona", "editPersona",
        "newPersona", "renderPersonas", "renderPlans", "planAction",\n        "saveProductDNA", "editProductDNA", "deleteProductDNA", "renderProductDNA",
    ]
    for name in required_functions:
        if not re.search(r"function\s+" + re.escape(name) + r"\s*\(", html):
            ok = fail("missing function: " + name) and ok
    if ok:
        print("PASS: creator and workspace action functions are present")

    selects = re.findall(r"\{id:'([^']+)',label:'([^']+)',type:'select',opts:\[(.*?)\]\}", html, re.S)
    if len(selects) < 30:
        ok = fail(f"expected detailed dropdown coverage; found {len(selects)} select definitions") and ok
    else:
        print(f"PASS: {len(selects)} detailed dropdown definitions found")
    empty = [field for field, label, opts in selects if not re.search(r"'[^']+'", opts)]
    if empty:
        ok = fail("dropdowns without options: " + ", ".join(empty)) and ok
    else:
        print("PASS: dropdown definitions include options")

    for marker, label in [
        ("TESTER MODE · MOCK OUTPUTS", "explicit demo mode"),
        ("Persona DNA", "Persona DNA workflow"),
        ("Voice Studio", "Voice Studio"),
        ("Rights & Safety", "rights and safety"),\n        ("Product DNA", "Product DNA workspace"),
    ]:
        if marker not in html:
            ok = fail("missing " + label) and ok
    if ok:
        print("PASS: key product and demo labels are present")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
