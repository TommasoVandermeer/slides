#!/usr/bin/env python3
"""Stima la durata di un deck Slidev dalle note del relatore.

Le note sono l'ultimo commento HTML di ogni slide. La stima assume un ritmo
di parlato costante (default 130 parole al minuto) e raggruppa le slide per
sezione: una sezione inizia a ogni slide con `layout: section` o `layout: cover`.
Le slide dopo una sezione intitolata "Backup" non contano nel totale.

Uso:
    python3 scripts/timing.py <deck>/slides.md [--target MIN] [--wpm N]
"""
import argparse
import re
import sys
from pathlib import Path

KEY_RE = re.compile(r"^[A-Za-z_][\w-]*\s*:")
COMMENT_RE = re.compile(r"<!--(.*?)-->", re.S)
HEADING_RE = re.compile(r"^#{1,3}\s+(.+?)\s*$", re.M)
CLICK_RE = re.compile(r"\[click(?::\d+)?\]")


def split_segments(text: str):
    """Divide il file sui separatori `---` fuori dai blocchi di codice."""
    segments, current, fence = [], [], None
    for line in text.splitlines():
        stripped = line.strip()
        m = re.match(r"^(```+|~~~+)", stripped)
        if m:
            if fence is None:
                fence = m.group(1)[:3]
            elif stripped.startswith(fence):
                fence = None
        if fence is None and stripped == "---":
            segments.append("\n".join(current))
            current = []
        else:
            current.append(line)
    segments.append("\n".join(current))
    return segments


def is_frontmatter(seg: str) -> bool:
    """Vero se il segmento è un blocco YAML (headmatter o frontmatter di slide)."""
    lines = [l for l in seg.splitlines() if l.strip()]
    if not lines or not any(KEY_RE.match(l) for l in lines):
        return False
    return all(KEY_RE.match(l) or l.startswith((" ", "\t")) or l.lstrip().startswith("- ")
               for l in lines)


def parse_slides(text: str):
    """Restituisce una lista di (frontmatter, contenuto), una voce per slide.

    Un blocco YAML si applica alla slide che lo segue; l'headmatter vale
    come frontmatter della prima slide.
    """
    slides, pending_fm = [], ""
    for seg in split_segments(text):
        if is_frontmatter(seg):
            pending_fm = seg
        else:
            slides.append((pending_fm, seg))
            pending_fm = ""
    return [s for s in slides if s[1].strip()]


def notes_of(content: str) -> str:
    comments = list(COMMENT_RE.finditer(content))
    if not comments:
        return ""
    last = comments[-1]
    if content[last.end():].strip():  # il commento non è in fondo: non sono note
        return ""
    return CLICK_RE.sub(" ", last.group(1))


def layout_of(fm: str) -> str:
    m = re.search(r"^layout:\s*['\"]?([\w-]+)", fm, re.M)
    return m.group(1) if m else ""


def title_of(content: str) -> str:
    body = COMMENT_RE.sub("", content)
    m = HEADING_RE.search(body)
    return m.group(1) if m else "(senza titolo)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slides", type=Path)
    ap.add_argument("--target", type=float, help="durata prevista del talk in minuti")
    ap.add_argument("--wpm", type=float, default=130, help="parole al minuto (default 130)")
    args = ap.parse_args()

    slides = parse_slides(args.slides.read_text(encoding="utf-8"))
    sections, current, backup = [], None, False
    rows = []
    for n, (fm, content) in enumerate(slides, start=1):
        layout, title = layout_of(fm), title_of(content)
        if layout in ("section", "cover") or current is None:
            current = {"name": title, "minutes": 0.0, "slides": 0}
            sections.append(current)
            backup = title.strip().lower().startswith("backup")
        words = len(re.findall(r"\w+", notes_of(content)))
        minutes = words / args.wpm
        rows.append((n, title, words, minutes, backup))
        if not backup:
            current["minutes"] += minutes
            current["slides"] += 1

    print(f"{'#':>3}  {'parole':>6}  {'min':>5}  titolo")
    for n, title, words, minutes, is_backup in rows:
        flag = "  [backup]" if is_backup else ("  ← senza note" if words == 0 else "")
        print(f"{n:>3}  {words:>6}  {minutes:>5.1f}  {title[:70]}{flag}")

    print("\nPer sezione:")
    total = 0.0
    for s in sections:
        if s["name"].strip().lower().startswith("backup"):
            continue
        total += s["minutes"]
        print(f"  {s['minutes']:>5.1f} min  {s['slides']:>2} slide  {s['name'][:60]}")
    print(f"\nTotale stimato: {total:.1f} min a {args.wpm:.0f} parole/min")
    if args.target:
        diff = total - args.target
        verdict = "in linea" if abs(diff) <= 0.1 * args.target else ("troppo lungo" if diff > 0 else "troppo corto")
        print(f"Target: {args.target:.0f} min → {diff:+.1f} min ({verdict}, tolleranza ±10%)")
    print("Nota: la stima vale quanto le note; slide senza note contano zero.")


if __name__ == "__main__":
    sys.exit(main())
