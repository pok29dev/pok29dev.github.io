#!/usr/bin/env python3
"""Minimal Markdown -> HTML for the company-policy source (headings, tables,
lists, blockquote, bold/italic/code, hard line breaks). Used to build a PDF
via LibreOffice, which keeps Thai tone marks in the PDF text layer."""
import html, re, sys

CSS = """
@page { size: A4; margin: 20mm 18mm; }
body { font-family: "Noto Sans Thai", "Noto Sans", sans-serif; font-size: 10.5pt;
       line-height: 1.55; color: #111; }
h1 { font-size: 17pt; margin: 0 0 10pt; border-bottom: 2px solid #333; padding-bottom: 6pt; }
h2 { font-size: 13pt; margin: 16pt 0 6pt; }
h3 { font-size: 11.5pt; margin: 12pt 0 5pt; }
p { margin: 0 0 7pt; }
ul, ol { margin: 0 0 8pt; padding-left: 18pt; }
li { margin-bottom: 2pt; }
blockquote { margin: 6pt 0 10pt; padding: 6pt 10pt; background: #f4f4f4;
             border-left: 3px solid #888; font-size: 10pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 12pt; font-size: 9.5pt; }
th, td { border: 0.7pt solid #666; padding: 3.5pt 5pt; text-align: left;
         vertical-align: top; }
th { background: #e8e8e8; font-weight: bold; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 9.5pt; }
hr { border: 0; border-top: 0.7pt solid #999; margin: 12pt 0; }
"""

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t

def is_table_row(l):
    return l.strip().startswith("|") and l.strip().endswith("|")

def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]

def main(src, dst):
    lines = open(src, encoding="utf-8").read().split("\n")
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        s = l.strip()
        if not s:
            out.append(""); i += 1; continue
        if is_table_row(l) and i + 1 < len(lines) and re.fullmatch(
                r"\|[\s:|-]+\|", lines[i + 1].strip()):
            head = cells(l); i += 2
            out.append("<table><thead><tr>" +
                       "".join(f"<th>{inline(c)}</th>" for c in head) +
                       "</tr></thead><tbody>")
            while i < len(lines) and is_table_row(lines[i]):
                out.append("<tr>" +
                           "".join(f"<td>{inline(c)}</td>" for c in cells(lines[i])) +
                           "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1; continue
        if re.fullmatch(r"(-{3,}|\*{3,})", s):
            out.append("<hr>"); i += 1; continue
        if s.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                buf.append(inline(lines[i].strip()[2:]))
                i += 1
            out.append("<blockquote>" + "<br>".join(buf) + "</blockquote>")
            continue
        if re.match(r"^-\s+", s):
            buf = []
            while i < len(lines) and re.match(r"^-\s+", lines[i].strip()):
                buf.append(f"<li>{inline(lines[i].strip()[2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(buf) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", s):
            buf = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                buf.append("<li>" + inline(re.sub(r"^\d+\.\s+", "", lines[i].strip())) + "</li>")
                i += 1
            out.append("<ol>" + "".join(buf) + "</ol>")
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not (
                is_table_row(lines[i]) or re.match(r"^(#{1,6}\s|[-*]\s|\d+\.\s|>\s)", lines[i].strip())
                or re.fullmatch(r"(-{3,}|\*{3,})", lines[i].strip())):
            buf.append(lines[i])
            i += 1
        text = "<br>".join(inline(b.rstrip()) if b.endswith("  ") else inline(b.strip())
                           for b in buf)
        out.append(f"<p>{text}</p>")
    doc = ("<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
           f"<style>{CSS}</style></head><body>\n" + "\n".join(out) + "\n</body></html>\n")
    open(dst, "w", encoding="utf-8").write(doc)
    print(f"{dst}: {len(doc)} bytes")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
