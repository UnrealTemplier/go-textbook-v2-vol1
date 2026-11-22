#!/usr/bin/env python3
"""Линтер пререквизитов для Тома 1 (go-textbook-v2-vol1).

Проверяет строгую линейность оглавления (см. CURRICULUM.md):
1. Запрещает «протекание» продвинутых терминов и понятий старших томов/модулей
   раньше модуля, где они впервые вводятся.
2. Запрещает любые блоки кода Go (```go) в Модуле 1 (Пролог: 0 кода Go).
3. Проверяет запрещённые в Томе 1 runtime/DB/distributed-символы также внутри
   блоков кода.

Запуск из корня тома: python3 book/tools/check_prerequisites.py
"""

import re
import sys
from pathlib import Path

# Словарь «термин → номер модуля, начиная с которого термин разрешён».
# 99 = запрещён во всём Томе 1 (принадлежит Томам 2–5 или красному списку стиля).
# Для чисто латинских идентификаторов/аббревиатур применяются границы слов (?<![A-Za-z0-9_]) ... (?![A-Za-z0-9_]),
# чтобы например "SSA" не срабатывал внутри слова "message".
FORBIDDEN_BEFORE_MODULE: dict[str, int] = {
    # --- Уровень 99: запрещено во всём Томе 1 (внутренности рантайма, Том 5) ---
    "mheap": 99,
    "mcache": 99,
    "mcentral": 99,
    "mspan": 99,
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
    "SliceHeader": 99,
    "unsafe.Pointer": 99,
    "eface": 99,
    "iface": 99,
    "hmap": 99,
    "hchan": 99,
    "SSA": 99,
    "escape analysis": 99,
    "pprof": 99,
    "cgo": 99,
    # --- Уровень 99: базы данных (Том 2) ---
    "PostgreSQL": 99,
    "MySQL": 99,
    "InnoDB": 99,
    "MVCC": 99,
    "ClickHouse": 99,
    "CockroachDB": 99,
    "MongoDB": 99,
    "Redis": 99,
    "Valkey": 99,
    "SQL": 99,
    "EXPLAIN ANALYZE": 99,
    "database/sql": 99,
    # --- Уровень 99: распределённые системы, брокеры, Prod (Тома 3–4) ---
    "Kubernetes": 99,
    "Kafka": 99,
    "RabbitMQ": 99,
    "NATS": 99,
    "Temporal": 99,
    "gRPC": 99,
    "Protobuf": 99,
    "GraphQL": 99,
    "Prometheus": 99,
    "OpenTelemetry": 99,
    "Jaeger": 99,
    "Raft": 99,
    "Paxos": 99,
    "CRDT": 99,
    "Event Sourcing": 99,
    "Testcontainers": 99,
    "Circuit Breaker": 99,
    # --- Уровень 99: красный список стиля (STYLE_GUIDE.md § 5) ---
    "Mechanical Sympathy": 99,
    "механическое сочувствие": 99,
    "механическое сопереживание": 99,
    # --- Уровень 2: синтаксис и тулинг Go (в Модуле 1 — 0 кода Go) ---
    "package main": 2,
    "fmt.Println": 2,
    "if err != nil": 2,
    "go.mod": 2,
    "gofmt": 2,
    "os.Args": 2,
    # --- Уровень 3: составные типы, память, интерфейсы и первые тесты ---
    "слайс": 3,
    "type assertion": 3,
    "утверждение типа": 3,
    "получатель-указатель": 3,
    "go test": 3,
    "testing.T": 3,
    "t.Run": 3,
    "t.TempDir": 3,
    # --- Уровень 4: stdlib и базовая конкурентность ---
    "goroutine": 4,
    "горутин": 4,
    "sync.Mutex": 4,
    "sync.RWMutex": 4,
    "sync.WaitGroup": 4,
    "context.Context": 4,
    "io.Reader": 4,
    "io.Writer": 4,
    "bufio.Scanner": 4,
    "encoding/json": 4,
    "log/slog": 4,
    "go test -race": 4,
    # --- Уровень 5: CS, ОС и Сети под кодом ---
    "IEEE 754": 5,
    "strace": 5,
    "ulimit": 5,
    "inode": 5,
    "epoll": 5,
    "net.Listen": 5,
    "net.Dial": 5,
    "SIGTERM": 5,
    "SIGINT": 5,
    # --- Уровень 6: вводный курс DSA ---
    "Big-O": 6,
    "B-Tree": 6,
    "бинарное дерево поиска": 6,
    "связный список": 6,
    "хеш-таблиц": 6,
    "BFS": 6,
    "DFS": 6,
    # --- Уровень 7: первый HTTP-бэкенд и базовый Docker ---
    "net/http": 7,
    "http.ServeMux": 7,
    "http.Handler": 7,
    "httptest": 7,
    "middleware": 7,
    "Graceful Shutdown": 7,
    "Dockerfile": 7,
    "Docker": 7,
}

# Термины, которые запрещено использовать даже внутри блоков кода во всём Томе 1
FORBIDDEN_IN_CODE: tuple[str, ...] = (
    "mheap",
    "mcache",
    "mcentral",
    "ABIInternal",
    "unsafe.Pointer",
    "SliceHeader",
    "database/sql",
    "net/http/pprof",
)

GO_FENCE_RE = re.compile(r"^\s*(?:>\s*)*```go\b", re.MULTILINE | re.IGNORECASE)
FENCE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)


def _compile_pattern(term: str) -> re.Pattern[str]:
    escaped = re.escape(term)
    # Если термин целиком состоит из ASCII-букв/цифр/дефиса/подчёркивания/точки/слэша,
    # требуем не-буквенные границы по краям (иначе "SSA" найдётся в "message", а "SQL" — в "NoSQL").
    is_ascii = all(ord(ch) < 128 for ch in term)
    if is_ascii:
        return re.compile(rf"(?<![A-Za-z0-9_]){escaped}(?![A-Za-z0-9_])", re.IGNORECASE)
    # Для кириллических основ (например «горутин», «слайс», «хеш-таблиц») ставим левую границу слова.
    return re.compile(rf"(?<![А-Яа-яЁёA-Za-z0-9_]){escaped}", re.IGNORECASE)


COMPILED_PATTERNS: dict[str, tuple[int, re.Pattern[str]]] = {
    term: (min_mod, _compile_pattern(term))
    for term, min_mod in FORBIDDEN_BEFORE_MODULE.items()
}

COMPILED_CODE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (term, _compile_pattern(term)) for term in FORBIDDEN_IN_CODE
]


def check_sources(sources: Path) -> list[str]:
    violations: list[str] = []
    for md in sorted(sources.rglob("*.md")):
        rel = md.relative_to(sources)
        m = re.match(r"(\d+)\.", rel.parts[0])
        mod_num = int(m.group(1)) if m else 0
        text = md.read_text(encoding="utf-8")

        # Модуль 1 (Пролог): 0 кода Go
        if mod_num == 1 and GO_FENCE_RE.search(text):
            violations.append(f"{rel}: в Модуле 1 (Пролог) запрещены блоки кода Go (```go)")

        # Проза вне блоков кода
        prose = FENCE_BLOCK_RE.sub("", text)
        for term, (min_mod, pat) in COMPILED_PATTERNS.items():
            if mod_num < min_mod and pat.search(prose):
                violations.append(
                    f"{rel}: термин «{term}» не допускается до модуля {min_mod}"
                )

        # Запрещённые символы уровня 99 внутри блоков кода
        for block in FENCE_BLOCK_RE.findall(text):
            for term, pat in COMPILED_CODE_PATTERNS:
                if pat.search(block):
                    violations.append(
                        f"{rel}: запрещённый в Томе 1 символ «{term}» внутри блока кода"
                    )

    return violations


def main() -> int:
    sources = Path("sources")
    if not sources.is_dir():
        print("Каталог sources/ не найден", file=sys.stderr)
        return 1
    violations = check_sources(sources)
    if violations:
        print(f"Найдено нарушений пререквизитов: {len(violations)}")
        for v in violations:
            print(f"  - {v}")
        return 1
    print("OK: нарушений пререквизитов не найдено.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
