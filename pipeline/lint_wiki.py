#!/usr/bin/env python3
"""Wiki 健康檢查（lint）。用法：python3 pipeline/lint_wiki.py
規則定義見 CLAUDE.md §3、§4.3。任何 ✗ 都要修到通過。
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
REQ_FM = ["title", "type", "sources", "updated"]

errors, warns = [], []
pages = {p.relative_to(WIKI).as_posix(): p.read_text(encoding="utf-8") for p in WIKI.rglob("*.md")}
source_ids = {re.match(r"sources/s(\d+)-", k).group(1) for k in pages if k.startswith("sources/")}


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


inbound = {k: 0 for k in pages}
for name, text in pages.items():
    fm = frontmatter(text)
    if fm is None:
        errors.append(f"{name}: 缺少 frontmatter")
        continue
    for k in REQ_FM:
        if k not in fm:
            errors.append(f"{name}: frontmatter 缺少 {k}")

    # 連結
    for link in re.findall(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)", text):
        target = (Path(name).parent / link).as_posix()
        target = Path(target).as_posix()
        # 正規化 ../
        parts = []
        for seg in target.split("/"):
            if seg == "..":
                parts and parts.pop()
            elif seg not in ("", "."):
                parts.append(seg)
        target = "/".join(parts)
        if target not in pages:
            errors.append(f"{name}: 連結失效 → {link}")
        elif target != name:
            inbound[target] += 1

    # 引用的來源必須存在
    for sid in set(re.findall(r"\[S(\d+)\]", text)):
        if sid not in source_ids:
            errors.append(f"{name}: 引用了不存在的來源 S{sid}")

# ---- v2（第 2 次執行後新增）：數字的引用與可追溯性 ----
# 原因：簡報檢查抓到的數字錯誤，有一半其實源自 concept 頁整理時漏了細節或沒標來源。
# 把檢查往前移到 Wiki 層：含數字的行必須有 [S#]，而且數字要出現在被引用的來源頁裡。
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
src_text = {sid: next(t for k, t in pages.items() if k.startswith(f"sources/s{sid}-")) for sid in source_ids}
raw_text = {}
for sid in source_ids:
    f = next((ROOT / "raw").glob(f"s{sid}-*.md"), None)
    raw_text[sid] = f.read_text(encoding="utf-8") if f else ""


def nums(line):
    return {n.replace(",", "") for n in NUM.findall(line) if len(n.replace(",", "")) >= 2}


for name, text in pages.items():
    if name in ("index.md", "log.md"):
        continue
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    is_source = name.startswith("sources/")
    for ln, line in enumerate(body.splitlines(), 1):
        if line.startswith("#") or line.startswith("- 出處") or "](" in line and not re.search(r"\[S\d+\]", line) and not nums(re.sub(r"\[[^\]]*\]\([^)]*\)", "", line)):
            continue
        clean = re.sub(r"\[[^\]]*\]\([^)]*\)", "", line)  # 去掉連結文字（例如 [S8](...)）
        ns = nums(clean)
        if not ns or "（綜合" in line or line.startswith("- 出處"):  # 接受（綜合）與（綜合：說明）
            continue
        cited = set(re.findall(r"\[S(\d+)\]", line))
        if not cited:
            errors.append(f"{name}:{ln} 含數字 {sorted(ns)} 但這一行沒有 [S#]")
            continue
        pool = "".join((raw_text if is_source else src_text)[c] for c in cited if c in src_text)
        pool_nums = {n.replace(",", "") for n in NUM.findall(pool)}
        for n in sorted(ns - pool_nums):
            layer = "raw/" if is_source else "sources/"
            errors.append(f"{name}:{ln} 數字 {n} 在被引用的 {layer} 來源中找不到（{', '.join('S'+c for c in sorted(cited))}）")

# 孤兒頁
for name, n in inbound.items():
    if n == 0 and name not in ("index.md", "log.md"):
        errors.append(f"{name}: 孤兒頁（沒有任何頁面連到它）")

# index 必須列出所有頁面
idx = pages.get("index.md", "")
for name in pages:
    if name not in ("index.md",) and f"({name})" not in idx:
        errors.append(f"index.md 沒有列出 {name}")

for w in warns:
    print("⚠", w)
for e in errors:
    print("✗", e)
if errors:
    print(f"\nlint 失敗：{len(errors)} 個錯誤")
    sys.exit(1)
print(f"✓ lint 通過：{len(pages)} 頁、{len(source_ids)} 份來源")
