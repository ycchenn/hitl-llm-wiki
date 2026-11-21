#!/usr/bin/env python3
"""把 wiki/、docs/、raw/ 的 Markdown 轉成可瀏覽的 HTML（放在 .md 旁邊），給 GitHub Pages 用。
用法：python3 pipeline/build_site.py      需要：pip install markdown
"""
import re, html
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parent.parent
TARGETS = list((ROOT / "wiki").rglob("*.md")) + list((ROOT / "docs").glob("*.md")) + \
          list((ROOT / "raw").glob("*.md")) + [ROOT / "CLAUDE.md"]

TPL = """<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · HITL LLM Wiki</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@700&display=swap" rel="stylesheet">
<style>
:root{{--paper:#f6f1e7;--ink:#1f2a2e;--muted:#5b6669;--line:#d9d0bf;--teal:#0f5257;--amber:#c8781b;--card:#fffdf8}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.8 "Noto Sans TC",system-ui,sans-serif}}
header{{background:var(--teal);color:#fff;padding:12px 24px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}}
header a{{color:#f5e3c8;text-decoration:none;font-size:15px}} header b{{font-family:"Noto Serif TC",serif;margin-right:auto}}
main{{max-width:860px;margin:0 auto;padding:32px 22px 80px}}
h1,h2{{font-family:"Noto Serif TC",serif;line-height:1.35}} h1{{font-size:30px}} h2{{font-size:23px;margin-top:2em;border-bottom:1px solid var(--line);padding-bottom:4px}}
a{{color:var(--teal)}} code{{background:#ece5d6;padding:1px 5px;border-radius:4px;font-size:.9em}}
pre{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;overflow:auto;font-size:14px;line-height:1.5}}
pre code{{background:none;padding:0}} table{{border-collapse:collapse;width:100%;font-size:15px;margin:1em 0;display:block;overflow-x:auto}}
th,td{{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}} th{{background:#ece5d6}}
blockquote{{margin:1em 0;padding:8px 16px;background:#f5e3c8;border-left:4px solid var(--amber);border-radius:6px}}
.fm{{font-size:13px;color:var(--muted);background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px 12px;margin-bottom:18px}}
.mermaid{{background:var(--card);text-align:center}}
</style></head><body>
<header><b>HITL · LLM Wiki</b>
<a href="{up}index.html">首頁</a><a href="{up}wiki/index.html">Wiki 索引</a>
<a href="{up}slides/index.html">教學簡報</a><a href="{up}docs/workflow.html">Loop / Graph</a>
<a href="{up}docs/run-log.html">執行紀錄</a><a href="{up}docs/reflection.html">反思</a></header>
<main>{fm}{body}<p style="margin-top:48px;font-size:13px;color:var(--muted)">原始檔：<code>{src}</code></p></main>
<script type="module">
if (document.querySelector('.mermaid')) {{
  const m = await import('https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs');
  m.default.initialize({{ startOnLoad: true, theme: 'neutral' }});
}}
</script>
</body></html>"""

for md_path in TARGETS:
    text = md_path.read_text(encoding="utf-8")
    fm_html, title = "", md_path.stem
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if m:
        text = text[m.end():]
        fm = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)
        title = fm.get("title", title).strip()
        fm_html = '<div class="fm">' + " · ".join(f"{k.strip()}: {html.escape(v.strip())}" for k, v in fm.items()) + "</div>"
    else:
        h = re.search(r"^# (.+)$", text, re.M)
        title = h.group(1) if h else title

    # mermaid 區塊先抽出來
    mermaids = []
    def keep(mm):
        mermaids.append(mm.group(1)); return f"\n\nMERMAID{len(mermaids)-1}\n\n"
    text = re.sub(r"```mermaid\n(.*?)```", keep, text, flags=re.S)

    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    for i, src in enumerate(mermaids):
        body = body.replace(f"<p>MERMAID{i}</p>", f'<pre class="mermaid">{html.escape(src)}</pre>')
    # .md 連結 → .html（外部連結不動）
    body = re.sub(r'href="(?!https?:)([^"]+?)\.md(#[^"]*)?"', lambda x: f'href="{x.group(1)}.html{x.group(2) or ""}"', body)

    rel = md_path.relative_to(ROOT)
    up = "../" * (len(rel.parts) - 1)
    out = TPL.format(title=html.escape(title), up=up, fm=fm_html, body=body, src=rel.as_posix())
    md_path.with_suffix(".html").write_text(out, encoding="utf-8")
    print("✓", rel.with_suffix(".html"))
