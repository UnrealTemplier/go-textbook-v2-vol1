# Том 1. Go и первый бэкенд: путь с нуля

> Линейный учебник по Go с нуля: интуитивный пролог в устройство компьютера и сети, синтаксис Go, стандартная библиотека, базовая конкурентность, вводный CS/DSA и первый HTTP-бэкенд.

* **Серия:** `go-textbook-v2` (Том 1 из 7)
* **Входные требования:** Базовое умение написать простую программу на любом языке (переменная, цикл, условие, функция). Знание Go не требуется.
* **Целевая версия Go:** `Go 1.22–1.24`
* **Движок:** `html-textbook-engine` (100% Offline-First, сборка в `dist/` для `file:///` и GitHub Pages)

## Сквозной проект тома (`project/`)

BookmarkFlow — консольный менеджер закладок, вырастающий в HTTP-сервис на файлах/JSON

Запуск тестов проекта:
```bash
cd project && go test ./...
```

## Сборка и проверка локально

```bash
python3 -m pip install -r requirements.txt
python3 -m engine.build --all --strict
python3 -m engine.audit --strict --no-mermaid-runtime
```

Открыть локально: `xdg-open dist/index.html`.
