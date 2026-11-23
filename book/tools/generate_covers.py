#!/usr/bin/env python3
"""
book/tools/generate_covers.py
Генерация 13 обложек разделов и подразделов Тома 1 в едином стиле инженерного чертежа
(Bell Labs Technical Journal / Blueprint, 1200×675, светлый фон + тёмные линии + акценты синего/терракотового,
invert_dark = true, license = "own") и обновление соответствующих media/credits.toml.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from book.tools.commons_fetch import credits_block, write_credits  # noqa: E402
from engine.media import load_credits  # noqa: E402

HEADER = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675">
  <defs>
    <pattern id="minorGrid" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#e2e8f0" stroke-width="0.8"/>
    </pattern>
    <pattern id="majorGrid" width="125" height="125" patternUnits="userSpaceOnUse">
      <rect width="125" height="125" fill="url(#minorGrid)"/>
      <path d="M 125 0 L 0 0 0 125" fill="none" stroke="#cbd5e1" stroke-width="1.4"/>
    </pattern>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#1e293b"/>
    </marker>
    <marker id="arrowBlue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0369a1"/>
    </marker>
    <marker id="arrowOrange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#c2410c"/>
    </marker>
  </defs>
  <style>
    .bg { fill: #fcfaf5; }
    .frame { fill: none; stroke: #1e293b; stroke-width: 2.5; }
    .inner-frame { fill: none; stroke: #475569; stroke-width: 1; }
    .box { fill: #ffffff; stroke: #1e293b; stroke-width: 2; }
    .box-accent { fill: #f0f9ff; stroke: #0369a1; stroke-width: 2.2; }
    .box-warm { fill: #fff7ed; stroke: #c2410c; stroke-width: 2.2; }
    .box-dark { fill: #f1f5f9; stroke: #334155; stroke-width: 2; }
    .line { fill: none; stroke: #1e293b; stroke-width: 2.2; }
    .line-blue { fill: none; stroke: #0369a1; stroke-width: 2.4; }
    .line-orange { fill: none; stroke: #c2410c; stroke-width: 2.4; }
    .line-dash { fill: none; stroke: #64748b; stroke-width: 1.6; stroke-dasharray: 6 4; }
    .title { font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 23px; font-weight: 700; fill: #0f172a; }
    .sub { font-family: "Inter", "IBM Plex Sans", sans-serif; font-size: 15px; fill: #334155; }
    .mono { font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 14px; fill: #0f172a; }
    .mono-bold { font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 15px; font-weight: 700; fill: #0f172a; }
    .mono-blue { font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 14px; font-weight: 700; fill: #0369a1; }
    .mono-orange { font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 14px; font-weight: 700; fill: #c2410c; }
    .label { font-family: "Inter", "IBM Plex Sans", sans-serif; font-size: 13px; fill: #475569; }
    .stamp { font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 11px; fill: #475569; letter-spacing: 0.5px; }
  </style>
  <rect width="1200" height="675" class="bg"/>
  <rect x="25" y="25" width="1150" height="625" fill="url(#majorGrid)"/>
  <rect x="25" y="25" width="1150" height="625" class="frame"/>
  <rect x="31" y="31" width="1138" height="613" class="inner-frame"/>
'''


def footer_block(code: str, title: str, subtitle: str) -> str:
    return f'''
  <!-- Title Banner & Engineering Stamp -->
  <rect x="31" y="31" width="1138" height="68" fill="#f8fafc" stroke="#1e293b" stroke-width="1.5"/>
  <rect x="31" y="31" width="135" height="68" fill="#0369a1"/>
  <text x="98" y="72" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="22" font-weight="700" fill="#ffffff">{code}</text>
  <text x="188" y="61" class="title">{title}</text>
  <text x="188" y="84" class="sub">{subtitle}</text>

  <rect x="775" y="592" width="394" height="52" fill="#f8fafc" stroke="#1e293b" stroke-width="1.5"/>
  <line x1="910" y1="592" x2="910" y2="644" stroke="#475569" stroke-width="1"/>
  <line x1="1060" y1="592" x2="1060" y2="644" stroke="#475569" stroke-width="1"/>
  <text x="842" y="613" text-anchor="middle" class="stamp">GO-TEXTBOOK-V2</text>
  <text x="842" y="632" text-anchor="middle" class="mono-blue">VOL.1 · GO 1.24</text>
  <text x="985" y="613" text-anchor="middle" class="stamp">ЛИСТ / ЧЕРТЁЖ</text>
  <text x="985" y="632" text-anchor="middle" class="mono">{code}</text>
  <text x="1115" y="613" text-anchor="middle" class="stamp">МАСШТАБ</text>
  <text x="1115" y="632" text-anchor="middle" class="mono">1 : 1</text>
</svg>
'''


COVERS = [
    {
        "dir": "sources/1. Пролог — от лампочки до бэкенда",
        "filename": "cover-module-01-prologue.svg",
        "code": "MOD 01",
        "title": "ПРОЛОГ: ОТ ЛАМПОЧКИ И ПЕРЕКЛЮЧАТЕЛЯ ДО HTTP-БЭКЕНДА",
        "subtitle": "9 глав без кода на Go: бит и байт → логические вентили и CPU → RAM и SSD → компилятор и ОС → TCP/IP и HTTP",
        "caption": "Инженерная карта Модуля 1: восхождение от электрического ключа и двоичного байта через процессор, память и ядро ОС к сетевым пакетам и HTTP-бэкенду",
        "alt": "Инженерный чертёж Модуля 1: цепочка от переключателя и байта через АЛУ, RAM, ядро ОС и TCP/IP до HTTP-сервера",
        "body": '''
  <!-- Stage 1: Switch & Bit -->
  <rect x="55" y="145" width="185" height="175" rx="6" class="box"/>
  <text x="147" y="172" text-anchor="middle" class="mono-blue">1. КЛЮЧ И БАЙТ</text>
  <line x1="75" y1="210" x2="115" y2="210" class="line"/>
  <line x1="115" y1="210" x2="150" y2="190" class="line-orange"/>
  <circle cx="115" cy="210" r="3.5" fill="#1e293b"/>
  <circle cx="155" cy="210" r="3.5" fill="#1e293b"/>
  <line x1="155" y1="210" x2="215" y2="210" class="line"/>
  <rect x="72" y="245" width="150" height="32" class="box-accent"/>
  <text x="147" y="266" text-anchor="middle" class="mono-bold">0 1 0 0 0 1 1 1</text>
  <text x="147" y="300" text-anchor="middle" class="label">8 бит = 256 комбинаций</text>

  <!-- Stage 2: Logic & CPU -->
  <rect x="275" y="145" width="205" height="175" rx="6" class="box"/>
  <text x="377" y="172" text-anchor="middle" class="mono-blue">2. ВЕНТИЛИ И CPU</text>
  <polygon points="315,195 315,245 360,235 360,205" fill="#fff7ed" stroke="#c2410c" stroke-width="2"/>
  <text x="336" y="225" text-anchor="middle" class="mono-orange">ALU</text>
  <rect x="380" y="195" width="80" height="22" class="box-dark"/>
  <text x="420" y="211" text-anchor="middle" class="mono">PC: 0x04</text>
  <rect x="380" y="224" width="80" height="22" class="box-dark"/>
  <text x="420" y="240" text-anchor="middle" class="mono">R1: 0x2A</text>
  <text x="377" y="275" text-anchor="middle" class="mono">Fetch→Decode→Exec</text>
  <text x="377" y="300" text-anchor="middle" class="label">3 ГГц ≈ 0.33 нс / такт</text>

  <!-- Stage 3: RAM & Disk -->
  <rect x="515" y="145" width="205" height="175" rx="6" class="box"/>
  <text x="617" y="172" text-anchor="middle" class="mono-blue">3. ПАМЯТЬ И ДИСК</text>
  <rect x="535" y="192" width="165" height="44" class="box-accent"/>
  <text x="617" y="212" text-anchor="middle" class="mono-bold">RAM [0x00..0xFF]</text>
  <text x="617" y="229" text-anchor="middle" class="label">~100 нс · энергозависима</text>
  <rect x="535" y="246" width="165" height="44" class="box-warm"/>
  <text x="617" y="266" text-anchor="middle" class="mono-bold">NVMe SSD / Диск</text>
  <text x="617" y="283" text-anchor="middle" class="label">~100 мкс · постоянный</text>

  <!-- Stage 4: Compiler & OS -->
  <rect x="755" y="145" width="190" height="175" rx="6" class="box"/>
  <text x="850" y="172" text-anchor="middle" class="mono-blue">4. КОД И ЯДРО ОС</text>
  <rect x="775" y="192" width="150" height="36" class="box-dark"/>
  <text x="850" y="215" text-anchor="middle" class="mono">Процесс PID 412</text>
  <line x1="850" y1="228" x2="850" y2="250" class="line-orange" marker-end="url(#arrowOrange)"/>
  <rect x="775" y="252" width="150" height="40" class="box-warm"/>
  <text x="850" y="277" text-anchor="middle" class="mono-orange">Ядро ОС (syscall)</text>
  <text x="850" y="307" text-anchor="middle" class="label">Изоляция и файлы</text>

  <!-- Stage 5: Network & HTTP Backend -->
  <rect x="975" y="145" width="170" height="175" rx="6" class="box-accent"/>
  <text x="1060" y="172" text-anchor="middle" class="mono-blue">5. HTTP-БЭКЕНД</text>
  <rect x="990" y="194" width="140" height="46" class="box"/>
  <text x="1060" y="213" text-anchor="middle" class="mono-bold">GET /bookmarks</text>
  <text x="1060" y="231" text-anchor="middle" class="mono-blue">TCP :8080</text>
  <rect x="990" y="250" width="140" height="44" class="box-warm"/>
  <text x="1060" y="270" text-anchor="middle" class="mono-orange">200 OK · JSON</text>
  <text x="1060" y="287" text-anchor="middle" class="label">BookmarkFlow</text>

  <!-- Connecting arrows between stages -->
  <line x1="240" y1="232" x2="272" y2="232" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="480" y1="232" x2="512" y2="232" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="720" y1="232" x2="752" y2="232" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="945" y1="232" x2="972" y2="232" class="line-blue" marker-end="url(#arrowBlue)"/>

  <!-- Bottom Timeline: 9 chapters map -->
  <rect x="55" y="365" width="1090" height="195" rx="6" class="box"/>
  <text x="80" y="398" class="mono-bold">ЛИНЕЙНЫЙ МАРШРУТ ПРОЛОГА (9 УРОКОВ · 0 СТРОК КОДА НА GO):</text>
  <line x1="80" y1="412" x2="1120" y2="412" stroke="#cbd5e1" stroke-width="1.5"/>

  <g font-family="JetBrains Mono, monospace" font-size="13" fill="#0f172a">
    <rect x="80" y="428" width="330" height="34" rx="4" class="box-dark"/>
    <text x="95" y="450">01. Свет, переключатели и байт</text>
    <rect x="80" y="472" width="330" height="34" rx="4" class="box-dark"/>
    <text x="95" y="494">02. Числа, hex, ASCII и UTF-8</text>
    <rect x="80" y="516" width="330" height="34" rx="4" class="box-dark"/>
    <text x="95" y="538">03. Вентили, сумматор и цикл CPU</text>

    <rect x="435" y="428" width="330" height="34" rx="4" class="box-dark"/>
    <text x="450" y="450">04. Память RAM, кэш и диск SSD</text>
    <rect x="435" y="472" width="330" height="34" rx="4" class="box-dark"/>
    <text x="450" y="494">05. Машинный код и компилятор</text>
    <rect x="435" y="516" width="330" height="34" rx="4" class="box-dark"/>
    <text x="450" y="538">06. Ядро ОС, процессы и файлы</text>

    <rect x="790" y="428" width="330" height="34" rx="4" class="box-dark"/>
    <text x="805" y="450">07. Пакеты, IP, порты, DNS и TCP</text>
    <rect x="790" y="472" width="330" height="34" rx="4" class="box-dark"/>
    <text x="805" y="494">08. Протокол HTTP, JSON и бэкенд</text>
    <rect x="790" y="516" width="330" height="34" rx="4" class="box-accent"/>
    <text x="805" y="538" fill="#0369a1" font-weight="700">09. Почему Go и план BookmarkFlow</text>
  </g>
'''
    },
    {
        "dir": "sources/2. Первые шаги на Go",
        "filename": "cover-module-02-first-steps.svg",
        "code": "MOD 02",
        "title": "ПЕРВЫЕ ШАГИ НА GO: СИНТАКСИС, ТИПЫ, ФУНКЦИИ И CLI",
        "subtitle": "17 глав: от go build и типов данных до UTF-8, циклов for, функций, defer, ошибок error и BookmarkFlow step01–step02",
        "caption": "Инженерная карта Модуля 2: путь от исходного файла main.go и компилятора Go 1.24 до консольного менеджера закладок BookmarkFlow в памяти",
        "alt": "Инженерный чертёж Модуля 2: анатомия программы на Go, типы, UTF-8, управление потоком, ошибки как значения и CLI BookmarkFlow",
        "body": '''
  <!-- Left: Source code & compiler -->
  <rect x="55" y="135" width="320" height="225" rx="6" class="box"/>
  <text x="215" y="164" text-anchor="middle" class="mono-blue">1. ИСХОДНИК И КОМПИЛЯТОР</text>
  <rect x="78" y="180" width="274" height="110" class="box-dark"/>
  <text x="95" y="205" class="mono">package main</text>
  <text x="95" y="228" class="mono">import "fmt"</text>
  <text x="95" y="251" class="mono">func main() {</text>
  <text x="95" y="274" class="mono">    fmt.Println("Go 1.24")</text>
  <rect x="78" y="304" width="130" height="36" class="box-accent"/>
  <text x="143" y="327" text-anchor="middle" class="mono-blue">gofmt + go vet</text>
  <rect x="222" y="304" width="130" height="36" class="box-warm"/>
  <text x="287" y="327" text-anchor="middle" class="mono-orange">go build</text>

  <!-- Center: Core Constructs -->
  <rect x="415" y="135" width="365" height="225" rx="6" class="box"/>
  <text x="597" y="164" text-anchor="middle" class="mono-blue">2. БАЗОВЫЕ КОНСТРУКЦИИ ЯЗЫКА</text>
  <rect x="435" y="182" width="155" height="48" class="box-accent"/>
  <text x="512" y="203" text-anchor="middle" class="mono-bold">int · float64 · bool</text>
  <text x="512" y="221" text-anchor="middle" class="label">Строгие типы и :=</text>
  <rect x="605" y="182" width="155" height="48" class="box-accent"/>
  <text x="682" y="203" text-anchor="middle" class="mono-bold">string · byte · rune</text>
  <text x="682" y="221" text-anchor="middle" class="label">UTF-8 без искажений</text>
  <rect x="435" y="242" width="155" height="48" class="box-dark"/>
  <text x="512" y="263" text-anchor="middle" class="mono-bold">if · switch · for</text>
  <text x="512" y="281" text-anchor="middle" class="label">for i := range n</text>
  <rect x="605" y="242" width="155" height="48" class="box-warm"/>
  <text x="682" y="263" text-anchor="middle" class="mono-orange">(val, err) + defer</text>
  <text x="682" y="281" text-anchor="middle" class="label">errors.Is / fmt.Errorf</text>
  <text x="597" y="330" text-anchor="middle" class="mono">Явный возврат ошибок вместо исключений</text>

  <!-- Right: CLI Project step01-02 -->
  <rect x="820" y="135" width="325" height="225" rx="6" class="box-accent"/>
  <text x="982" y="164" text-anchor="middle" class="mono-blue">3. BOOKMARKFLOW (STEP 01–02)</text>
  <rect x="842" y="182" width="280" height="112" class="box"/>
  <text x="858" y="206" class="mono-bold">$ bookmark add "Go" https://go.dev</text>
  <text x="858" y="230" class="mono">$ bookmark list</text>
  <text x="858" y="254" class="mono-blue">ID | TITLE | URL</text>
  <text x="858" y="276" class="mono">1  | Go    | https://go.dev</text>
  <rect x="842" y="306" width="280" height="36" class="box-warm"/>
  <text x="982" y="329" text-anchor="middle" class="mono-orange">os.Args · валидация · код выхода</text>

  <line x1="375" y1="247" x2="412" y2="247" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="780" y1="247" x2="817" y2="247" class="line-blue" marker-end="url(#arrowBlue)"/>

  <!-- Bottom flow: Error handling & UTF-8 -->
  <rect x="55" y="390" width="1090" height="175" rx="6" class="box"/>
  <text x="80" y="422" class="mono-bold">КЛЮЧЕВАЯ ДИСЦИПЛИНА МОДУЛЯ 2: ПРОВЕРКА ОШИБОК И СТЕК DEFER (LIFO)</text>
  <rect x="80" y="442" width="230" height="95" class="box-dark"/>
  <text x="195" y="472" text-anchor="middle" class="mono-bold">Вход: os.Args</text>
  <text x="195" y="497" text-anchor="middle" class="mono">strings.TrimSpace</text>
  <text x="195" y="520" text-anchor="middle" class="label">Очистка аргументов</text>

  <line x1="310" y1="490" x2="355" y2="490" class="line" marker-end="url(#arrow)"/>

  <rect x="358" y="442" width="250" height="95" class="box-warm"/>
  <text x="483" y="472" text-anchor="middle" class="mono-orange">if err != nil</text>
  <text x="483" y="497" text-anchor="middle" class="mono">fmt.Errorf("...: %w", err)</text>
  <text x="483" y="520" text-anchor="middle" class="label">Ранний выход с контекстом</text>

  <line x1="608" y1="490" x2="653" y2="490" class="line" marker-end="url(#arrow)"/>

  <rect x="656" y="442" width="220" height="95" class="box-accent"/>
  <text x="766" y="472" text-anchor="middle" class="mono-blue">utf8.RuneCountInString</text>
  <text x="766" y="497" text-anchor="middle" class="mono">fmt.Printf("%-20s")</text>
  <text x="766" y="520" text-anchor="middle" class="label">Ровные колонки таблицы</text>

  <line x1="876" y1="490" x2="921" y2="490" class="line" marker-end="url(#arrow)"/>

  <rect x="924" y="442" width="195" height="95" class="box"/>
  <text x="1021" y="472" text-anchor="middle" class="mono-bold">project/step02/</text>
  <text x="1021" y="497" text-anchor="middle" class="mono-blue">add · list · search</text>
  <text x="1021" y="520" text-anchor="middle" class="label">Готовый CLI в памяти</text>
'''
    },
    {
        "dir": "sources/3. Данные, память, интерфейсы и первые тесты",
        "filename": "cover-module-03-data-memory.svg",
        "code": "MOD 03",
        "title": "ДАННЫЕ, ПАМЯТЬ, ИНТЕРФЕЙСЫ И ПЕРВЫЕ ТЕСТЫ GO TEST",
        "subtitle": "19 глав: указатели, слайсы (ptr, len, cap), мапы, структуры, методы, интерфейсы, дженерики и тесты BookmarkFlow step03–step04",
        "caption": "Инженерная карта Модуля 3: от указателей и 24-байтного заголовка слайса через структуры и интерфейс Store к табличным тестам go test",
        "alt": "Инженерный чертёж Модуля 3: заголовок слайса, структура Bookmark, интерфейс Store и модульные тесты go test",
        "body": '''
  <!-- Box 1: Slice Header & Backing Array -->
  <rect x="55" y="135" width="340" height="230" rx="6" class="box"/>
  <text x="225" y="164" text-anchor="middle" class="mono-blue">1. ПАМЯТЬ И СЛАЙС (24 БАЙТА)</text>
  <rect x="75" y="184" width="115" height="105" class="box-accent"/>
  <text x="132" y="208" text-anchor="middle" class="mono-bold">ptr: 0xc000</text>
  <line x1="75" y1="218" x2="190" y2="218" stroke="#0369a1"/>
  <text x="132" y="242" text-anchor="middle" class="mono">len: 2</text>
  <line x1="75" y1="252" x2="190" y2="252" stroke="#0369a1"/>
  <text x="132" y="276" text-anchor="middle" class="mono">cap: 4</text>

  <rect x="235" y="184" width="135" height="135" class="box-dark"/>
  <text x="302" y="208" text-anchor="middle" class="mono-bold">[0] "go"</text>
  <text x="302" y="238" text-anchor="middle" class="mono-bold">[1] "cli"</text>
  <text x="302" y="268" text-anchor="middle" class="label">[2] "" (запас)</text>
  <text x="302" y="298" text-anchor="middle" class="label">[3] "" (запас)</text>
  <line x1="190" y1="202" x2="232" y2="202" class="line-orange" marker-end="url(#arrowOrange)"/>
  <text x="225" y="346" text-anchor="middle" class="label">Указатели &amp;T / *T · Массивы · Мапы</text>

  <!-- Box 2: Structs & Interfaces -->
  <rect x="425" y="135" width="350" height="230" rx="6" class="box"/>
  <text x="600" y="164" text-anchor="middle" class="mono-blue">2. СТРУКТУРЫ И ИНТЕРФЕЙС STORE</text>
  <rect x="448" y="184" width="304" height="68" class="box-warm"/>
  <text x="600" y="208" text-anchor="middle" class="mono-orange">type Store interface</text>
  <text x="600" y="234" text-anchor="middle" class="mono">Add(Bookmark) · List() · Delete(id)</text>

  <rect x="448" y="274" width="142" height="65" class="box-accent"/>
  <text x="519" y="300" text-anchor="middle" class="mono-bold">*MemoryStore</text>
  <text x="519" y="322" text-anchor="middle" class="label">в оперативной памяти</text>

  <rect x="610" y="274" width="142" height="65" class="box-accent"/>
  <text x="681" y="300" text-anchor="middle" class="mono-bold">*FileStore</text>
  <text x="681" y="322" text-anchor="middle" class="label">JSON-файл на диске</text>

  <line x1="519" y1="274" x2="560" y2="254" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="681" y1="274" x2="640" y2="254" class="line-blue" marker-end="url(#arrowBlue)"/>

  <!-- Box 3: Testing -->
  <rect x="805" y="135" width="340" height="230" rx="6" class="box-accent"/>
  <text x="975" y="164" text-anchor="middle" class="mono-blue">3. АВТОТЕСТЫ (GO TEST)</text>
  <rect x="828" y="184" width="294" height="115" class="box"/>
  <text x="845" y="210" class="mono-bold">func TestStore(t *testing.T)</text>
  <text x="845" y="236" class="mono">dir := t.TempDir()</text>
  <text x="845" y="262" class="mono">t.Run(tc.name, func(t *testing.T))</text>
  <text x="845" y="286" class="mono-blue">PASS: 100% табличных кейсов</text>
  <rect x="828" y="312" width="294" height="36" class="box-warm"/>
  <text x="975" y="335" text-anchor="middle" class="mono-orange">project/step03/ &amp; project/step04/</text>

  <!-- Bottom summary -->
  <rect x="55" y="395" width="1090" height="170" rx="6" class="box"/>
  <text x="80" y="427" class="mono-bold">ЭВОЛЮЦИЯ АРХИТЕКТУРЫ BOOKMARKFLOW В МОДУЛЕ 3:</text>
  <rect x="80" y="448" width="310" height="90" class="box-dark"/>
  <text x="235" y="476" text-anchor="middle" class="mono-bold">Было в Модуле 2:</text>
  <text x="235" y="502" text-anchor="middle" class="mono">ids []int, urls []string</text>
  <text x="235" y="524" text-anchor="middle" class="label">Разрозненные списки без сохранения</text>

  <line x1="390" y1="493" x2="440" y2="493" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="443" y="448" width="310" height="90" class="box-accent"/>
  <text x="598" y="476" text-anchor="middle" class="mono-blue">Шаг 3 (step03):</text>
  <text x="598" y="502" text-anchor="middle" class="mono-bold">type Bookmark struct + JSON</text>
  <text x="598" y="524" text-anchor="middle" class="label">Методы и сохранение на диск</text>

  <line x1="753" y1="493" x2="803" y2="493" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="806" y="448" width="310" height="90" class="box-warm"/>
  <text x="961" y="476" text-anchor="middle" class="mono-orange">Шаг 4 (step04):</text>
  <text x="961" y="502" text-anchor="middle" class="mono-bold">Интерфейс Store + go test</text>
  <text x="961" y="524" text-anchor="middle" class="label">Подменяемое хранилище и тесты</text>
'''
    },
    {
        "dir": "sources/4. Стандартная библиотека, философия Go и базовая конкурентность",
        "filename": "cover-module-04-stdlib-concurrency.svg",
        "code": "MOD 04",
        "title": "СТАНДАРТНАЯ БИБЛИОТЕКА, ФИЛОСОФИЯ GO И КОНКУРЕНТНОСТЬ",
        "subtitle": "30 глав в 3 подразделах: рабочие пакеты stdlib (4.1) → 7 эссе о философии Go (4.2) → горутины, каналы и step05 (4.3)",
        "caption": "Инженерная карта Модуля 4: три опоры зрелого Go-кода — потоковая стандартная библиотека, инженерная философия простоты и конкурентный пул воркеров",
        "alt": "Инженерный чертёж Модуля 4: стандартная библиотека io/bufio/json/slog, 7 эссе философии Go и конкурентный Worker Pool",
        "body": '''
  <!-- Pillar 1: Stdlib -->
  <rect x="55" y="135" width="340" height="275" rx="6" class="box"/>
  <text x="225" y="165" text-anchor="middle" class="mono-blue">4.1. СТАНДАРТНАЯ БИБЛИОТЕКА</text>
  <rect x="80" y="185" width="290" height="46" class="box-accent"/>
  <text x="225" y="213" text-anchor="middle" class="mono-bold">io.Reader → bufio → io.Writer</text>
  <rect x="80" y="242" width="138" height="42" class="box-dark"/>
  <text x="149" y="268" text-anchor="middle" class="mono">strings / bytes</text>
  <rect x="232" y="242" width="138" height="42" class="box-dark"/>
  <text x="301" y="268" text-anchor="middle" class="mono">os / io/fs</text>
  <rect x="80" y="295" width="138" height="42" class="box-dark"/>
  <text x="149" y="321" text-anchor="middle" class="mono">encoding/json</text>
  <rect x="232" y="295" width="138" height="42" class="box-dark"/>
  <text x="301" y="321" text-anchor="middle" class="mono">log/slog · time</text>
  <text x="225" y="375" text-anchor="middle" class="label">12 уроков · 0 внешних зависимостей</text>

  <!-- Pillar 2: Philosophy -->
  <rect x="430" y="135" width="340" height="275" rx="6" class="box"/>
  <text x="600" y="165" text-anchor="middle" class="mono-blue">4.2. ФИЛОСОФИЯ GO (7 ЭССЕ)</text>
  <rect x="455" y="185" width="290" height="38" class="box-warm"/>
  <text x="600" y="209" text-anchor="middle" class="mono-orange">25 ключевых слов · Ясность</text>
  <rect x="455" y="233" width="290" height="38" class="box-dark"/>
  <text x="600" y="257" text-anchor="middle" class="mono">Ошибки — обычные значения</text>
  <rect x="455" y="281" width="290" height="38" class="box-dark"/>
  <text x="600" y="305" text-anchor="middle" class="mono">Маленькие интерфейсы и gofmt</text>
  <rect x="455" y="329" width="290" height="38" class="box-dark"/>
  <text x="600" y="353" text-anchor="middle" class="mono">Полезные нули и наследие Unix</text>
  <text x="600" y="392" text-anchor="middle" class="label">7 эссе · осознанные компромиссы</text>

  <!-- Pillar 3: Concurrency -->
  <rect x="805" y="135" width="340" height="275" rx="6" class="box-accent"/>
  <text x="975" y="165" text-anchor="middle" class="mono-blue">4.3. КОНКУРЕНТНОСТЬ БЕЗ БОЛИ</text>
  <rect x="830" y="185" width="290" height="46" class="box"/>
  <text x="975" y="213" text-anchor="middle" class="mono-bold">go worker(ctx, jobs, results)</text>
  <rect x="830" y="242" width="138" height="42" class="box"/>
  <text x="899" y="268" text-anchor="middle" class="mono">chan / select</text>
  <rect x="982" y="242" width="138" height="42" class="box"/>
  <text x="1051" y="268" text-anchor="middle" class="mono">WaitGroup</text>
  <rect x="830" y="295" width="138" height="42" class="box"/>
  <text x="899" y="321" text-anchor="middle" class="mono">RWMutex</text>
  <rect x="982" y="295" width="138" height="42" class="box-warm"/>
  <text x="1051" y="321" text-anchor="middle" class="mono-orange">go test -race</text>
  <text x="975" y="375" text-anchor="middle" class="label">11 уроков · context.Context и пул</text>

  <!-- Bottom integration: project/step05 -->
  <rect x="55" y="435" width="1090" height="130" rx="6" class="box-warm"/>
  <text x="80" y="468" class="mono-orange">ИТОГ МОДУЛЯ 4 — PROJECT/STEP05 (КОНКУРЕНТНЫЙ ЧЕКЕР BOOKMARKFLOW):</text>
  <text x="80" y="502" class="mono">SafeStore (sync.RWMutex)  +  Worker Pool (N горутин)  +  context.WithTimeout  +  go test -race ./...</text>
  <text x="80" y="534" class="sub">200 сохранённых ссылок проверяются конкурентно за доли секунды без гонок данных и утечек горутин.</text>
'''
    },
    {
        "dir": "sources/4. Стандартная библиотека, философия Go и базовая конкурентность/1. Рабочая стандартная библиотека",
        "filename": "cover-sub-04-01-stdlib.svg",
        "code": "SUB 4.1",
        "title": "ПОДРАЗДЕЛ 4.1: РАБОЧАЯ СТАНДАРТНАЯ БИБЛИОТЕКА GO",
        "subtitle": "12 глав: потоки io.Reader/Writer, буферизация bufio, строки, файлы io/fs, флаги, время, JSON, CSV/URL, log/slog и коллекции",
        "caption": "Схема Подраздела 4.1: сквозной конвейер потоков байтов io.Reader и io.Writer, объединяющий файлы, буферы, кодировщики JSON/CSV и логгер log/slog",
        "alt": "Инженерный чертёж Подраздела 4.1: конвейер io.Reader и io.Writer в стандартной библиотеке Go",
        "body": '''
  <!-- Central Pipeline: io.Reader -> bufio -> transform -> io.Writer -->
  <rect x="55" y="140" width="1090" height="210" rx="6" class="box"/>
  <text x="600" y="172" text-anchor="middle" class="mono-blue">УНИВЕРСАЛЬНЫЙ ПОТОКОВЫЙ КОНВЕЙЕР БАЙТОВ В СТАНДАРТНОЙ БИБЛИОТЕКЕ GO</text>

  <rect x="80" y="200" width="210" height="115" class="box-dark"/>
  <text x="185" y="226" text-anchor="middle" class="mono-bold">Источники байтов</text>
  <text x="185" y="252" text-anchor="middle" class="mono">os.File · strings.Reader</text>
  <text x="185" y="276" text-anchor="middle" class="mono">bytes.Buffer · embed.FS</text>
  <text x="185" y="300" text-anchor="middle" class="label">возвращают ([]byte, error)</text>

  <line x1="290" y1="257" x2="340" y2="257" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="343" y="200" width="220" height="115" class="box-accent"/>
  <text x="453" y="228" text-anchor="middle" class="mono-blue">io.Reader / bufio</text>
  <text x="453" y="256" text-anchor="middle" class="mono-bold">Read(p []byte) (n, err)</text>
  <text x="453" y="280" text-anchor="middle" class="mono">bufio.Scanner · LimitReader</text>
  <text x="453" y="302" text-anchor="middle" class="label">Буфер 4 КБ · Токены до 64 КБ</text>

  <line x1="563" y1="257" x2="613" y2="257" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="616" y="200" width="230" height="115" class="box-warm"/>
  <text x="731" y="228" text-anchor="middle" class="mono-orange">Разбор и структура</text>
  <text x="731" y="256" text-anchor="middle" class="mono-bold">encoding/json · csv</text>
  <text x="731" y="280" text-anchor="middle" class="mono">strconv · regexp · net/url</text>
  <text x="731" y="302" text-anchor="middle" class="label">Теги struct и валидация</text>

  <line x1="846" y1="257" x2="896" y2="257" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="899" y="200" width="220" height="115" class="box-accent"/>
  <text x="1009" y="228" text-anchor="middle" class="mono-blue">io.Writer / Выход</text>
  <text x="1009" y="256" text-anchor="middle" class="mono-bold">Write(p []byte) (n, err)</text>
  <text x="1009" y="280" text-anchor="middle" class="mono">bufio.Writer.Flush()</text>
  <text x="1009" y="302" text-anchor="middle" class="mono">log/slog (Text / JSON)</text>

  <!-- Bottom cards -->
  <rect x="55" y="380" width="345" height="185" rx="6" class="box"/>
  <text x="227" y="412" text-anchor="middle" class="mono-bold">ФАЙЛЫ, ФЛАГИ И ВРЕМЯ</text>
  <text x="80" y="445" class="mono">• path/filepath &amp; io/fs</text>
  <text x="80" y="473" class="mono">• flag.NewFlagSet &amp; //go:embed</text>
  <text x="80" y="501" class="mono">• time.Time (Monotonic Clock)</text>
  <text x="80" y="529" class="mono">• Шаблон даты: 2006-01-02 15:04:05</text>

  <rect x="427" y="380" width="345" height="185" rx="6" class="box"/>
  <text x="600" y="412" text-anchor="middle" class="mono-bold">КОЛЛЕКЦИИ GO 1.22–1.24</text>
  <text x="452" y="445" class="mono">• slices.SortFunc &amp; BinarySearch</text>
  <text x="452" y="473" class="mono">• slices.Compact &amp; DeleteFunc</text>
  <text x="452" y="501" class="mono">• maps.Clone &amp; maps.Equal</text>
  <text x="452" y="529" class="mono">• cmp.Compare &amp; cmp.Or</text>

  <rect x="800" y="380" width="345" height="185" rx="6" class="box"/>
  <text x="972" y="412" text-anchor="middle" class="mono-bold">ГРАНИЦА ОШИБОК И ПАНИКИ</text>
  <text x="825" y="445" class="mono-blue">• Ожидаемый сбой → error</text>
  <text x="825" y="473" class="mono-orange">• Баг инварианта → panic</text>
  <text x="825" y="501" class="mono">• Перехват → recover() в defer</text>
  <text x="825" y="529" class="label">Только на границе пакета/сервера</text>
'''
    },
    {
        "dir": "sources/4. Стандартная библиотека, философия Go и базовая конкурентность/2. Философия Go в 7 коротких эссе",
        "filename": "cover-sub-04-02-philosophy.svg",
        "code": "SUB 4.2",
        "title": "ПОДРАЗДЕЛ 4.2: ФИЛОСОФИЯ GO В 7 КОРОТКИХ ЭССЕ",
        "subtitle": "От наследия Bell Labs и Unix до 25 ключевых слов, явных ошибок, маленьких интерфейсов, gofmt и полезных нулевых значений",
        "caption": "Схема Подраздела 4.2: семь инженерных принципов Go, выросших из опыта создания Unix в Bell Labs и практики разработки больших серверных систем",
        "alt": "Инженерный чертёж Подраздела 4.2: семь принципов философии языка Go",
        "body": '''
  <!-- Top row: 4 essays -->
  <rect x="55" y="135" width="255" height="190" rx="6" class="box"/>
  <text x="182" y="165" text-anchor="middle" class="mono-blue">ЭССЕ 1 · ПРОСТОТА</text>
  <text x="182" y="202" text-anchor="middle" class="mono-bold">25 ключевых слов</text>
  <text x="182" y="232" text-anchor="middle" class="label">Меньше фич — меньше</text>
  <text x="182" y="252" text-anchor="middle" class="label">мультипликативной сложности.</text>
  <text x="182" y="288" text-anchor="middle" class="mono">Читаемость &gt; Хитрость</text>

  <rect x="333" y="135" width="255" height="190" rx="6" class="box"/>
  <text x="460" y="165" text-anchor="middle" class="mono-blue">ЭССЕ 2 · ОШИБКИ</text>
  <text x="460" y="202" text-anchor="middle" class="mono-bold">if err != nil</text>
  <text x="460" y="232" text-anchor="middle" class="label">Ошибки — обычные значения,</text>
  <text x="460" y="252" text-anchor="middle" class="label">а не скрытые прыжки try/catch.</text>
  <text x="460" y="288" text-anchor="middle" class="mono">Явный поток управления</text>

  <rect x="611" y="135" width="255" height="190" rx="6" class="box"/>
  <text x="738" y="165" text-anchor="middle" class="mono-blue">ЭССЕ 3 · КОМПОЗИЦИЯ</text>
  <text x="738" y="202" text-anchor="middle" class="mono-bold">1–2 метода в интерфейсе</text>
  <text x="738" y="232" text-anchor="middle" class="label">Принимай узкие интерфейсы,</text>
  <text x="738" y="252" text-anchor="middle" class="label">возвращай конкретные типы.</text>
  <text x="738" y="288" text-anchor="middle" class="mono">io.Reader · Store</text>

  <rect x="889" y="135" width="255" height="190" rx="6" class="box"/>
  <text x="1016" y="165" text-anchor="middle" class="mono-blue">ЭССЕ 4 · СТАНДАРТ GOFMT</text>
  <text x="1016" y="202" text-anchor="middle" class="mono-bold">Один формат для всех</text>
  <text x="1016" y="232" text-anchor="middle" class="label">Ноль споров о скобках</text>
  <text x="1016" y="252" text-anchor="middle" class="label">на код-ревью и чистые git diff.</text>
  <text x="1016" y="288" text-anchor="middle" class="mono">Машинный формат кода</text>

  <!-- Bottom row: 3 essays -->
  <rect x="55" y="355" width="340" height="205" rx="6" class="box"/>
  <text x="225" y="387" text-anchor="middle" class="mono-blue">ЭССЕ 5 · НУЛЕВЫЕ ЗНАЧЕНИЯ</text>
  <text x="225" y="424" text-anchor="middle" class="mono-bold">var buf bytes.Buffer</text>
  <text x="225" y="452" text-anchor="middle" class="mono-bold">var mu sync.Mutex</text>
  <text x="225" y="486" text-anchor="middle" class="label">Структура работает сразу после объявления</text>
  <text x="225" y="508" text-anchor="middle" class="label">без обязательного конструктора.</text>

  <rect x="425" y="355" width="350" height="205" rx="6" class="box-accent"/>
  <text x="600" y="387" text-anchor="middle" class="mono-blue">ЭССЕ 6 · НАСЛЕДИЕ UNIX В GO</text>
  <text x="600" y="424" text-anchor="middle" class="mono-bold">Bell Labs (1969) → Go (2009)</text>
  <text x="600" y="456" text-anchor="middle" class="label">«Пишите ясно — не умничайте.»</text>
  <text x="600" y="482" text-anchor="middle" class="label">Маленькие ортогональные инструменты</text>
  <text x="600" y="508" text-anchor="middle" class="label">и продуктивность через удаление лишнего.</text>

  <rect x="805" y="355" width="340" height="205" rx="6" class="box-warm"/>
  <text x="975" y="387" text-anchor="middle" class="mono-orange">ЭССЕ 7 · ЧЕСТНЫЕ ГРАНИЦЫ</text>
  <text x="975" y="424" text-anchor="middle" class="mono-bold">Инженерная матрица выбора</text>
  <text x="975" y="456" text-anchor="middle" class="label">Где Go лучший: бэкенды, сеть, CLI, облако.</text>
  <text x="975" y="482" text-anchor="middle" class="label">Где нужен другой язык: ядра ОС (C/Rust),</text>
  <text x="975" y="508" text-anchor="middle" class="label">ML/ноутбуки (Python), браузер (TS).</text>
'''
    },
    {
        "dir": "sources/4. Стандартная библиотека, философия Go и базовая конкурентность/3. Конкурентность без боли",
        "filename": "cover-sub-04-03-concurrency.svg",
        "code": "SUB 4.3",
        "title": "ПОДРАЗДЕЛ 4.3: КОНКУРЕНТНОСТЬ БЕЗ БОЛИ",
        "subtitle": "11 глав: конкурентность vs параллелизм, горутины, каналы, select, WaitGroup, Mutex/RWMutex, -race, context и Worker Pool",
        "caption": "Схема Подраздела 4.3: архитектура пула воркеров на горутинах и каналах с отменой через context.Context и защитой состояния через sync.RWMutex",
        "alt": "Инженерный чертёж Подраздела 4.3: пул горутин-воркеров, каналы jobs и results, context.Context и sync.RWMutex",
        "body": '''
  <!-- Worker Pool Architecture Diagram -->
  <rect x="55" y="135" width="225" height="240" rx="6" class="box"/>
  <text x="167" y="165" text-anchor="middle" class="mono-blue">КОНТЕКСТ И ЗАДАЧИ</text>
  <rect x="77" y="185" width="180" height="65" class="box-warm"/>
  <text x="167" y="212" text-anchor="middle" class="mono-orange">context.Context</text>
  <text x="167" y="235" text-anchor="middle" class="mono">WithTimeout(5 * s)</text>
  <rect x="77" y="270" width="180" height="80" class="box-accent"/>
  <text x="167" y="298" text-anchor="middle" class="mono-blue">jobs chan Bookmark</text>
  <text x="167" y="322" text-anchor="middle" class="mono">буфер + close(jobs)</text>

  <line x1="280" y1="310" x2="355" y2="205" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="280" y1="310" x2="355" y2="275" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="280" y1="310" x2="355" y2="345" class="line-blue" marker-end="url(#arrowBlue)"/>

  <!-- Workers -->
  <rect x="360" y="135" width="420" height="240" rx="6" class="box-accent"/>
  <text x="570" y="165" text-anchor="middle" class="mono-blue">ПУЛ ВОРКЕРОВ (N ГОРУТИН · СТЕК ОТ 2 КБ)</text>
  <rect x="390" y="182" width="360" height="44" class="box"/>
  <text x="570" y="209" text-anchor="middle" class="mono-bold">Горутина #1: select { case &lt;-ctx.Done(): ... }</text>
  <rect x="390" y="238" width="360" height="44" class="box"/>
  <text x="570" y="265" text-anchor="middle" class="mono-bold">Горутина #2: select { case job := &lt;-jobs: ... }</text>
  <rect x="390" y="294" width="360" height="44" class="box"/>
  <text x="570" y="321" text-anchor="middle" class="mono-bold">Горутина #N: проверка URL + wg.Done()</text>
  <text x="570" y="360" text-anchor="middle" class="label">Ограничение параллелизма · Защита от утечек горутин</text>

  <line x1="780" y1="205" x2="855" y2="255" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="780" y1="275" x2="855" y2="255" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="780" y1="345" x2="855" y2="255" class="line-blue" marker-end="url(#arrowBlue)"/>

  <!-- Results & Sync -->
  <rect x="860" y="135" width="285" height="240" rx="6" class="box"/>
  <text x="1002" y="165" text-anchor="middle" class="mono-blue">СБОР И СИНХРОНИЗАЦИЯ</text>
  <rect x="882" y="185" width="240" height="75" class="box-accent"/>
  <text x="1002" y="214" text-anchor="middle" class="mono-blue">results chan CheckResult</text>
  <text x="1002" y="240" text-anchor="middle" class="mono">wg.Wait() → close(results)</text>
  <rect x="882" y="275" width="240" height="80" class="box-warm"/>
  <text x="1002" y="304" text-anchor="middle" class="mono-orange">SafeStore (sync.RWMutex)</text>
  <text x="1002" y="328" text-anchor="middle" class="mono">RLock / Lock · go test -race</text>

  <!-- Bottom rule bar -->
  <rect x="55" y="405" width="1090" height="160" rx="6" class="box"/>
  <text x="80" y="438" class="mono-bold">ДВА ИНСТРУМЕНТА КОНКУРЕНТНОСТИ В GO И КОГДА КАКОЙ ВЫБИРАТЬ:</text>
  <rect x="80" y="458" width="490" height="82" class="box-accent"/>
  <text x="325" y="486" text-anchor="middle" class="mono-blue">Каналы (chan T) + select</text>
  <text x="325" y="514" text-anchor="middle" class="sub">Передача владения данными, конвейеры задач, сигналы отмены</text>
  <rect x="610" y="458" width="510" height="82" class="box-warm"/>
  <text x="865" y="486" text-anchor="middle" class="mono-orange">Мьютексы (sync.Mutex / sync.RWMutex)</text>
  <text x="865" y="514" text-anchor="middle" class="sub">Защита внутреннего состояния структуры (кэш, счётчик, Store)</text>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом",
        "filename": "cover-module-05-cs-foundation.svg",
        "code": "MOD 05",
        "title": "КОМПЬЮТЕР, ОС LINUX И СЕТИ ПОД ТВОИМ КОДОМ НА GO",
        "subtitle": "38 глав в 3 подразделах: процессор и память (5.1) → ядро Linux, процессы и файлы (5.2) → стек TCP/IP, сокеты, TLS и HTTP (5.3)",
        "caption": "Инженерная карта Модуля 5: три этажа под программой на Go — аппаратная архитектура CPU и кэшей, ядро Linux с системными вызовами и сетевой стек TCP/IP",
        "alt": "Инженерный чертёж Модуля 5: три уровня под кодом Go — железо CPU/RAM, ядро Linux и сетевой стек TCP/IP",
        "body": '''
  <!-- 3 Horizontal Layers under Go code -->
  <rect x="55" y="130" width="1090" height="75" rx="6" class="box-accent"/>
  <text x="600" y="162" text-anchor="middle" class="mono-blue">ВАША ПРОГРАММА НА GO (BOOKMARKFLOW · PROJECT/STEP06)</text>
  <text x="600" y="188" text-anchor="middle" class="mono">[]Bookmark в памяти  ·  Атомарное сохранение через os.Rename  ·  TCP-сервер на net.Listen(":9090")</text>

  <!-- Layer 5.1 -->
  <rect x="55" y="230" width="345" height="335" rx="6" class="box"/>
  <text x="227" y="262" text-anchor="middle" class="mono-blue">5.1. КОМПЬЮТЕР ИЗНУТРИ (12 ГЛАВ)</text>
  <rect x="80" y="282" width="295" height="50" class="box-dark"/>
  <text x="227" y="305" text-anchor="middle" class="mono-bold">Биты · Доп. код · IEEE 754</text>
  <text x="227" y="324" text-anchor="middle" class="label">Почему 0.1 + 0.2 != 0.3</text>
  <rect x="80" y="344" width="295" height="50" class="box-dark"/>
  <text x="227" y="367" text-anchor="middle" class="mono-bold">Конвейер CPU и кэши L1–L3</text>
  <text x="227" y="386" text-anchor="middle" class="label">Кэш-линии 64 Б и локальность слайсов</text>
  <rect x="80" y="406" width="295" height="50" class="box-dark"/>
  <text x="227" y="429" text-anchor="middle" class="mono-bold">Стек, куча, GC и выравнивание</text>
  <text x="227" y="448" text-anchor="middle" class="label">Паддинг полей struct и endianness</text>
  <rect x="80" y="468" width="295" height="50" class="box-accent"/>
  <text x="227" y="491" text-anchor="middle" class="mono-blue">Автономный бинарник Go</text>
  <text x="227" y="510" text-anchor="middle" class="label">Компиляция и замер локальности</text>

  <!-- Layer 5.2 -->
  <rect x="427" y="230" width="345" height="335" rx="6" class="box"/>
  <text x="600" y="262" text-anchor="middle" class="mono-blue">5.2. ОС И LINUX (13 ГЛАВ)</text>
  <rect x="452" y="282" width="295" height="50" class="box-dark"/>
  <text x="600" y="305" text-anchor="middle" class="mono-bold">User Space ↔ Kernel Space</text>
  <text x="600" y="324" text-anchor="middle" class="label">Процессы PID, потоки ОС и syscalls</text>
  <rect x="452" y="344" width="295" height="50" class="box-dark"/>
  <text x="600" y="367" text-anchor="middle" class="mono-bold">Виртуальная память и inode</text>
  <text x="600" y="386" text-anchor="middle" class="label">Страницы 4 КБ · RSS · Файловая система</text>
  <rect x="452" y="406" width="295" height="50" class="box-dark"/>
  <text x="600" y="429" text-anchor="middle" class="mono-bold">Дескрипторы, трубы и сигналы</text>
  <text x="600" y="448" text-anchor="middle" class="label">ulimit -n · stdin/stdout · SIGTERM</text>
  <rect x="452" y="468" width="295" height="50" class="box-warm"/>
  <text x="600" y="491" text-anchor="middle" class="mono-orange">strace · /proc · Атомарный Rename</text>
  <text x="600" y="510" text-anchor="middle" class="label">Защита файла от обрыва питания</text>

  <!-- Layer 5.3 -->
  <rect x="800" y="230" width="345" height="335" rx="6" class="box"/>
  <text x="972" y="262" text-anchor="middle" class="mono-blue">5.3. СЕТИ И HTTP (13 ГЛАВ)</text>
  <rect x="825" y="282" width="295" height="50" class="box-dark"/>
  <text x="972" y="305" text-anchor="middle" class="mono-bold">4 слоя TCP/IP · IPv4/IPv6 · NAT</text>
  <text x="972" y="324" text-anchor="middle" class="label">Кадр → Пакет → Сегмент → Сообщение</text>
  <rect x="825" y="344" width="295" height="50" class="box-dark"/>
  <text x="972" y="367" text-anchor="middle" class="mono-bold">DNS · TCP Handshake · UDP</text>
  <text x="972" y="386" text-anchor="middle" class="label">SYN/ACK · Поток байтов · TIME_WAIT</text>
  <rect x="825" y="406" width="295" height="50" class="box-accent"/>
  <text x="972" y="429" text-anchor="middle" class="mono-blue">Сокеты Go: net.Listen &amp; Conn</text>
  <text x="972" y="448" text-anchor="middle" class="label">Конкурентный TCP-сервер step06</text>
  <rect x="825" y="468" width="295" height="50" class="box-dark"/>
  <text x="972" y="491" text-anchor="middle" class="mono-bold">TLS/HTTPS · HTTP/1.1–3 · curl/ss</text>
  <text x="972" y="510" text-anchor="middle" class="label">Анатомия веба и диагностика</text>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/1. Компьютер изнутри",
        "filename": "cover-sub-05-01-computer-inside.svg",
        "code": "SUB 5.1",
        "title": "ПОДРАЗДЕЛ 5.1: КОМПЬЮТЕР ИЗНУТРИ ГЛАЗАМИ GO-ИНЖЕНЕРА",
        "subtitle": "12 глав: битовые маски, дополнительный код, IEEE 754, конвейер CPU, пирамида кэшей L1–L3, кэш-линии 64 Б, стек/куча и выравнивание",
        "caption": "Схема Подраздела 5.1: путь данных от битового представления и выравнивания структуры Go через 64-байтную кэш-линию в регистры и конвейер ядра CPU",
        "alt": "Инженерный чертёж Подраздела 5.1: регистры и конвейер CPU, кэши L1-L3, кэш-линия 64 байта и раскладка структур в памяти",
        "body": '''
  <!-- Left: CPU Core & Pipeline -->
  <rect x="55" y="135" width="350" height="235" rx="6" class="box"/>
  <text x="230" y="164" text-anchor="middle" class="mono-blue">ЯДРО CPU: РЕГИСТРЫ И КОНВЕЙЕР</text>
  <rect x="80" y="184" width="300" height="50" class="box-warm"/>
  <text x="230" y="207" text-anchor="middle" class="mono-orange">[Fetch] → [Decode] → [Execute] → [Write]</text>
  <text x="230" y="226" text-anchor="middle" class="label">Предсказатель ветвлений (штраф промаха ~15–20 тактов)</text>
  <rect x="80" y="248" width="142" height="44" class="box-dark"/>
  <text x="151" y="275" text-anchor="middle" class="mono">Регистры (~0.3 нс)</text>
  <rect x="238" y="248" width="142" height="44" class="box-accent"/>
  <text x="309" y="275" text-anchor="middle" class="mono-blue">L1 Кэш (~1 нс)</text>
  <rect x="80" y="304" width="300" height="44" class="box-accent"/>
  <text x="230" y="331" text-anchor="middle" class="mono-bold">L2 (~4 нс)  →  L3 (~15 нс)</text>

  <!-- Right: 64-byte Cache Line & RAM -->
  <rect x="435" y="135" width="710" height="235" rx="6" class="box"/>
  <text x="790" y="164" text-anchor="middle" class="mono-blue">КЭШ-ЛИНИЯ 64 БАЙТА И ЛОКАЛЬНОСТЬ СЛАЙСОВ В RAM (~100 НС)</text>
  <rect x="460" y="186" width="660" height="68" class="box-accent"/>
  <text x="790" y="210" text-anchor="middle" class="mono-bold">Кэш-линия (64 Б) при чтении []int64 загружает сразу 8 соседних элементов:</text>
  <text x="790" y="238" text-anchor="middle" class="mono-blue">[ int64 #0 | int64 #1 | int64 #2 | int64 #3 | int64 #4 | int64 #5 | int64 #6 | int64 #7 ]</text>

  <rect x="460" y="272" width="320" height="76" class="box-dark"/>
  <text x="620" y="298" text-anchor="middle" class="mono-bold">[]Bookmark (значения подряд)</text>
  <text x="620" y="324" text-anchor="middle" class="label">Минимум промахов кэша и нагрузки на GC</text>

  <rect x="800" y="272" width="320" height="76" class="box-warm"/>
  <text x="960" y="298" text-anchor="middle" class="mono-orange">[]*Bookmark (прыжки по адресам)</text>
  <text x="960" y="324" text-anchor="middle" class="label">Промах кэша на каждом указателе (~100 нс)</text>

  <!-- Bottom: Number representations & struct alignment -->
  <rect x="55" y="395" width="530" height="170" rx="6" class="box"/>
  <text x="320" y="426" text-anchor="middle" class="mono-bold">ПРЕДСТАВЛЕНИЕ ЧИСЕЛ В БИТАХ</text>
  <text x="80" y="460" class="mono">• Доп. код (int8): -128..127 (0xFF = -1)</text>
  <text x="80" y="490" class="mono">• IEEE 754 (float64): [знак 1 | эксп 11 | мантисса 52]</text>
  <text x="80" y="520" class="mono-orange">• Деньги хранят в целых копейках/центах (int64)</text>
  <text x="80" y="546" class="mono">• Endianness: LittleEndian (x86/ARM) vs BigEndian (сеть)</text>

  <rect x="615" y="395" width="530" height="170" rx="6" class="box"/>
  <text x="880" y="426" text-anchor="middle" class="mono-bold">ВЫРАВНИВАНИЕ СТРУКТУРЫ (24 Б → 16 Б)</text>
  <rect x="640" y="446" width="480" height="44" class="box-warm"/>
  <text x="880" y="473" text-anchor="middle" class="mono">Bad (24 Б):  [bool 1Б][pad 7Б][int64 8Б][bool 1Б][pad 7Б]</text>
  <rect x="640" y="502" width="340" height="44" class="box-accent"/>
  <text x="810" y="529" text-anchor="middle" class="mono-blue">Good (16 Б): [int64 8Б][bool][bool][pad 6Б]</text>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/2. Операционная система и Linux",
        "filename": "cover-sub-05-02-linux-os.svg",
        "code": "SUB 5.2",
        "title": "ПОДРАЗДЕЛ 5.2: ОПЕРАЦИОННАЯ СИСТЕМА И LINUX",
        "subtitle": "13 глав: User/Kernel Space, процессы, виртуальная память, inode, файловые дескрипторы, пайпы, сигналы, syscalls, strace и os.Rename",
        "caption": "Схема Подраздела 5.2: процесс на Go в пространстве пользователя, таблица файловых дескрипторов, граница системных вызовов и атомарная замена файла через inode",
        "alt": "Инженерный чертёж Подраздела 5.2: анатомия процесса Linux, файловые дескрипторы, системные вызовы и ядро ОС",
        "body": '''
  <!-- Top Half: User Space Process -->
  <rect x="55" y="130" width="1090" height="205" rx="6" class="box"/>
  <text x="80" y="160" class="mono-blue">ПРОСТРАНСТВО ПОЛЬЗОВАТЕЛЯ (USER SPACE) — ПРОЦЕСС GO (PID 4821)</text>

  <rect x="80" y="178" width="310" height="135" class="box-dark"/>
  <text x="235" y="204" text-anchor="middle" class="mono-bold">Виртуальная память (страницы 4 КБ)</text>
  <text x="235" y="232" text-anchor="middle" class="mono">Код · Куча Go · Стеки горутин</text>
  <text x="235" y="258" text-anchor="middle" class="mono">ENV · cwd · Сигналы (SIGTERM)</text>
  <text x="235" y="288" text-anchor="middle" class="label">Изолировано MMU от чужих процессов</text>

  <rect x="420" y="178" width="340" height="135" class="box-accent"/>
  <text x="590" y="204" text-anchor="middle" class="mono-blue">Таблица файловых дескрипторов (FD)</text>
  <text x="445" y="234" class="mono">FD 0 → stdin   (поток ввода)</text>
  <text x="445" y="258" class="mono">FD 1 → stdout  (конвейер | pipe)</text>
  <text x="445" y="282" class="mono">FD 2 → stderr  (логи и ошибки)</text>
  <text x="445" y="304" class="mono-bold">FD 3 → bookmarks.json.tmp (файл/сокет)</text>

  <rect x="790" y="178" width="330" height="135" class="box-warm"/>
  <text x="955" y="204" text-anchor="middle" class="mono-orange">Атомарное сохранение файла</text>
  <text x="815" y="234" class="mono">1. CreateTemp("*.tmp") + Write</text>
  <text x="815" y="258" class="mono">2. tmp.Sync() + tmp.Close()</text>
  <text x="815" y="284" class="mono-bold">3. os.Rename(tmp, "bookmarks.json")</text>
  <text x="815" y="304" text-anchor="middle" class="label">Переключение ссылки на новый inode</text>

  <!-- Syscall Boundary Line -->
  <line x1="55" y1="360" x2="1145" y2="360" stroke="#c2410c" stroke-width="3" stroke-dasharray="10 6"/>
  <rect x="405" y="344" width="390" height="32" fill="#fff7ed" stroke="#c2410c" stroke-width="2"/>
  <text x="600" y="365" text-anchor="middle" class="mono-orange">ГРАНИЦА СИСТЕМНЫХ ВЫЗОВОВ (SYSCALLS · STRACE)</text>

  <!-- Bottom Half: Kernel Space -->
  <rect x="55" y="390" width="1090" height="175" rx="6" class="box-accent"/>
  <text x="80" y="420" class="mono-blue">ПРОСТРАНСТВО ЯДРА LINUX (KERNEL SPACE — RING 0)</text>

  <rect x="80" y="438" width="320" height="105" class="box"/>
  <text x="240" y="466" text-anchor="middle" class="mono-bold">Планировщик и таблица страниц</text>
  <text x="240" y="494" text-anchor="middle" class="mono">Потоки ОС · MMU · OOM Killer</text>
  <text x="240" y="520" text-anchor="middle" class="label">Видит реальную физическую RAM</text>

  <rect x="435" y="438" width="330" height="105" class="box"/>
  <text x="600" y="466" text-anchor="middle" class="mono-bold">VFS и таблица inode (ext4 / xfs)</text>
  <text x="600" y="494" text-anchor="middle" class="mono">inode #8421: размер, права 0600, блоки</text>
  <text x="600" y="520" text-anchor="middle" class="label">Каталог — таблица «имя → номер inode»</text>

  <rect x="800" y="438" width="320" height="105" class="box"/>
  <text x="960" y="466" text-anchor="middle" class="mono-bold">Сетевой стек и драйверы дисков</text>
  <text x="960" y="494" text-anchor="middle" class="mono">Буферы сокетов · Page Cache · NVMe</text>
  <text x="960" y="520" text-anchor="middle" class="label">Диагностика через /proc/&lt;pid&gt;/fd</text>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/3. Сети и HTTP",
        "filename": "cover-sub-05-03-networks-http.svg",
        "code": "SUB 5.3",
        "title": "ПОДРАЗДЕЛ 5.3: СЕТИ, СОКЕТЫ GO И ПРОТОКОЛ HTTP",
        "subtitle": "13 глав: 4 слоя TCP/IP, IPv4/IPv6, порты и NAT, DNS, TCP/UDP, сокеты net.Listen (step06), TLS/HTTPS, HTTP/1.1–3 и утилиты curl/dig/ss",
        "caption": "Схема Подраздела 5.3: путь сетевого запроса через четыре слоя модели TCP/IP, трёхстороннее рукопожатие TCP, сокеты пакета net и протокол HTTP",
        "alt": "Инженерный чертёж Подраздела 5.3: инкапсуляция TCP/IP, рукопожатие TCP, сокеты Go и структура HTTP-запроса",
        "body": '''
  <!-- Top: 4 Layers Encapsulation -->
  <rect x="55" y="135" width="1090" height="185" rx="6" class="box"/>
  <text x="600" y="164" text-anchor="middle" class="mono-blue">ИНКАПСУЛЯЦИЯ ДАННЫХ В ЧЕТЫРЁХСЛОЙНОЙ МОДЕЛИ TCP/IP</text>

  <rect x="80" y="186" width="1040" height="110" class="box-dark"/>
  <text x="155" y="246" text-anchor="middle" class="mono-bold">Кадр Ethernet (MAC)</text>

  <rect x="245" y="198" width="790" height="86" class="box"/>
  <text x="340" y="246" text-anchor="middle" class="mono-bold">IP-пакет (IPv4/IPv6)</text>

  <rect x="445" y="210" width="570" height="62" class="box-accent"/>
  <text x="555" y="246" text-anchor="middle" class="mono-blue">TCP-сегмент (Порт :8080)</text>

  <rect x="675" y="220" width="320" height="42" class="box-warm"/>
  <text x="835" y="246" text-anchor="middle" class="mono-orange">HTTP / Сообщение BookmarkFlow</text>

  <text x="1080" y="246" text-anchor="middle" class="mono">CRC</text>

  <!-- Bottom 3 panels: DNS+TCP, Go Socket step06, TLS+HTTP -->
  <rect x="55" y="345" width="345" height="220" rx="6" class="box"/>
  <text x="227" y="376" text-anchor="middle" class="mono-blue">1. DNS И НАДЁЖНЫЙ TCP</text>
  <text x="80" y="408" class="mono">• DNS: A / AAAA / CNAME + TTL</text>
  <text x="80" y="436" class="mono">• 127.0.0.1 vs 0.0.0.0 · NAT</text>
  <text x="80" y="464" class="mono-bold">• TCP: SYN → SYN+ACK → ACK</text>
  <text x="80" y="492" class="mono">• Поток байтов vs датаграммы UDP</text>
  <text x="80" y="520" class="mono">• Диагностика: dig · ss -tulpn · nc</text>

  <rect x="427" y="345" width="345" height="220" rx="6" class="box-accent"/>
  <text x="600" y="376" text-anchor="middle" class="mono-blue">2. СОКЕТЫ GO (PROJECT/STEP06)</text>
  <rect x="450" y="394" width="300" height="145" class="box"/>
  <text x="468" y="422" class="mono-bold">ln, _ := net.Listen("tcp", addr)</text>
  <text x="468" y="450" class="mono">conn, _ := ln.Accept()</text>
  <text x="468" y="478" class="mono">go handleConn(conn, store)</text>
  <text x="468" y="506" class="mono-orange">conn.SetDeadline(time.Now()...)</text>
  <text x="468" y="528" class="label">Текстовый протокол PING / ADD / LIST</text>

  <rect x="800" y="345" width="345" height="220" rx="6" class="box"/>
  <text x="972" y="376" text-anchor="middle" class="mono-blue">3. TLS И ПРОТОКОЛ HTTP</text>
  <text x="825" y="408" class="mono">• TLS 1.3: сертификат и ключи</text>
  <text x="825" y="436" class="mono-bold">• GET /api/v1/bookmarks HTTP/1.1</text>
  <text x="825" y="464" class="mono">• Заголовки, Keep-Alive, статусы</text>
  <text x="825" y="492" class="mono">• Идемпотентность GET/PUT/DELETE</text>
  <text x="825" y="520" class="mono">• HTTP/2 (мультиплекс.) и HTTP/3</text>
'''
    },
    {
        "dir": "sources/6. Вводный курс структур данных и алгоритмов",
        "filename": "cover-module-06-intro-dsa.svg",
        "code": "MOD 06",
        "title": "ВВОДНЫЙ КУРС СТРУКТУР ДАННЫХ И АЛГОРИТМОВ НА GO",
        "subtitle": "11 глав: оценка сложности Big-O, слайсы vs списки, стек/очередь, хеш-таблица, бинарный поиск, сортировки, BST, B-Tree, графы и step07",
        "caption": "Инженерная карта Модуля 6: от кривых сложности Big-O и хеш-таблиц до многоключевых страниц B-Tree, графов и инвертированного индекса TagIndex в BookmarkFlow",
        "alt": "Инженерный чертёж Модуля 6: Big-O, хеш-таблица, бинарный поиск, B-Tree, графы и TagIndex",
        "body": '''
  <!-- Box 1: Big-O & Binary Search -->
  <rect x="55" y="135" width="345" height="235" rx="6" class="box"/>
  <text x="227" y="164" text-anchor="middle" class="mono-blue">1. СЛОЖНОСТЬ И БИНАРНЫЙ ПОИСК</text>
  <rect x="80" y="184" width="295" height="105" class="box-dark"/>
  <text x="98" y="210" class="mono-blue">O(1)        — мапа / индекс слайса</text>
  <text x="98" y="234" class="mono-bold">O(log n)    — 20 шагов на 1 000 000</text>
  <text x="98" y="258" class="mono">O(n log n)  — slices.SortFunc</text>
  <text x="98" y="280" class="mono-orange">O(n²)       — вложенный цикл (10¹²)</text>
  <text x="227" y="322" text-anchor="middle" class="mono">Стек (LIFO) · Кольцевой буфер (FIFO)</text>
  <text x="227" y="348" text-anchor="middle" class="label">Кэш-локальность слайса против списка</text>

  <!-- Box 2: Hash Table, BST, B-Tree, Graphs -->
  <rect x="427" y="135" width="345" height="235" rx="6" class="box"/>
  <text x="600" y="164" text-anchor="middle" class="mono-blue">2. ХЕШ-ТАБЛИЦЫ, ДЕРЕВЬЯ И ГРАФЫ</text>
  <rect x="452" y="184" width="295" height="50" class="box-accent"/>
  <text x="600" y="207" text-anchor="middle" class="mono-bold">hash(key) % buckets → O(1)</text>
  <text x="600" y="226" text-anchor="middle" class="label">Бакеты, коллизии и рост таблицы</text>
  <rect x="452" y="246" width="295" height="50" class="box-warm"/>
  <text x="600" y="269" text-anchor="middle" class="mono-orange">BST в RAM vs B-Tree на диске</text>
  <text x="600" y="288" text-anchor="middle" class="label">Страница 4 КБ (мостик к Тому 2 «БД»)</text>
  <rect x="452" y="308" width="295" height="46" class="box-dark"/>
  <text x="600" y="336" text-anchor="middle" class="mono">Графы: списки смежности · BFS / DFS</text>

  <!-- Box 3: TagIndex step07 -->
  <rect x="800" y="135" width="345" height="235" rx="6" class="box-accent"/>
  <text x="972" y="164" text-anchor="middle" class="mono-blue">3. BOOKMARKFLOW (PROJECT/STEP07)</text>
  <rect x="825" y="184" width="295" height="125" class="box"/>
  <text x="842" y="210" class="mono-bold">type TagIndex struct</text>
  <text x="842" y="236" class="mono">byTag: "go"  → [1, 4, 9, 15]</text>
  <text x="842" y="260" class="mono">byTag: "web" → [4, 15, 22]</text>
  <text x="842" y="288" class="mono-orange">Пересечение 2 указателями: [4, 15]</text>
  <rect x="825" y="320" width="295" height="36" class="box-warm"/>
  <text x="972" y="343" text-anchor="middle" class="mono-orange">BinarySearchByID + SortByTitle</text>

  <!-- Bottom comparison bar -->
  <rect x="55" y="395" width="1090" height="170" rx="6" class="box"/>
  <text x="80" y="428" class="mono-bold">ИНЖЕНЕРНЫЙ ИТОГ МОДУЛЯ 6 НА 1 000 000 ЗАКЛАДОК:</text>
  <rect x="80" y="448" width="320" height="92" class="box-dark"/>
  <text x="240" y="476" text-anchor="middle" class="mono-bold">Линейный поиск O(n)</text>
  <text x="240" y="502" text-anchor="middle" class="mono">До 1 000 000 проверок</text>
  <text x="240" y="524" text-anchor="middle" class="label">Полный перебор слайса на каждый запрос</text>

  <line x1="400" y1="494" x2="438" y2="494" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="441" y="448" width="320" height="92" class="box-accent"/>
  <text x="601" y="476" text-anchor="middle" class="mono-blue">Бинарный поиск по ID O(log n)</text>
  <text x="601" y="502" text-anchor="middle" class="mono-bold">Максимум 20 сравнений</text>
  <text x="601" y="524" text-anchor="middle" class="label">На отсортированном слайсе закладок</text>

  <line x1="761" y1="494" x2="799" y2="494" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="802" y="448" width="318" height="92" class="box-warm"/>
  <text x="961" y="476" text-anchor="middle" class="mono-orange">Инвертированный TagIndex</text>
  <text x="961" y="502" text-anchor="middle" class="mono-bold">O(1) по тегу · O(k₁+k₂) пересечение</text>
  <text x="961" y="524" text-anchor="middle" class="label">Мгновенная фильтрация без аллокаций</text>
'''
    },
    {
        "dir": "sources/7. Первый реальный HTTP-бэкенд на Go",
        "filename": "cover-module-07-http-backend.svg",
        "code": "MOD 07",
        "title": "ПЕРВЫЙ РЕАЛЬНЫЙ HTTP-БЭКЕНД НА GO (PROJECT/FINAL)",
        "subtitle": "20 глав: net/http, роутинг Go 1.22+, JSON CRUD, слои сервиса, цепочка middleware, Graceful Shutdown, httptest и многоэтапный Dockerfile",
        "caption": "Инженерная карта Модуля 7: полная архитектура финального HTTP-сервиса BookmarkFlow на стандартной библиотеке Go 1.24 с тестами httptest и контейнером Docker",
        "alt": "Инженерный чертёж Модуля 7: архитектура HTTP-бэкенда BookmarkFlow, middleware, ServeMux Go 1.22+, слои Service/Store, httptest и Dockerfile",
        "body": '''
  <!-- Top Pipeline: HTTP Request -> Middleware -> ServeMux -> Service -> FileStore -->
  <rect x="55" y="130" width="1090" height="230" rx="6" class="box"/>
  <text x="600" y="160" text-anchor="middle" class="mono-blue">АРХИТЕКТУРА HTTP-СЕРВИСА BOOKMARKFLOW (PROJECT/FINAL · GO 1.24 · 0 ФРЕЙМВОРКОВ)</text>

  <rect x="75" y="182" width="175" height="150" class="box-dark"/>
  <text x="162" y="210" text-anchor="middle" class="mono-bold">HTTP-клиент</text>
  <text x="162" y="238" text-anchor="middle" class="mono">POST / GET / PUT</text>
  <text x="162" y="262" text-anchor="middle" class="mono">DELETE / healthz</text>
  <text x="162" y="290" text-anchor="middle" class="mono-blue">JSON Payload</text>
  <text x="162" y="314" text-anchor="middle" class="label">curl / браузер / тесты</text>

  <line x1="250" y1="257" x2="282" y2="257" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="285" y="182" width="215" height="150" class="box-warm"/>
  <text x="392" y="210" text-anchor="middle" class="mono-orange">Цепочка Middleware</text>
  <text x="392" y="238" text-anchor="middle" class="mono">1. RequestID (X-Request-ID)</text>
  <text x="392" y="262" text-anchor="middle" class="mono">2. Logging (log/slog)</text>
  <text x="392" y="286" text-anchor="middle" class="mono">3. Recover (500 JSON)</text>
  <text x="392" y="314" text-anchor="middle" class="label">Таймауты http.Server</text>

  <line x1="500" y1="257" x2="532" y2="257" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="535" y="182" width="215" height="150" class="box-accent"/>
  <text x="642" y="210" text-anchor="middle" class="mono-blue">http.ServeMux 1.22+</text>
  <text x="642" y="238" text-anchor="middle" class="mono">"POST /api/v1/bookmarks"</text>
  <text x="642" y="262" text-anchor="middle" class="mono">"GET .../{id}"</text>
  <text x="642" y="286" text-anchor="middle" class="mono">r.PathValue("id")</text>
  <text x="642" y="314" text-anchor="middle" class="label">MaxBytesReader (64 КБ)</text>

  <line x1="750" y1="257" x2="782" y2="257" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="785" y="182" width="160" height="150" class="box"/>
  <text x="865" y="210" text-anchor="middle" class="mono-bold">Слой Service</text>
  <text x="865" y="238" text-anchor="middle" class="mono">Валидация</text>
  <text x="865" y="262" text-anchor="middle" class="mono">LinkChecker</text>
  <text x="865" y="286" text-anchor="middle" class="mono">(Worker Pool)</text>
  <text x="865" y="314" text-anchor="middle" class="label">r.Context()</text>

  <line x1="945" y1="257" x2="977" y2="257" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="980" y="182" width="145" height="150" class="box-accent"/>
  <text x="1052" y="210" text-anchor="middle" class="mono-blue">Интерфейс Store</text>
  <text x="1052" y="238" text-anchor="middle" class="mono-bold">*FileStore</text>
  <text x="1052" y="262" text-anchor="middle" class="mono">sync.RWMutex</text>
  <text x="1052" y="286" text-anchor="middle" class="mono">os.Rename</text>
  <text x="1052" y="314" text-anchor="middle" class="mono-orange">→ БД в Томе 2</text>

  <!-- Bottom 3 panels: Lifecycle, httptest, Docker -->
  <rect x="55" y="385" width="345" height="180" rx="6" class="box"/>
  <text x="227" y="416" text-anchor="middle" class="mono-bold">ЖИЗНЕННЫЙ ЦИКЛ СЕРВЕРА</text>
  <text x="80" y="448" class="mono">• Конфиг: умолчания → ENV → флаги</text>
  <text x="80" y="476" class="mono">• GET /healthz → 200 OK</text>
  <text x="80" y="504" class="mono-orange">• SIGINT/SIGTERM → srv.Shutdown(ctx)</text>
  <text x="80" y="532" class="label">Завершение без обрыва активных запросов</text>

  <rect x="427" y="385" width="345" height="180" rx="6" class="box"/>
  <text x="600" y="416" text-anchor="middle" class="mono-bold">ТЕСТИРОВАНИЕ (HTTPTEST + RACE)</text>
  <text x="452" y="448" class="mono">• httptest.NewRequest &amp; NewRecorder</text>
  <text x="452" y="476" class="mono">• httptest.NewServer (E2E CRUD)</text>
  <text x="452" y="504" class="mono-blue">• go test -race ./...</text>
  <text x="452" y="532" class="label">100% офлайн без внешних сайтов</text>

  <rect x="800" y="385" width="345" height="180" rx="6" class="box-warm"/>
  <text x="972" y="416" text-anchor="middle" class="mono-orange">ПОСТАВКА В DOCKER-КОНТЕЙНЕРЕ</text>
  <text x="825" y="448" class="mono">• Stage 1: golang:1.24-alpine (build)</text>
  <text x="825" y="476" class="mono">• CGO_ENABLED=0 (статический ELF)</text>
  <text x="825" y="504" class="mono-bold">• Stage 2: distroless/static:nonroot</text>
  <text x="825" y="532" class="label">Минимум мегабайт · Запуск без root</text>
'''
    },
]


def main() -> int:
    for item in COVERS:
        target_dir = os.path.join(ROOT, item["dir"])
        media_dir = os.path.join(target_dir, "media")
        os.makedirs(media_dir, exist_ok=True)
        svg_path = os.path.join(media_dir, item["filename"])
        svg_text = HEADER + item["body"] + footer_block(item["code"], item["title"], item["subtitle"])
        with open(svg_path, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(svg_text)

        credits_path = os.path.join(media_dir, "credits.toml")
        entry = {
            "caption": item["caption"],
            "alt": item["alt"],
            "author": "Серия go-textbook-v2",
            "license": "own",
            "invert_dark": True,
        }
        write_credits(credits_path, item["filename"], credits_block(item["filename"], entry, []))
        load_credits(credits_path)
        print(f"OK: {os.path.relpath(svg_path, ROOT)} ({len(svg_text) / 1024:.1f} КБ)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
