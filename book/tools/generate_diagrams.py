#!/usr/bin/env python3
"""
book/tools/generate_diagrams.py
Генерация 31 точной технической SVG-схемы Тома 1 в едином стиле инженерного чертежа
(светлый фон #fcfaf5, тёмный контур #1e293b, акценты #0369a1 и #c2410c, invert_dark = true,
license = "own") и обновление соответствующих media/credits.toml.
"""

import os
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from book.tools.commons_fetch import credits_block, write_credits  # noqa: E402
from engine.media import image_size, load_credits  # noqa: E402


def wrap_svg(w: int, h: int, title: str, subtitle: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#e2e8f0" stroke-width="0.7"/>
    </pattern>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#1e293b"/>
    </marker>
    <marker id="arrowBlue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0369a1"/>
    </marker>
    <marker id="arrowOrange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#c2410c"/>
    </marker>
  </defs>
  <style>
    .bg {{ fill: #fcfaf5; }}
    .frame {{ fill: none; stroke: #1e293b; stroke-width: 2; }}
    .box {{ fill: #ffffff; stroke: #1e293b; stroke-width: 1.8; }}
    .box-accent {{ fill: #f0f9ff; stroke: #0369a1; stroke-width: 2; }}
    .box-warm {{ fill: #fff7ed; stroke: #c2410c; stroke-width: 2; }}
    .box-dark {{ fill: #f1f5f9; stroke: #334155; stroke-width: 1.8; }}
    .line {{ fill: none; stroke: #1e293b; stroke-width: 2; }}
    .line-blue {{ fill: none; stroke: #0369a1; stroke-width: 2.2; }}
    .line-orange {{ fill: none; stroke: #c2410c; stroke-width: 2.2; }}
    .line-dash {{ fill: none; stroke: #64748b; stroke-width: 1.6; stroke-dasharray: 6 4; }}
    .h1 {{ font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 19px; font-weight: 700; fill: #0f172a; }}
    .sub {{ font-family: "Inter", "IBM Plex Sans", sans-serif; font-size: 13.5px; fill: #334155; }}
    .mono {{ font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 13px; fill: #0f172a; }}
    .mono-sm {{ font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 11.5px; fill: #334155; }}
    .mono-bold {{ font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 13.5px; font-weight: 700; fill: #0f172a; }}
    .mono-blue {{ font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 13.5px; font-weight: 700; fill: #0369a1; }}
    .mono-orange {{ font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 13.5px; font-weight: 700; fill: #c2410c; }}
    .label {{ font-family: "Inter", "IBM Plex Sans", sans-serif; font-size: 12.5px; fill: #475569; }}
  </style>
  <rect width="{w}" height="{h}" class="bg"/>
  <rect x="16" y="16" width="{w - 32}" height="{h - 32}" fill="url(#grid)"/>
  <rect x="16" y="16" width="{w - 32}" height="{h - 32}" class="frame"/>
  <rect x="16" y="16" width="{w - 32}" height="58" fill="#f8fafc" stroke="#1e293b" stroke-width="1.6"/>
  <rect x="16" y="16" width="8" height="58" fill="#0369a1"/>
  <text x="38" y="42" class="h1">{title}</text>
  <text x="38" y="63" class="sub">{subtitle}</text>
{body}
</svg>
'''


DIAGRAMS = [
    # -----------------------------------------------------------------------
    # МОДУЛЬ 1 (4 схемы)
    # -----------------------------------------------------------------------
    {
        "dir": "sources/1. Пролог — от лампочки до бэкенда",
        "filename": "byte-weights-and-utf8.svg",
        "w": 1040, "h": 460,
        "title": "ВЕСА БИТОВ В БАЙТЕ (01000001) И ДЛИНА СИМВОЛОВ В UTF-8",
        "subtitle": "Позиционные степени двойки от 128 до 1 и переменная длина кодировки UTF-8 для латиницы, кириллицы и эмодзи",
        "caption": "Схема весов битов в одном байте (01000001 = 64 + 1 = 65 = 'A') и сравнение числа байтов в UTF-8",
        "alt": "Схема позиционных весов восьми битов в байте 01000001 и длины символов G, П и ракеты в UTF-8",
        "body": '''
  <!-- Top: 8-bit weights -->
  <rect x="38" y="92" width="964" height="170" rx="6" class="box"/>
  <text x="58" y="118" class="mono-blue">ОДИН БАЙТ = 8 БИТОВ (01000001₂ = 64 + 1 = 65₁₀ = 0x41 = ASCII 'A')</text>
  <!-- 8 cells -->
  <g transform="translate(58, 134)">
    <rect x="0" y="0" width="92" height="72" class="box-dark"/><text x="46" y="20" text-anchor="middle" class="mono-sm">2⁷ = 128</text><text x="46" y="52" text-anchor="middle" class="h1">0</text>
    <rect x="98" y="0" width="92" height="72" class="box-accent"/><text x="144" y="20" text-anchor="middle" class="mono-blue">2⁶ = 64</text><text x="144" y="52" text-anchor="middle" class="h1">1</text>
    <rect x="196" y="0" width="92" height="72" class="box-dark"/><text x="242" y="20" text-anchor="middle" class="mono-sm">2⁵ = 32</text><text x="242" y="52" text-anchor="middle" class="h1">0</text>
    <rect x="294" y="0" width="92" height="72" class="box-dark"/><text x="340" y="20" text-anchor="middle" class="mono-sm">2⁴ = 16</text><text x="340" y="52" text-anchor="middle" class="h1">0</text>
    <rect x="392" y="0" width="92" height="72" class="box-dark"/><text x="438" y="20" text-anchor="middle" class="mono-sm">2³ = 8</text><text x="438" y="52" text-anchor="middle" class="h1">0</text>
    <rect x="490" y="0" width="92" height="72" class="box-dark"/><text x="536" y="20" text-anchor="middle" class="mono-sm">2² = 4</text><text x="536" y="52" text-anchor="middle" class="h1">0</text>
    <rect x="588" y="0" width="92" height="72" class="box-dark"/><text x="634" y="20" text-anchor="middle" class="mono-sm">2¹ = 2</text><text x="634" y="52" text-anchor="middle" class="h1">0</text>
    <rect x="686" y="0" width="92" height="72" class="box-accent"/><text x="732" y="20" text-anchor="middle" class="mono-blue">2⁰ = 1</text><text x="732" y="52" text-anchor="middle" class="h1">1</text>
    <rect x="798" y="0" width="126" height="72" class="box-warm"/>
    <text x="861" y="26" text-anchor="middle" class="mono-orange">Hex: 0x41</text>
    <text x="861" y="50" text-anchor="middle" class="mono-bold">0100 | 0001</text>
  </g>
  <text x="58" y="242" class="label">Старшая четвёрка битов 0100₂ = 4, младшая 0001₂ = 1 — поэтому шестнадцатеричная запись 0x41 читается мгновенно.</text>

  <!-- Bottom: UTF-8 lengths -->
  <rect x="38" y="280" width="964" height="146" rx="6" class="box"/>
  <text x="58" y="308" class="mono-blue">ПЕРЕМЕННАЯ ДЛИНА В UTF-8: ОТ 1 ДО 4 БАЙТОВ НА ОДИН СИМВОЛ UNICODE</text>

  <rect x="58" y="324" width="270" height="84" class="box-accent"/>
  <text x="193" y="350" text-anchor="middle" class="mono-bold">'G' (U+0047 · ASCII)</text>
  <text x="193" y="374" text-anchor="middle" class="mono-blue">[ 0x47 ] → 1 байт</text>
  <text x="193" y="395" text-anchor="middle" class="label">Совместимо со старым ASCII</text>

  <rect x="358" y="324" width="300" height="84" class="box-dark"/>
  <text x="508" y="350" text-anchor="middle" class="mono-bold">'П' (U+041F · Кириллица)</text>
  <text x="508" y="374" text-anchor="middle" class="mono">[ 0xD0 | 0x9F ] → 2 байта</text>
  <text x="508" y="395" text-anchor="middle" class="label">Первый бит 1 показывает продолжение</text>

  <rect x="688" y="324" width="294" height="84" class="box-warm"/>
  <text x="835" y="350" text-anchor="middle" class="mono-bold">Ракета 🚀 (U+1F680)</text>
  <text x="835" y="374" text-anchor="middle" class="mono-orange">[ F0 | 9F | 9A | 80 ] → 4 байта</text>
  <text x="835" y="395" text-anchor="middle" class="label">Один символ ≠ 1 байт</text>
'''
    },
    {
        "dir": "sources/1. Пролог — от лампочки до бэкенда",
        "filename": "logic-gates-half-adder.svg",
        "w": 1040, "h": 500,
        "title": "ЛОГИЧЕСКИЕ ВЕНТИЛИ (И, ИЛИ, НЕ, XOR) И СХЕМА ПОЛУСУММАТОРА",
        "subtitle": "Как из элементарных переключателей собирается сложение двух битов A + B с выходом суммы и переноса",
        "caption": "Стандартизированные обозначения вентилей AND, OR, NOT, XOR и схема полусумматора (Half Adder) с таблицей истинности",
        "alt": "Логические вентили AND, OR, NOT, XOR и схема полусумматора двух битов A и B",
        "body": '''
  <!-- Top row: 4 basic gates -->
  <rect x="38" y="92" width="228" height="145" rx="6" class="box"/>
  <text x="152" y="116" text-anchor="middle" class="mono-blue">И (AND)</text>
  <line x1="68" y1="150" x2="105" y2="150" class="line"/><line x1="68" y1="180" x2="105" y2="180" class="line"/>
  <path d="M 105 135 L 145 135 A 28 30 0 0 1 145 195 L 105 195 Z" class="box-accent"/>
  <line x1="173" y1="165" x2="215" y2="165" class="line"/>
  <text x="152" y="222" text-anchor="middle" class="label">1, только если A=1 и B=1</text>

  <rect x="283" y="92" width="228" height="145" rx="6" class="box"/>
  <text x="397" y="116" text-anchor="middle" class="mono-blue">ИЛИ (OR)</text>
  <line x1="313" y1="150" x2="356" y2="150" class="line"/><line x1="313" y1="180" x2="356" y2="180" class="line"/>
  <path d="M 348 135 Q 368 165 348 195 Q 395 195 422 165 Q 395 135 348 135 Z" class="box-accent"/>
  <line x1="422" y1="165" x2="462" y2="165" class="line"/>
  <text x="397" y="222" text-anchor="middle" class="label">1, если хотя бы один вход = 1</text>

  <rect x="528" y="92" width="228" height="145" rx="6" class="box"/>
  <text x="642" y="116" text-anchor="middle" class="mono-blue">НЕ (NOT / Инвертор)</text>
  <line x1="565" y1="165" x2="605" y2="165" class="line"/>
  <polygon points="605,138 605,192 662,165" class="box-warm"/>
  <circle cx="670" cy="165" r="6" class="box-warm"/>
  <line x1="676" y1="165" x2="715" y2="165" class="line"/>
  <text x="642" y="222" text-anchor="middle" class="label">Меняет 0 → 1 и 1 → 0</text>

  <rect x="773" y="92" width="228" height="145" rx="6" class="box"/>
  <text x="887" y="116" text-anchor="middle" class="mono-orange">ИСКЛ. ИЛИ (XOR)</text>
  <line x1="803" y1="150" x2="846" y2="150" class="line"/><line x1="803" y1="180" x2="846" y2="180" class="line"/>
  <path d="M 836 135 Q 856 165 836 195" class="line"/>
  <path d="M 846 135 Q 866 165 846 195 Q 893 195 920 165 Q 893 135 846 135 Z" class="box-warm"/>
  <line x1="920" y1="165" x2="960" y2="165" class="line"/>
  <text x="887" y="222" text-anchor="middle" class="label">1, когда входы различаются</text>

  <!-- Bottom left: Half Adder -->
  <rect x="38" y="256" width="550" height="212" rx="6" class="box"/>
  <text x="58" y="284" class="mono-bold">ПОЛУСУММАТОР (HALF ADDER): СКЛАДЫВАЕТ ДВА БИТА A И B</text>
  <text x="72" y="330" class="mono-bold">A</text>
  <text x="72" y="408" class="mono-bold">B</text>
  <!-- Wire A -->
  <line x1="95" y1="325" x2="255" y2="325" class="line-blue"/>
  <circle cx="155" cy="325" r="4" fill="#0369a1"/>
  <polyline points="155,325 155,392 255,392" class="line-blue"/>
  <!-- Wire B -->
  <line x1="95" y1="403" x2="185" y2="403" class="line-orange"/>
  <circle cx="185" cy="403" r="4" fill="#c2410c"/>
  <polyline points="185,403 185,352 255,352" class="line-orange"/>
  <line x1="185" y1="403" x2="255" y2="418" class="line-orange"/>
  <!-- XOR box -->
  <rect x="255" y="308" width="120" height="58" rx="6" class="box-accent"/>
  <text x="315" y="343" text-anchor="middle" class="mono-blue">XOR</text>
  <line x1="375" y1="337" x2="445" y2="337" class="line" marker-end="url(#arrow)"/>
  <text x="458" y="342" class="mono-bold">Сумма (Sum)</text>
  <!-- AND box -->
  <rect x="255" y="378" width="120" height="58" rx="6" class="box-warm"/>
  <text x="315" y="413" text-anchor="middle" class="mono-orange">AND</text>
  <line x1="375" y1="407" x2="445" y2="407" class="line" marker-end="url(#arrow)"/>
  <text x="458" y="412" class="mono-bold">Перенос (Carry)</text>

  <!-- Bottom right: Truth Table -->
  <rect x="610" y="256" width="392" height="212" rx="6" class="box-dark"/>
  <text x="806" y="284" text-anchor="middle" class="mono-bold">ТАБЛИЦА ИСТИННОСТИ (A + B)</text>
  <line x1="635" y1="300" x2="977" y2="300" stroke="#475569" stroke-width="1.5"/>
  <text x="670" y="324" text-anchor="middle" class="mono-bold">A</text>
  <text x="735" y="324" text-anchor="middle" class="mono-bold">B</text>
  <text x="830" y="324" text-anchor="middle" class="mono-blue">Сумма</text>
  <text x="930" y="324" text-anchor="middle" class="mono-orange">Перенос</text>
  <line x1="635" y1="335" x2="977" y2="335" stroke="#94a3b8"/>
  <text x="670" y="362" text-anchor="middle" class="mono">0</text><text x="735" y="362" text-anchor="middle" class="mono">0</text><text x="830" y="362" text-anchor="middle" class="mono">0</text><text x="930" y="362" text-anchor="middle" class="mono">0</text>
  <text x="670" y="390" text-anchor="middle" class="mono">0</text><text x="735" y="390" text-anchor="middle" class="mono">1</text><text x="830" y="390" text-anchor="middle" class="mono-blue">1</text><text x="930" y="390" text-anchor="middle" class="mono">0</text>
  <text x="670" y="418" text-anchor="middle" class="mono">1</text><text x="735" y="418" text-anchor="middle" class="mono">0</text><text x="830" y="418" text-anchor="middle" class="mono-blue">1</text><text x="930" y="418" text-anchor="middle" class="mono">0</text>
  <text x="670" y="446" text-anchor="middle" class="mono-bold">1</text><text x="735" y="446" text-anchor="middle" class="mono-bold">1</text><text x="830" y="446" text-anchor="middle" class="mono-bold">0</text><text x="930" y="446" text-anchor="middle" class="mono-orange">1 (10₂=2)</text>
'''
    },
    {
        "dir": "sources/1. Пролог — от лампочки до бэкенда",
        "filename": "ram-cells-and-latency-scale.svg",
        "w": 1040, "h": 500,
        "title": "АДРЕСУЕМЫЕ ЯЧЕЙКИ RAM И РАЗРЫВ ЗАДЕРЖЕК ОТ РЕГИСТРОВ ДО ДИСКА",
        "subtitle": "Каждая ячейка RAM хранит 1 байт по номеру-адресу; обращение к дискам в тысячи раз медленнее памяти",
        "caption": "Модель адресуемых ячеек оперативной памяти и логарифмическая шкала задержек от регистров CPU (~0.3 нс) до HDD (~5 мс)",
        "alt": "Модель ячеек оперативной памяти с адресами и логарифмическое сравнение задержек кэша, RAM, SSD и HDD",
        "body": '''
  <!-- Top: RAM cells -->
  <rect x="38" y="92" width="964" height="145" rx="6" class="box"/>
  <text x="58" y="118" class="mono-blue">ОПЕРАТИВНАЯ ПАМЯТЬ (RAM): ЛИНЕЙНЫЙ РЯД ПРОНУМЕРОВАННЫХ ЯЧЕЕК ПО 1 БАЙТУ</text>
  <g transform="translate(58, 134)">
    <text x="55" y="14" text-anchor="middle" class="mono-sm">0x0000</text><rect x="0" y="22" width="110" height="54" class="box-accent"/><text x="55" y="48" text-anchor="middle" class="mono-bold">0x47 ('G')</text><text x="55" y="66" text-anchor="middle" class="label">1 байт</text>
    <text x="170" y="14" text-anchor="middle" class="mono-sm">0x0001</text><rect x="115" y="22" width="110" height="54" class="box-accent"/><text x="170" y="48" text-anchor="middle" class="mono-bold">0x6F ('o')</text><text x="170" y="66" text-anchor="middle" class="label">1 байт</text>
    <text x="285" y="14" text-anchor="middle" class="mono-sm">0x0002</text><rect x="230" y="22" width="110" height="54" class="box-dark"/><text x="285" y="48" text-anchor="middle" class="mono-bold">0x21 ('!')</text><text x="285" y="66" text-anchor="middle" class="label">1 байт</text>
    <text x="400" y="14" text-anchor="middle" class="mono-sm">0x0003</text><rect x="345" y="22" width="110" height="54" class="box-dark"/><text x="400" y="48" text-anchor="middle" class="mono">0x00 (0)</text><text x="400" y="66" text-anchor="middle" class="label">1 байт</text>
    <text x="515" y="14" text-anchor="middle" class="mono-sm">0x0004</text><rect x="460" y="22" width="110" height="54" class="box-warm"/><text x="515" y="48" text-anchor="middle" class="mono-orange">0x2A (42)</text><text x="515" y="66" text-anchor="middle" class="label">1 байт</text>
    <text x="630" y="14" text-anchor="middle" class="mono-sm">0x0005</text><rect x="575" y="22" width="110" height="54" class="box-dark"/><text x="630" y="48" text-anchor="middle" class="mono">0x00</text><text x="630" y="66" text-anchor="middle" class="label">1 байт</text>
    <text x="745" y="14" text-anchor="middle" class="mono-sm">0x0006</text><rect x="690" y="22" width="110" height="54" class="box-dark"/><text x="745" y="48" text-anchor="middle" class="mono">0x00</text><text x="745" y="66" text-anchor="middle" class="label">1 байт</text>
    <text x="865" y="14" text-anchor="middle" class="mono-sm">0x0007</text><rect x="805" y="22" width="118" height="54" class="box-dark"/><text x="864" y="48" text-anchor="middle" class="mono">0xFF</text><text x="864" y="66" text-anchor="middle" class="label">1 байт</text>
  </g>
  <text x="58" y="225" class="label">Произвольный доступ (Random Access): чтение по адресу 0x7FFF0002 занимает столько же времени, сколько чтение 0x0000.</text>

  <!-- Bottom: Log Latency Bars -->
  <rect x="38" y="254" width="964" height="214" rx="6" class="box"/>
  <text x="58" y="282" class="mono-blue">МАСШТАБ ЗАДЕРЖЕК (ЛОГАРИФМИЧЕСКАЯ ШКАЛА · ЕСЛИ 1 ТАКТ CPU = 1 СЕКУНДА):</text>

  <text x="58" y="316" class="mono-bold">Регистры CPU</text>
  <rect x="230" y="300" width="32" height="22" fill="#0369a1"/><text x="274" y="316" class="mono">~0.3 нс  →  1 секунда</text>

  <text x="58" y="348" class="mono-bold">Кэш L1 (ядро)</text>
  <rect x="230" y="332" width="80" height="22" fill="#0284c7"/><text x="322" y="348" class="mono">~1 нс    →  3 секунды (взять со стола)</text>

  <text x="58" y="380" class="mono-bold">RAM (ОЗУ)</text>
  <rect x="230" y="364" width="240" height="22" fill="#0ea5e9"/><text x="482" y="380" class="mono">~100 нс  →  5 минут (энергозависимая)</text>

  <text x="58" y="412" class="mono-bold">NVMe SSD</text>
  <rect x="230" y="396" width="430" height="22" fill="#ea580c"/><text x="672" y="412" class="mono-orange">~100 мкс →  3.5 дня (1000× медленнее RAM)</text>

  <text x="58" y="444" class="mono-bold">Диск HDD</text>
  <rect x="230" y="428" width="560" height="22" fill="#c2410c"/><text x="802" y="444" class="mono-orange">~5–10 мс →  6–12 месяцев</text>
'''
    },
    {
        "dir": "sources/1. Пролог — от лампочки до бэкенда",
        "filename": "http-request-response-anatomy.svg",
        "w": 1040, "h": 480,
        "title": "АНАТОМИЯ HTTP-ЗАПРОСА И HTTP-ОТВЕТА НА ПРИМЕРЕ JSON API",
        "subtitle": "Текстовая структура протокола HTTP/1.1: стартовая строка, заголовки, пустая строка-разделитель и тело JSON",
        "caption": "Структура HTTP-запроса клиента и HTTP-ответа сервера с кодом состояния 201 Created и телом JSON",
        "alt": "Схема HTTP-запроса POST и HTTP-ответа 201 Created со стартовой строкой, заголовками и телом JSON",
        "body": '''
  <!-- Left: Request -->
  <rect x="38" y="92" width="462" height="352" rx="6" class="box-accent"/>
  <text x="269" y="120" text-anchor="middle" class="mono-blue">HTTP-ЗАПРОС (ОТ КЛИЕНТА К СЕРВЕРУ)</text>

  <rect x="58" y="136" width="422" height="56" class="box"/>
  <text x="72" y="158" class="mono-orange">1. Стартовая строка (Метод · Путь · Версия):</text>
  <text x="72" y="180" class="mono-bold">POST /bookmarks HTTP/1.1</text>

  <rect x="58" y="202" width="422" height="92" class="box"/>
  <text x="72" y="224" class="mono-blue">2. Заголовки (метаданные парой Ключ: Значение):</text>
  <text x="72" y="246" class="mono">Host: api.example.com</text>
  <text x="72" y="266" class="mono">Content-Type: application/json</text>
  <text x="72" y="286" class="mono">Content-Length: 48</text>

  <rect x="58" y="304" width="422" height="28" class="box-dark"/>
  <text x="269" y="323" text-anchor="middle" class="mono-sm">3. Пустая строка (\r\n) — граница заголовков</text>

  <rect x="58" y="342" width="422" height="84" class="box-warm"/>
  <text x="72" y="364" class="mono-orange">4. Тело запроса (JSON):</text>
  <text x="72" y="388" class="mono">{"title": "Go Docs",</text>
  <text x="72" y="410" class="mono"> "url": "https://go.dev/doc"}</text>

  <!-- Center Arrow -->
  <line x1="504" y1="220" x2="536" y2="220" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="536" y1="310" x2="504" y2="310" class="line-orange" marker-end="url(#arrowOrange)"/>

  <!-- Right: Response -->
  <rect x="540" y="92" width="462" height="352" rx="6" class="box"/>
  <text x="771" y="120" text-anchor="middle" class="mono-orange">HTTP-ОТВЕТ (ОТ БЭКЕНДА КЛИЕНТУ)</text>

  <rect x="560" y="136" width="422" height="56" class="box-warm"/>
  <text x="574" y="158" class="mono-orange">1. Строка статуса (Версия · Код · Пояснение):</text>
  <text x="574" y="180" class="mono-bold">HTTP/1.1 201 Created</text>

  <rect x="560" y="202" width="422" height="92" class="box"/>
  <text x="574" y="224" class="mono-blue">2. Заголовки ответа:</text>
  <text x="574" y="246" class="mono">Content-Type: application/json; charset=utf-8</text>
  <text x="574" y="266" class="mono">Content-Length: 62</text>
  <text x="574" y="286" class="mono">Location: /bookmarks/42</text>

  <rect x="560" y="304" width="422" height="28" class="box-dark"/>
  <text x="771" y="323" text-anchor="middle" class="mono-sm">3. Пустая строка (\r\n) — граница заголовков</text>

  <rect x="560" y="342" width="422" height="84" class="box-accent"/>
  <text x="574" y="364" class="mono-blue">4. Тело ответа (JSON):</text>
  <text x="574" y="388" class="mono">{"id": 42, "title": "Go Docs",</text>
  <text x="574" y="410" class="mono"> "url": "https://go.dev/doc"}</text>
'''
    },

    # -----------------------------------------------------------------------
    # МОДУЛЬ 2 (3 схемы)
    # -----------------------------------------------------------------------
    {
        "dir": "sources/2. Первые шаги на Go",
        "filename": "go-string-bytes-runes-utf8.svg",
        "w": 1040, "h": 440,
        "title": "СТРОКА В GO: БАЙТЫ (BYTE) ПРОТИВ РУН (RUNE) В UTF-8",
        "subtitle": "На примере s := \"GoПривет\" — почему len(s) == 14, а символов (рун) ровно 8",
        "caption": "Раскладка строки \"GoПривет\" в памяти: 14 байтов UTF-8 против 8 кодовых точек Unicode (rune)",
        "alt": "Раскладка строки GoПривет на 14 байтов и 8 рун с байтовыми индексами цикла for range",
        "body": '''
  <!-- Top: 14 byte boxes -->
  <rect x="38" y="92" width="964" height="190" rx="6" class="box"/>
  <text x="58" y="118" class="mono-blue">s := "GoПривет"  →  len(s) = 14 байтов (индексация s[i] возвращает uint8 / byte)</text>

  <!-- 14 bytes across 920px: width 64 each, gap 2 -->
  <g transform="translate(58, 134)">
    <!-- G (0) -->
    <rect x="0" y="20" width="60" height="44" class="box-accent"/><text x="30" y="13" text-anchor="middle" class="mono-sm">0</text><text x="30" y="47" text-anchor="middle" class="mono-bold">47</text>
    <!-- o (1) -->
    <rect x="64" y="20" width="60" height="44" class="box-accent"/><text x="94" y="13" text-anchor="middle" class="mono-sm">1</text><text x="94" y="47" text-anchor="middle" class="mono-bold">6F</text>
    <!-- П (2..3) -->
    <rect x="128" y="20" width="60" height="44" class="box-warm"/><text x="158" y="13" text-anchor="middle" class="mono-sm">2</text><text x="158" y="47" text-anchor="middle" class="mono">D0</text>
    <rect x="190" y="20" width="60" height="44" class="box-warm"/><text x="220" y="13" text-anchor="middle" class="mono-sm">3</text><text x="220" y="47" text-anchor="middle" class="mono">9F</text>
    <!-- р (4..5) -->
    <rect x="256" y="20" width="60" height="44" class="box-dark"/><text x="286" y="13" text-anchor="middle" class="mono-sm">4</text><text x="286" y="47" text-anchor="middle" class="mono">D1</text>
    <rect x="318" y="20" width="60" height="44" class="box-dark"/><text x="348" y="13" text-anchor="middle" class="mono-sm">5</text><text x="348" y="47" text-anchor="middle" class="mono">80</text>
    <!-- и (6..7) -->
    <rect x="384" y="20" width="60" height="44" class="box-warm"/><text x="414" y="13" text-anchor="middle" class="mono-sm">6</text><text x="414" y="47" text-anchor="middle" class="mono">D0</text>
    <rect x="446" y="20" width="60" height="44" class="box-warm"/><text x="476" y="13" text-anchor="middle" class="mono-sm">7</text><text x="476" y="47" text-anchor="middle" class="mono">B8</text>
    <!-- в (8..9) -->
    <rect x="512" y="20" width="60" height="44" class="box-dark"/><text x="542" y="13" text-anchor="middle" class="mono-sm">8</text><text x="542" y="47" text-anchor="middle" class="mono">D0</text>
    <rect x="574" y="20" width="60" height="44" class="box-dark"/><text x="604" y="13" text-anchor="middle" class="mono-sm">9</text><text x="604" y="47" text-anchor="middle" class="mono">B2</text>
    <!-- е (10..11) -->
    <rect x="640" y="20" width="60" height="44" class="box-warm"/><text x="670" y="13" text-anchor="middle" class="mono-sm">10</text><text x="670" y="47" text-anchor="middle" class="mono">D0</text>
    <rect x="702" y="20" width="60" height="44" class="box-warm"/><text x="732" y="13" text-anchor="middle" class="mono-sm">11</text><text x="732" y="47" text-anchor="middle" class="mono">B5</text>
    <!-- т (12..13) -->
    <rect x="768" y="20" width="60" height="44" class="box-dark"/><text x="798" y="13" text-anchor="middle" class="mono-sm">12</text><text x="798" y="47" text-anchor="middle" class="mono">D1</text>
    <rect x="830" y="20" width="60" height="44" class="box-dark"/><text x="860" y="13" text-anchor="middle" class="mono-sm">13</text><text x="860" y="47" text-anchor="middle" class="mono">82</text>

    <!-- Rune brackets underneath -->
    <rect x="0" y="76" width="60" height="34" class="box-accent"/><text x="30" y="98" text-anchor="middle" class="mono-blue">'G'</text>
    <rect x="64" y="76" width="60" height="34" class="box-accent"/><text x="94" y="98" text-anchor="middle" class="mono-blue">'o'</text>
    <rect x="128" y="76" width="122" height="34" class="box-warm"/><text x="189" y="98" text-anchor="middle" class="mono-orange">'П' (2 Б)</text>
    <rect x="256" y="76" width="122" height="34" class="box-dark"/><text x="317" y="98" text-anchor="middle" class="mono-bold">'р' (2 Б)</text>
    <rect x="384" y="76" width="122" height="34" class="box-warm"/><text x="445" y="98" text-anchor="middle" class="mono-orange">'и' (2 Б)</text>
    <rect x="512" y="76" width="122" height="34" class="box-dark"/><text x="573" y="98" text-anchor="middle" class="mono-bold">'в' (2 Б)</text>
    <rect x="640" y="76" width="122" height="34" class="box-warm"/><text x="701" y="98" text-anchor="middle" class="mono-orange">'е' (2 Б)</text>
    <rect x="768" y="76" width="122" height="34" class="box-dark"/><text x="829" y="98" text-anchor="middle" class="mono-bold">'т' (2 Б)</text>
  </g>
  <text x="58" y="264" class="label">utf8.RuneCountInString(s) = 8 рун (тип rune = int32). Попытка взять s[2] даёт байт 0xD0, а не букву 'П'.</text>

  <!-- Bottom comparison -->
  <rect x="38" y="298" width="465" height="110" rx="6" class="box-warm"/>
  <text x="58" y="326" class="mono-orange">for i := 0; i &lt; len(s); i++</text>
  <text x="58" y="352" class="mono">Идёт по БАЙТАМ (14 итераций: 0, 1, 2, 3, ...)</text>
  <text x="58" y="378" class="label">Резка s[0:3] = "Go\xd0" — ломает букву 'П' пополам!</text>

  <rect x="537" y="298" width="465" height="110" rx="6" class="box-accent"/>
  <text x="557" y="326" class="mono-blue">for i, r := range s</text>
  <text x="557" y="352" class="mono">Декодирует РУНЫ (8 итераций: i = 0, 1, 2, 4, 6, 8, 10, 12)</text>
  <text x="557" y="378" class="label">Переменная r имеет тип rune; индекс i прыгает на размер руны.</text>
'''
    },
    {
        "dir": "sources/2. Первые шаги на Go",
        "filename": "defer-lifo-stack.svg",
        "w": 1040, "h": 440,
        "title": "МЕХАНИКА DEFER: РАННЕЕ ВЫЧИСЛЕНИЕ АРГУМЕНТОВ И СТЕК LIFO",
        "subtitle": "Аргументы вычисляются в момент вызова defer, а сами отложенные вызовы исполняются в обратном порядке перед return",
        "caption": "Порядок работы defer: вычисление аргументов при регистрации, хранение в стеке LIFO и выполнение после return функции",
        "alt": "Схема работы оператора defer в Go: вычисление аргументов сразу и выполнение вызовов в порядке стека LIFO",
        "body": '''
  <!-- Left: Function code -->
  <rect x="38" y="92" width="320" height="316" rx="6" class="box"/>
  <text x="58" y="120" class="mono-blue">КОД ФУНКЦИИ</text>
  <rect x="56" y="136" width="284" height="252" class="box-dark"/>
  <text x="70" y="162" class="mono-bold">func run() {</text>
  <text x="70" y="188" class="mono">  x := 10</text>
  <text x="70" y="216" class="mono-blue">  defer fmt.Println("1:", x)</text>
  <text x="70" y="244" class="mono">  x = 20</text>
  <text x="70" y="272" class="mono-orange">  defer fmt.Println("2:", x)</text>
  <text x="70" y="300" class="mono">  fmt.Println("body:", x)</text>
  <text x="70" y="328" class="mono-bold">}</text>
  <text x="70" y="366" class="label">Значение x фиксируется сразу!</text>

  <!-- Center: LIFO Stack -->
  <rect x="392" y="92" width="320" height="316" rx="6" class="box-accent"/>
  <text x="552" y="120" text-anchor="middle" class="mono-blue">СТЕК ОТЛОЖЕННЫХ ВЫЗОВОВ (LIFO)</text>

  <rect x="422" y="148" width="260" height="68" class="box-warm"/>
  <text x="552" y="175" text-anchor="middle" class="mono-orange">ВЕРШИНА СТЕКА (выполнится 1-й)</text>
  <text x="552" y="199" text-anchor="middle" class="mono-bold">fmt.Println("2:", 20)</text>

  <rect x="422" y="236" width="260" height="68" class="box"/>
  <text x="552" y="263" text-anchor="middle" class="mono-blue">ДНО СТЕКА (выполнится 2-й)</text>
  <text x="552" y="287" text-anchor="middle" class="mono-bold">fmt.Println("1:", 10)</text>

  <text x="552" y="344" text-anchor="middle" class="mono">Last In, First Out:</text>
  <text x="552" y="368" text-anchor="middle" class="label">Последний зарегистрированный</text>
  <text x="552" y="388" text-anchor="middle" class="label">убирается и запускается первым.</text>

  <line x1="358" y1="212" x2="418" y2="265" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="358" y1="268" x2="418" y2="185" class="line-orange" marker-end="url(#arrowOrange)"/>

  <!-- Right: Console output timeline -->
  <rect x="746" y="92" width="256" height="316" rx="6" class="box"/>
  <text x="874" y="120" text-anchor="middle" class="mono-bold">ВЫВОД В ТЕРМИНАЛЕ</text>

  <rect x="766" y="148" width="216" height="58" class="box-dark"/>
  <text x="782" y="172" class="label">Шаг 1 (тело функции):</text>
  <text x="782" y="194" class="mono-bold">body: 20</text>

  <rect x="766" y="224" width="216" height="58" class="box-warm"/>
  <text x="782" y="248" class="label">Шаг 2 (с вершины стека):</text>
  <text x="782" y="270" class="mono-orange">2: 20</text>

  <rect x="766" y="300" width="216" height="58" class="box-accent"/>
  <text x="782" y="324" class="label">Шаг 3 (с дна стека):</text>
  <text x="782" y="346" class="mono-blue">1: 10</text>

  <text x="874" y="388" text-anchor="middle" class="label">Идеально для f.Close() после открытия</text>

  <line x1="684" y1="182" x2="762" y2="250" class="line-orange" marker-end="url(#arrowOrange)"/>
  <line x1="684" y1="270" x2="762" y2="328" class="line-blue" marker-end="url(#arrowBlue)"/>
'''
    },
    {
        "dir": "sources/2. Первые шаги на Go",
        "filename": "error-wrapping-chain.svg",
        "w": 1040, "h": 400,
        "title": "ОБОРАЧИВАНИЕ ОШИБОК (%w) И ПРОВЕРКА ЦЕПОЧКИ ЧЕРЕЗ ERRORS.IS",
        "subtitle": "Каждый слой добавляет человеческий контекст, но сохраняет первопричину внутри цепочки",
        "caption": "Цепочка оборачивания ошибок через fmt.Errorf(\"…: %w\", err) и её раскрутка функцией errors.Is",
        "alt": "Схема цепочки обёрнутых ошибок от os.ErrNotExist через readConfig к loadBookmarks и проверки через errors.Is",
        "body": '''
  <!-- 3 layered boxes left to right -->
  <rect x="38" y="102" width="270" height="145" rx="6" class="box-warm"/>
  <text x="173" y="130" text-anchor="middle" class="mono-orange">1. ПЕРВОПРИЧИНА (ЯДРО)</text>
  <rect x="58" y="146" width="230" height="56" class="box"/>
  <text x="173" y="170" text-anchor="middle" class="mono-bold">os.ErrNotExist</text>
  <text x="173" y="190" text-anchor="middle" class="label">"file does not exist"</text>
  <text x="173" y="228" text-anchor="middle" class="label">Сигнальная ошибка ОС</text>

  <line x1="308" y1="174" x2="364" y2="174" class="line-orange" marker-end="url(#arrowOrange)"/>

  <rect x="368" y="102" width="300" height="145" rx="6" class="box-accent"/>
  <text x="518" y="130" text-anchor="middle" class="mono-blue">2. ПРОМЕЖУТОЧНЫЙ СЛОЙ</text>
  <rect x="388" y="146" width="260" height="56" class="box"/>
  <text x="518" y="170" text-anchor="middle" class="mono-bold">fmt.Errorf("read %s: %w",</text>
  <text x="518" y="190" text-anchor="middle" class="mono">path, err)</text>
  <text x="518" y="228" text-anchor="middle" class="label">%w сохраняет ссылку на внутреннюю err</text>

  <line x1="668" y1="174" x2="724" y2="174" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="728" y="102" width="274" height="145" rx="6" class="box"/>
  <text x="865" y="130" text-anchor="middle" class="mono-bold">3. ВЕРХНИЙ УРОВЕНЬ (CLI)</text>
  <rect x="748" y="146" width="234" height="56" class="box-dark"/>
  <text x="865" y="170" text-anchor="middle" class="mono-bold">fmt.Errorf("load: %w", err)</text>
  <text x="865" y="190" text-anchor="middle" class="label">"load: read bm.json: file..."</text>
  <text x="865" y="228" text-anchor="middle" class="label">Читаемое сообщение для лога</text>

  <!-- Bottom: errors.Is vs == -->
  <rect x="38" y="274" width="465" height="96" rx="6" class="box-warm"/>
  <text x="58" y="302" class="mono-orange">НЕНАДЁЖНО: if err == os.ErrNotExist</text>
  <text x="58" y="328" class="mono">Вернёт false! Сравнение == видит только внешнюю</text>
  <text x="58" y="350" class="mono">обёртку и не заглядывает внутрь цепочки.</text>

  <rect x="537" y="274" width="465" height="96" rx="6" class="box-accent"/>
  <text x="557" y="302" class="mono-blue">ПРАВИЛЬНО: if errors.Is(err, os.ErrNotExist)</text>
  <text x="557" y="328" class="mono">Вернёт true! Проходит всю цепочку Unwrap()</text>
  <text x="557" y="350" class="mono">и находит os.ErrNotExist на любой глубине.</text>
'''
    },

    # -----------------------------------------------------------------------
    # МОДУЛЬ 3 (5 схем)
    # -----------------------------------------------------------------------
    {
        "dir": "sources/3. Данные, память, интерфейсы и первые тесты",
        "filename": "pointers-memory-addresses.svg",
        "w": 1040, "h": 440,
        "title": "АДРЕСА И УКАЗАТЕЛИ В GO (&amp;, * И NIL-УКАЗАТЕЛЬ)",
        "subtitle": "Указатель хранит не само число, а адрес ячейки оперативной памяти, где это число лежит",
        "caption": "Модель указателя p := &amp;x и разыменования *p = 99 в памяти, а также нулевое значение *int = nil",
        "alt": "Схема переменных x и p в памяти: взятие адреса амперсандом, изменение значения через *p и nil-указатель",
        "body": '''
  <!-- Step 1: x := 42 -->
  <rect x="38" y="96" width="290" height="220" rx="6" class="box"/>
  <text x="183" y="124" text-anchor="middle" class="mono-blue">1. ПЕРЕМЕННАЯ x И АДРЕС &amp;x</text>
  <rect x="68" y="148" width="230" height="72" class="box-accent"/>
  <text x="183" y="172" text-anchor="middle" class="mono-sm">Адрес в RAM: 0xc000018080</text>
  <text x="183" y="202" text-anchor="middle" class="h1">x: 42  →  99</text>
  <text x="183" y="250" text-anchor="middle" class="mono">var x int = 42</text>
  <text x="183" y="274" text-anchor="middle" class="mono-blue">*p = 99 меняет эту ячейку</text>
  <text x="183" y="298" text-anchor="middle" class="label">8 байтов для int на amd64/arm64</text>

  <!-- Step 2: p := &x -->
  <rect x="374" y="96" width="290" height="220" rx="6" class="box"/>
  <text x="519" y="124" text-anchor="middle" class="mono-blue">2. УКАЗАТЕЛЬ p := &amp;x (*int)</text>
  <rect x="404" y="148" width="230" height="72" class="box-warm"/>
  <text x="519" y="172" text-anchor="middle" class="mono-sm">Адрес p: 0xc000018088</text>
  <text x="519" y="202" text-anchor="middle" class="mono-orange">p: 0xc000018080</text>
  <text x="519" y="250" text-anchor="middle" class="mono">&amp;x — «дай адрес x»</text>
  <text x="519" y="274" text-anchor="middle" class="mono">*p — «пройди по адресу»</text>
  <text x="519" y="298" text-anchor="middle" class="label">Адресная арифметика в Go запрещена</text>

  <line x1="404" y1="184" x2="302" y2="184" class="line-orange" marker-end="url(#arrowOrange)"/>

  <!-- Step 3: nil pointer -->
  <rect x="710" y="96" width="292" height="220" rx="6" class="box-dark"/>
  <text x="856" y="124" text-anchor="middle" class="mono-orange">3. ПУСТОЙ УКАЗАТЕЛЬ (NIL)</text>
  <rect x="740" y="148" width="232" height="72" class="box"/>
  <text x="856" y="172" text-anchor="middle" class="mono-sm">var q *int</text>
  <text x="856" y="202" text-anchor="middle" class="mono-orange">q == nil (0x0)</text>
  <text x="856" y="250" text-anchor="middle" class="mono">Никуда не указывает!</text>
  <text x="856" y="274" text-anchor="middle" class="mono-orange">Чтение *q → PANIC</text>
  <text x="856" y="298" text-anchor="middle" class="label">Всегда проверяйте if q != nil</text>

  <!-- Bottom rule -->
  <rect x="38" y="336" width="964" height="74" rx="6" class="box-accent"/>
  <text x="58" y="366" class="mono-bold">В GO ВСЁ ПЕРЕДАЁТСЯ ПО ЗНАЧЕНИЮ: f(p) КОПИРУЕТ 8-БАЙТНЫЙ АДРЕС, А НЕ САМУ СТРУКТУРУ.</text>
  <text x="58" y="392" class="sub">Именно поэтому функция через копию адреса *T способна изменить оригинальную переменную вызывающего кода.</text>
'''
    },
    {
        "dir": "sources/3. Данные, память, интерфейсы и первые тесты",
        "filename": "slice-header-and-append.svg",
        "w": 1040, "h": 520,
        "title": "ЗАГОЛОВОК СЛАЙСА (PTR, LEN, CAP) И ПЕРЕЕЗД МАССИВА ПРИ APPEND",
        "subtitle": "Пока len &lt; cap, append пишет в запас старого массива; при len == cap создаётся новый массив в 2× больше",
        "caption": "24-байтный заголовок слайса (ptr, len, cap) и перевыделение базового массива при заполнении ёмкости в append",
        "alt": "Схема заголовка слайса ptr len cap и переезда элементов в новый базовый массив при append",
        "body": '''
  <!-- Top: Before append (len=2, cap=4) -->
  <rect x="38" y="92" width="964" height="175" rx="6" class="box"/>
  <text x="58" y="118" class="mono-blue">ДО ПЕРЕПОЛНЕНИЯ: tags := make([]string, 2, 4)  →  append(tags, "net") (МЕСТО ЕСТЬ: len &lt; cap)</text>

  <rect x="58" y="136" width="210" height="112" class="box-accent"/>
  <text x="163" y="158" text-anchor="middle" class="mono-bold">Заголовок (24 Б)</text>
  <line x1="58" y1="168" x2="268" y2="168" stroke="#0369a1"/>
  <text x="163" y="190" text-anchor="middle" class="mono-blue">ptr: 0xc0001000</text>
  <text x="163" y="214" text-anchor="middle" class="mono">len: 2  →  3</text>
  <text x="163" y="238" text-anchor="middle" class="mono">cap: 4</text>

  <line x1="268" y1="184" x2="346" y2="184" class="line-blue" marker-end="url(#arrowBlue)"/>

  <g transform="translate(350, 146)">
    <text x="0" y="-6" class="mono-sm">Базовый массив [4]string @ 0xc0001000</text>
    <rect x="0" y="6" width="145" height="68" class="box-dark"/><text x="72" y="34" text-anchor="middle" class="mono-bold">[0] "go"</text><text x="72" y="56" text-anchor="middle" class="label">внутри len</text>
    <rect x="150" y="6" width="145" height="68" class="box-dark"/><text x="222" y="34" text-anchor="middle" class="mono-bold">[1] "cli"</text><text x="222" y="56" text-anchor="middle" class="label">внутри len</text>
    <rect x="300" y="6" width="145" height="68" class="box-warm"/><text x="372" y="34" text-anchor="middle" class="mono-orange">[2] "net"</text><text x="372" y="56" text-anchor="middle" class="label">дописано на месте</text>
    <rect x="450" y="6" width="145" height="68" class="box"/><text x="522" y="34" text-anchor="middle" class="mono-sm">[3] ""</text><text x="522" y="56" text-anchor="middle" class="label">скрытый запас cap</text>
  </g>

  <!-- Bottom: Relocation on len == cap -->
  <rect x="38" y="285" width="964" height="202" rx="6" class="box"/>
  <text x="58" y="313" class="mono-orange">ПРИ len == cap (4 == 4): append(tags, "web") ВЫДЕЛЯЕТ НОВЫЙ МАССИВ И ОБНОВЛЯЕТ ptr</text>

  <rect x="58" y="334" width="210" height="112" class="box-warm"/>
  <text x="163" y="356" text-anchor="middle" class="mono-bold">Новый заголовок</text>
  <line x1="58" y1="366" x2="268" y2="366" stroke="#c2410c"/>
  <text x="163" y="388" text-anchor="middle" class="mono-orange">ptr: 0xc0002400</text>
  <text x="163" y="412" text-anchor="middle" class="mono">len: 5</text>
  <text x="163" y="436" text-anchor="middle" class="mono">cap: 8 (2× рост)</text>

  <line x1="268" y1="382" x2="346" y2="382" class="line-orange" marker-end="url(#arrowOrange)"/>

  <g transform="translate(350, 344)">
    <text x="0" y="-6" class="mono-sm">Новый массив [8]string @ 0xc0002400 (старые элементы скопированы)</text>
    <rect x="0" y="6" width="76" height="68" class="box-dark"/><text x="38" y="44" text-anchor="middle" class="mono-sm">"go"</text>
    <rect x="80" y="6" width="76" height="68" class="box-dark"/><text x="118" y="44" text-anchor="middle" class="mono-sm">"cli"</text>
    <rect x="160" y="6" width="76" height="68" class="box-dark"/><text x="198" y="44" text-anchor="middle" class="mono-sm">"net"</text>
    <rect x="240" y="6" width="76" height="68" class="box-dark"/><text x="278" y="44" text-anchor="middle" class="mono-sm">"api"</text>
    <rect x="320" y="6" width="76" height="68" class="box-warm"/><text x="358" y="44" text-anchor="middle" class="mono-orange">"web"</text>
    <rect x="400" y="6" width="62" height="68" class="box"/><text x="431" y="44" text-anchor="middle" class="mono-sm">[5]</text>
    <rect x="466" y="6" width="62" height="68" class="box"/><text x="497" y="44" text-anchor="middle" class="mono-sm">[6]</text>
    <rect x="532" y="6" width="62" height="68" class="box"/><text x="563" y="44" text-anchor="middle" class="mono-sm">[7]</text>
  </g>
  <text x="350" y="460" class="mono-bold">Правило: tags = append(tags, x) — всегда сохраняйте возвращённый заголовок!</text>
'''
    },
    {
        "dir": "sources/3. Данные, память, интерфейсы и первые тесты",
        "filename": "slice-aliasing-and-three-index.svg",
        "w": 1040, "h": 500,
        "title": "АЛИАСИНГ СЛАЙСОВ И ЗАЩИТА ТРЁХИНДЕКСНЫМ СРЕЗОМ s[low:high:max]",
        "subtitle": "Срез b := a[1:3] наследует запас ёмкости до конца массива a — его append тихо перезапишет элемент a[3]",
        "caption": "Опасность общего базового массива при append к подсрезу и разрыв этой связи через a[1:3:3] или slices.Clone",
        "alt": "Сравнение обычного среза a[1:3], затирающего элемент a[3] при append, и трёхиндексного среза a[1:3:3]",
        "body": '''
  <!-- Top: Aliasing problem -->
  <rect x="38" y="92" width="964" height="184" rx="6" class="box-warm"/>
  <text x="58" y="120" class="mono-orange">ЛОВУШКА АЛИАСИНГА: a := []int{10, 20, 30, 40};  b := a[1:3] (cap=3)  →  b = append(b, 999)</text>

  <rect x="58" y="142" width="175" height="54" class="box"/>
  <text x="145" y="165" text-anchor="middle" class="mono-bold">a: len=4, cap=4</text>
  <text x="145" y="185" text-anchor="middle" class="mono-sm">ptr → [0]</text>

  <rect x="58" y="206" width="175" height="54" class="box"/>
  <text x="145" y="229" text-anchor="middle" class="mono-orange">b: len=2, cap=3</text>
  <text x="145" y="249" text-anchor="middle" class="mono-sm">ptr → [1] (общий массив!)</text>

  <g transform="translate(300, 146)">
    <rect x="0" y="0" width="155" height="72" class="box-dark"/><text x="77" y="30" text-anchor="middle" class="mono-bold">[0]: 10</text><text x="77" y="52" text-anchor="middle" class="label">a[0]</text>
    <rect x="165" y="0" width="155" height="72" class="box-accent"/><text x="242" y="30" text-anchor="middle" class="mono-bold">[1]: 20</text><text x="242" y="52" text-anchor="middle" class="label">a[1] и b[0]</text>
    <rect x="330" y="0" width="155" height="72" class="box-accent"/><text x="407" y="30" text-anchor="middle" class="mono-bold">[2]: 30</text><text x="407" y="52" text-anchor="middle" class="label">a[2] и b[1]</text>
    <rect x="495" y="0" width="175" height="72" class="box-warm"/><text x="582" y="30" text-anchor="middle" class="mono-orange">[3]: 40 → 999!</text><text x="582" y="52" text-anchor="middle" class="mono-orange">перезаписано b!</text>
  </g>
  <line x1="233" y1="168" x2="296" y2="168" class="line" marker-end="url(#arrow)"/>
  <line x1="233" y1="232" x2="462" y2="218" class="line-orange" marker-end="url(#arrowOrange)"/>
  <text x="300" y="252" class="mono-bold">Итог: a неожиданно стал [10, 20, 30, 999].</text>

  <!-- Bottom: 3-index fix -->
  <rect x="38" y="294" width="964" height="174" rx="6" class="box-accent"/>
  <text x="58" y="322" class="mono-blue">ЗАЩИТА: b := a[1:3:3]  (cap = max - low = 3 - 1 = 2 == len)  →  append ПЕРЕЕЗЖАЕТ В НОВЫЙ МАССИВ</text>

  <rect x="58" y="344" width="215" height="96" class="box"/>
  <text x="165" y="370" text-anchor="middle" class="mono-blue">b: len=2, cap=2</text>
  <text x="165" y="396" text-anchor="middle" class="mono">Запаса в массиве a нет!</text>
  <text x="165" y="420" text-anchor="middle" class="label">a[3] защищён от записи</text>

  <line x1="273" y1="392" x2="345" y2="392" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="350" y="344" width="335" height="96" class="box"/>
  <text x="517" y="370" text-anchor="middle" class="mono-bold">Новый массив для b после append(b, 999)</text>
  <text x="517" y="400" text-anchor="middle" class="mono-blue">[ 20 | 30 | 999 | (резерв) ]</text>
  <text x="517" y="424" text-anchor="middle" class="label">Старый массив a = [10, 20, 30, 40] не тронут</text>

  <rect x="708" y="344" width="272" height="96" class="box-dark"/>
  <text x="844" y="370" text-anchor="middle" class="mono-bold">Или явная копия:</text>
  <text x="844" y="398" text-anchor="middle" class="mono-blue">copy(dst, src)</text>
  <text x="844" y="422" text-anchor="middle" class="mono">slices.Clone(src)</text>
'''
    },
    {
        "dir": "sources/3. Данные, память, интерфейсы и первые тесты",
        "filename": "interface-value-and-typed-nil.svg",
        "w": 1040, "h": 440,
        "title": "ПАРА (ТИП, ЗНАЧЕНИЕ) В ИНТЕРФЕЙСЕ И ЛОВУШКА ТИПИЗИРОВАННОГО NIL",
        "subtitle": "Интерфейсное значение в Go равно nil только тогда, когда пусты ОБА его слова: и тип, и указатель на данные",
        "caption": "Внутреннее представление значения интерфейса как пары (тип, данные): истинный nil против типизированного nil",
        "alt": "Сравнение пустого интерфейса (nil, nil) и интерфейса с типизированным nil (*MyError, nil), дающего err != nil",
        "body": '''
  <!-- Left: True nil -->
  <rect x="38" y="96" width="462" height="225" rx="6" class="box-accent"/>
  <text x="269" y="124" text-anchor="middle" class="mono-blue">1. ИСТИННЫЙ NIL (var err error = nil)</text>

  <rect x="78" y="148" width="180" height="82" class="box"/>
  <text x="168" y="176" text-anchor="middle" class="mono-sm">Слово 1: Динамический тип</text>
  <text x="168" y="208" text-anchor="middle" class="h1">nil</text>

  <rect x="278" y="148" width="180" height="82" class="box"/>
  <text x="368" y="176" text-anchor="middle" class="mono-sm">Слово 2: Данные</text>
  <text x="368" y="208" text-anchor="middle" class="h1">nil</text>

  <rect x="78" y="248" width="380" height="48" class="box"/>
  <text x="268" y="278" text-anchor="middle" class="mono-blue">err == nil  →  true (оба поля пустые)</text>

  <!-- Right: Typed nil -->
  <rect x="540" y="96" width="462" height="225" rx="6" class="box-warm"/>
  <text x="771" y="124" text-anchor="middle" class="mono-orange">2. ТИПИЗИРОВАННЫЙ NIL (var p *MyError = nil; err = p)</text>

  <rect x="580" y="148" width="180" height="82" class="box"/>
  <text x="670" y="176" text-anchor="middle" class="mono-sm">Слово 1: Динамический тип</text>
  <text x="670" y="208" text-anchor="middle" class="mono-orange">*MyError</text>

  <rect x="780" y="148" width="180" height="82" class="box"/>
  <text x="870" y="176" text-anchor="middle" class="mono-sm">Слово 2: Данные</text>
  <text x="870" y="208" text-anchor="middle" class="h1">nil</text>

  <rect x="580" y="248" width="380" height="48" class="box"/>
  <text x="770" y="278" text-anchor="middle" class="mono-orange">err == nil  →  FALSE! (тип *MyError задан)</text>

  <!-- Bottom rule -->
  <rect x="38" y="340" width="964" height="70" rx="6" class="box"/>
  <text x="58" y="368" class="mono-bold">ЗОЛОТОЕ ПРАВИЛО: ФУНКЦИЯ, ВОЗВРАЩАЮЩАЯ error, ДОЛЖНА ЯВНО ВОЗВРАЩАТЬ return nil</text>
  <text x="58" y="394" class="sub">Не объявляйте var err *MyError с последующим return err — при отсутствии ошибки верните интерфейс nil напрямую.</text>
'''
    },
    {
        "dir": "sources/3. Данные, память, интерфейсы и первые тесты",
        "filename": "bookmarkflow-store-layers.svg",
        "w": 1040, "h": 420,
        "title": "ИНТЕРФЕЙС STORE В BOOKMARKFLOW (PROJECT/STEP04)",
        "subtitle": "Зависимость логики от узкого контракта позволяет подменять хранилище в памяти и на диске без переписывания CLI",
        "caption": "Архитектурная граница Store в BookmarkFlow: CLI работает с интерфейсом, а MemoryStore и FileStore проверяются единым набором тестов",
        "alt": "Схема интерфейса Store в BookmarkFlow с двумя реализациями MemoryStore и FileStore и тестами через t.TempDir",
        "body": '''
  <!-- Left: Caller -->
  <rect x="38" y="110" width="235" height="200" rx="6" class="box"/>
  <text x="155" y="142" text-anchor="middle" class="mono-bold">Команды CLI</text>
  <text x="155" y="172" text-anchor="middle" class="mono">add · list · search</text>
  <text x="155" y="198" text-anchor="middle" class="mono">delete</text>
  <rect x="58" y="224" width="195" height="64" class="box-dark"/>
  <text x="155" y="250" text-anchor="middle" class="mono-sm">Не знает, где лежат</text>
  <text x="155" y="270" text-anchor="middle" class="mono-sm">данные: RAM или JSON</text>

  <line x1="273" y1="210" x2="345" y2="210" class="line-blue" marker-end="url(#arrowBlue)"/>

  <!-- Center: Store interface -->
  <rect x="350" y="110" width="300" height="200" rx="6" class="box-warm"/>
  <text x="500" y="142" text-anchor="middle" class="mono-orange">type Store interface</text>
  <rect x="372" y="160" width="256" height="128" class="box"/>
  <text x="388" y="188" class="mono">Add(title, url) (Bookmark, err)</text>
  <text x="388" y="216" class="mono">List() ([]Bookmark, error)</text>
  <text x="388" y="244" class="mono">Search(query) ([]Bookmark, err)</text>
  <text x="388" y="272" class="mono">Delete(id int) error</text>

  <!-- Right: Two implementations -->
  <rect x="720" y="96" width="282" height="104" rx="6" class="box-accent"/>
  <text x="861" y="126" text-anchor="middle" class="mono-blue">*MemoryStore</text>
  <text x="861" y="154" text-anchor="middle" class="mono">Хранит слайс в RAM</text>
  <text x="861" y="178" text-anchor="middle" class="label">Мгновенно в unit-тестах</text>

  <rect x="720" y="220" width="282" height="104" rx="6" class="box-accent"/>
  <text x="861" y="250" text-anchor="middle" class="mono-blue">*FileStore</text>
  <text x="861" y="278" text-anchor="middle" class="mono">Сохраняет в JSON-файл</text>
  <text x="861" y="302" text-anchor="middle" class="label">В тестах — папка t.TempDir()</text>

  <line x1="720" y1="148" x2="654" y2="184" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="720" y1="272" x2="654" y2="236" class="line-blue" marker-end="url(#arrowBlue)"/>

  <!-- Bottom -->
  <rect x="38" y="340" width="964" height="52" rx="6" class="box-dark"/>
  <text x="520" y="371" text-anchor="middle" class="mono-bold">Один контрактный тест runStoreTests(t, store) проверяет обе реализации — одинаковое поведение гарантировано.</text>
'''
    },

    # -----------------------------------------------------------------------
    # МОДУЛЬ 4 (4 схемы)
    # -----------------------------------------------------------------------
    {
        "dir": "sources/4. Стандартная библиотека, философия Go и базовая конкурентность/1. Рабочая стандартная библиотека",
        "filename": "io-reader-writer-pipeline.svg",
        "w": 1040, "h": 400,
        "title": "ПОТОКОВЫЙ КОНВЕЙЕР IO.READER И IO.WRITER",
        "subtitle": "Маленькие однометодные интерфейсы соединяют файлы, ограничители размера, буферы и JSON-кодировщики в цепочку",
        "caption": "Композиция потоков в стандартной библиотеке Go: от os.File и io.LimitReader до bufio.Scanner и io.Writer",
        "alt": "Схема потокового конвейера байтов от источника io.Reader через обёртки io.LimitReader и буфер к приёмнику io.Writer",
        "body": '''
  <rect x="38" y="106" width="200" height="150" rx="6" class="box-dark"/>
  <text x="138" y="138" text-anchor="middle" class="mono-bold">Источник (io.Reader)</text>
  <text x="138" y="168" text-anchor="middle" class="mono">*os.File</text>
  <text x="138" y="194" text-anchor="middle" class="mono">*strings.Reader</text>
  <text x="138" y="220" text-anchor="middle" class="mono">*bytes.Buffer</text>
  <text x="138" y="244" text-anchor="middle" class="label">Read(p []byte)</text>

  <line x1="238" y1="181" x2="278" y2="181" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="282" y="106" width="220" height="150" rx="6" class="box-warm"/>
  <text x="392" y="138" text-anchor="middle" class="mono-orange">Ограничитель</text>
  <text x="392" y="172" text-anchor="middle" class="mono-bold">io.LimitReader(r, N)</text>
  <text x="392" y="202" text-anchor="middle" class="label">Тоже реализует io.Reader!</text>
  <text x="392" y="228" text-anchor="middle" class="label">Защита от чтения лишних ГБ</text>

  <line x1="502" y1="181" x2="542" y2="181" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="546" y="106" width="220" height="150" rx="6" class="box-accent"/>
  <text x="656" y="138" text-anchor="middle" class="mono-blue">Обработка потока</text>
  <text x="656" y="170" text-anchor="middle" class="mono-bold">bufio.NewScanner(r)</text>
  <text x="656" y="198" text-anchor="middle" class="mono-bold">json.NewDecoder(r)</text>
  <text x="656" y="228" text-anchor="middle" class="label">Читает порциями, а не весь файл</text>

  <line x1="766" y1="181" x2="806" y2="181" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="810" y="106" width="192" height="150" rx="6" class="box"/>
  <text x="906" y="138" text-anchor="middle" class="mono-bold">Приёмник (io.Writer)</text>
  <text x="906" y="168" text-anchor="middle" class="mono">os.Stdout</text>
  <text x="906" y="194" text-anchor="middle" class="mono">*bufio.Writer</text>
  <text x="906" y="220" text-anchor="middle" class="mono">*bytes.Buffer</text>
  <text x="906" y="244" text-anchor="middle" class="label">Write(p []byte)</text>

  <!-- Bottom note -->
  <rect x="38" y="282" width="964" height="86" rx="6" class="box"/>
  <text x="58" y="314" class="mono-bold">io.Copy(dst, src) ПЕРЕКАЧИВАЕТ БАЙТЫ НАПРЯМУЮ С ПОСТОЯННЫМ БУФЕРОМ 32 КБ</text>
  <text x="58" y="344" class="sub">Функция тестируется с bytes.Buffer в памяти и без изменений работает в продакшене с гигабайтными файлами.</text>
'''
    },
    {
        "dir": "sources/4. Стандартная библиотека, философия Go и базовая конкурентность/3. Конкурентность без боли",
        "filename": "concurrency-vs-parallelism.svg",
        "w": 1040, "h": 460,
        "title": "КОНКУРЕНТНОСТЬ (СТРУКТУРА) ПРОТИВ ПАРАЛЛЕЛИЗМА (ИСПОЛНЕНИЕ)",
        "subtitle": "Конкурентная программа разбита на независимые задачи; параллельно они бегут только при наличии нескольких ядер CPU",
        "caption": "Таймлайн работы двух горутин: конкурентное чередование на одном ядре CPU против истинного параллелизма на двух ядрах",
        "alt": "Временная диаграмма различия между конкурентным чередованием на одном ядре и параллельным выполнением на двух ядрах",
        "body": '''
  <!-- Top: Concurrency on 1 core -->
  <rect x="38" y="92" width="964" height="162" rx="6" class="box"/>
  <text x="58" y="120" class="mono-blue">КОНКУРЕНТНОСТЬ НА 1 ЯДРЕ CPU (GOMAXPROCS=1): БЫСТРОЕ ПЕРЕКЛЮЧЕНИЕ МЕЖДУ ЗАДАЧАМИ</text>
  <text x="58" y="164" class="mono-bold">Ядро 1:</text>
  <rect x="140" y="140" width="130" height="38" class="box-accent"/><text x="205" y="164" text-anchor="middle" class="mono-blue">Горутина A</text>
  <rect x="275" y="140" width="145" height="38" class="box-warm"/><text x="347" y="164" text-anchor="middle" class="mono-orange">Горутина B</text>
  <rect x="425" y="140" width="110" height="38" class="box-accent"/><text x="480" y="164" text-anchor="middle" class="mono-blue">Горутина A</text>
  <rect x="540" y="140" width="135" height="38" class="box-dark"/><text x="607" y="164" text-anchor="middle" class="mono">Ожидание I/O</text>
  <rect x="680" y="140" width="150" height="38" class="box-warm"/><text x="755" y="164" text-anchor="middle" class="mono-orange">Горутина B</text>
  <rect x="835" y="140" width="140" height="38" class="box-accent"/><text x="905" y="164" text-anchor="middle" class="mono-blue">Горутина A</text>
  <text x="140" y="206" class="label">Пока задача A ждёт ответа по сети или с диска, ядро не простаивает — оно переключается на задачу B.</text>
  <text x="140" y="232" class="mono-sm">Время ─────────────────────────────────────────────────────────────────────────────────────────────▶</text>

  <!-- Bottom: Parallelism on 2 cores -->
  <rect x="38" y="272" width="964" height="156" rx="6" class="box"/>
  <text x="58" y="300" class="mono-orange">ПАРАЛЛЕЛИЗМ НА 2 ЯДРАХ CPU (GOMAXPROCS ≥ 2): ОДНОВРЕМЕННОЕ ВЫПОЛНЕНИЕ В ОДИН МОМЕНТ</text>
  <text x="58" y="342" class="mono-bold">Ядро 1:</text>
  <rect x="140" y="318" width="260" height="36" class="box-accent"/><text x="270" y="341" text-anchor="middle" class="mono-blue">Горутина A (шаг 1)</text>
  <rect x="408" y="318" width="280" height="36" class="box-accent"/><text x="548" y="341" text-anchor="middle" class="mono-blue">Горутина A (шаг 2)</text>

  <text x="58" y="392" class="mono-bold">Ядро 2:</text>
  <rect x="140" y="368" width="260" height="36" class="box-warm"/><text x="270" y="391" text-anchor="middle" class="mono-orange">Горутина B (шаг 1)</text>
  <rect x="408" y="368" width="280" height="36" class="box-warm"/><text x="548" y="391" text-anchor="middle" class="mono-orange">Горутина B (шаг 2)</text>

  <rect x="715" y="318" width="260" height="86" class="box-dark"/>
  <text x="845" y="348" text-anchor="middle" class="mono-bold">Одинаковый Go-код</text>
  <text x="845" y="372" text-anchor="middle" class="label">Рантайм сам распределяет</text>
  <text x="845" y="392" text-anchor="middle" class="label">горутины по доступным ядрам</text>
'''
    },
    {
        "dir": "sources/4. Стандартная библиотека, философия Go и базовая конкурентность/3. Конкурентность без боли",
        "filename": "channels-unbuffered-vs-buffered.svg",
        "w": 1040, "h": 460,
        "title": "НЕБУФЕРИЗИРОВАННЫЙ (РАНДЕВУ) ПРОТИВ БУФЕРИЗИРОВАННОГО КАНАЛА",
        "subtitle": "make(chan T) синхронизирует две горутины в одной точке; make(chan T, 3) даёт FIFO-очередь на 3 элемента",
        "caption": "Сравнение синхронного обмена через небуферизированный канал и очереди с ограниченной ёмкостью в буферизированном канале",
        "alt": "Сравнение небуферизированного канала с синхронным рандеву и буферизированного канала-очереди FIFO",
        "body": '''
  <!-- Top: Unbuffered -->
  <rect x="38" y="92" width="964" height="156" rx="6" class="box"/>
  <text x="58" y="120" class="mono-blue">1. НЕБУФЕРИЗИРОВАННЫЙ КАНАЛ: ch := make(chan string) — СИНХРОННОЕ РАНДЕВУ</text>

  <rect x="58" y="142" width="240" height="72" class="box-accent"/>
  <text x="178" y="170" text-anchor="middle" class="mono-bold">Отправитель</text>
  <text x="178" y="194" text-anchor="middle" class="mono-blue">ch &lt;- "https://go.dev"</text>

  <line x1="298" y1="178" x2="430" y2="178" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="434" y="142" width="172" height="72" class="box-warm"/>
  <text x="520" y="170" text-anchor="middle" class="mono-orange">Буфер = 0</text>
  <text x="520" y="194" text-anchor="middle" class="label">Ждут друг друга!</text>

  <line x1="606" y1="178" x2="738" y2="178" class="line-blue" marker-end="url(#arrowBlue)"/>

  <rect x="742" y="142" width="240" height="72" class="box-accent"/>
  <text x="862" y="170" text-anchor="middle" class="mono-bold">Получатель</text>
  <text x="862" y="194" text-anchor="middle" class="mono-blue">url := &lt;-ch</text>

  <text x="58" y="234" class="label">Обе горутины продолжают путь только после того, как передача из рук в руки состоялась.</text>

  <!-- Bottom: Buffered -->
  <rect x="38" y="266" width="964" height="162" rx="6" class="box"/>
  <text x="58" y="294" class="mono-orange">2. БУФЕРИЗИРОВАННЫЙ КАНАЛ: ch := make(chan int, 3) — ОЧЕРЕДЬ FIFO НА 3 МЕСТА</text>

  <rect x="58" y="316" width="230" height="76" class="box-dark"/>
  <text x="173" y="344" text-anchor="middle" class="mono-bold">Отправитель ch &lt;- 30</text>
  <text x="173" y="368" text-anchor="middle" class="label">Блокируется, только если</text>
  <text x="173" y="384" text-anchor="middle" class="mono-orange">буфер полон (3/3)</text>

  <line x1="288" y1="354" x2="348" y2="354" class="line" marker-end="url(#arrow)"/>

  <g transform="translate(352, 320)">
    <rect x="0" y="0" width="110" height="68" class="box-accent"/><text x="55" y="40" text-anchor="middle" class="mono-bold">10 (выход)</text>
    <rect x="114" y="0" width="110" height="68" class="box-accent"/><text x="169" y="40" text-anchor="middle" class="mono-bold">20</text>
    <rect x="228" y="0" width="110" height="68" class="box"/><text x="283" y="40" text-anchor="middle" class="mono-sm">[ свободно ]</text>
  </g>

  <line x1="696" y1="354" x2="752" y2="354" class="line" marker-end="url(#arrow)"/>

  <rect x="756" y="316" width="226" height="76" class="box-dark"/>
  <text x="869" y="344" text-anchor="middle" class="mono-bold">Получатель v := &lt;-ch</text>
  <text x="869" y="368" text-anchor="middle" class="label">Блокируется, только если</text>
  <text x="869" y="384" text-anchor="middle" class="mono-blue">буфер пуст (0/3)</text>

  <text x="58" y="414" class="label">Важно: буфер на 1..N спасает горутину от зависания при отмене контекста через select { case ch &lt;- res: case &lt;-ctx.Done(): }.</text>
'''
    },
    {
        "dir": "sources/4. Стандартная библиотека, философия Go и базовая конкурентность/3. Конкурентность без боли",
        "filename": "worker-pool-context-flow.svg",
        "w": 1040, "h": 480,
        "title": "ПАТТЕРН WORKER POOL: ОГРАНИЧЕНИЕ ЗАДАЧ, WAITGROUP И CONTEXT",
        "subtitle": "Фиксированное число воркеров читает из общего канала jobs, следит за ctx.Done() и пишет итоги в results",
        "caption": "Архитектура пула воркеров в Go: закрытие jobs по завершении постановки, отмена по context.Context и закрытие results после wg.Wait()",
        "alt": "Схема Worker Pool с каналом задач jobs, N воркерами, отменой по context.Context, WaitGroup и каналом results",
        "body": '''
  <!-- Context Banner -->
  <rect x="38" y="92" width="964" height="46" rx="6" class="box-warm"/>
  <text x="520" y="120" text-anchor="middle" class="mono-orange">ctx, cancel := context.WithTimeout(parent, 5*time.Second)  →  сигнал &lt;-ctx.Done() виден всем узлам</text>

  <!-- Producer -->
  <rect x="38" y="160" width="210" height="190" rx="6" class="box"/>
  <text x="143" y="190" text-anchor="middle" class="mono-bold">Постановщик</text>
  <text x="143" y="220" text-anchor="middle" class="mono">for _, url := range urls</text>
  <text x="143" y="246" text-anchor="middle" class="mono-blue">jobs &lt;- url</text>
  <text x="143" y="276" text-anchor="middle" class="mono-orange">close(jobs)</text>
  <text x="143" y="314" text-anchor="middle" class="label">Закрывает канал задач</text>
  <text x="143" y="332" text-anchor="middle" class="label">только отправитель</text>

  <!-- jobs channel -->
  <line x1="248" y1="255" x2="294" y2="255" class="line-blue" marker-end="url(#arrowBlue)"/>
  <rect x="298" y="205" width="110" height="100" rx="6" class="box-accent"/>
  <text x="353" y="238" text-anchor="middle" class="mono-blue">jobs</text>
  <text x="353" y="262" text-anchor="middle" class="mono">chan Job</text>
  <text x="353" y="286" text-anchor="middle" class="label">очередь</text>

  <line x1="408" y1="255" x2="452" y2="188" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="408" y1="255" x2="452" y2="255" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="408" y1="255" x2="452" y2="322" class="line-blue" marker-end="url(#arrowBlue)"/>

  <!-- N Workers -->
  <rect x="456" y="156" width="248" height="200" rx="6" class="box-accent"/>
  <text x="580" y="180" text-anchor="middle" class="mono-blue">N ВОРКЕРОВ + wg.Add(N)</text>
  <rect x="476" y="192" width="208" height="36" class="box"/><text x="580" y="215" text-anchor="middle" class="mono">Worker #1 (defer wg.Done)</text>
  <rect x="476" y="236" width="208" height="36" class="box"/><text x="580" y="259" text-anchor="middle" class="mono">Worker #2 (defer wg.Done)</text>
  <rect x="476" y="280" width="208" height="36" class="box"/><text x="580" y="303" text-anchor="middle" class="mono">Worker #N (select ctx/jobs)</text>
  <text x="580" y="340" text-anchor="middle" class="label">Ограничивает нагрузку на сеть/CPU</text>

  <line x1="704" y1="188" x2="748" y2="255" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="704" y1="255" x2="748" y2="255" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="704" y1="322" x2="748" y2="255" class="line-blue" marker-end="url(#arrowBlue)"/>

  <!-- results + closer -->
  <rect x="752" y="160" width="250" height="190" rx="6" class="box"/>
  <text x="877" y="190" text-anchor="middle" class="mono-bold">results chan Result</text>
  <rect x="772" y="206" width="210" height="58" class="box-dark"/>
  <text x="877" y="229" text-anchor="middle" class="mono">go func() {</text>
  <text x="877" y="251" text-anchor="middle" class="mono-orange">  wg.Wait(); close(results)</text>
  <rect x="772" y="274" width="210" height="58" class="box-accent"/>
  <text x="877" y="297" text-anchor="middle" class="mono-blue">for r := range results</text>
  <text x="877" y="319" text-anchor="middle" class="label">Чистый выход без deadlock</text>

  <!-- Bottom rule -->
  <rect x="38" y="374" width="964" height="76" rx="6" class="box-dark"/>
  <text x="58" y="404" class="mono-bold">ПОРЯДОК ЗАВЕРШЕНИЯ: close(jobs) → воркеры дочитывают или выходят по ctx.Done() → wg.Wait() → close(results)</text>
  <text x="58" y="430" class="sub">Запуск 10 000 горутин напрямую исчерпает сокеты; пул из 8–32 воркеров даёт стабильную скорость и нулевые утечки.</text>
'''
    },

    # -----------------------------------------------------------------------
    # МОДУЛЬ 5 (9 схем)
    # -----------------------------------------------------------------------
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/1. Компьютер изнутри",
        "filename": "ieee754-float64-bits.svg",
        "w": 1040, "h": 440,
        "title": "СТАНДАРТ IEEE 754 (FLOAT64): 64 БИТА ЗНАКА, ЭКСПОНЕНТЫ И МАНТИССЫ",
        "subtitle": "Почему 0.1 + 0.2 в двоичной дроби не равно точному 0.3 и деньги в бэкенде хранят в целых (int64)",
        "caption": "Битовая раскладка 64-битного числа IEEE 754 (float64) и причина погрешности двоичной записи 0.1",
        "alt": "Битовая схема числа float64 по стандарту IEEE 754: 1 бит знака, 11 битов экспоненты и 52 бита мантиссы",
        "body": '''
  <!-- Top: 64-bit bar -->
  <rect x="38" y="96" width="964" height="150" rx="6" class="box"/>
  <text x="58" y="124" class="mono-blue">РАСКЛАДКА 64 БИТОВ FLOAT64: (-1)^знак × (1 + мантисса) × 2^(экспонента - 1023)</text>

  <rect x="58" y="142" width="76" height="66" class="box-warm"/>
  <text x="96" y="168" text-anchor="middle" class="mono-orange">Знак</text>
  <text x="96" y="192" text-anchor="middle" class="mono-bold">1 бит [63]</text>

  <rect x="142" y="142" width="230" height="66" class="box-accent"/>
  <text x="257" y="168" text-anchor="middle" class="mono-blue">Экспонента (порядок)</text>
  <text x="257" y="192" text-anchor="middle" class="mono-bold">11 битов [62..52]</text>

  <rect x="380" y="142" width="602" height="66" class="box-dark"/>
  <text x="681" y="168" text-anchor="middle" class="mono-bold">Дробная часть (мантисса)</text>
  <text x="681" y="192" text-anchor="middle" class="mono">52 бита точности (~15–17 значащих десятичных цифр) [51..0]</text>

  <text x="58" y="232" class="label">Внутри 52 битов мантиссы хранятся степени двойки 1/2, 1/4, 1/8, 1/16, ... — но не степени десятки 1/10!</text>

  <!-- Bottom: 0.1 + 0.2 -->
  <rect x="38" y="264" width="465" height="146" rx="6" class="box-warm"/>
  <text x="58" y="292" class="mono-orange">ПЕРИОДИЧЕСКАЯ ДРОБЬ 0.1 В ДВОИЧНОЙ СИСТЕМЕ</text>
  <text x="58" y="322" class="mono">0.1₁₀ = 0.0001100110011001100110011...₂ (бесконечно)</text>
  <text x="58" y="350" class="mono">0.1 + 0.2 = 0.30000000000000004440892...</text>
  <text x="58" y="380" class="label">Округление на 53-м бите даёт разницу при сравнении ==.</text>

  <rect x="537" y="264" width="465" height="146" rx="6" class="box-accent"/>
  <text x="557" y="292" class="mono-blue">ИНЖЕНЕРНЫЕ ПРАВИЛА В GO</text>
  <text x="557" y="322" class="mono-bold">1. Деньги и цены → int64 в копейках / центах</text>
  <text x="557" y="350" class="mono">2. Физику/метрики → math.Abs(a-b) &lt; 1e-9</text>
  <text x="557" y="380" class="mono">3. Проверка на NaN → math.IsNaN(x) (NaN != NaN!)</text>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/1. Компьютер изнутри",
        "filename": "cpu-pipeline-branch-flush.svg",
        "w": 1040, "h": 480,
        "title": "КОНВЕЙЕР ИНСТРУКЦИЙ CPU И СБРОС ПРИ ПРОМАХЕ ПРЕДСКАЗАНИЯ (FLUSH)",
        "subtitle": "Идеальная сборочная линия завершает по инструкции за такт, но неверный прогноз if выбрасывает загруженные шаги",
        "caption": "4-ступенчатый конвейер CPU (F/D/E/W): максимальная пропускная способность при верном прогнозе против штрафа сброса при промахе ветвления",
        "alt": "Временная диаграмма конвейера процессора F D E W без ветвлений и со сбросом конвейера при промахе предсказателя",
        "body": '''
  <!-- Top: Ideal pipeline -->
  <rect x="38" y="92" width="964" height="170" rx="6" class="box"/>
  <text x="58" y="120" class="mono-blue">1. ИДЕАЛЬНЫЙ ПОТОК (ИЛИ ВЕРНЫЙ ПРОГНОЗ ВЕТВЛЕНИЯ): 1 ИНСТРУКЦИЯ КАЖДЫЙ ТАКТ</text>
  <text x="175" y="146" class="mono-sm">Такт 1      Такт 2      Такт 3      Такт 4      Такт 5      Такт 6      Такт 7</text>

  <text x="58" y="176" class="mono-bold">Инстр. 1</text>
  <rect x="170" y="156" width="68" height="26" class="box-accent"/><text x="204" y="174" text-anchor="middle" class="mono-sm">F</text>
  <rect x="242" y="156" width="68" height="26" class="box-accent"/><text x="276" y="174" text-anchor="middle" class="mono-sm">D</text>
  <rect x="314" y="156" width="68" height="26" class="box-accent"/><text x="348" y="174" text-anchor="middle" class="mono-sm">E</text>
  <rect x="386" y="156" width="68" height="26" class="box-accent"/><text x="420" y="174" text-anchor="middle" class="mono-bold">W</text>

  <text x="58" y="208" class="mono-bold">Инстр. 2</text>
  <rect x="242" y="188" width="68" height="26" class="box-dark"/><text x="276" y="206" text-anchor="middle" class="mono-sm">F</text>
  <rect x="314" y="188" width="68" height="26" class="box-dark"/><text x="348" y="206" text-anchor="middle" class="mono-sm">D</text>
  <rect x="386" y="188" width="68" height="26" class="box-dark"/><text x="420" y="206" text-anchor="middle" class="mono-sm">E</text>
  <rect x="458" y="188" width="68" height="26" class="box-dark"/><text x="492" y="206" text-anchor="middle" class="mono-bold">W</text>

  <text x="58" y="240" class="mono-bold">Инстр. 3</text>
  <rect x="314" y="220" width="68" height="26" class="box-accent"/><text x="348" y="238" text-anchor="middle" class="mono-sm">F</text>
  <rect x="386" y="220" width="68" height="26" class="box-accent"/><text x="420" y="238" text-anchor="middle" class="mono-sm">D</text>
  <rect x="458" y="220" width="68" height="26" class="box-accent"/><text x="492" y="238" text-anchor="middle" class="mono-sm">E</text>
  <rect x="530" y="220" width="68" height="26" class="box-accent"/><text x="564" y="238" text-anchor="middle" class="mono-bold">W</text>

  <rect x="650" y="160" width="330" height="82" class="box-accent"/>
  <text x="815" y="192" text-anchor="middle" class="mono-blue">Ступени: F (Выборка) → D (Декод)</text>
  <text x="815" y="218" text-anchor="middle" class="mono-blue">→ E (Исполнение) → W (Запись)</text>

  <!-- Bottom: Branch misprediction -->
  <rect x="38" y="280" width="964" height="168" rx="6" class="box-warm"/>
  <text x="58" y="308" class="mono-orange">2. ПРОМАХ ПРЕДСКАЗАТЕЛЯ НА СЛУЧАЙНОМ IF: СПЕКУЛЯТИВНЫЕ ШАГИ ВЫБРАСЫВАЮТСЯ (FLUSH)</text>

  <text x="58" y="348" class="mono-bold">if v &gt;= 128</text>
  <rect x="170" y="328" width="68" height="26" class="box"/><text x="204" y="346" text-anchor="middle" class="mono-sm">F</text>
  <rect x="242" y="328" width="68" height="26" class="box"/><text x="276" y="346" text-anchor="middle" class="mono-sm">D</text>
  <rect x="314" y="328" width="110" height="26" class="box-warm"/><text x="369" y="346" text-anchor="middle" class="mono-orange">E (промах!)</text>

  <text x="58" y="382" class="mono-orange">Ложная ветка</text>
  <rect x="242" y="362" width="68" height="26" class="box-warm"/><text x="276" y="380" text-anchor="middle" class="mono-orange">F (✕)</text>
  <rect x="314" y="362" width="68" height="26" class="box-warm"/><text x="348" y="380" text-anchor="middle" class="mono-orange">D (✕)</text>
  <text x="396" y="380" class="mono-orange">← сброс конвейера (15–20 тактов в реальном CPU)</text>

  <text x="58" y="416" class="mono-blue">Верная ветка</text>
  <rect x="432" y="396" width="68" height="26" class="box-accent"/><text x="466" y="414" text-anchor="middle" class="mono-blue">F</text>
  <rect x="504" y="396" width="68" height="26" class="box-accent"/><text x="538" y="414" text-anchor="middle" class="mono-blue">D</text>
  <rect x="576" y="396" width="68" height="26" class="box-accent"/><text x="610" y="414" text-anchor="middle" class="mono-blue">E</text>
  <rect x="648" y="396" width="68" height="26" class="box-accent"/><text x="682" y="414" text-anchor="middle" class="mono-blue">W</text>
  <text x="732" y="414" class="label">Перезапуск с нового адреса</text>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/1. Компьютер изнутри",
        "filename": "cache-line-64b-locality.svg",
        "w": 1040, "h": 480,
        "title": "КЭШ-ЛИНИЯ 64 БАЙТА: []BOOKMARK ПРОТИВ []*BOOKMARK",
        "subtitle": "Контроллер памяти загружает из RAM сразу блок в 64 байта — плотный слайс значений использует его целиком",
        "caption": "Пространственная локальность данных: слайс структур []Bookmark попадает в 64-байтную кэш-линию против прыжков по указателям []*Bookmark",
        "alt": "Сравнение 64-байтной кэш-линии при обходе плотного слайса []Bookmark и слайса указателей []*Bookmark",
        "body": '''
  <!-- Top: []Bookmark -->
  <rect x="38" y="92" width="964" height="168" rx="6" class="box-accent"/>
  <text x="58" y="120" class="mono-blue">1. ПЛОТНЫЙ СЛАЙС []Item (ПО 16 БАЙТОВ): ОДНА КЭШ-ЛИНИЯ (64 Б) ПРИНОСИТ 4 ЭЛЕМЕНТА СРАЗУ</text>

  <g transform="translate(58, 138)">
    <rect x="0" y="0" width="220" height="72" class="box"/>
    <text x="110" y="28" text-anchor="middle" class="mono-bold">Item[0] (16 Б)</text>
    <text x="110" y="54" text-anchor="middle" class="mono-orange">1 промах RAM (~100 нс)</text>

    <rect x="228" y="0" width="220" height="72" class="box"/>
    <text x="338" y="28" text-anchor="middle" class="mono-bold">Item[1] (16 Б)</text>
    <text x="338" y="54" text-anchor="middle" class="mono-blue">Попадание L1 (~1 нс)</text>

    <rect x="456" y="0" width="220" height="72" class="box"/>
    <text x="566" y="28" text-anchor="middle" class="mono-bold">Item[2] (16 Б)</text>
    <text x="566" y="54" text-anchor="middle" class="mono-blue">Попадание L1 (~1 нс)</text>

    <rect x="684" y="0" width="220" height="72" class="box"/>
    <text x="794" y="28" text-anchor="middle" class="mono-bold">Item[3] (16 Б)</text>
    <text x="794" y="54" text-anchor="middle" class="mono-blue">Попадание L1 (~1 нс)</text>
  </g>
  <text x="58" y="238" class="label">Плюс аппаратный предвыборщик (prefetcher) угадывает линейное чтение и заранее подтягивает следующие кэш-линии.</text>

  <!-- Bottom: []*Bookmark -->
  <rect x="38" y="278" width="964" height="170" rx="6" class="box-warm"/>
  <text x="58" y="306" class="mono-orange">2. СЛАЙС УКАЗАТЕЛЕЙ []*Item: КАЖДЫЙ УКАЗАТЕЛЬ ВЕДЁТ В СЛУЧАЙНОЕ МЕСТО КУЧИ</text>

  <rect x="58" y="326" width="140" height="62" class="box"/><text x="128" y="362" text-anchor="middle" class="mono">ptr[0] ──▶</text>
  <rect x="210" y="326" width="140" height="62" class="box"/><text x="280" y="362" text-anchor="middle" class="mono">ptr[1] ──▶</text>
  <rect x="362" y="326" width="140" height="62" class="box"/><text x="432" y="362" text-anchor="middle" class="mono">ptr[2] ──▶</text>

  <rect x="560" y="318" width="130" height="50" class="box-dark"/><text x="625" y="348" text-anchor="middle" class="mono-sm">0xc00018a0</text>
  <rect x="715" y="318" width="130" height="50" class="box-dark"/><text x="780" y="348" text-anchor="middle" class="mono-sm">0xc0094400</text>
  <rect x="865" y="318" width="120" height="50" class="box-dark"/><text x="925" y="348" text-anchor="middle" class="mono-sm">0xc00310c0</text>

  <text x="560" y="400" class="mono-orange">Три разных кэш-линии = 3 промаха в RAM (3 × 100 нс)!</text>
  <text x="58" y="428" class="label">Дополнительная цена: лишние 8 Б на каждый указатель и лишняя работа для сборщика мусора.</text>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/1. Компьютер изнутри",
        "filename": "struct-alignment-padding.svg",
        "w": 1040, "h": 460,
        "title": "ВЫРАВНИВАНИЕ ПОЛЕЙ СТРУКТУРЫ GO: BADLAYOUT (24 Б) → GOODLAYOUT (16 Б)",
        "subtitle": "Компилятор выравнивает поля по адресам, кратным их размеру, чтобы CPU не читал одно число за два обращения",
        "caption": "Побайтовая карта смещений BadLayout (24 байта с 14 байтами паддинга) и GoodLayout (16 байтов, экономия 33%)",
        "alt": "Сравнение побайтового размещения полей структур BadLayout 24 байта и GoodLayout 16 байтов с паддингом",
        "body": '''
  <!-- Top: BadLayout (24 bytes) -->
  <rect x="38" y="92" width="964" height="162" rx="6" class="box-warm"/>
  <text x="58" y="120" class="mono-orange">BADLAYOUT: struct { Active bool; ID int64; Deleted bool }  →  unsafe.Sizeof = 24 байта (14 Б пустые!)</text>

  <g transform="translate(58, 138)">
    <rect x="0" y="20" width="38" height="56" class="box-accent"/><text x="19" y="13" text-anchor="middle" class="mono-sm">0</text><text x="19" y="53" text-anchor="middle" class="mono-bold">A</text>
    <rect x="40" y="20" width="260" height="56" class="box-dark"/><text x="170" y="13" text-anchor="middle" class="mono-sm">1..7</text><text x="170" y="53" text-anchor="middle" class="mono-orange">паддинг (7 Б)</text>
    <rect x="302" y="20" width="296" height="56" class="box-accent"/><text x="450" y="13" text-anchor="middle" class="mono-sm">8..15 (кратно 8)</text><text x="450" y="53" text-anchor="middle" class="mono-blue">ID: int64 (8 Б)</text>
    <rect x="600" y="20" width="38" height="56" class="box-accent"/><text x="619" y="13" text-anchor="middle" class="mono-sm">16</text><text x="619" y="53" text-anchor="middle" class="mono-bold">D</text>
    <rect x="640" y="20" width="280" height="56" class="box-dark"/><text x="780" y="13" text-anchor="middle" class="mono-sm">17..23 (округление до 8)</text><text x="780" y="53" text-anchor="middle" class="mono-orange">хвостовой паддинг (7 Б)</text>
  </g>
  <text x="58" y="236" class="label">Хвостовой паддинг нужен, чтобы в слайсе []BadLayout у второго элемента поле ID тоже легло на адрес, кратный 8.</text>

  <!-- Bottom: GoodLayout (16 bytes) -->
  <rect x="38" y="274" width="964" height="154" rx="6" class="box-accent"/>
  <text x="58" y="302" class="mono-blue">GOODLAYOUT: struct { ID int64; Active bool; Deleted bool }  →  unsafe.Sizeof = 16 байтов (экономия 33%!)</text>

  <g transform="translate(58, 320)">
    <rect x="0" y="20" width="296" height="56" class="box-accent"/><text x="148" y="13" text-anchor="middle" class="mono-sm">0..7</text><text x="148" y="53" text-anchor="middle" class="mono-blue">ID: int64 (8 Б)</text>
    <rect x="298" y="20" width="38" height="56" class="box-accent"/><text x="317" y="13" text-anchor="middle" class="mono-sm">8</text><text x="317" y="53" text-anchor="middle" class="mono-bold">A</text>
    <rect x="338" y="20" width="38" height="56" class="box-accent"/><text x="357" y="13" text-anchor="middle" class="mono-sm">9</text><text x="357" y="53" text-anchor="middle" class="mono-bold">D</text>
    <rect x="378" y="20" width="220" height="56" class="box-dark"/><text x="488" y="13" text-anchor="middle" class="mono-sm">10..15</text><text x="488" y="53" text-anchor="middle" class="mono">паддинг (6 Б)</text>
    <rect x="625" y="20" width="295" height="56" class="box"/><text x="772" y="45" text-anchor="middle" class="mono-blue">4 структуры в 1 кэш-линию 64 Б</text><text x="772" y="65" text-anchor="middle" class="label">на 10 млн записей экономится 80 МБ</text>
  </g>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/1. Компьютер изнутри",
        "filename": "endianness-big-vs-little.svg",
        "w": 1040, "h": 420,
        "title": "ПОРЯДОК БАЙТОВ (ENDIANNESS): LITTLE-ENDIAN ПРОТИВ BIG-ENDIAN",
        "subtitle": "Как 32-битное число 0x12345678 раскладывается по четырём соседним байтам памяти или сетевого буфера",
        "caption": "Хранение числа 0x12345678 по адресам +0..+3 в Little-Endian (x86-64/ARM64) и Big-Endian (сетевые протоколы)",
        "alt": "Сравнение порядка байтов числа 0x12345678 в Little-Endian и Big-Endian по адресам памяти",
        "body": '''
  <!-- Source number -->
  <rect x="38" y="92" width="964" height="56" rx="6" class="box-dark"/>
  <text x="520" y="126" text-anchor="middle" class="mono-bold">Число uint32:  0x  12 (старший байт, MSB)  |  34  |  56  |  78 (младший байт, LSB)</text>

  <!-- Left: Little-Endian -->
  <rect x="38" y="168" width="465" height="218" rx="6" class="box-accent"/>
  <text x="270" y="198" text-anchor="middle" class="mono-blue">LITTLE-ENDIAN (x86-64, ARM64)</text>
  <text x="270" y="220" text-anchor="middle" class="label">Младший байт (78) кладётся по младшему адресу +0</text>

  <g transform="translate(65, 240)">
    <text x="48" y="14" text-anchor="middle" class="mono-sm">addr +0</text><rect x="0" y="22" width="96" height="58" class="box-warm"/><text x="48" y="56" text-anchor="middle" class="h1">78</text>
    <text x="152" y="14" text-anchor="middle" class="mono-sm">addr +1</text><rect x="104" y="22" width="96" height="58" class="box"/><text x="152" y="56" text-anchor="middle" class="h1">56</text>
    <text x="256" y="14" text-anchor="middle" class="mono-sm">addr +2</text><rect x="208" y="22" width="96" height="58" class="box"/><text x="256" y="56" text-anchor="middle" class="h1">34</text>
    <text x="360" y="14" text-anchor="middle" class="mono-sm">addr +3</text><rect x="312" y="22" width="96" height="58" class="box-accent"/><text x="360" y="56" text-anchor="middle" class="h1">12</text>
  </g>
  <text x="270" y="364" text-anchor="middle" class="mono">binary.LittleEndian.PutUint32(buf, 0x12345678)</text>

  <!-- Right: Big-Endian -->
  <rect x="537" y="168" width="465" height="218" rx="6" class="box-warm"/>
  <text x="769" y="198" text-anchor="middle" class="mono-orange">BIG-ENDIAN (СЕТЕВОЙ ПОРЯДОК)</text>
  <text x="769" y="220" text-anchor="middle" class="label">Старший байт (12) идёт первым — как мы пишем на бумаге</text>

  <g transform="translate(564, 240)">
    <text x="48" y="14" text-anchor="middle" class="mono-sm">addr +0</text><rect x="0" y="22" width="96" height="58" class="box-accent"/><text x="48" y="56" text-anchor="middle" class="h1">12</text>
    <text x="152" y="14" text-anchor="middle" class="mono-sm">addr +1</text><rect x="104" y="22" width="96" height="58" class="box"/><text x="152" y="56" text-anchor="middle" class="h1">34</text>
    <text x="256" y="14" text-anchor="middle" class="mono-sm">addr +2</text><rect x="208" y="22" width="96" height="58" class="box"/><text x="256" y="56" text-anchor="middle" class="h1">56</text>
    <text x="360" y="14" text-anchor="middle" class="mono-sm">addr +3</text><rect x="312" y="22" width="96" height="58" class="box-warm"/><text x="360" y="56" text-anchor="middle" class="h1">78</text>
  </g>
  <text x="769" y="364" text-anchor="middle" class="mono">binary.BigEndian.PutUint32(buf, 0x12345678)</text>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/2. Операционная система и Linux",
        "filename": "virtual-memory-pages-mmu.svg",
        "w": 1040, "h": 480,
        "title": "ВИРТУАЛЬНАЯ ПАМЯТЬ И MMU: ИЗОЛЯЦИЯ ПРОЦЕССОВ ЧЕРЕЗ СТРАНИЦЫ 4 КБ",
        "subtitle": "Два процесса видят одинаковый виртуальный адрес 0x1000, но MMU переводит его в разные физические кадры RAM",
        "caption": "Трансляция виртуальных адресов процессов A и B через таблицы страниц и контроллер MMU в физические кадры оперативной памяти",
        "alt": "Схема трансляции виртуальных страниц процессов A и B через MMU в изолированные кадры физической памяти RAM",
        "body": '''
  <!-- Process A -->
  <rect x="38" y="96" width="260" height="162" rx="6" class="box-accent"/>
  <text x="168" y="124" text-anchor="middle" class="mono-blue">ПРОЦЕСС A (PID 101)</text>
  <rect x="58" y="140" width="220" height="44" class="box"/><text x="168" y="167" text-anchor="middle" class="mono-bold">Вирт. стр. 0x1000 (4 КБ)</text>
  <rect x="58" y="196" width="220" height="44" class="box"/><text x="168" y="223" text-anchor="middle" class="mono">Вирт. стр. 0x2000 (4 КБ)</text>

  <!-- Process B -->
  <rect x="38" y="280" width="260" height="162" rx="6" class="box-warm"/>
  <text x="168" y="308" text-anchor="middle" class="mono-orange">ПРОЦЕСС B (PID 202)</text>
  <rect x="58" y="324" width="220" height="44" class="box"/><text x="168" y="351" text-anchor="middle" class="mono-bold">Вирт. стр. 0x1000 (4 КБ)</text>
  <rect x="58" y="380" width="220" height="44" class="box"/><text x="168" y="407" text-anchor="middle" class="mono">Нет прав на память A!</text>

  <!-- Center: MMU -->
  <rect x="370" y="138" width="280" height="256" rx="6" class="box-dark"/>
  <text x="510" y="170" text-anchor="middle" class="mono-bold">MMU + ТАБЛИЦЫ СТРАНИЦ</text>
  <text x="510" y="196" text-anchor="middle" class="label">(Аппаратура CPU + Ядро Linux)</text>
  <rect x="392" y="218" width="236" height="66" class="box"/><text x="510" y="244" text-anchor="middle" class="mono-blue">A: 0x1000 → Кадр #5</text><text x="510" y="268" text-anchor="middle" class="mono">A: 0x2000 → Кадр #2</text>
  <rect x="392" y="300" width="236" height="66" class="box"/><text x="510" y="326" text-anchor="middle" class="mono-orange">B: 0x1000 → Кадр #8</text><text x="510" y="350" text-anchor="middle" class="label">Доступ к чужому → SIGSEGV</text>

  <line x1="298" y1="162" x2="366" y2="236" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="298" y1="218" x2="366" y2="268" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="298" y1="346" x2="366" y2="328" class="line-orange" marker-end="url(#arrowOrange)"/>

  <!-- Right: Physical RAM -->
  <rect x="720" y="96" width="282" height="346" rx="6" class="box"/>
  <text x="861" y="124" text-anchor="middle" class="mono-bold">ФИЗИЧЕСКАЯ RAM (ПЛАНКА)</text>
  <rect x="742" y="144" width="238" height="46" class="box-dark"/><text x="861" y="172" text-anchor="middle" class="mono">Кадр #0..1 (Ядро Linux)</text>
  <rect x="742" y="200" width="238" height="46" class="box-accent"/><text x="861" y="228" text-anchor="middle" class="mono-blue">Кадр #2 (Данные A · 0x2000)</text>
  <rect x="742" y="256" width="238" height="46" class="box-accent"/><text x="861" y="284" text-anchor="middle" class="mono-blue">Кадр #5 (Код A · 0x1000)</text>
  <rect x="742" y="312" width="238" height="46" class="box-warm"/><text x="861" y="340" text-anchor="middle" class="mono-orange">Кадр #8 (Код B · 0x1000)</text>
  <rect x="742" y="368" width="238" height="52" class="box"/><text x="861" y="392" text-anchor="middle" class="mono-sm">Свободная память /</text><text x="861" y="410" text-anchor="middle" class="mono-sm">Страничный кэш диска</text>

  <line x1="650" y1="242" x2="738" y2="278" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="650" y1="268" x2="738" y2="224" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="650" y1="328" x2="738" y2="335" class="line-orange" marker-end="url(#arrowOrange)"/>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/2. Операционная система и Linux",
        "filename": "linux-inode-fd-atomic-rename.svg",
        "w": 1040, "h": 480,
        "title": "АТОМАРНАЯ ЗАМЕНА ФАЙЛА В LINUX: INODE, SYNC И OS.RENAME",
        "subtitle": "Запись в новый временный файл + сброс на диск + атомарное переключение указателя каталога на новый inode",
        "caption": "Механизм безопасного сохранения bookmarks.json: временный файл, Sync() и атомарный os.Rename в таблице каталога",
        "alt": "Схема атомарного сохранения файла в Linux через временный файл, Sync и os.Rename с переключением inode",
        "body": '''
  <!-- Left: Before Rename -->
  <rect x="38" y="92" width="462" height="270" rx="6" class="box"/>
  <text x="269" y="120" text-anchor="middle" class="mono-blue">ШАГ 1–2: ПИШЕМ В ВРЕМЕННЫЙ ФАЙЛ + TMP.SYNC()</text>

  <rect x="58" y="140" width="200" height="102" class="box-dark"/>
  <text x="158" y="164" text-anchor="middle" class="mono-bold">Записи каталога:</text>
  <text x="72" y="194" class="mono">bookmarks.json → #401</text>
  <text x="72" y="222" class="mono-orange">bm.tmp.8391    → #402</text>

  <rect x="292" y="140" width="188" height="46" class="box-accent"/>
  <text x="386" y="168" text-anchor="middle" class="mono-blue">inode #401 (старый OK)</text>
  <rect x="292" y="198" width="188" height="46" class="box-warm"/>
  <text x="386" y="226" text-anchor="middle" class="mono-orange">inode #402 (новый + Sync)</text>

  <line x1="258" y1="190" x2="290" y2="165" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="258" y1="218" x2="290" y2="220" class="line-orange" marker-end="url(#arrowOrange)"/>

  <text x="58" y="280" class="mono">• Если свет погаснет на этом шаге:</text>
  <text x="58" y="304" class="label">  старый файл bookmarks.json (#401) остался нетронутым!</text>
  <text x="58" y="328" class="label">  битый хвост останется только во временном файле.</text>

  <!-- Center arrow -->
  <line x1="504" y1="226" x2="536" y2="226" class="line-blue" marker-end="url(#arrowBlue)"/>

  <!-- Right: After Rename -->
  <rect x="540" y="92" width="462" height="270" rx="6" class="box-accent"/>
  <text x="771" y="120" text-anchor="middle" class="mono-blue">ШАГ 3: OS.RENAME(TMP, "BOOKMARKS.JSON")</text>

  <rect x="560" y="140" width="205" height="102" class="box"/>
  <text x="662" y="164" text-anchor="middle" class="mono-bold">Запись каталога:</text>
  <text x="574" y="198" class="mono-blue">bookmarks.json → #402</text>
  <text x="574" y="224" class="label">(одна атомарная операция)</text>

  <rect x="795" y="140" width="188" height="46" class="box-dark"/>
  <text x="889" y="168" text-anchor="middle" class="mono-sm">inode #401 (удалён)</text>
  <rect x="795" y="198" width="188" height="46" class="box-accent"/>
  <text x="889" y="226" text-anchor="middle" class="mono-blue">inode #402 (новый файл)</text>

  <line x1="765" y1="194" x2="793" y2="220" class="line-blue" marker-end="url(#arrowBlue)"/>

  <text x="560" y="280" class="mono-bold">• Для любого читателя на диске всегда</text>
  <text x="560" y="304" class="mono-bold">  существует либо целиком старый,</text>
  <text x="560" y="328" class="mono-bold">  либо целиком новый JSON.</text>

  <!-- Bottom rule -->
  <rect x="38" y="382" width="964" height="66" rx="6" class="box-warm"/>
  <text x="58" y="410" class="mono-orange">ВАЖНО: ВРЕМЕННЫЙ ФАЙЛ СОЗДАЁТСЯ В ТОМ ЖЕ КАТАЛОГЕ (os.CreateTemp(dir, ...))</text>
  <text x="58" y="434" class="sub">Перемещение между разными файловыми системами (например, из /tmp в /var) не атомарно — ядро скопирует байты по одному.</text>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/3. Сети и HTTP",
        "filename": "tcp-handshake-and-close.svg",
        "w": 1040, "h": 500,
        "title": "ЖИЗНЕННЫЙ ЦИКЛ TCP-СОЕДИНЕНИЯ: РУКОПОЖАТИЕ, ПОТОК И ЗАКРЫТИЕ",
        "subtitle": "Трёхстороннее рукопожатие (SYN → SYN+ACK → ACK), нумерация байтов и закрытие через FIN / TIME_WAIT",
        "caption": "Последовательность пакетов TCP: установка соединения за 3 шага, передача нумерованных байтов и 4-шаговое закрытие",
        "alt": "Диаграмма обмена TCP-пакетами: трёхстороннее рукопожатие SYN, SYN+ACK, ACK, передача данных и закрытие FIN",
        "body": '''
  <!-- Lifelines -->
  <rect x="140" y="92" width="170" height="40" rx="6" class="box-accent"/>
  <text x="225" y="117" text-anchor="middle" class="mono-blue">КЛИЕНТ (Go)</text>
  <line x1="225" y1="132" x2="225" y2="462" stroke="#0369a1" stroke-width="2.5"/>

  <rect x="520" y="92" width="170" height="40" rx="6" class="box-warm"/>
  <text x="605" y="117" text-anchor="middle" class="mono-orange">СЕРВЕР (Listen)</text>
  <line x1="605" y1="132" x2="605" y2="462" stroke="#c2410c" stroke-width="2.5"/>

  <!-- 1. Handshake -->
  <line x1="225" y1="164" x2="600" y2="188" class="line-blue" marker-end="url(#arrowBlue)"/>
  <text x="415" y="166" text-anchor="middle" class="mono-bold">1. SYN (seq = 100)</text>

  <line x1="605" y1="210" x2="230" y2="234" class="line-orange" marker-end="url(#arrowOrange)"/>
  <text x="415" y="212" text-anchor="middle" class="mono-bold">2. SYN + ACK (seq = 500, ack = 101)</text>

  <line x1="225" y1="256" x2="600" y2="280" class="line-blue" marker-end="url(#arrowBlue)"/>
  <text x="415" y="258" text-anchor="middle" class="mono-bold">3. ACK (ack = 501) → Соединение открыто!</text>

  <!-- 2. Data stream -->
  <rect x="255" y="294" width="320" height="36" rx="4" class="box-dark"/>
  <text x="415" y="317" text-anchor="middle" class="mono-blue">Поток байтов: GET /ping (seq=101, len=10) + ACK=111</text>

  <!-- 3. Teardown -->
  <line x1="225" y1="352" x2="600" y2="374" class="line" marker-end="url(#arrow)"/>
  <text x="415" y="354" text-anchor="middle" class="mono">4. FIN (клиент закрыл запись)</text>

  <line x1="605" y1="392" x2="230" y2="412" class="line" marker-end="url(#arrow)"/>
  <text x="415" y="394" text-anchor="middle" class="mono">5. ACK + FIN (сервер закрыл запись)</text>

  <line x1="225" y1="432" x2="600" y2="452" class="line" marker-end="url(#arrow)"/>
  <text x="415" y="434" text-anchor="middle" class="mono">6. ACK → TIME_WAIT (~60 с, защита от запоздалых сегментов)</text>

  <!-- Side Notes -->
  <rect x="720" y="140" width="282" height="145" rx="6" class="box"/>
  <text x="861" y="168" text-anchor="middle" class="mono-blue">НАДЁЖНОСТЬ TCP</text>
  <text x="738" y="196" class="mono">• Каждому байту дан номер Seq</text>
  <text x="738" y="222" class="mono">• Потеря → повторная отправка</text>
  <text x="738" y="248" class="mono">• Нет границ сообщений!</text>
  <text x="738" y="270" class="label">Нужен разделитель (\n или длина)</text>

  <rect x="720" y="302" width="282" height="148" rx="6" class="box-warm"/>
  <text x="861" y="330" text-anchor="middle" class="mono-orange">ПОЧЕМУ НУЖЕН TIME_WAIT</text>
  <text x="738" y="358" class="label">1. Гарантия доставки финального ACK</text>
  <text x="738" y="382" class="label">2. Старые блуждающие пакеты не</text>
  <text x="738" y="402" class="label">   попадут в новое соединение</text>
  <text x="738" y="426" class="mono">net.DialTimeout · SetDeadline</text>
'''
    },
    {
        "dir": "sources/5. Компьютер, ОС и Сети под твоим кодом/3. Сети и HTTP",
        "filename": "http1-vs-http2-multiplexing.svg",
        "w": 1040, "h": 480,
        "title": "ЭВОЛЮЦИЯ ТРАНСПОРТА ВЕБА: HTTP/1.1 → HTTP/2 → HTTP/3 (QUIC)",
        "subtitle": "Как мультиплексирование потоков убрало очередь ожидания ответа в одном TCP-соединении, а QUIC переехал на UDP",
        "caption": "Сравнение очередности запросов в HTTP/1.1, мультиплексирования бинарных потоков HTTP/2 поверх TCP и независимых потоков HTTP/3 поверх QUIC/UDP",
        "alt": "Сравнение передачи ресурсов в HTTP/1.1 с очередью, HTTP/2 с мультиплексированием по TCP и HTTP/3 поверх UDP",
        "body": '''
  <!-- HTTP/1.1 -->
  <rect x="38" y="92" width="964" height="110" rx="6" class="box-warm"/>
  <text x="58" y="118" class="mono-orange">HTTP/1.1 (1 ЗАПРОС ЗА РАЗ НА 1 TCP-СОЕДИНЕНИЕ — БЛОКИРОВКА В ГОЛОВЕ ОЧЕРЕДИ)</text>
  <rect x="58" y="134" width="220" height="44" class="box"/><text x="168" y="161" text-anchor="middle" class="mono">Запрос 1 (app.js) ──▶ Ответ 1</text>
  <rect x="290" y="134" width="240" height="44" class="box"/><text x="410" y="161" text-anchor="middle" class="mono">Запрос 2 (style.css) ──▶ Ответ 2</text>
  <rect x="542" y="134" width="220" height="44" class="box"/><text x="652" y="161" text-anchor="middle" class="mono">Запрос 3 (data) ──▶ Ответ 3</text>
  <text x="782" y="161" class="label">Браузер открывает до 6 TCP</text>

  <!-- HTTP/2 -->
  <rect x="38" y="218" width="964" height="114" rx="6" class="box-accent"/>
  <text x="58" y="244" class="mono-blue">HTTP/2 (МУЛЬТИПЛЕКСИРОВАНИЕ БИНАРНЫХ ФРЕЙМОВ В ОДНОМ TCP-СОЕДИНЕНИИ)</text>
  <rect x="58" y="260" width="115" height="48" class="box"/><text x="115" y="289" text-anchor="middle" class="mono-blue">Stream 1</text>
  <rect x="180" y="260" width="115" height="48" class="box-dark"/><text x="237" y="289" text-anchor="middle" class="mono-bold">Stream 3</text>
  <rect x="302" y="260" width="115" height="48" class="box-warm"/><text x="359" y="289" text-anchor="middle" class="mono-orange">Stream 5</text>
  <rect x="424" y="260" width="115" height="48" class="box"/><text x="481" y="289" text-anchor="middle" class="mono-blue">Stream 1</text>
  <rect x="546" y="260" width="115" height="48" class="box-dark"/><text x="603" y="289" text-anchor="middle" class="mono-bold">Stream 3</text>
  <text x="682" y="280" class="mono">Сжатие заголовков HPACK</text>
  <text x="682" y="302" class="label">Но потеря 1 TCP-пакета тормозит всё!</text>

  <!-- HTTP/3 -->
  <rect x="38" y="348" width="964" height="106" rx="6" class="box"/>
  <text x="58" y="374" class="mono-bold">HTTP/3 (QUIC ПОВЕРХ UDP + ВСТРОЕННЫЙ TLS 1.3): ПОТОКИ ПОЛНОСТЬЮ НЕЗАВИСИМЫ</text>
  <rect x="58" y="390" width="280" height="44" class="box-accent"/><text x="198" y="417" text-anchor="middle" class="mono-blue">QUIC Stream 1 (идёт без задержки)</text>
  <rect x="354" y="390" width="280" height="44" class="box-warm"/><text x="494" y="417" text-anchor="middle" class="mono-orange">QUIC Stream 3 (ждёт повтор пакета)</text>
  <rect x="650" y="390" width="332" height="44" class="box-dark"/><text x="816" y="417" text-anchor="middle" class="mono">Быстрый старт (0-RTT / 1-RTT) на мобильных</text>
'''
    },

    # -----------------------------------------------------------------------
    # МОДУЛЬ 6 (4 схемы)
    # -----------------------------------------------------------------------
    {
        "dir": "sources/6. Вводный курс структур данных и алгоритмов",
        "filename": "big-o-growth-curves.svg",
        "w": 1040, "h": 480,
        "title": "КЛАССЫ СЛОЖНОСТИ BIG-O: РОСТ ЧИСЛА ОПЕРАЦИЙ ОТ РАЗМЕРА ВХОДА N",
        "subtitle": "На 10 элементах разница незаметна, но на миллионе записей O(log n) делает 20 шагов, а O(n²) — триллион",
        "caption": "Кривые роста сложности O(1), O(log n), O(n), O(n log n) и O(n²) и сравнение числа операций при n = 1000 и n = 1 000 000",
        "alt": "График роста времени работы алгоритмов O(1), O(log n), O(n), O(n log n), O(n²) с таблицей значений",
        "body": '''
  <!-- Left: Coordinate chart -->
  <rect x="38" y="92" width="520" height="356" rx="6" class="box"/>
  <text x="298" y="120" text-anchor="middle" class="mono-blue">РОСТ ЧИСЛА ОПЕРАЦИЙ T(n)</text>

  <!-- Axes -->
  <line x1="88" y1="406" x2="520" y2="406" class="line" marker-end="url(#arrow)"/>
  <line x1="88" y1="406" x2="88" y2="142" class="line" marker-end="url(#arrow)"/>
  <text x="515" y="428" text-anchor="end" class="mono-sm">Размер входа n</text>
  <text x="98" y="152" class="mono-sm">Операции</text>

  <!-- Curves -->
  <!-- O(1) -->
  <line x1="88" y1="392" x2="495" y2="392" stroke="#0284c7" stroke-width="2.6"/>
  <text x="502" y="396" class="mono-blue">O(1)</text>
  <!-- O(log n) -->
  <path d="M 88 392 Q 180 364 495 352" fill="none" stroke="#0369a1" stroke-width="2.6"/>
  <text x="502" y="356" class="mono-blue">O(log n)</text>
  <!-- O(n) -->
  <line x1="88" y1="406" x2="465" y2="256" stroke="#334155" stroke-width="2.4"/>
  <text x="472" y="256" class="mono-bold">O(n)</text>
  <!-- O(n log n) -->
  <path d="M 88 406 C 210 350, 310 265, 385 162" fill="none" stroke="#ea580c" stroke-width="2.6"/>
  <text x="394" y="166" class="mono-orange">O(n log n)</text>
  <!-- O(n^2) -->
  <path d="M 88 406 C 145 390, 195 290, 225 148" fill="none" stroke="#c2410c" stroke-width="3"/>
  <text x="234" y="158" class="mono-orange">O(n²)</text>

  <!-- Right: Concrete numbers table -->
  <rect x="578" y="92" width="424" height="356" rx="6" class="box-dark"/>
  <text x="790" y="122" text-anchor="middle" class="mono-bold">РЕАЛЬНЫЕ ЦИФРЫ ОПЕРАЦИЙ</text>
  <line x1="598" y1="138" x2="982" y2="138" stroke="#64748b"/>
  <text x="640" y="164" class="mono-bold">Класс</text>
  <text x="780" y="164" text-anchor="middle" class="mono-bold">n = 1 000</text>
  <text x="915" y="164" text-anchor="middle" class="mono-bold">n = 1 000 000</text>
  <line x1="598" y1="176" x2="982" y2="176" stroke="#94a3b8"/>

  <text x="615" y="212" class="mono-blue">O(1)</text><text x="780" y="212" text-anchor="middle" class="mono">1</text><text x="915" y="212" text-anchor="middle" class="mono-blue">1 (мапа)</text>
  <text x="615" y="252" class="mono-blue">O(log n)</text><text x="780" y="252" text-anchor="middle" class="mono">10</text><text x="915" y="252" text-anchor="middle" class="mono-blue">20 (бинпоиск)</text>
  <text x="615" y="292" class="mono-bold">O(n)</text><text x="780" y="292" text-anchor="middle" class="mono">1 000</text><text x="915" y="292" text-anchor="middle" class="mono">1 000 000</text>
  <text x="615" y="332" class="mono-orange">O(n log n)</text><text x="780" y="332" text-anchor="middle" class="mono">10 000</text><text x="915" y="332" text-anchor="middle" class="mono-orange">~20 000 000</text>
  <text x="615" y="372" class="mono-orange">O(n²)</text><text x="780" y="372" text-anchor="middle" class="mono">1 000 000</text><text x="915" y="372" text-anchor="middle" class="mono-orange">10¹² (часы!)</text>

  <text x="790" y="422" text-anchor="middle" class="label">Big-O описывает форму роста, но кэш-линии влияют на константу.</text>
'''
    },
    {
        "dir": "sources/6. Вводный курс структур данных и алгоритмов",
        "filename": "ring-buffer-fifo.svg",
        "w": 1040, "h": 460,
        "title": "КОЛЬЦЕВОЙ БУФЕР FIFO НА СЛАЙСЕ GO БЕЗ УТЕЧКИ ПАМЯТИ",
        "subtitle": "Индексы head и tail заворачиваются по модулю ёмкости (idx + 1) % cap — массив переиспользуется бесконечно",
        "caption": "Кольцевой буфер ёмкостью 8 с указателями head и tail и сравнение с утечкой памяти при наивном сдвиге слайса q = q[1:]",
        "alt": "Схема кольцевого буфера FIFO на 8 слотов с индексами head и tail и сравнение с утечкой памяти при q = q[1:]",
        "body": '''
  <!-- Left: Ring buffer array wrapped around -->
  <rect x="38" y="92" width="580" height="336" rx="6" class="box"/>
  <text x="328" y="120" text-anchor="middle" class="mono-blue">КОЛЬЦЕВОЙ БУФЕР (CAP = 8, SIZE = 4): HEAD = 5, TAIL = 1</text>

  <g transform="translate(62, 165)">
    <text x="30" y="-12" text-anchor="middle" class="mono-sm">[0]</text><rect x="0" y="0" width="60" height="66" class="box-accent"/><text x="30" y="38" text-anchor="middle" class="mono-bold">D</text>
    <text x="94" y="-12" text-anchor="middle" class="mono-orange">tail=1</text><rect x="64" y="0" width="60" height="66" class="box"/><text x="94" y="38" text-anchor="middle" class="mono-sm">nil</text>
    <text x="158" y="-12" text-anchor="middle" class="mono-sm">[2]</text><rect x="128" y="0" width="60" height="66" class="box"/><text x="158" y="38" text-anchor="middle" class="mono-sm">nil</text>
    <text x="222" y="-12" text-anchor="middle" class="mono-sm">[3]</text><rect x="192" y="0" width="60" height="66" class="box"/><text x="222" y="38" text-anchor="middle" class="mono-sm">nil</text>
    <text x="286" y="-12" text-anchor="middle" class="mono-sm">[4]</text><rect x="256" y="0" width="60" height="66" class="box"/><text x="286" y="38" text-anchor="middle" class="mono-sm">nil</text>
    <text x="350" y="-12" text-anchor="middle" class="mono-blue">head=5</text><rect x="320" y="0" width="60" height="66" class="box-warm"/><text x="350" y="38" text-anchor="middle" class="mono-bold">A</text>
    <text x="414" y="-12" text-anchor="middle" class="mono-sm">[6]</text><rect x="384" y="0" width="60" height="66" class="box-accent"/><text x="414" y="38" text-anchor="middle" class="mono-bold">B</text>
    <text x="478" y="-12" text-anchor="middle" class="mono-sm">[7]</text><rect x="448" y="0" width="60" height="66" class="box-accent"/><text x="478" y="38" text-anchor="middle" class="mono-bold">C</text>

    <!-- Wrap-around arrow from [7] back to [0] -->
    <path d="M 478 66 L 478 102 L 30 102 L 30 70" class="line-blue" marker-end="url(#arrowBlue)"/>
    <text x="254" y="94" text-anchor="middle" class="mono-blue">перенос по кругу: (7 + 1) % 8 == 0</text>
  </g>

  <rect x="62" y="302" width="532" height="104" class="box-dark"/>
  <text x="80" y="330" class="mono-bold">Push(x): buf[tail] = x;  tail = (tail + 1) % len(buf);  size++</text>
  <text x="80" y="358" class="mono-bold">Pop():   v := buf[head]; buf[head] = zero; head = (head+1)%cap</text>
  <text x="80" y="386" class="label">Обнуление слота важно для указателей, чтобы сборщик мусора освободил объект.</text>

  <!-- Right: Naive q[1:] leak -->
  <rect x="638" y="92" width="364" height="336" rx="6" class="box-warm"/>
  <text x="820" y="120" text-anchor="middle" class="mono-orange">ПОЧЕМУ НАИВНОЕ q = q[1:] ОПАСНО</text>

  <rect x="662" y="144" width="316" height="92" class="box"/>
  <text x="820" y="172" text-anchor="middle" class="mono">После 1 000 000 Enqueue + Dequeue:</text>
  <text x="820" y="198" text-anchor="middle" class="mono-orange">[ хлам | хлам | ... | 1 элемент ]</text>
  <text x="820" y="222" text-anchor="middle" class="label">ptr ушёл вправо, но старый массив жив</text>

  <rect x="662" y="256" width="316" height="148" class="box"/>
  <text x="820" y="284" text-anchor="middle" class="mono-bold">Два последствия:</text>
  <text x="680" y="314" class="mono">1. Память «мёртвых» слотов слева</text>
  <text x="680" y="336" class="mono">   никогда не возвращается.</text>
  <text x="680" y="366" class="mono">2. cap уменьшается и постоянно</text>
  <text x="680" y="388" class="mono">   вызывает новые аллокации.</text>
'''
    },
    {
        "dir": "sources/6. Вводный курс структур данных и алгоритмов",
        "filename": "hash-table-buckets-collisions.svg",
        "w": 1040, "h": 460,
        "title": "ХЕШ-ТАБЛИЦА ИЗНУТРИ: ХЕШ-ФУНКЦИЯ, БАКЕТЫ И КОЛЛИЗИИ",
        "subtitle": "Преобразование строкового ключа в индекс корзины за O(1) и разрешение совпадений индексов",
        "caption": "Устройство хеш-таблицы: отображение ключей через hash(key) % N в массив бакетов и обработка коллизий",
        "alt": "Схема работы хеш-таблицы с вычислением хеш-кода, массивом бакетов и разрешением коллизии двух ключей",
        "body": '''
  <!-- Left: Keys & Hash Function -->
  <rect x="38" y="100" width="240" height="240" rx="6" class="box"/>
  <text x="158" y="128" text-anchor="middle" class="mono-bold">КЛЮЧИ (STRING)</text>
  <rect x="58" y="148" width="200" height="44" class="box-accent"/><text x="158" y="175" text-anchor="middle" class="mono-blue">"go"</text>
  <rect x="58" y="206" width="200" height="44" class="box-warm"/><text x="158" y="233" text-anchor="middle" class="mono-orange">"cli"</text>
  <rect x="58" y="264" width="200" height="44" class="box-warm"/><text x="158" y="291" text-anchor="middle" class="mono-orange">"web"  (коллизия!)</text>

  <!-- Hash Box -->
  <rect x="330" y="150" width="210" height="140" rx="6" class="box-dark"/>
  <text x="435" y="182" text-anchor="middle" class="mono-bold">hash(key) % 4</text>
  <text x="435" y="214" text-anchor="middle" class="mono-blue">"go"  → индекс 1</text>
  <text x="435" y="242" text-anchor="middle" class="mono-orange">"cli" → индекс 3</text>
  <text x="435" y="270" text-anchor="middle" class="mono-orange">"web" → индекс 3</text>

  <line x1="258" y1="170" x2="326" y2="205" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="258" y1="228" x2="326" y2="236" class="line-orange" marker-end="url(#arrowOrange)"/>
  <line x1="258" y1="286" x2="326" y2="266" class="line-orange" marker-end="url(#arrowOrange)"/>

  <!-- Right: Buckets -->
  <rect x="595" y="96" width="407" height="252" rx="6" class="box"/>
  <text x="798" y="124" text-anchor="middle" class="mono-blue">МАССИВ БАКЕТОВ (N = 4)</text>

  <rect x="615" y="140" width="90" height="40" class="box-dark"/><text x="660" y="165" text-anchor="middle" class="mono">[0] пусто</text>
  <rect x="615" y="190" width="90" height="40" class="box-accent"/><text x="660" y="215" text-anchor="middle" class="mono-blue">[1]</text>
  <rect x="725" y="190" width="125" height="40" class="box"/><text x="787" y="215" text-anchor="middle" class="mono-bold">"go": 42</text>

  <rect x="615" y="240" width="90" height="40" class="box-dark"/><text x="660" y="265" text-anchor="middle" class="mono">[2] пусто</text>
  <rect x="615" y="290" width="90" height="40" class="box-warm"/><text x="660" y="315" text-anchor="middle" class="mono-orange">[3]</text>
  <rect x="725" y="290" width="120" height="40" class="box-warm"/><text x="785" y="315" text-anchor="middle" class="mono-bold">"cli": 7</text>
  <rect x="862" y="290" width="122" height="40" class="box-warm"/><text x="923" y="315" text-anchor="middle" class="mono-bold">"web": 19</text>

  <line x1="540" y1="210" x2="612" y2="210" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="540" y1="255" x2="612" y2="308" class="line-orange" marker-end="url(#arrowOrange)"/>
  <line x1="705" y1="210" x2="723" y2="210" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="705" y1="310" x2="723" y2="310" class="line-orange" marker-end="url(#arrowOrange)"/>
  <line x1="845" y1="310" x2="860" y2="310" class="line-orange" marker-end="url(#arrowOrange)"/>

  <!-- Bottom note -->
  <rect x="38" y="366" width="964" height="64" rx="6" class="box-dark"/>
  <text x="58" y="394" class="mono-bold">ПЕРЕХЕШИРОВАНИЕ (RESIZE): КОГДА БАКЕТЫ ПЕРЕПОЛНЯЮТСЯ (HIGH LOAD FACTOR), ТАБЛИЦА УДВАИВАЕТСЯ</text>
  <text x="58" y="416" class="label">Поэтому порядок обхода map в Go случаен и при вставке возможен редкий переезд в новый массив бакетов.</text>
'''
    },
    {
        "dir": "sources/6. Вводный курс структур данных и алгоритмов",
        "filename": "btree-disk-pages-vs-bst.svg",
        "w": 1040, "h": 480,
        "title": "BST В ПАМЯТИ ПРОТИВ СТРАНИЧНОГО B-TREE / B+ TREE НА ДИСКЕ",
        "subtitle": "Для 16 миллионов ключей двоичное дерево требует 24 случайных прыжка, а B-Tree с фактором 256 — всего 3 страницы",
        "caption": "Сравнение высоты 24-уровневого BST и 3-уровневого B-Tree/B+ Tree под 4-килобайтные страницы диска (мостик к Тому 2)",
        "alt": "Сравнение глубокого бинарного дерева BST и плоского страничного B+ Tree с цепочкой листьев для 16 миллионов записей",
        "body": '''
  <!-- Left: Tall BST -->
  <rect x="38" y="92" width="320" height="356" rx="6" class="box-warm"/>
  <text x="198" y="120" text-anchor="middle" class="mono-orange">БИНАРНОЕ ДЕРЕВО (BST)</text>
  <text x="198" y="142" text-anchor="middle" class="label">1 ключ в узле · log₂(16M) = 24 уровня</text>

  <circle cx="198" cy="178" r="18" class="box"/><text x="198" y="183" text-anchor="middle" class="mono-bold">50</text>
  <circle cx="138" cy="230" r="18" class="box"/><text x="138" y="235" text-anchor="middle" class="mono">25</text>
  <circle cx="258" cy="230" r="18" class="box"/><text x="258" y="235" text-anchor="middle" class="mono">75</text>
  <circle cx="100" cy="282" r="18" class="box"/><text x="100" y="287" text-anchor="middle" class="mono">10</text>
  <circle cx="176" cy="282" r="18" class="box"/><text x="176" y="287" text-anchor="middle" class="mono">35</text>
  <line x1="184" y1="191" x2="152" y2="216" class="line"/><line x1="212" y1="191" x2="244" y2="216" class="line"/>
  <line x1="126" y1="244" x2="110" y2="266" class="line"/><line x1="150" y1="244" x2="166" y2="266" class="line"/>
  <text x="198" y="330" text-anchor="middle" class="mono-orange">⋮ ещё 21 прыжок по SSD ⋮</text>

  <rect x="58" y="352" width="280" height="76" class="box"/>
  <text x="198" y="378" text-anchor="middle" class="mono-bold">24 × 100 мкс = 2.4 мс</text>
  <text x="198" y="402" text-anchor="middle" class="label">99% прочитанной страницы 4 КБ</text>
  <text x="198" y="418" text-anchor="middle" class="label">пропадает впустую</text>

  <!-- Right: Wide B+ Tree -->
  <rect x="382" y="92" width="620" height="356" rx="6" class="box-accent"/>
  <text x="692" y="120" text-anchor="middle" class="mono-blue">B-TREE / B+ TREE (УЗЕЛ = СТРАНИЦА 4 КБ · 256 КЛЮЧЕЙ)</text>
  <text x="692" y="142" text-anchor="middle" class="label">Высота = 3 уровня для 256³ = 16 777 216 ключей</text>

  <!-- Root page -->
  <rect x="532" y="162" width="320" height="44" class="box"/>
  <text x="692" y="189" text-anchor="middle" class="mono-bold">Корень: [ ... | 30 | ... | 70 | ... ]</text>

  <line x1="590" y1="206" x2="495" y2="250" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="692" y1="206" x2="692" y2="250" class="line-blue" marker-end="url(#arrowBlue)"/>
  <line x1="794" y1="206" x2="889" y2="250" class="line-blue" marker-end="url(#arrowBlue)"/>

  <!-- Leaf pages linked -->
  <rect x="404" y="254" width="180" height="58" class="box"/>
  <text x="494" y="280" text-anchor="middle" class="mono-bold">Лист 1: [10 | 20]</text>
  <text x="494" y="300" text-anchor="middle" class="label">ключи &lt; 30</text>

  <rect x="602" y="254" width="180" height="58" class="box-warm"/>
  <text x="692" y="280" text-anchor="middle" class="mono-orange">Лист 2: [40|50|60]</text>
  <text x="692" y="300" text-anchor="middle" class="label">диапазон 30..70</text>

  <rect x="800" y="254" width="180" height="58" class="box"/>
  <text x="890" y="280" text-anchor="middle" class="mono-bold">Лист 3: [80 | 90]</text>
  <text x="890" y="300" text-anchor="middle" class="label">ключи &gt; 70</text>

  <!-- Linked list pointers between leaves (B+ Tree) -->
  <line x1="584" y1="283" x2="600" y2="283" class="line-orange" marker-end="url(#arrowOrange)"/>
  <line x1="782" y1="283" x2="798" y2="283" class="line-orange" marker-end="url(#arrowOrange)"/>

  <rect x="404" y="336" width="576" height="92" class="box"/>
  <text x="424" y="364" class="mono-bold">1. Внутри страницы — slices.BinarySearch (~15 нс в L1-кэше).</text>
  <text x="424" y="390" class="mono-bold">2. В B+ Tree листья сшиты в цепочку — быстрые выборки диапазонов.</text>
  <text x="424" y="414" class="label">Подробнее о страницах и индексах БД — в Томе 2 «Базы данных».</text>
'''
    },

    # -----------------------------------------------------------------------
    # МОДУЛЬ 7 (2 схемы)
    # -----------------------------------------------------------------------
    {
        "dir": "sources/7. Первый реальный HTTP-бэкенд на Go",
        "filename": "http-middleware-onion.svg",
        "w": 1040, "h": 460,
        "title": "ЦЕПОЧКА MIDDLEWARE ВОКРУГ HTTP.HANDLER («ЛУКОВИЦА»)",
        "subtitle": "Запрос проходит слои снаружи внутрь (RequestID → Logging → Recover → ServeMux → Handler), а ответ — обратно",
        "caption": "Прохождение HTTP-запроса и ответа через цепочку middleware с записью статуса ответа в statusRecorder",
        "alt": "Схема прохождения HTTP-запроса и ответа через вложенные слои middleware RequestID, Logging, Recover и ServeMux",
        "body": '''
  <!-- Concentric layer boxes -->
  <rect x="38" y="92" width="964" height="336" rx="10" class="box"/>
  <text x="58" y="120" class="mono-blue">1. RequestIDMiddleware (ставит X-Request-ID в r.Context() и заголовок ответа)</text>

  <rect x="78" y="134" width="884" height="274" rx="10" class="box-dark"/>
  <text x="98" y="160" class="mono-bold">2. LoggingMiddleware (оборачивает w в statusRecorder, замеряет time.Since(start), пишет в log/slog)</text>

  <rect x="118" y="174" width="804" height="214" rx="10" class="box-warm"/>
  <text x="138" y="200" class="mono-orange">3. RecoverMiddleware (defer recover() — превращает неожиданную панику в 500 JSON)</text>

  <rect x="158" y="214" width="724" height="154" rx="10" class="box-accent"/>
  <text x="178" y="240" class="mono-blue">4. http.ServeMux Go 1.22+ (сопоставляет "GET /api/v1/bookmarks/{id}" → Handler)</text>

  <rect x="238" y="256" width="564" height="90" rx="8" class="box"/>
  <text x="520" y="288" text-anchor="middle" class="mono-bold">5. Бизнес-обработчик (BookmarksHandler)</text>
  <text x="520" y="314" text-anchor="middle" class="mono">r.PathValue("id") → Service → Store → writeJSON(w, 200, data)</text>
  <text x="520" y="334" text-anchor="middle" class="label">Если паники не было — статус 200 фиксируется в statusRecorder на обратном пути</text>

  <!-- Request IN / Response OUT arrows -->
  <line x1="20" y1="295" x2="234" y2="295" class="line-blue" marker-end="url(#arrowBlue)"/>
  <text x="125" y="286" text-anchor="middle" class="mono-blue">Запрос ──▶</text>

  <line x1="806" y1="305" x2="1018" y2="305" class="line-orange" marker-end="url(#arrowOrange)"/>
  <text x="915" y="294" text-anchor="middle" class="mono-orange">◀── Ответ</text>
'''
    },
    {
        "dir": "sources/7. Первый реальный HTTP-бэкенд на Go",
        "filename": "docker-multistage-build.svg",
        "w": 1040, "h": 440,
        "title": "МНОГОЭТАПНАЯ СБОРКА DOCKERFILE ДЛЯ HTTP-СЕРВИСА НА GO",
        "subtitle": "Компилятор и исходники остаются на этапе сборки; в рабочий образ попадает один статический бинарник без оболочки",
        "caption": "Многоэтапная сборка Docker для BookmarkFlow: перенос статического бинарника из образа golang:1.24-alpine в distroless/static:nonroot",
        "alt": "Схема многоэтапной сборки Dockerfile: из этапа builder с компилятором Go копируется только бинарник в distroless",
        "body": '''
  <!-- Stage 1: Builder -->
  <rect x="38" y="96" width="420" height="310" rx="6" class="box-dark"/>
  <text x="248" y="126" text-anchor="middle" class="mono-bold">ЭТАП 1: BUILDER (golang:1.24-alpine · ~250 МБ)</text>

  <rect x="62" y="146" width="372" height="54" class="box"/>
  <text x="248" y="170" text-anchor="middle" class="mono">COPY go.mod ./  &amp;&amp;  COPY . .</text>
  <text x="248" y="190" text-anchor="middle" class="label">Исходники проекта и компилятор Go</text>

  <rect x="62" y="216" width="372" height="72" class="box-accent"/>
  <text x="248" y="242" text-anchor="middle" class="mono-blue">RUN CGO_ENABLED=0 GOOS=linux \\</text>
  <text x="248" y="266" text-anchor="middle" class="mono-bold">go build -o /out/bookmarkflow ./cmd/server</text>

  <rect x="62" y="304" width="372" height="78" class="box-warm"/>
  <text x="248" y="334" text-anchor="middle" class="mono-orange">Всё лишнее отбрасывается!</text>
  <text x="248" y="358" text-anchor="middle" class="label">Компилятор, кэш и исходники НЕ едут в прод</text>

  <!-- Copy arrow -->
  <line x1="458" y1="252" x2="578" y2="252" class="line-blue" marker-end="url(#arrowBlue)"/>
  <text x="518" y="236" text-anchor="middle" class="mono-blue">COPY --from=builder</text>
  <text x="518" y="274" text-anchor="middle" class="mono-sm">1 файл (~9 МБ)</text>

  <!-- Stage 2: Runtime -->
  <rect x="582" y="96" width="420" height="310" rx="6" class="box-accent"/>
  <text x="792" y="126" text-anchor="middle" class="mono-blue">ЭТАП 2: FINAL (distroless/static:nonroot · ~12 МБ)</text>

  <rect x="606" y="146" width="372" height="76" class="box"/>
  <text x="792" y="176" text-anchor="middle" class="mono-bold">/usr/local/bin/bookmarkflow</text>
  <text x="792" y="202" text-anchor="middle" class="label">Единый автономный статический ELF-файл</text>

  <rect x="606" y="238" width="372" height="72" class="box-dark"/>
  <text x="792" y="264" text-anchor="middle" class="mono">USER nonroot:nonroot · EXPOSE 8080</text>
  <text x="792" y="288" text-anchor="middle" class="mono">ENTRYPOINT ["/usr/local/bin/bookmarkflow"]</text>

  <rect x="606" y="326" width="372" height="56" class="box"/>
  <text x="792" y="352" text-anchor="middle" class="mono-blue">Нет bash/sh, пакетного менеджера и компилятора</text>
  <text x="792" y="370" text-anchor="middle" class="label">Минимальная поверхность атаки и быстрый старт</text>
'''
    },
]


def main() -> int:
    assert len(DIAGRAMS) == 31, f"Expected 31 diagrams, got {len(DIAGRAMS)}"
    for item in DIAGRAMS:
        target_dir = os.path.join(ROOT, item["dir"])
        media_dir = os.path.join(target_dir, "media")
        os.makedirs(media_dir, exist_ok=True)
        svg_path = os.path.join(media_dir, item["filename"])
        svg_text = wrap_svg(item["w"], item["h"], item["title"], item["subtitle"], item["body"])
        ET.fromstring(svg_text)  # Validate well-formed XML
        with open(svg_path, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(svg_text)

        sz = image_size(svg_path)
        assert sz == (item["w"], item["h"]), f"Size mismatch for {svg_path}: {sz}"

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
        rel = os.path.relpath(svg_path, ROOT)
        print(f"OK: {rel} ({sz[0]}x{sz[1]}, {len(svg_text) / 1024:.1f} КБ, path_len={len(rel)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
