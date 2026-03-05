#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reduziert jede Confluence-Seite in 'Internal_Knowledge.md' auf die Abschnitte
**Overview** und **Tables**, ohne deren Inhalt zu verändern. Alles andere wird entfernt.

Seiten-Grenzen:
- Primär: eine Zeile mit '>====...====' (mind. 10 '=') gefolgt (nach optionalen Leerzeilen)
  von einem Frontmatter-Block:
      ---
      title:
      ...
      ---
- Zusätzlich wird der Datei-Anfang als potentielle erste Seite unterstützt, wenn dort direkt
  ein Frontmatter-Block beginnt.

Beibehalten:
- Frontmatter jeder Seite bleibt 1:1 erhalten.
- Aus dem Seiteninhalt werden nur die zwei Abschnitte '**Overview**' und '**Tables**'
  (inkl. ihrer Setext-Underline '====...') + deren jeweiliger Inhalt kopiert.
- Reihenfolge der Abschnitte bleibt so, wie sie im Original vorkommt.
- Es werden KEINE Platzhalter eingefügt.

Ausgabe:
- Schreibt nach 'Internal_Knowledge_Overview_Tables.md'.
- Zwischen Seiten wird wieder der Trenner '>====...====' eingefügt, falls nötig, um die Struktur zu wahren.
"""

import re
from typing import List, Tuple, Optional

INPUT_PATH = "Internal_Knowledge.md"
OUTPUT_PATH = "Internal_Knowledge_Overview_Tables.md"

# --- Erkennung der Seiten-Grenzen ---

# Exakte Trennerzeile (mindestens 10 '=' nach '>')
GT_SEP_LINE_RE = re.compile(r'^\s*(={10,})\s*$', re.MULTILINE)

# Frontmatter-Block (am Anfang eines Seitenchunks)
FRONTMATTER_BLOCK_AT_START_RE = re.compile(
    r'(?s)\A\s*---\s*\n(.*?)\n---\s*\n'
)

def find_frontmatter_span_from(text: str, start_pos: int) -> Optional[Tuple[int, int]]:
    """
    Sucht ab start_pos (unter Überspringen von Leerzeilen) nach einem Frontmatter-Block
    und prüft, ob darin eine 'title:'-Zeile vorkommt.
    Rückgabe: (fm_start, fm_end) oder None.
    """
    pos = start_pos
    n = len(text)

    # Leere/Whitespace-Zeilen überspringen
    while pos < n:
        # finde Zeilenende
        nl = text.find('\n', pos)
        line = text[pos:nl if nl != -1 else n]
        if line.strip() == "":
            pos = nl + 1 if nl != -1 else n
            continue
        break

    # Jetzt muss Frontmatter beginnen
    if not text.startswith('---', pos):
        return None

    # Finde Ende des Frontmatter-Blocks
    fm_start = pos
    fm_end_marker = '\n---\n'
    end_idx = text.find(fm_end_marker, fm_start + 3)
    if end_idx == -1:
        return None  # unvollständiger Frontmatter

    fm_end = end_idx + len(fm_end_marker)
    fm_content = text[fm_start:fm_end]

    # Enthält eine title:-Zeile?
    if re.search(r'(?mi)^\s*title\s*:', fm_content) is None:
        return None

    return (fm_start, fm_end)

def find_page_spans(text: str) -> List[Tuple[int, int]]:
    """
    Liefert (start, end) Offsets je Seite im Gesamtdokument.
    Eine Seite beginnt:
      - am Dateianfang, falls dort ein Frontmatter-Block mit title: steht, oder
      - an einer Trennerzeile '>====...' WENN danach (nach optionalen Leerzeilen) ein
        Frontmatter-Block mit 'title:' folgt.
    Ende ist jeweils der Beginn der nächsten Seite oder Dateiende.
    """
    spans: List[Tuple[int, int]] = []
    n = len(text)

    # 1) Datei-Anfang
    m0 = FRONTMATTER_BLOCK_AT_START_RE.match(text)
    if m0 and re.search(r'(?mi)^\s*title\s*:', text[:m0.end()]):
        spans.append((0, None))

    # 2) Trenner + Frontmatter(title:)
    for m in GT_SEP_LINE_RE.finditer(text):
        sep_start = m.start()
        sep_end = m.end()
        fm_span = find_frontmatter_span_from(text, sep_end)
        if fm_span is not None:
            # Seite beginnt MIT dem Trenner (er soll erhalten bleiben)
            spans.append((sep_start, None))

    # sortieren und Enden setzen
    spans = sorted(set(spans), key=lambda t: t[0])
    resolved: List[Tuple[int, int]] = []
    for i, (s, _) in enumerate(spans):
        e = spans[i + 1][0] if i + 1 < len(spans) else n
        resolved.append((s, e))
    return resolved

# --- Extraktion von Frontmatter + Abschnitten ---

def extract_frontmatter(page_text: str) -> Tuple[str, str]:
    """
    Extrahiert Frontmatter am *Seitenanfang* und gibt (frontmatter, rest) zurück.
    Wenn kein Frontmatter am Anfang, frontmatter="" und rest=page_text.
    """
    m = FRONTMATTER_BLOCK_AT_START_RE.match(page_text)
    if not m:
        return "", page_text
    fm = page_text[m.start():m.end()]
    rest = page_text[m.end():]
    return fm, rest

def normalize_heading_name(line: str) -> str:
    # Entfernt führende/folgende Spaces und Sternchen, lowercased
    return line.strip().strip('*').strip().lower()

def is_setext_underline(line: str) -> bool:
    s = line.strip()
    return len(s) > 0 and set(s) == {'='}

def find_setext_section(lines: List[str], target_name: str) -> Optional[Tuple[int, int]]:
    """
    Findet eine Setext-Section:
        **Name**
        ========
        (Inhalt...)
    und gibt (start_index, end_index_excl) zurück,
    wobei start_index auf der Namens-Zeile liegt und end_index_excl
    die erste Zeile der *nächsten* Setext-Section (oder len(lines)) ist.
    """
    # alle Kandidaten im Text finden (erste passende nehmen)
    starts = []
    for i in range(len(lines) - 1):
        if normalize_heading_name(lines[i]) == target_name and is_setext_underline(lines[i + 1]):
            starts.append(i)
    if not starts:
        return None

    start = starts[0]
    # Ende: nächste Setext-Überschrift (beliebiger Name)
    j = start + 2
    while j < len(lines) - 1:
        if is_setext_underline(lines[j + 1]):
            # j ist Zeile mit neuem Namen, j+1 ist =====
            break
        j += 1
    end = j if j < len(lines) - 1 else len(lines)
    return (start, end)

def find_all_sections(lines: List[str], target_names: List[str]) -> List[Tuple[int, int]]:
    """
    Sucht alle gewünschten Setext-Sections (z.B. ["overview", "tables"]) und
    gibt sie als nicht überlappende Spans in der Reihenfolge ihres Auftretens zurück.
    """
    spans = []
    for name in target_names:
        sec = find_setext_section(lines, name)
        if sec:
            spans.append(sec)
    spans.sort(key=lambda t: t[0])

    # Überlappungen (sollten nicht auftreten) sicher ausschließen
    cleaned = []
    last_end = -1
    for s, e in spans:
        if s >= last_end:
            cleaned.append((s, e))
            last_end = e
    return cleaned

def keep_only_overview_and_tables(page_text: str) -> str:
    """
    Behält Frontmatter + genau die Abschnitte **Overview** und **Tables** (mit Inhalt) bei.
    Keine sonstigen Änderungen an deren Inhalt.
    """
    # Falls die Seite mit dem Trenner anfängt: diesen Block erhalten
    prefix = ""
    rest_page = page_text
    # Prüfe auf führenden Trenner
    m = GT_SEP_LINE_RE.match(rest_page.lstrip().splitlines()[0]) if rest_page.strip() else None
    if rest_page.strip().startswith("=") and m:
        # Wir erhalten den kompletten ersten Linienblock (Trenner + evtl. leere Zeilen bis Frontmatter)
        lines_all = rest_page.splitlines(keepends=True)
        i = 0
        # sammle solange, bis Frontmatter beginnt oder Text zu Ende
        while i < len(lines_all):
            prefix += lines_all[i]
            # Stop, wenn nächste Zeile mit Frontmatter beginnt
            if i + 1 < len(lines_all) and lines_all[i + 1].lstrip().startswith("---"):
                i += 1
                break
            i += 1
        rest_page = "".join(lines_all[i:])

    frontmatter, content = extract_frontmatter(rest_page)

    # Arbeiten auf Zeilenebene, um Inhalte 1:1 zu übernehmen
    content_lines = content.splitlines()
    spans = find_all_sections(content_lines, ["overview", "tables"])

    kept_parts: List[str] = []
    for s, e in spans:
        block = "\n".join(content_lines[s:e]).rstrip()
        kept_parts.append(block)

    # Zusammenbauen
    out_chunks: List[str] = []
    if prefix:
        out_chunks.append(prefix.rstrip("\n"))
    if frontmatter:
        out_chunks.append(frontmatter.rstrip("\n"))
    if kept_parts:
        out_chunks.append("\n\n".join(kept_parts).rstrip("\n"))
    # Wenn keine passenden Sections existieren: nur Frontmatter

    return "\n".join(chunk for chunk in out_chunks if chunk != "").rstrip() + "\n"

# --- Hauptablauf ---

def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        raw = f.read()

    page_spans = find_page_spans(raw)
    if not page_spans:
        # Fallback: ganze Datei als eine "Seite"
        page_spans = [(0, len(raw))]

    pages = [raw[s:e] for (s, e) in page_spans]
    processed_pages = [keep_only_overview_and_tables(p) for p in pages]

    # Beim Zusammenfügen: doppelten Trenner vermeiden
    cleaned = []
    for i, p in enumerate(processed_pages):
        p_stripped = p.lstrip()
        starts_with_gt_sep = bool(p_stripped and GT_SEP_LINE_RE.match(p_stripped.splitlines()[0]))
        if i > 0 and not starts_with_gt_sep:
            cleaned.append("================================================================================\n\n")
        cleaned.append(p)

    final_text = "".join(cleaned).rstrip() + "\n"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"Done. Wrote: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()