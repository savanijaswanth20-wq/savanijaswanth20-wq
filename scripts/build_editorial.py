#!/usr/bin/env python3
"""Build original, self-contained SVG panels for Jaswanth's GitHub profile.

Python standard library only. Display lettering uses licensed Barlow Condensed
outlines so GitHub renders it consistently without requesting a web font.
The avatar is the owner's unchanged public GitHub photograph. All motion is CSS
and has a prefers-reduced-motion fallback; no script or remote assets are used.
"""

import base64
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOURCE = ASSETS / "editorial-source"
OWNER = "savanijaswanth20-wq"
BG, PANEL, LINE = "#070c18", "#101c30", "#243a59"
WHITE, MUTED, BLUE, SKY, CORAL = "#f3f6ff", "#a1b2cd", "#247bff", "#8fc1ff", "#ff4c68"
DISPLAY = json.loads((SOURCE / "display-glyphs.json").read_text())
PHOTO = base64.b64encode((ASSETS / "profile-avatar.jpg").read_bytes()).decode()

STYLE = """text{font-family:Arial,Helvetica,sans-serif}
.mono{font-family:'Courier New',monospace}
.float{animation:float 7s ease-in-out infinite}
.orbit{transform-box:fill-box;transform-origin:center;animation:orbit 28s linear infinite}
.reverse{animation-direction:reverse;animation-duration:36s}
.pulse{animation:pulse 3.5s ease-in-out infinite}
.signal{animation:signal 2.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
.scan{stroke-dasharray:24 76;animation:scan 8s linear infinite}
.swing{transform-box:fill-box;transform-origin:50% 0;animation:swing 8s ease-in-out infinite}
@keyframes float{50%{transform:translateY(-8px)}}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes pulse{50%{opacity:.45}}
@keyframes signal{50%{transform:scaleY(.55)}}
@keyframes scan{to{stroke-dashoffset:-100}}
@keyframes swing{25%{transform:rotate(1deg)}75%{transform:rotate(-1deg)}}
@media(prefers-reduced-motion:reduce){.float,.orbit,.reverse,.pulse,.signal,.scan,.swing{animation:none}.scan{stroke-dasharray:none}}
"""


def text(x, y, value, size=22, color=MUTED, weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" {extra}>{escape(str(value))}</text>')


def label(x, y, value, color=MUTED, size=13):
    return text(x, y, value, size, color, 700, 'class="mono" letter-spacing="1.3"')


def heading(x, y, value, size=80, color=WHITE, max_width=None):
    units = DISPLAY["units"]
    glyphs = DISPLAY["glyphs"]
    advance = sum(glyphs[c]["advance"] for c in value)
    if max_width:
        size = min(size, max_width * units / advance)
    parts, offset = [], 0
    for character in value:
        glyph = glyphs[character]
        if glyph["path"]:
            parts.append(f'<path transform="translate({offset} 0)" d="{glyph["path"]}"/>')
        offset += glyph["advance"]
    scale = size / units
    return (f'<g fill="{color}" transform="translate({x} {y}) scale({scale:.5f} {-scale:.5f})" '
            f'aria-label="{escape(value, quote=True)}">{"".join(parts)}</g>')


def rect(x, y, width, height, fill=PANEL, stroke=LINE, radius=14, extra=""):
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'rx="{radius}" fill="{fill}" stroke="{stroke}" {extra}/>')


def slashes(x, y, color=CORAL):
    return f'<path d="M{x} {y}l-8 18h8l8-18zm14 0l-8 18h8l8-18zm14 0l-8 18h8l8-18z" fill="{color}"/>'


def top(number, title, width):
    return label(36, 42, f"{number} / {title}") + slashes(width - 74, 26)


def svg(width, height, title, description, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs>
 <radialGradient id="blue-glow"><stop stop-color="#153b7f" stop-opacity=".65"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>
 <radialGradient id="red-glow"><stop stop-color="#702638" stop-opacity=".35"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>
 <linearGradient id="card" x2="1" y2="1"><stop stop-color="#152b49"/><stop offset="1" stop-color="#0d1728"/></linearGradient>
 <linearGradient id="cube" x2="1" y2="1"><stop stop-color="#428dff"/><stop offset="1" stop-color="#174783"/></linearGradient>
 <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#244365"/></pattern>
 <clipPath id="panel"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="24"/></clipPath>
</defs>
<style>{STYLE}</style>
<g clip-path="url(#panel)">
 <rect width="{width}" height="{height}" fill="{BG}"/>
 <ellipse cx="{int(width*.79)}" cy="{int(height*.43)}" rx="{int(width*.43)}" ry="{int(height*.65)}" fill="url(#blue-glow)"/>
 <ellipse cx="{width}" cy="{height}" rx="{int(width*.42)}" ry="{int(height*.60)}" fill="url(#red-glow)"/>
 <rect width="{width}" height="{height}" fill="url(#dots)" opacity=".4"/>
 {body}
</g>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="24" fill="none" stroke="{LINE}"/>
</svg>\n'''


def portrait(x, y, diameter, rings=True):
    identifier = f"photo-{x}-{y}-{diameter}"
    center = diameter / 2
    orbit = ""
    if rings:
        orbit = f'''<g class="orbit"><circle cx="{center}" cy="{center}" r="{center+24}" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="180 350"/><circle cx="{center}" cy="-24" r="5" fill="{CORAL}"/></g>
        <g class="orbit reverse"><circle cx="{center}" cy="{center}" r="{center+39}" fill="none" stroke="#244365" stroke-dasharray="7 10"/></g>'''
    return f'''<g transform="translate({x} {y})">
    <defs><clipPath id="{identifier}"><circle cx="{center}" cy="{center}" r="{center-2}"/></clipPath></defs>
    {orbit}<circle cx="{center}" cy="{center}" r="{center}" fill="{PANEL}" stroke="{SKY}" stroke-width="2"/>
    <image x="0" y="0" width="{diameter}" height="{diameter}" href="data:image/jpeg;base64,{PHOTO}" clip-path="url(#{identifier})"/>
    </g>'''


def chip(x, y, width, value, color=SKY):
    return rect(x, y, width, 36, "#122642", "#294b77", 7) + label(x + 13, y + 24, value, color, 12)


def hero(mobile=False):
    w, h = (600, 1010) if mobile else (1200, 640)
    body = top("SVJ", "PYTHON + AI DEVELOPER", w)
    body += f'<path d="M36 65H{w-36}" stroke="{LINE}"/>'
    body += label(36, 108 if mobile else 113, "HELLO, I'M", SKY, 16)
    body += heading(36, 172, "SAVVANI VENKATA", 58 if mobile else 63, max_width=528 if mobile else 740)
    body += heading(32, 299 if mobile else 318, "JASWANTH", 136 if mobile else 166, SKY, 534 if mobile else 768)
    body += text(36, 344 if mobile else 364, "Python Backend & AI Developer", 26 if mobile else 31, WHITE, 700)
    body += text(36, 392 if mobile else 416, "APIs. Business applications.", 23 if mobile else 25)
    body += text(36, 426 if mobile else 452, "Practical AI. Built with purpose.", 23 if mobile else 25)
    if mobile:
        body += portrait(154, 509, 292)
        body += label(300, 866, "TIRUPATI, INDIA", SKY, 14).replace('font-weight="700"', 'font-weight="700" text-anchor="middle"')
        body += chip(66, 893, 144, "PYTHON APIs") + chip(225, 893, 140, "FULL-STACK") + chip(380, 893, 154, "AI SYSTEMS")
        body += label(36, 979, "OPEN TO ROLES IN BENGALURU", CORAL, 14)
    else:
        body += portrait(838, 153, 310)
        body += rect(806, 503, 350, 51, "#102447", "#2f62a6", 9)
        body += slashes(830, 519, BLUE) + label(872, 536, "BACKEND / FULL-STACK / AI", WHITE, 12)
        body += chip(36, 488, 144, "PYTHON APIs") + chip(194, 488, 145, "FULL-STACK") + chip(353, 488, 154, "AI SYSTEMS")
        body += f'<path d="M36 565H1164" stroke="{LINE}"/>'
        body += label(36, 602, "TIRUPATI, INDIA", SKY, 14)
        body += label(350, 602, "ALGONEX IT SOLUTIONS", MUTED, 14)
        body += f'<circle class="pulse" cx="835" cy="597" r="5" fill="{CORAL}"/>'
        body += label(852, 602, "OPEN TO BENGALURU ROLES", WHITE, 13)
    return svg(w, h, "Savvani Venkata Jaswanth — Python Backend & AI Developer", "Python APIs, full-stack business applications and practical AI integrations. Tirupati, India. Python Backend Developer at Algonex IT Solutions. Open to opportunities in Bengaluru.", body)


def terminal(x, y, width):
    body = rect(x, y, width, 205, "#0b1425", LINE, 12)
    body += rect(x, y, width, 32, "#172b48", "none", 12)
    for i, color in enumerate([CORAL, SKY, BLUE]):
        body += f'<circle cx="{x+17+i*13}" cy="{y+16}" r="3" fill="{color}"/>'
    body += text(x+69, y+21, "svj / build / iterate", 12, MUTED, extra='class="mono"')
    body += text(x+20, y+75, "> turn_ideas_into_products()", 18, SKY, extra='class="mono"')
    for i, word in enumerate(["UNDERSTAND", "ENGINEER", "IMPROVE"]):
        xx = x+20+i*(width-30)/3
        card_width = (width-60)/3
        body += rect(round(xx, 1), y+101, round(card_width, 1), 75, "#12233c", CORAL if i==2 else "#2b5484", 7)
        body += heading(xx+12, y+131, f"0{i+1}", 32, CORAL if i==2 else SKY)
        body += label(xx+12, y+159, word, MUTED, 10)
    return body


def about(mobile=False):
    w, h = (600, 1130) if mobile else (1200, 640)
    body = top("01", "FROM IDEA TO WORKING PRODUCT", w)
    body += heading(36, 131, "IDEA TO IMPACT.", 74, max_width=528)
    body += terminal(36, 176, 528)
    rows = [("01", "Python APIs & backend systems", "Routes, data, sessions and business logic."),
            ("02", "Full-stack business applications", "From the interface to the order workflow."),
            ("03", "Practical AI integrations", "Useful tools around real user problems.")]
    for i, (number, title, detail) in enumerate(rows):
        y = 437+i*73
        body += heading(36, y, number, 32, CORAL if i==2 else BLUE)
        body += text(85, y-2, title, 23, WHITE, 700)
        body += text(85, y+27, detail, 19)
    if mobile:
        body += f'<path d="M36 651H564" stroke="{LINE}"/>'
        body += label(36, 700, "BUSINESS THINKING + ENGINEERING", SKY, 13)
        body += heading(36, 790, "GROW THROUGH", 79, max_width=528)
        body += heading(36, 876, "BUILDING.", 96, SKY)
        body += rect(36, 922, 528, 171, "#0e1d34", LINE, 12)
        body += label(60, 957, "EDUCATION / 2026", CORAL)
        body += text(60, 1001, "B.Com (Computers)", 28, WHITE, 700)
        body += text(60, 1038, "Emeralds Degree College", 24)
        body += text(60, 1072, "Learning by building working products.", 22)
    else:
        body += f'<path d="M607 86V598" stroke="{LINE}"/>'
        body += label(647, 104, "BUSINESS THINKING + ENGINEERING", SKY, 13)
        body += heading(646, 182, "GROW THROUGH", 79, max_width=518)
        body += heading(646, 263, "BUILDING.", 95, SKY)
        body += rect(647, 302, 517, 174, "#0e1d34", LINE, 12)
        body += label(671, 337, "CURRENT DIRECTION", CORAL)
        for i, line in enumerate(["Connect a useful interface to a clear API.", "Understand the data behind the workflow.", "Make AI serve an actual business need."]):
            body += text(671, 376+i*34, line, 21, WHITE if i==0 else MUTED)
        body += label(647, 522, "EDUCATION / 2026", SKY)
        body += text(647, 562, "B.Com (Computers)", 28, WHITE, 700)
        body += text(647, 597, "Emeralds Degree College", 22)
    return svg(w, h, "From idea to impact", "I build Python APIs, full-stack business applications and practical AI integrations. B.Com (Computers), Emeralds Degree College, 2026.", body)


def cube(x, y, scale=1):
    icons = [(55, 85, "Py"), (340, 98, "API"), (366, 261, "AI"), (67, 305, "DB")]
    body = '<ellipse cx="205" cy="305" rx="155" ry="28" fill="#0e2041"/>'
    body += '<g class="orbit"><ellipse cx="204" cy="185" rx="184" ry="106" transform="rotate(-28 204 185)" fill="none" stroke="#2866b7"/><circle cx="373" cy="119" r="6" fill="#ff4c68"/></g>'
    body += '<g class="orbit reverse"><ellipse cx="204" cy="185" rx="115" ry="179" transform="rotate(20 204 185)" fill="none" stroke="#24476e" stroke-dasharray="10 8"/></g>'
    body += '<g class="float"><path d="M204 92 300 147 204 202 108 147Z" fill="url(#cube)" stroke="#74afff" stroke-width="2"/><path d="M108 147 204 202V306L108 251Z" fill="#183b72" stroke="#4988de" stroke-width="2"/><path d="M204 202 300 147V251L204 306Z" fill="#102c59" stroke="#4988de" stroke-width="2"/>'
    body += heading(150, 181, "SVJ", 67, WHITE) + '</g>'
    for xx, yy, icon in icons:
        body += f'<circle cx="{xx}" cy="{yy}" r="29" fill="#0f213d" stroke="#315887"/>'
        body += text(xx, yy+7, icon, 20, CORAL if icon=="AI" else SKY, 700, 'text-anchor="middle"')
    return f'<g transform="translate({x} {y}) scale({scale})">{body}</g>'


def stack(mobile=False):
    w, h = (600, 1105) if mobile else (1200, 660)
    body = top("02", "MY ENGINE ROOM", w)
    if mobile:
        body += heading(36, 134, "ENGINEER WITH", 77, max_width=528)
        body += heading(36, 222, "PURPOSE.", 100, SKY)
        body += cube(78, 252, 1.08)
        start_x, start_y, cw, ch, gap = 36, 654, 164, 110, 18
    else:
        body += heading(36, 135, "ENGINEER WITH PURPOSE.", 83, max_width=1128)
        body += label(36, 175, "LANGUAGES / APIs / DATA / INTERFACES", SKY, 14)
        body += cube(66, 239, 1.18)
        body += label(60, 625, "THE TOOLKIT BEHIND THE WORK.", MUTED, 13)
        start_x, start_y, cw, ch, gap = 594, 252, 176, 91, 20
    tools = [("Py", "Python"), ("TS", "TypeScript"), ("SQL", "SQL"),
             ("API", "FastAPI"), ("R", "React"), ("N", "Next.js"),
             ("DB", "Supabase"), ("FB", "Firebase"), ("AI", "Gemini API")]
    for i, (icon, name) in enumerate(tools):
        col, row = i%3, i//3
        x, y = start_x+col*(cw+gap), start_y+row*(ch+33)
        color = CORAL if row==2 and col==2 else SKY
        if not mobile and col==0:
            body += label(x, y-14, ["01 / LANGUAGES", "02 / API + INTERFACE", "03 / DATA + AI"][row], MUTED, 11)
        body += rect(x, y, cw, ch, "#101e33", LINE, 10)
        body += label(x+16, y+29, icon, color, 16)
        body += text(x+16, y+75 if mobile else y+65, name, 23, WHITE, 700)
        body += f'<path class="scan" d="M{x+16} {y+ch-1}h{cw-32}" pathLength="100" stroke="{color}" stroke-width="2"/>'
    if mobile:
        body += label(36, 1081, "CODE / CONNECT / LEARN / REPEAT", MUTED, 12)
    return svg(w, h, "My engineering toolkit", "Python, TypeScript, SQL, FastAPI, React, Next.js, Supabase, Firebase and Gemini API. A dimensional SVJ monogram with moving orbits.", body)


def builder_pass(x, y, width=360):
    scale = width/360
    body = '<path d="M166 -86h28v86h-28z" fill="#173d75" stroke="#477fc4"/>'
    body += label(180, -30, "SVJ / BUILD", SKY, 10).replace('font-weight="700"', 'font-weight="700" text-anchor="middle"')
    body += rect(164, -9, 32, 26, "#b8cbe5", "#d3def0", 7)
    body += rect(0, 0, 360, 483, "url(#card)", "#3d679d", 18)
    body += '<path d="M18 2H342" stroke="#ff4c68" stroke-width="5"/>'
    body += label(24, 39, "SVJ / BUILDER PASS", WHITE, 13)
    body += label(270, 39, "2026", SKY, 12)
    body += rect(147, 12, 66, 6, "#070c18", "none", 3)
    body += portrait(75, 71, 210, rings=False)
    body += chip(24, 302, 312, "PYTHON BACKEND + AI", SKY)
    body += heading(24, 393, "JASWANTH", 68, max_width=312)
    body += label(24, 418, "TIRUPATI / INDIA", SKY, 12)
    for i in range(72):
        bar_width = 1 if i%3 else 2
        body += f'<rect x="{25+i*4.35:.2f}" y="441" width="{bar_width}" height="{13+(i%4)*2}" fill="#9fb9df"/>'
    body += label(24, 474, "PERSONAL PROFILE / GITHUB", MUTED, 9)
    return f'<g transform="translate({x} {y}) scale({scale})"><g class="swing">{body}</g></g>'


def render_dashboard(owner, public_repos, followers, stars, updated=None, mobile=False):
    updated = updated or datetime.now(timezone.utc).strftime("%d %b %Y").upper()
    w, h = (600, 1320) if mobile else (1200, 780)
    body = top("03", "THE PERSON BEHIND THE CODE", w)
    hx, hy = (36, 145) if mobile else (478, 132)
    body += heading(hx, hy, "REAL WORK.", 108 if mobile else 95, max_width=528 if mobile else 686)
    body += heading(hx, hy+82, "VISIBLE PROGRESS.", 73, SKY, 528 if mobile else 686)
    body += label(hx, hy+118, f"PUBLIC SNAPSHOT / {updated}", MUTED, 12)
    values = [(public_repos, "PUBLIC REPOS"), (followers, "FOLLOWERS"), (stars, "ORIGINAL REPO STARS")]
    start_x, start_y, cw = (36, 306, 164) if mobile else (478, 292, 216)
    for i, (value, caption) in enumerate(values):
        x = start_x+i*(cw+18)
        body += rect(x, start_y, cw, 125, "#101e33", LINE, 12)
        body += heading(x+19, start_y+76, f"{int(value):,}", 72, CORAL if i==0 else SKY, cw-38)
        if mobile:
            lines = [("PUBLIC", "REPOS"), ("FOLLOWERS",), ("ORIGINAL", "REPO STARS")][i]
            for j, line in enumerate(lines):
                body += label(x+19, start_y+101+j*17, line, MUTED, 12)
        else:
            body += label(x+19, start_y+106, caption, MUTED, 11)
    if mobile:
        body += builder_pass(120, 552, 360)
        body += label(36, 1105, "PROJECTS / CURRENT FOCUS", SKY, 13)
        body += text(36, 1144, "RoboServe AI", 28, WHITE, 700)
        body += text(36, 1176, "Conversational ordering + Python APIs", 22)
        body += text(36, 1226, "SAVVORA", 28, WHITE, 700)
        body += text(36, 1258, "E-commerce workflows + data", 22)
        body += label(36, 1298, "OPEN TO BACKEND + AI OPPORTUNITIES", CORAL, 12)
    else:
        body += heading(30, 168, "SVJ", 133, "#142e53")
        body += builder_pass(60, 257)
        body += label(478, 462, "PROJECTS / CURRENT FOCUS", SKY, 13)
        projects = [("RoboServe AI", "Conversational ordering / FastAPI / WebSockets"),
                    ("SAVVORA", "E-commerce workflows / FastAPI / Supabase")]
        for i, (name, detail) in enumerate(projects):
            y = 496+i*76
            body += text(478, y, name, 27, WHITE, 700)
            body += text(478, y+29, detail, 20)
            body += f'<path d="M478 {y+43}H1164" stroke="{LINE}"/>'
        body += rect(478, 663, 686, 77, "#12233d", "#2d5386", 12)
        body += label(500, 693, "OPEN TO BACKEND + AI OPPORTUNITIES", CORAL, 13)
        body += text(500, 724, "Tirupati, India / Open to roles in Bengaluru", 21)
    return svg(w, h, f"Jaswanth's builder profile — {updated}", f"GitHub @{owner}: {public_repos} public repositories, {followers} followers, {stars} stars on owned public non-fork repositories. Python Backend and AI Developer. Public snapshot: {updated}. Decorative personal builder pass.", body)


def connect(mobile=False):
    w, h = (600, 740) if mobile else (1200, 580)
    body = top("04", "START A CONVERSATION", w)
    if mobile:
        body += heading(36, 149, "LET'S BUILD.", 100, max_width=528)
        body += heading(36, 228, "SOMETHING USEFUL.", 64, SKY, 528)
        body += text(36, 275, "Ideas. Opportunities. Working products.", 23)
        start_x, start_y, cw = 36, 324, 528
    else:
        body += heading(36, 148, "LET'S", 111)
        body += heading(36, 243, "CONNECT.", 111, SKY)
        body += portrait(139, 304, 199, rings=False)
        body += heading(491, 142, "BUILD SOMETHING USEFUL.", 63, max_width=673)
        body += text(491, 182, "Ideas. Opportunities. Working products.", 23)
        start_x, start_y, cw = 491, 228, 673
    rows = [("01", "LinkedIn", "Connect & exchange ideas"), ("02", "Portfolio", "Explore the projects and interfaces"),
            ("03", "Email", "savanijaswanth20@gmail.com"), ("04", "Resume", "Experience, education and achievements")]
    for i, (number, name, detail) in enumerate(rows):
        y = start_y+i*86
        body += rect(start_x, y, cw, 73, "#101e33", LINE, 10)
        body += f'<path d="M{start_x+1} {y+11}V{y+62}" stroke="{CORAL if i%2 else BLUE}" stroke-width="3"/>'
        body += label(start_x+20, y+32, number, SKY, 15)
        body += text(start_x+63, y+30, name, 25, WHITE, 700)
        body += text(start_x+63, y+57, detail, 18 if mobile else 19)
        body += f'<path d="M{start_x+cw-43} {y+37}h20m-7-7 7 7-7 7" fill="none" stroke="{CORAL if i%2 else BLUE}" stroke-width="2"/>'
    body += label(36, h-27, "CURIOUS BY NATURE. BUILDING WITH PURPOSE.", MUTED, 11)
    return svg(w, h, "Let's build something useful", "Connect with Savvani Venkata Jaswanth through LinkedIn, portfolio, email or résumé. Use the clickable links below this panel.", body)


PROJECTS = [
    ("roboserve", "01", "ROBOSERVE AI", "VOICE TO ORDER", "Menu search, carts, confirmation and kitchen tracking.", "PYTHON / FASTAPI / WEBSOCKETS / GEMINI"),
    ("savvora", "02", "SAVVORA", "COMMERCE WORKFLOWS", "Products, inventory, orders, returns and administration.", "FASTAPI / SUPABASE / POSTGRESQL / NEXT.JS"),
    ("school-erp", "03", "SCHOOL ERP", "SCHOOL OPERATIONS", "Admissions, marks, results, fees and a parent portal.", "REACT / TYPESCRIPT / FIREBASE / TAILWIND"),
]


def project_card(project, mobile=False):
    slug, number, name, category, detail, tools = project
    w, h = (600, 270) if mobile else (1200, 205)
    body = label(36, 39, f"{number} / {category}", SKY, 13)
    body += heading(36, 116, name, 82, max_width=528 if mobile else 950)
    if mobile:
        # Two deliberate lines keep the descriptions readable on a phone.
        descriptions = {"roboserve": ["Menu search, carts, confirmation", "and kitchen tracking."],
                        "savvora": ["Products, inventory, orders, returns", "and administration."],
                        "school-erp": ["Admissions, marks, results, fees", "and a parent portal."]}
        for i, line in enumerate(descriptions[slug]):
            body += text(36, 158+i*30, line, 24)
        body += label(36, 229, tools, MUTED, 11)
    else:
        body += text(36, 155, detail, 25)
        body += label(36, 183, tools, MUTED, 12)
        body += '<path d="M1065 110h64m-21-21 21 21-21 21" fill="none" stroke="#247bff" stroke-width="3"/>'
    return svg(w, h, name.title(), f"{name}: {detail} {tools}. Open the linked repository.", body)


def achievements(mobile=False):
    w, h = (600, 680) if mobile else (1200, 365)
    body = top("05", "WORK RECOGNISED", w)
    body += heading(36, 128, "BEYOND THE CODE.", 79, max_width=w-72)
    items = [("TOP 2.8%", "Meta PyTorch OpenEnv", "Nationwide hackathon"),
             ("FINALIST", "IIT Madras E-Summit 2026", "AI automation platform"),
             ("1ST PLACE", "GNOSIS 2025", "AI / GenAI paper presentation")]
    for i, (result, event, detail) in enumerate(items):
        x, y, cw = (36, 163+i*145, 528) if mobile else (36+i*382, 169, 364)
        body += rect(x, y, cw, 125, "#101e33", LINE, 12)
        body += heading(x+20, y+53, result, 50, CORAL if i==0 else SKY, cw-40)
        body += text(x+20, y+85, event, 22 if mobile else 20, WHITE, 700)
        body += text(x+20, y+112, detail, 19 if mobile else 18)
    if mobile:
        body += text(36, 632, "PayTM Ideathon + Global Fabric Days", 23, WHITE, 700)
        body += text(36, 663, "2026 / AI solution design + continued learning", 21)
    else:
        body += text(36, 340, "PayTM Ideathon 2026 / AI solution design", 20)
        body += text(616, 340, "Global Fabric Days 2026 / Continued learning", 20)
    return svg(w, h, "Experience beyond the code", "Meta PyTorch OpenEnv: top 2.8% nationwide. IIT Madras E-Summit 2026: finalist. GNOSIS 2025: first place for an AI and GenAI paper. PayTM Ideathon 2026: AI solution design. Microsoft Global Fabric Days 2026: learning.", body)


def button(name, caption, width):
    color = CORAL if name=="email" else SKY
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="40" viewBox="0 0 {width} 40" role="img" aria-label="{escape(caption)}"><rect x=".5" y=".5" width="{width-1}" height="39" rx="8" fill="#12243f" stroke="#315889"/><path d="M15 25 25 15m-10 0h10v10" fill="none" stroke="{color}" stroke-width="1.5"/><text x="36" y="26" font-family="Arial,Helvetica,sans-serif" font-size="15" font-weight="700" fill="#f3f6ff">{escape(caption)}</text></svg>\n'''


def build_all(public_repos=23, followers=3, stars=0):
    builders = {"hero": hero, "about": about, "stack": stack, "connect": connect, "achievements": achievements}
    for name, builder in builders.items():
        for mobile in (False, True):
            (ASSETS / f"editorial-{name}{'-mobile' if mobile else ''}.svg").write_text(builder(mobile), encoding="utf-8")
    for project in PROJECTS:
        for mobile in (False, True):
            (ASSETS / f"editorial-project-{project[0]}{'-mobile' if mobile else ''}.svg").write_text(project_card(project, mobile), encoding="utf-8")
    for mobile in (False, True):
        (ASSETS / f"editorial-dashboard{'-mobile' if mobile else ''}.svg").write_text(render_dashboard(OWNER, public_repos, followers, stars, mobile=mobile), encoding="utf-8")
    for name, caption, width in [("portfolio", "Portfolio", 121), ("resume", "Resume PDF", 144), ("linkedin", "LinkedIn", 122), ("email", "Email me", 122)]:
        (ASSETS / f"{name}.svg").write_text(button(name, caption, width), encoding="utf-8")
    print("Built original editorial panels, responsive variants and contact buttons.")


if __name__ == "__main__":
    build_all()
