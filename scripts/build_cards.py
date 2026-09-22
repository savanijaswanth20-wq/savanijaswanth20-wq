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
    return f'<g class="float"><ellipse cx="113" cy="175" rx="88" ry="13" fill="#2c2630"/><path d="M27 66 61 28H164L204 66 114 169Z" fill="#392d38" stroke="{c}" stroke-width="2"/><path d="M27 66H204M61 28 84 66 114 169 142 66 164 28M84 66 111 28 142 66" fill="none" stroke="{c}" stroke-width="1.5"/><circle class="pulse" cx="204" cy="45" r="4" fill="{c}"/></g>'
PROJECTS=[
('roboserve','01','RoboServe AI','voice','#79dfff','Conversational ordering, from voice to kitchen.','Menus, sessions, carts and order tracking.','PYTHON · FASTAPI · WEBSOCKETS · GEMINI'),
('savvora','02','SAVVORA','commerce','#bca1ff','An e-commerce system from catalog to checkout.','Products, orders, inventory and administration.','FASTAPI · SUPABASE · POSTGRESQL'),
('school-erp','03','School ERP','school','#bce891','A connected workspace for school operations.','Admissions, results, fees and a parent portal.','REACT · TYPESCRIPT · FIREBASE · TAILWIND'),
('chinni-jewels','04','Chinni Jewels','jewels','#ebc29e','A storefront made for a jewellery business.','Product discovery, WhatsApp orders and admin.','HTML · CSS · JAVASCRIPT · SUPABASE')]
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
print('Built eight responsive project cards, a footer and a divider.')
