"""Generate self-contained animated SVG cards for a GitHub README."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
ASSETS.mkdir(parents=True,exist_ok=True)
STYLE='''text{font-family:Arial,Helvetica,sans-serif}.float{animation:float 6s ease-in-out infinite}.pulse{animation:pulse 4s ease-in-out infinite}.orbit{transform-box:fill-box;transform-origin:center;animation:orbit 12s linear infinite}@keyframes float{50%{transform:translateY(-7px)}}@keyframes pulse{50%{opacity:.4}}@keyframes orbit{to{transform:rotate(360deg)}}@media(prefers-reduced-motion:reduce){.float,.pulse,.orbit{animation:none}}'''
def svg(w,h,title,body,color):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#111b2e"/><stop offset="1" stop-color="#080e1c"/></linearGradient><linearGradient id="accent" x2="1" y2="1"><stop stop-color="{color}"/><stop offset="1" stop-color="#27364f"/></linearGradient></defs><style>{STYLE}</style><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="url(#bg)" stroke="#26324a"/>{body}</svg>\n'''
def tx(x,y,body,size=20,color='#b8c6dc',weight=400,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(body)}</text>'
def art(kind,c):
    if kind=='voice':
        bars=''.join(f'<rect x="{25+i*16}" y="{105-v/2}" width="7" height="{v}" rx="4" fill="{c}" opacity="{.4+(i%3)*.25}"/>' for i,v in enumerate([22,42,64,36,80,106,70,42,78,52,30,18]))
        return f'<g class="float"><rect x="4" y="20" width="224" height="162" rx="22" fill="#101d2c" stroke="#2a5060"/>{tx(23,48,"VOICE → ORDER",12,c,600)}{bars}{tx(23,163,"AI / FASTAPI / WEBSOCKETS",9,"#7995ac")}</g>'
    if kind=='commerce':
        return f'<g class="float"><path d="M28 61 102 28 166 65 92 101Z" fill="#65538c" stroke="{c}"/><path d="M28 61V150L92 188V101Z" fill="#25223e" stroke="#6e5e9a"/><path d="M92 101V188L166 151V65Z" fill="#3e325c" stroke="#8676b5"/><path d="M65 43 133 81V127" fill="none" stroke="{c}" stroke-width="5"/><rect x="154" y="23" width="63" height="31" rx="9" fill="#241f38" stroke="#806bb1"/>{tx(163,44,"SHOP",14,c,600)}</g>'
    if kind=='school':
        return f'<g class="float"><rect x="7" y="18" width="220" height="177" rx="17" fill="#152025" stroke="#35544b"/>{tx(26,48,"SCHOOL ERP",14,c,600)}'+''.join(f'<rect x="24" y="{62+i*38}" width="186" height="28" rx="7" fill="#1c2f32"/><circle cx="39" cy="{76+i*38}" r="4" fill="{c}"/>{tx(54,81+i*38,s,13,"#bdd7d4")}' for i,s in enumerate(['Admissions','Results','Parent portal']))+'</g>'
    if kind=='portfolio':
        return f'<g class="float"><rect x="28" y="37" width="195" height="150" rx="16" fill="#17263a" stroke="#466381"/><rect x="9" y="18" width="195" height="150" rx="16" fill="#101d2e" stroke="{c}"/><path d="M10 48H203" stroke="#466381"/><circle cx="25" cy="33" r="3" fill="{c}"/><circle cx="37" cy="33" r="3" fill="#7892b2"/><circle cx="49" cy="33" r="3" fill="#7892b2"/>{tx(27,100,"SVJ",35,c,700)}{tx(28,126,"DESIGN × CODE",10,"#b8c6dc",600)}<path d="M131 80 153 66 176 80 153 94Z M131 80V109L153 123 176 109V80 M153 94V123" fill="#23445b" stroke="{c}" stroke-width="1.5"/></g>'
    return f'<g class="float"><ellipse cx="113" cy="175" rx="88" ry="13" fill="#2c2630"/><path d="M27 66 61 28H164L204 66 114 169Z" fill="#392d38" stroke="{c}" stroke-width="2"/><path d="M27 66H204M61 28 84 66 114 169 142 66 164 28M84 66 111 28 142 66" fill="none" stroke="{c}" stroke-width="1.5"/><circle class="pulse" cx="204" cy="45" r="4" fill="{c}"/></g>'
PROJECTS=[
('roboserve','01','RoboServe AI','voice','#79dfff','Conversational ordering, from voice to kitchen.','Menus, sessions, carts and order tracking.','PYTHON · FASTAPI · WEBSOCKETS · GEMINI'),
('savvora','02','SAVVORA','commerce','#bca1ff','An e-commerce system from catalog to checkout.','Products, orders, inventory and administration.','FASTAPI · SUPABASE · POSTGRESQL'),
('school-erp','03','School ERP','school','#bce891','A connected workspace for school operations.','Admissions, results, fees and a parent portal.','REACT · TYPESCRIPT · FIREBASE · TAILWIND'),
('chinni-jewels','04','Chinni Jewels','jewels','#ebc29e','A storefront made for a jewellery business.','Product discovery, WhatsApp orders and admin.','HTML · CSS · JAVASCRIPT · SUPABASE'),
('portfolio','05','Interactive Portfolio','portfolio','#96c9ff','A personal space for projects and experiments.','Animated interfaces, case studies and interactions.','HTML · CSS · JAVASCRIPT · RESPONSIVE UI')]
for slug,n,title,kind,color,d1,d2,stack in PROJECTS:
    for mobile in (False,True):
        w,h=(640,465) if mobile else (1100,238)
        body=tx(32,38,f'{n} / SELECTED PROJECT',11,color,600,'letter-spacing="2"')
        body+=tx(31,85,title,38,'#f3f7ff',700)
        body+=tx(33,119,d1,17 if mobile else 19)
        body+=tx(33,148,d2,17 if mobile else 19)
        body+=tx(33,182,stack,10 if mobile else 12,color,600,'letter-spacing=".4"')
        body+=f'<g transform="translate({206 if mobile else 826} {219 if mobile else 10})">{art(kind,color)}</g>'
        if not mobile:body+=tx(34,212,'VIEW REPOSITORY  ↗',10,'#7e92b0',600,'letter-spacing="1.6"')
        (ASSETS/f'project-{slug}{"-mobile" if mobile else ""}.svg').write_text(svg(w,h,f'{title}. {d1} {d2} {stack}',body,color))

body=tx(34,42,'BUILD. CONNECT. IMPROVE.',26,'#f3f7ff',700)+tx(35,75,'From a business problem to a working product.',16)
body+=tx(994,58,'SVJ',30,'#79dfff',700)
(ASSETS/'footer.svg').write_text(svg(1100,109,'Build. Connect. Improve. — Savvani Venkata Jaswanth',body,'#79dfff'))
(ASSETS/'divider.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="24" viewBox="0 0 1100 24"><defs><linearGradient id="l"><stop stop-color="#79dfff"/><stop offset=".5" stop-color="#bca1ff"/><stop offset="1" stop-color="#bce891"/></linearGradient></defs><path d="M0 12H1100" stroke="url(#l)" opacity=".45"/></svg>\n')

# Keep the smaller contact button consistent with the existing contact row.
(ASSETS/'resume.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="132" height="36" viewBox="0 0 132 36" role="img" aria-labelledby="title"><title id="title">Read my résumé (PDF)</title><rect x=".5" y=".5" width="131" height="35" rx="9" fill="#142935" stroke="#2c5465"/><path d="M17 11v11m-4-4 4 4 4-4m-9 7h10" fill="none" stroke="#79dfff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><text x="33" y="23" fill="#edf2f8" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="600">Résumé PDF</text></svg>\n''')

ACHIEVEMENTS=[
    ('TOP 2.8%', 'Meta PyTorch OpenEnv', 'Nationwide hackathon', '#79dfff'),
    ('FINALIST', 'IIT Madras E-Summit', '2026 · AI automation platform', '#bca1ff'),
    ('1ST PLACE', 'GNOSIS 2025', 'AI / GenAI paper presentation', '#bce891'),
]
for mobile in (False,True):
    w,h=(640,710) if mobile else (1100,340)
    body=tx(32,39,'BEYOND THE CODE',12,'#79dfff',600,'letter-spacing="2"')
    body+=tx(31,78,'Ideas tested. Work recognised.',29 if mobile else 32,'#f3f7ff',700)
    for i,(result,event,detail,color) in enumerate(ACHIEVEMENTS):
        x,y=(32,109+i*145) if mobile else (32+i*348,109)
        cw,ch=(576,126) if mobile else (340,134)
        body+=f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="15" fill="#142036" stroke="#293952"/>'
        body+=tx(x+20,y+42,result,30,color,700)
        body+=tx(x+20,y+76,event,19,'#f3f7ff',600)
        body+=tx(x+20,y+103,detail,15)
    if mobile:
        body+=tx(33,580,'PayTM Ideathon 2026',20,'#f3f7ff',600)
        body+=tx(33,607,'Designed an AI-powered business solution.',17)
        body+=tx(33,652,'Microsoft Global Fabric Days 2026',20,'#f3f7ff',600)
        body+=tx(33,679,'Learning across data, analytics and cloud.',17)
    else:
        body+=tx(34,281,'PayTM Ideathon 2026',18,'#f3f7ff',600)
        body+=tx(34,310,'Designed an AI-powered business solution.',15)
        body+=tx(565,281,'Microsoft Global Fabric Days 2026',18,'#f3f7ff',600)
        body+=tx(565,310,'Learning across data, analytics and cloud.',15)
    title='Achievements: Meta PyTorch OpenEnv top 2.8% nationwide; IIT Madras E-Summit 2026 finalist; GNOSIS 2025 first place; PayTM Ideathon 2026 solution; Microsoft Global Fabric Days 2026 learning.'
    (ASSETS/f'achievements{"-mobile" if mobile else ""}.svg').write_text(svg(w,h,title,body,'#79dfff'))

for mobile in (False,True):
    w,h=(640,150) if mobile else (1100,102)
    body=f'<circle class="pulse" cx="36" cy="34" r="5" fill="#bce891"/>'
    body+=tx(51,39,'OPEN TO OPPORTUNITIES',11,'#bce891',600,'letter-spacing="1.6"')
    if mobile:
        body+=tx(31,83,'Python Backend, Full-Stack and AI roles',23,'#f3f7ff',600)
        body+=tx(31,121,'Bengaluru · Junior developer & internships',19)
    else:
        body+=tx(31,76,'Python Backend, Full-Stack and AI opportunities in Bengaluru.',24,'#f3f7ff',600)
        body+=tx(784,38,'JUNIOR DEVELOPER / INTERNSHIPS',10,'#b8c6dc',600,'letter-spacing=".7"')
    (ASSETS/f'hiring{"-mobile" if mobile else ""}.svg').write_text(svg(w,h,'Open to Python Backend, Full-Stack and AI opportunities in Bengaluru. Junior developer and internship roles.',body,'#bce891'))

# A two-column toolkit keeps labels legible on narrow screens.
body=''
for i,(label,icon,color) in enumerate([
    ('Python','Py','#f0c987'),('FastAPI','API','#69f0c2'),
    ('SQL','SQL','#96c9ff'),('React','UI','#87def5'),
    ('Supabase','DB','#78e5b3'),('AI integration','AI','#b3a6ff')]):
    x,y=12+(i%2)*314,12+(i//2)*152
    body+=f'<g transform="translate({x} {y})"><rect width="302" height="140" rx="15" fill="#11182a" stroke="#28324b"/><g class="float"><rect x="123" y="21" width="56" height="48" rx="14" fill="#1c273e"/>{tx(151,53,icon,22,color,600,"text-anchor=\"middle\"")}</g>{tx(151,107,label,21,"#e3eaf4",500,"text-anchor=\"middle\"")}</g>'
(ASSETS/'stack-mobile.svg').write_text(svg(640,468,'Core tools: Python, FastAPI, SQL, React, Supabase, and AI integration.',body,'#79dfff'))

body=tx(30,46,'BUILD. CONNECT. IMPROVE.',28,'#f3f7ff',700)
body+=tx(31,84,'From a business problem to a working product.',20)
body+=tx(31,128,'SAVVANI VENKATA JASWANTH',12,'#79dfff',600,'letter-spacing="2"')
(ASSETS/'footer-mobile.svg').write_text(svg(640,155,'Build. Connect. Improve. — Savvani Venkata Jaswanth',body,'#79dfff'))
print('Built ten project cards, responsive achievements, hiring, toolkit and footer assets, plus the résumé button.')
