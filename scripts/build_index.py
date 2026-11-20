#!/usr/bin/env python3
"""Genera la pagina indice dei deck pubblicati (dist/index.html).

Per ogni deck elencato in decks.txt legge dal headmatter di `slides.md`:
- `title`: titolo mostrato (default: nome della cartella);
- `info`: descrizione facoltativa, di cui si usa la prima riga non vuota.
La data viene dal nome della cartella (GG-MM-AAAA-<tema>). I deck sono
ordinati dal più recente e raggruppati per anno. Lo stile è in
scripts/index.template.html.

Uso:
    python3 scripts/build_index.py decks.txt dist/index.html
"""
import html
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = Path(__file__).with_name("index.template.html")
DATE_RE = re.compile(r"^(\d{2})-(\d{2})-(\d{4})(?:-(.+))?$")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def headmatter(path: Path) -> dict:
    """Legge le coppie `chiave: valore` del primo blocco `---` del deck."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data, key = {}, None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            data[key] = "" if value in ("|", ">", "|-", ">-") else value.strip("'\"")
        elif key and line.startswith((" ", "\t")) and not data[key]:
            data[key] = line.strip()  # prima riga di un blocco multilinea
    return data


def deck_entry(name: str) -> dict:
    meta = headmatter(ROOT / name / "slides.md")
    m = DATE_RE.match(name)
    when = date(int(m[3]), int(m[2]), int(m[1])) if m else None
    info = re.sub(r"[*_`#]", "", meta.get("info", "")).strip()
    return {
        "name": name,
        "title": meta.get("title") or name,
        "info": info,
        "date": when,
    }


def render(deck: dict) -> str:
    when = deck["date"]
    if when:
        date_html = (f'<time datetime="{when.isoformat()}">'
                     f'<span class="day">{when.day:02d}</span>'
                     f'<span class="month">{MONTHS[when.month - 1]}</span>'
                     f"</time>")
    else:
        date_html = '<time></time>'
    info = f'<p class="info">{html.escape(deck["info"])}</p>' if deck["info"] else ""
    href = html.escape(deck["name"], quote=True)
    badge = '<span class="badge">Upcoming</span>'
    arrow = ('<span class="arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" '
             'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
             '<path d="M5 12h14M12 5l7 7-7 7"/></svg></span>')
    return (f'          <li><a class="deck" href="{href}/">{date_html}'
            f'<div class="body"><h3>{html.escape(deck["title"])}{badge}</h3>{info}</div>'
            f'{arrow}</a></li>')


def render_all(decks: list) -> str:
    """Raggruppa i deck per anno (i deck senza data finiscono in fondo)."""
    if not decks:
        return '      <p class="empty">No talks published yet.</p>'
    groups: dict = {}
    for d in decks:
        groups.setdefault(d["date"].year if d["date"] else None, []).append(d)
    sections = []
    for year, items in groups.items():
        label = str(year) if year else "Other"
        rows = "\n".join(render(d) for d in items)
        sections.append(f'      <section class="year" aria-label="{label}">\n'
                        f'        <h2>{label}</h2>\n'
                        f'        <ul class="decks">\n{rows}\n        </ul>\n'
                        f'      </section>')
    return "\n".join(sections)


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    decks_file, out = Path(sys.argv[1]), Path(sys.argv[2])
    names = [l.strip() for l in decks_file.read_text().splitlines()
             if l.strip() and not l.lstrip().startswith("#")]
    decks = sorted((deck_entry(n) for n in names),
                   key=lambda d: d["date"] or date.min, reverse=True)
    items = render_all(decks)
    page = TEMPLATE.read_text(encoding="utf-8")
    page = page.replace("{{ decks }}", items).replace("{{ year }}", str(date.today().year))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
