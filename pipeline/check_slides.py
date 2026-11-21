#!/usr/bin/env python3
"""簡報檢查。用法：python3 pipeline/check_slides.py
規則定義見 CLAUDE.md §5 步驟 4。失敗時只需重新生成失敗的投影片。
"""
import re, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
deck = (ROOT / "slides" / "index.html").read_text(encoding="utf-8")
MAX_CJK = 120

# v1.1：class 可能是 "slide cover" 等，必須用 \bslide\b 比對（第 1 次執行時封面被漏掉）
slides = re.findall(r'<section class="[^"]*\bslide\b[^"]*"([^>]*)>(.*?)</section>', deck, re.S)
fails = {}


def fail(i, msg):
    fails.setdefault(i, []).append(msg)


def visible_text(fragment):
    fragment = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", fragment, flags=re.S)
    fragment = re.sub(r'<aside class="notes">.*?</aside>', "", fragment, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", fragment))


def numbers(text):
    # 抓出 1,195 / 1.3 / 175 / 31 這類數字（忽略年份以外的單一位數 1–9，太常見）
    out = set()
    for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text):
        n = n.replace(",", "")
        if len(n) == 1:
            continue
        out.add(n)
    return out


for i, (attrs, body) in enumerate(slides, 1):
    m = re.search(r'data-wiki="([^"]*)"', attrs)
    refs = m.group(1).split() if m else []
    if not refs:
        fail(i, "沒有 data-wiki，無法追溯內容來源")
        continue
    wiki_text, wiki_sources = "", set()
    for r in refs:
        p = WIKI / r
        if not p.exists():
            fail(i, f"data-wiki 指到不存在的頁面 {r}")
            continue
        t = p.read_text(encoding="utf-8")
        wiki_text += t
        fm = re.search(r"^sources:\s*\[(.*?)\]", t, re.M)
        if fm:
            wiki_sources |= {s.strip() for s in fm.group(1).split(",")}

    main = re.sub(r'<footer class="src">.*?</footer>', "", body, flags=re.S)
    text = visible_text(main)

    # 1) 數字必須出現在引用的 Wiki 頁
    wiki_nums = {n.replace(",", "") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", wiki_text)}
    for n in sorted(numbers(text)):
        if n not in wiki_nums:
            fail(i, f"數字 {n} 不在引用的 Wiki 頁面中（{' '.join(refs)}）")

    # 2) 字數上限
    cjk = len(re.findall(r"[一-鿿]", text))
    if cjk > MAX_CJK:
        fail(i, f"內文 {cjk} 個中文字，超過 {MAX_CJK}")

    # 3) 頁腳來源要屬於引用頁面的 sources
    foot = re.search(r'<footer class="src">(.*?)</footer>', body, re.S)
    cited = set(re.findall(r"S\d+", foot.group(1))) if foot else set()
    if not foot:
        fail(i, "缺少來源頁腳 <footer class=\"src\">")
    for s in cited - wiki_sources:
        fail(i, f"頁腳列出 {s}，但引用的 Wiki 頁面沒有這個來源")

for i, msgs in fails.items():
    for msg in msgs:
        print(f"✗ 第 {i} 張：{msg}")
if fails:
    print(f"\n簡報檢查失敗：{len(fails)} / {len(slides)} 張需要重新生成 → {sorted(fails)}")
    sys.exit(1)
print(f"✓ 簡報檢查通過：{len(slides)} 張投影片，皆可追溯到 Wiki")
