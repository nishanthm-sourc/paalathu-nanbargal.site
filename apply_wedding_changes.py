#!/usr/bin/env python3
"""Apply all wedding site corrections to ajith_anitha_wedding_v2.html."""
from pathlib import Path
import re

HTML = Path(__file__).resolve().parent / "ajith_anitha_wedding_v2.html"

NAME_TO_URL = {
    "Vicky": "https://www.instagram.com/vikeerthi?igsh=MWk5dm1lZTR5amNuaA==",
    "Nishanth": "https://www.instagram.com/mr_peradox?igsh=bTM5ZHE0OTN5Mm92",
    "Sridhar": "https://www.instagram.com/sridharthomas0212?igsh=NWkya2dhcXpzaGd6",
    "Dhanasekaran": "https://www.instagram.com/itz_dhana001?igsh=MXhxMHJzencza2RuaQ==",
    "Chinna": "https://www.instagram.com/chinnappar_chinn?igsh=ZmNoazkwYjU3anJ0",
    "Ajay": "https://www.instagram.com/ajayjustin_?igsh=MWJidGl2MmhkdWdjeA==",
    "Aswinth": "https://www.instagram.com/its_aswinth?igsh=MWx1eHZsd3FmNmFzYg==",
    "Ajith Kumar": "https://www.instagram.com/v.i.p_ponraj?igsh=MW80cW1zOG12NG92cg==",
}

LOCATION_CSS = """.location-name{
  font-family:'Cormorant Garamond',Georgia,serif;
  font-size:1.35rem;font-weight:600;letter-spacing:0.03em;
  color:#ffe4e6;margin-top:0.4rem;line-height:1.4;
}"""

POSTER_LINK_CSS = (
    ".poster-photo-wrap a{display:block;width:100%;height:100%;"
    "cursor:pointer;touch-action:manipulation;-webkit-tap-highlight-color:transparent;}"
)

LOC_STYLE = (
    "font-size:1.1rem;font-weight:600;color:rgba(255,255,255,0.9);"
    "margin-top:0.4rem;line-height:1.6;"
)
LOC_FIXES = {
    "sivagiri": "Sivagiri",
    "rajapalaym": "Rajapalayam",
    "rajapalam": "Rajapalam",
    "reception venue": "Rajapalam",
}


def apply_instagram_links(text: str) -> tuple[str, int]:
    pattern = re.compile(
        r'(<div class="poster-photo-wrap">)(.*?)(<img class="poster-photo")',
        re.S,
    )
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        prefix, middle, img = m.group(1), m.group(2), m.group(3)
        if '<a href="' in middle:
            return m.group(0)
        # Find poster-name after this block
        after = text[m.end() : m.end() + 800]
        name_m = re.search(r'<p class="poster-name">([^<]+)</p>', after)
        if not name_m:
            return m.group(0)
        name = name_m.group(1).strip()
        url = NAME_TO_URL.get(name)
        if not url:
            return m.group(0)
        count += 1
        link = (
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" '
            f'title="Visit {name} on Instagram">'
        )
        return f"{prefix}{link}{middle}{img}"

    # Pattern needs full text for lookahead; use name-based pass instead
    block_pat = re.compile(
        r'(<div class="poster-photo-wrap">)(.*?)(</div>\s*<div class="poster-inner">.*?'
        r'<p class="poster-name">([^<]+)</p>)',
        re.S,
    )

    def block_repl(m: re.Match) -> str:
        nonlocal count
        wrap_open, inner, tail, name = m.group(1), m.group(2), m.group(3), m.group(4).strip()
        url = NAME_TO_URL.get(name)
        if not url:
            return m.group(0)
        if '<a href="' in inner:
            # Update href if wrong
            new_inner = re.sub(
                r'<a href="[^"]*"',
                f'<a href="{url}"',
                inner,
                count=1,
            )
            if new_inner != inner:
                count += 1
            return wrap_open + new_inner + tail
        link = (
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" '
            f'title="Visit {name} on Instagram">'
        )
        count += 1
        if inner.strip().startswith("<img"):
            inner = link + inner + "</a>"
        else:
            inner = link + inner + "</a>"
        return wrap_open + inner + tail

    return block_pat.sub(block_repl, text), count


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    changes: list[str] = []

    # Hero headline
    new = re.sub(
        r"A\s+grand,?\s*cinematic\s+wedding\s+for\s+two\s+families\s+united\s+by\s+love\.?",
        "A wedding for two families united by love.",
        text,
        flags=re.I,
    )
    if new != text:
        changes.append("hero headline")
        text = new

    if "A wedding for two families united by love." not in text:
        text = text.replace(
            ">A grand, cinematic wedding for two families united by love.<",
            ">A wedding for two families united by love.<",
        )
        changes.append("hero headline (literal)")

    # Chip
    if "Grand Wedding Ceremony" in text:
        text = text.replace(
            "✦ 25 May 2026 · 10:00 AM · Grand Wedding Ceremony",
            "✦ 25 May 2026 · 10:00 AM · Wedding Ceremony",
        )
        changes.append("chip text")

    # Location CSS
    if ".location-name" not in text:
        text = text.replace(
            ".location-box{\n  border-radius:1.2rem;border:1px solid rgba(255,255,255,0.1);\n"
            "  background:rgba(0,0,0,0.2);padding:0.75rem 1rem;margin-top:auto;\n}",
            ".location-box{\n  border-radius:1.2rem;border:1px solid rgba(255,255,255,0.1);\n"
            "  background:rgba(0,0,0,0.2);padding:0.75rem 1rem;margin-top:auto;\n}\n"
            + LOCATION_CSS,
        )
        changes.append("location-name CSS")

    # Poster touch CSS
    old_link_css = '.poster-photo-wrap a { display:block; width:100%; height:100%; }'
    if old_link_css in text:
        text = text.replace(old_link_css, POSTER_LINK_CSS)
        changes.append("poster touch CSS")
    elif POSTER_LINK_CSS not in text:
        text = text.replace(
            ".poster-photo-wrap{position:relative;height:300px;overflow:hidden;}",
            ".poster-photo-wrap{position:relative;height:300px;overflow:hidden;}\n"
            + POSTER_LINK_CSS,
        )
        changes.append("poster touch CSS (insert)")

    # Location labels
    loc_pat = re.compile(rf'<p style="{re.escape(LOC_STYLE)}">([^<]+)</p>')

    def loc_repl(m: re.Match) -> str:
        name = m.group(1).strip()
        fixed = LOC_FIXES.get(name.lower(), name)
        if fixed == "sivagiri":
            fixed = "Sivagiri"
        return f'<p class="location-name font-display">{fixed}</p>'

    text2, n_loc = loc_pat.subn(loc_repl, text)
    if n_loc:
        changes.append(f"location labels ({n_loc})")
        text = text2

    # Ensure styled locations even if already partially updated
    for old, new in [
        (">sivagiri</p>", ">Sivagiri</p>"),
        (">Sivigiri</p>", ">Sivagiri</p>"),
        (">Reception Venue</p>", ">Rajapalam</p>"),
        (">Rajapalaym</p>", ">Rajapalayam</p>"),
    ]:
        if old in text:
            text = text.replace(old, new.replace(">", ' class="location-name font-display">', 1) if 'class=' not in new else new)
            changes.append(f"fix {old}")

    # Normalize location paragraphs without class
    text = re.sub(
        r'<p class="location-name font-display">(Rajapalayam|Sivagiri|Rajapalam)</p>',
        r'<p class="location-name font-display">\1</p>',
        text,
    )
    for place in ("Rajapalayam", "Sivagiri", "Rajapalam"):
        bare = f'<p style="{LOC_STYLE}">{place}</p>'
        styled = f'<p class="location-name font-display">{place}</p>'
        if bare in text:
            text = text.replace(bare, styled)
            changes.append(f"style {place}")

    text = text.replace("\\https://", "https://")

    text, n_insta = apply_instagram_links(text)
    if n_insta:
        changes.append(f"instagram links ({n_insta})")

    HTML.write_text(text, encoding="utf-8")
    index = HTML.parent / "index.html"
    index.write_text(text, encoding="utf-8")

    print("Applied to", HTML.name, "and", index.name)
    if changes:
        for c in changes:
            print(" -", c)
    else:
        print(" - all changes already present")

    # Verify
    checks = {
        "hero": "A wedding for two families united by love." in text,
        "chip": "· Wedding Ceremony</span>" in text and "Grand Wedding Ceremony" not in text,
        "locations styled": text.count("location-name font-display") >= 4,
        "Sivagiri": "Sivagiri" in text and ">sivagiri<" not in text,
        "Rajapalam reception": "Rajapalam</p>" in text,
        "instagram (8)": sum(1 for u in NAME_TO_URL.values() if u in text) == 8,
    }
    print("\nVerification:")
    for k, ok in checks.items():
        print(f"  {'OK' if ok else 'FAIL'}: {k}")


if __name__ == "__main__":
    main()
