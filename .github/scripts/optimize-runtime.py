#!/usr/bin/env python3
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected 1 match, found {count}")
    return text.replace(old, new, 1)


def optimize_scrape():
    path = ROOT / 'notify-bot/src/scrape.js'
    text = path.read_text(encoding='utf-8')
    old = "const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36';"
    new = old + "\nconst SCRAPE_DEBUG = process.env.SCRAPE_DEBUG === '1';"
    text = replace_once(text, old, new, 'scrape debug flag')
    text = replace_once(text, "    if (items.length > 0) {\n      // 除錯用：研究能不能做「距離篩選」", "    if (items.length > 0 && SCRAPE_DEBUG) {\n      // 除錯用：研究能不能做「距離篩選」", 'gate deep scrape diagnostics')
    path.write_text(text, encoding='utf-8')


def optimize_state():
    path = ROOT / 'notify-bot/src/state.js'
    text = path.read_text(encoding='utf-8')
    old_head = "const fs = require('fs');\n\nconst MAX_KEEP = 500;"
    new_head = """const fs = require('fs');\n\nconst MAX_KEEP = 500;\n\nfunction writeJsonAtomic(path, value) {\n  const tmp = `${path}.${process.pid}.tmp`;\n  fs.writeFileSync(tmp, JSON.stringify(value, null, 2) + '\\n');\n  fs.renameSync(tmp, path);\n}"""
    text = replace_once(text, old_head, new_head, 'atomic JSON helper')
    text = replace_once(text, "  fs.writeFileSync(path, JSON.stringify(trimmed, null, 2) + '\\n');", "  writeJsonAtomic(path, trimmed);", 'seen atomic write')
    text = replace_once(text, "  fs.writeFileSync(path, JSON.stringify(result, null, 2) + '\\n');", "  writeJsonAtomic(path, result);", 'listings atomic write')
    text = replace_once(text, "  fs.writeFileSync(path, JSON.stringify(out, null, 2) + '\\n');", "  writeJsonAtomic(path, out);", 'subscriber atomic write')
    path.write_text(text, encoding='utf-8')


optimize_scrape()
optimize_state()
print('optimized 591 runtime')
