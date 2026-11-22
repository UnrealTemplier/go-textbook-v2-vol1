#!/usr/bin/env python3
"""Линтер пререквизитов для Тома 1 (go-textbook-v2-vol1).

Проверяет, что продвинутые термины (mheap, SSA, ABIInternal, Kubernetes, SQL и др.)
не «протекают» в ранние модули раньше главы, где они впервые вводятся.
Запуск из корня тома: python3 book/tools/check_prerequisites.py
"""

import re
import sys
from pathlib import Path

# Словарь «термин → номер модуля, начиная с которого термин разрешён» (99 = запрещён во всём Томе 1)
FORBIDDEN_BEFORE_MODULE = {
    "mheap": 99,
    "mcache": 99,
    "mcentral": 99,
    "ABIInternal": 99,
    "ABI0": 99,
    "netpoller": 99,
    "sysmon": 99,
    "work-stealing": 99,
    "Tri-color": 99,
    "write barrier": 99,
    "GOMEMLIMIT": 99,
    "GOGC": 99,
    "Swiss Tables": 99,
    "GCShape": 99,
    "unsafe.Pointer": 99,
    "Kubernetes": 99,
    "Mechanical Sympathy": 99,
    "механическое сочувствие": 99,
    "механическое сопереживание": 99,
    "PostgreSQL": 99,
    "MySQL": 99,
    "MVCC": 99,
    "goroutine": 4,
    "горутин": 4,
    "sync.Mutex": 4,
    "context.Context": 4,
    "net/http": 7,
    "Dockerfile": 7,
}


def main() -> int:
    sources = Path("sources")
    if not sources.is_dir():
        print("Каталог sources/ не найден", file=sys.stderr)
        return 1
    violations = []
    for md in sorted(sources.rglob("*.md")):
        rel = md.relative_to(sources)
        m = re.match(r"(\d+)\.", rel.parts[0])
        mod_num = int(m.group(1)) if m else 0
        if mod_num <= 1:
            # Вводные служебные страницы каркаса/пролога проверяем строго
            pass
        text = md.read_text(encoding="utf-8")
        # Пропускаем блоки кода при проверке прозы
        prose = re.sub(r"```.*?```", "", text, flags=re.S)
        for term, min_mod in FORBIDDEN_BEFORE_MODULE.items():
            if mod_num < min_mod and re.search(re.escape(term), prose, re.I):
                violations.append(f"{rel}: термин «{term}» не допускается до модуля {min_mod}")
    if violations:
        print(f"Найдено нарушений пререквизитов: {len(violations)}")
        for v in violations:
            print(f"  - {v}")
        return 1
    print("OK: нарушений пререквизитов не найдено.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
