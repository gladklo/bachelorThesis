#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import List, Tuple

INPUT_PATH = "Internal_Knowledge_BO_Tables.md"
OUTPUT_PATH = "Internal_Knowledge_Without_Empty.md"

# Separator-Zeile: mind. 10 '=' auf einer eigenen Zeile
SEP_RE = re.compile(r'^\s*={10,}\s*$', re.MULTILINE)

def find_separator_line_indices(text: str) -> List[Tuple[int, int]]:
    """
    Liefert eine Liste von (start, end) Positionen für jede Separator-Zeile.
    """
    return [(m.start(), m.end()) for m in SEP_RE.finditer(text)]

def split_into_pages(text: str) -> List[Tuple[str, str]]:
    """
    Teilt das Dokument in Seiten auf.

    Rückgabe: Liste von Tupeln (sep_text, page_text)
      - sep_text: der Separator-Text, der dieser Seite vorangestellt war (oder "" bei der ersten Seite ohne Separator)
      - page_text: der eigentliche Seiteninhalt AB dem Frontmatter (oder sonstigem Text) bis zum nächsten Separator
    """
    seps = find_separator_line_indices(text)
    pages: List[Tuple[str, str]] = []

    if not seps:
        # keine Separatoren: gesamte Datei als eine "Seite" ohne sep_text
        return [("", text)]

    cursor = 0
    # Falls die Datei NICHT mit einem Separator beginnt, ist vor dem ersten Separator eine "Seite"
    if seps[0][0] > 0:
        pages.append(("", text[0:seps[0][0]]))
        cursor = seps[0][0]

    # Für jede Separator-Position den folgenden Bereich als Seite nehmen
    for i, (sep_start, sep_end) in enumerate(seps):
        next_start = seps[i+1][0] if i + 1 < len(seps) else len(text)
        sep_text = text[sep_start:sep_end]
        page_text = text[sep_end:next_start]
        pages.append((sep_text, page_text))
        cursor = next_start

    # Falls nach dem letzten Separator noch Text übrig ist (sollte durch obige Logik abgedeckt sein)
    if cursor < len(text):
        pages.append(("", text[cursor:]))

    return pages

def extract_frontmatter_and_rest(page_text: str) -> Tuple[str, str]:
    """
    Findet den Frontmatter-Block irgendwo am Anfang (unter Überspringen leerer Zeilen)
    und gibt (frontmatter_block, content_after) zurück.
    Wenn kein Frontmatter gefunden wird, ("" , page_text) zurückgeben.
    """
    # Skip führende Leerzeilen
    i = 0
    lines = page_text.splitlines(keepends=True)
    while i < len(lines) and lines[i].strip() == "":
        i += 1

    # Jetzt muss Frontmatter beginnen
    if i < len(lines) and lines[i].lstrip().startswith("---"):
        # Frontmatter-Anfang
        fm_start_pos = sum(len(x) for x in lines[:i])
        # Suche Ende-Zeile '---'
        j = i + 1
        end_found = False
        while j < len(lines):
            if lines[j].strip() == "---":
                end_found = True
                j += 1  # content beginnt NACH dieser Zeile
                break
            j += 1
        if end_found:
            fm_end_pos = sum(len(x) for x in lines[:j])
            frontmatter_block = page_text[fm_start_pos:fm_end_pos]
            content_after = page_text[fm_end_pos:]
            return frontmatter_block, content_after

    # Kein Frontmatter gefunden
    return "", page_text

def page_has_nonempty_content_after_frontmatter(page_text: str) -> bool:
    """
    True, wenn nach dem Frontmatter noch nicht-leerer Inhalt steht.
    """
    _, after = extract_frontmatter_and_rest(page_text)
    # Irgendetwas außer Whitespace?
    return after.strip() != ""

def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        raw = f.read()

    pages = split_into_pages(raw)

    kept_chunks: List[str] = []
    for idx, (sep_text, page_text) in enumerate(pages):
        # Seiten ohne Frontmatter UND ohne Inhalt ignorieren (extra robust)
        if page_text.strip() == "":
            # komplett leer
            continue

        keep = page_has_nonempty_content_after_frontmatter(page_text)

        if keep:
            # Separator wieder einfügen (falls vorhanden)
            if sep_text:
                kept_chunks.append(sep_text.rstrip("\n") + "\n\n")
            kept_chunks.append(page_text.strip("\n") + "\n")

    # Zusammenführen
    final_output = "".join(kept_chunks).rstrip() + "\n"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(final_output)

    print(f"Done. Wrote: {OUTPUT_PATH} (kept {len(kept_chunks)} chunks).")

if __name__ == "__main__":
    main()