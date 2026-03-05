#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import List, Tuple, Optional

INPUT_PATH = "Internal_Knowledge.md"
OUTPUT_PATH = "Internal_Knowledge_Overview_Tables.md"

# --- Erkennung der Seiten-Grenzen ---

# Exakte Trennerzeile (mindestens 10 '=' in einer eigenen Zeile)
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
      - an einer Trennerzeile '====...' WENN danach (nach optionalen Leerzeilen) ein
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

# --- Überschriften/Abschnitte parsen ---

def normalize_heading_name(line: str) -> str:
    # Entfernt führende/folgende Spaces und Sternchen, lowercased
    return line.strip().strip('*').strip().lower()

def is_setext_underline(line: str) -> bool:
    s = line.strip()
    return len(s) > 0 and set(s) == {'='}

def find_all_setext_sections(lines: List[str]) -> List[Tuple[str, int, int]]:
    """
    Findet ALLE Setext-Sections und liefert Liste (name_norm, start_idx, end_idx_excl).
    - name_norm: normalisierter Name (z.B. 'overview', 'tables', 'general description')
    - start_idx: Index der Überschriftenzeile
    - end_idx_excl: Zeile der nächsten Section (oder len(lines))
    """
    sections: List[Tuple[str, int, int]] = []
    i = 0
    while i < len(lines) - 1:
        name_line = lines[i]
        underline = lines[i + 1] if i + 1 < len(lines) else ""
        if is_setext_underline(underline):
            name_norm = normalize_heading_name(name_line)
            # Ende suchen: nächste Setext-Überschrift
            j = i + 2
            while j < len(lines) - 1:
                if is_setext_underline(lines[j + 1]):
                    break
                j += 1
            end_idx = j if j < len(lines) - 1 else len(lines)
            sections.append((name_norm, i, end_idx))
            i = end_idx
        else:
            i += 1
    return sections

# --- Markdown-Tabellen parsen ---

ROW_WITH_PIPES_RE = re.compile(r'^\s*\|.*\|\s*$')
SEPARATOR_ROW_RE = re.compile(r'^\s*\|(?:\s*:?-{3,}:?\s*\|)+\s*$')

def extract_first_markdown_table(block_text: str) -> Optional[str]:
    """
    Findet die erste Markdown-Tabelle im übergebenen Block (z. B. Overview-Section)
    und gibt den Tabellen-Text (mehrzeilig) zurück.
    """
    lines = block_text.splitlines()
    i = 0
    in_code = False
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            i += 1
            continue
        if ROW_WITH_PIPES_RE.match(line):
            if i + 1 < len(lines) and SEPARATOR_ROW_RE.match(lines[i + 1]):
                # sammle komplette Tabelle
                j = i + 2
                while j < len(lines) and ROW_WITH_PIPES_RE.match(lines[j]):
                    j += 1
                table_text = "\n".join(lines[i:j]).rstrip()
                return table_text
        i += 1
    return None

def parse_md_table(table_text: str) -> List[List[str]]:
    """
    Parst eine Markdown-Tabelle in eine Liste von Zeilen (Zellen als Strings ohne Pipes).
    Header/Separator stehen in rows[0] und rows[1]; Daten ab rows[2:].
    """
    rows = []
    for raw in table_text.splitlines():
        if not raw.strip().startswith("|"):
            continue
        parts = [c.strip(" \t*`") for c in raw.strip().split("|")]
        if parts and parts[0] == "":
            parts = parts[1:]
        if parts and parts[-1] == "":
            parts = parts[:-1]
        rows.append(parts)
    return rows

def is_na_value(s: str) -> bool:
    return s.strip().lower() in {"", "n/a", "na", "-", "–", "—"}

def extract_key_props_from_overview(overview_block: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extrahiert aus der ersten Tabelle der Overview-Section:
      - ET Business Object
      - Name (en)
    und gibt (et_bo, name_en) zurück (beides Optional[str]).
    """
    table_text = extract_first_markdown_table(overview_block)
    if not table_text:
        return None, None
    rows = parse_md_table(table_text)
    data_rows = rows[2:] if len(rows) >= 2 else []

    et_bo = None
    name_en = None

    for r in data_rows:
        if not r:
            continue
        key = r[0] if len(r) > 0 else ""
        key_norm = key.strip().strip("*").strip().lower()
        # Finde erste nicht-leere Zelle rechts neben dem Key
        def first_value_right(vals: List[str]) -> Optional[str]:
            for val in vals:
                if not is_na_value(val):
                    return val.strip()
            return None

        if key_norm == "et business object" and et_bo is None:
            et_bo = first_value_right(r[1:])
        if key_norm == "name (en)" and name_en is None:
            name_en = first_value_right(r[1:])

    return et_bo, name_en

# --- Zusammenstellung der gewünschten Abschnitte ---

def keep_only_selected_sections_with_rag_props(page_text: str) -> str:
    """
    Behält Frontmatter + genau die Abschnitte:
      **Overview**, **General Description**, **Tables** / **Table**
    (mit Inhalt) bei. Keine sonstigen Änderungen an deren Originalinhalten.

    Zusätzlich: Aus der Overview-Tabelle die Keys 'ET Business Object' und 'Name (en)'
    extrahieren und am Ende des 'Tables'/'Table'-Abschnitts als Key-Value-Zeilen wiederholen.
    Falls es keinen Tables/Table-Abschnitt gibt, wird einer erzeugt, der nur diese zwei
    Zeilen enthält (falls vorhanden).
    """
    # Falls die Seite mit dem Trenner anfängt: diesen Block erhalten
    prefix = ""
    rest_page = page_text
    # Prüfe auf führenden Trenner
    first_nonempty = rest_page.strip().splitlines()[0] if rest_page.strip() else ""
    m = GT_SEP_LINE_RE.match(first_nonempty) if first_nonempty else None
    if rest_page.strip().startswith("=") and m:
        # Wir erhalten den kompletten ersten Linienblock (Trenner + evtl. leere Zeilen bis Frontmatter)
        lines_all = rest_page.splitlines(keepends=True)
        i = 0
        while i < len(lines_all):
            prefix += lines_all[i]
            # Stop, wenn nächste Zeile mit Frontmatter beginnt
            if i + 1 < len(lines_all) and lines_all[i + 1].lstrip().startswith("---"):
                i += 1
                break
            i += 1
        rest_page = "".join(lines_all[i:])

    # Frontmatter extrahieren
    m_fm = FRONTMATTER_BLOCK_AT_START_RE.match(rest_page)
    if m_fm:
        frontmatter = rest_page[m_fm.start():m_fm.end()]
        content = rest_page[m_fm.end():]
    else:
        frontmatter = ""
        content = rest_page

    # Alle Setext-Sections finden
    content_lines = content.splitlines()
    sections = find_all_setext_sections(content_lines)

    # Relevante Sections sammeln (in Original-Reihenfolge)
    wanted_names = {"overview", "general description", "tables", "table"}
    kept_named_blocks: List[Tuple[str, str]] = []  # (name_norm, block_text)

    overview_block_text = None
    tables_idx_in_kept: Optional[int] = None  # Index der letzten Tables/Table Section in kept_named_blocks

    for (name_norm, s, e) in sections:
        if name_norm in wanted_names:
            block_text = "\n".join(content_lines[s:e]).rstrip()
            kept_named_blocks.append((name_norm, block_text))
            if name_norm == "overview":
                overview_block_text = block_text
            if name_norm in {"tables", "table"}:
                tables_idx_in_kept = len(kept_named_blocks) - 1

    # Aus Overview die Key-Props holen
    et_bo, name_en = (None, None)
    if overview_block_text:
        et_bo, name_en = extract_key_props_from_overview(overview_block_text)

    # Wenn Key-Props existieren, als zusätzliche Zeilen ans Ende von Tables/Table anhängen.
    rag_lines = []
    if et_bo and not is_na_value(et_bo):
        rag_lines.append(f"**ET Business Object:** {et_bo}")
    if name_en and not is_na_value(name_en):
        rag_lines.append(f"**Name (en):** {name_en}")
    rag_block = "\n".join(rag_lines).rstrip()

    if rag_block:
        if tables_idx_in_kept is not None:
            # An bestehende Tables/Table-Section anhängen (mit Leerzeile davor)
            name_norm, tbl_block = kept_named_blocks[tables_idx_in_kept]
            if tbl_block.endswith("\n"):
                new_tbl_block = tbl_block + "\n" + rag_block + "\n"
            else:
                new_tbl_block = tbl_block + "\n\n" + rag_block + "\n"
            kept_named_blocks[tables_idx_in_kept] = (name_norm, new_tbl_block.rstrip())
        else:
            # Keine Tables/Table-Section vorhanden -> neue **Tables** Section erzeugen
            heading = "**Tables**"
            underline = "=" * len(heading)
            new_tbl_block = f"{heading}\n{underline}\n\n{rag_block}"
            kept_named_blocks.append(("tables", new_tbl_block))

    # Zusammenbauen
    out_chunks: List[str] = []
    if prefix:
        out_chunks.append(prefix.rstrip("\n"))
    if frontmatter:
        out_chunks.append(frontmatter.rstrip("\n"))
    if kept_named_blocks:
        # In Original-Reihenfolge (bereits gewährleistet)
        for _, block in kept_named_blocks:
            out_chunks.append(block.rstrip("\n"))

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
    processed_pages = [keep_only_selected_sections_with_rag_props(p) for p in pages]

    # Beim Zusammenfügen: doppelten Trenner vermeiden
    cleaned = []
    for i, p in enumerate(processed_pages):
        p_stripped = p.lstrip()
        starts_with_sep = bool(p_stripped and GT_SEP_LINE_RE.match(p_stripped.splitlines()[0]))
        if i > 0 and not starts_with_sep:
            cleaned.append("================================================================================\n\n")
        cleaned.append(p)

    final_text = "".join(cleaned).rstrip() + "\n"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"Done. Wrote: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()