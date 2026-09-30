from pathlib import Path
import sys, json, html, shutil
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.vendor'))
import markdown,yaml
OUT=ROOT/'dist'; OUT.mkdir(exist_ok=True)
CONFIG=json.loads((ROOT/'site.json').read_text())
SITE_URL=CONFIG['url'].rstrip('/')
E=html.escape
sections={'zaciname':('Začínáme','Váš první krok k pohodlnější domácnosti.'),'co-chci-usnadnit':('Co chci usnadnit','Vyberte si podle běžného života.'),'co-koupit':('Co koupit','Nejdřív potřeba, potom nákup.'),'navody':('Návody','Malé kroky s konkrétním výsledkem.'),'pomoc':('Pomoc','Když něco nefunguje, začněte tady.'),'dalsi-moznosti':('Další možnosti','Rozšíření pro váš další krok.')}
pages=[]
for p in sorted((ROOT/'obsah').rglob('*.md')):
 _,front,body=p.read_text().split('---',2);meta=yaml.safe_load(front)
 for key in ('title','description','cas','obtiznost'): assert key in meta,p
 slug=p.relative_to(ROOT/'obsah').with_suffix('').as_posix()
 md=markdown.Markdown(extensions=['toc','tables','fenced_code','admonition'])
 content=md.convert(body)
 pages.append(dict(meta,slug=slug,body=content,toc=md.toc))
nav=''.join(f'<a href="/{k}/">{v[0]}</a>' for k,v in list(sections.items())[:5])
def shell(title,description,body,route):
 return f'''<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · HAwiki.cz</title><meta name="description" content="{E(description,quote=True)}"><link rel="canonical" href="{SITE_URL}/{route + '/' if route else ''}"><meta name="theme-color" content="#18bcf2"><link rel="stylesheet" href="/assets/style.css"><link rel="icon" href="/assets/favicon.svg"><script src="/assets/search.js" defer></script></head><body><a class="skip" href="#obsah">Přejít k obsahu</a><header><a class="brand" href="/"><span class="logo">⌂</span>HAwiki<span class="brand-light">.cz</span></a><nav aria-label="Hlavní navigace">{nav}</nav><a class="search-link" href="/hledani/">Hledat ↗</a></header><main id="obsah">{body}</main><footer><div><a class="brand" href="/">⌂ HAwiki.cz</a><p>Home Assistant srozumitelně. Pro české a slovenské domácnosti.</p></div><div><a href="/dalsi-moznosti/">Další možnosti a HACS</a><p>Nezávislý průvodce. Není oficiálním webem Home Assistant.</p></div></footer></body></html>'''
def write(route,title,desc,body):
 p=OUT/route/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(shell(title,desc,body,route))
def cards(items):
 return '<div class="cards">'+''.join(f'<a class="card" href="/{p["slug"]}/"><span class="eyebrow">{E(p["obtiznost"])} · {E(p["cas"])}</span><h3>{E(p["title"])}</h3><p>{E(p["description"])}</p><span class="read">Přečíst průvodce <span>↗</span></span></a>' for p in items)+'</div>'
for p in pages:
 section=p['slug'].split('/')[0]
 body=f'''<div class="article-head"><div class="crumb"><a href="/">Domů</a> / <a href="/{section}/">{sections[section][0]}</a></div><span class="eyebrow">{E(p['obtiznost'])} · {E(p['cas'])}</span><h1>{E(p['title'])}</h1><p class="intro">{E(p['description'])}</p><p class="review">Kontrola zdrojů: {E(p['kontrola_zdroju'])} · {E(p['stav'])}</p></div><div class="article-layout"><article>{p['body']}</article><aside><strong>V tomto článku</strong>{p['toc']}<div class="aside-tip">Začněte jednou věcí.<br>Další přidáte, až bude fungovat.</div></aside></div>'''
 write(p['slug'],p['title'],p['description'],body)
for key,(title,desc) in sections.items():
 write(key,title,desc,f'<section class="section-head"><span class="eyebrow">PRŮVODCE DOMÁCNOSTÍ</span><h1>{title}</h1><p class="intro">{desc}</p></section>'+cards([p for p in pages if p['slug'].startswith(key+'/')]))
write('', 'Chytrá domácnost začíná jedním krokem','Praktický průvodce Home Assistant pro běžné domácnosti.', '''<section class="hero"><div><span class="eyebrow">HOME ASSISTANT PRO KAŽDÉHO</span><h1>Méně starostí.<br>Více <em>pohodlí doma.</em></h1><p class="intro">Světla, která myslí na vás. Jednodušší ovládání. Začněte jednou malou změnou — provedeme vás krok za krokem.</p><div class="actions"><a class="button" href="/zaciname/co-je-home-assistant/">Chci začít od nuly <span>→</span></a><a class="text-link" href="/navody/">Prohlédnout návody ↗</a></div><p class="small">Česky a srozumitelně · Vlastním tempem</p></div><div class="house" aria-label="Ilustrace večerního pohodlí doma" role="img"><div class="roof"></div><div class="room"><div class="window"><i></i></div><div class="lamp"></div><div class="sofa"></div><div class="plant">❧</div><div class="floor"></div></div><div class="house-note"><span class="status-dot"></span>19:00 · Lampa se rozsvítila</div><span class="illustration-label">Malé změny. Příjemnější den.</span></div></section><section class="start-strip"><span class="number">01</span><div><strong>Nemusíte měnit celou domácnost.</strong><p>Jedna lampa a jednoduché pravidlo jsou dobrý začátek.</p></div><a href="/navody/lampa-vecer/">Vyzkoušet první návod →</a></section><section><div class="section-title"><div><span class="eyebrow">OD NÁPADU K PRVNÍMU VÝSLEDKU</span><h2>Začněte právě tady</h2></div><a href="/zaciname/">Vše pro začátečníky ↗</a></div>'''+cards([p for p in pages if p['slug'].startswith('zaciname/')])+'''</section><section class="practical"><div class="section-title"><div><span class="eyebrow">UŽITEČNÉ V BĚŽNÉM ŽIVOTĚ</span><h2>Co vám doma pomůže?</h2></div></div>'''+cards([p for p in pages if p['slug'] in ['co-chci-usnadnit/svetla','navody/lampa-vecer','pomoc/zalohovani']])+'''</section><section class="help-banner"><div><h2>Zasekli jste se?</h2><p>Projdeme spolu nejběžnější příčiny. Od těch nejjednodušších.</p></div><a class="button" href="/pomoc/">Najít pomoc →</a></section>''')
write('hledani','Hledání','Najděte návod podle toho, co potřebujete.', '<section class="section-head"><span class="eyebrow">NAJDĚTE SVOU ODPOVĚĎ</span><h1>S čím potřebujete pomoci?</h1><label for="query">Hledat v článcích</label><input type="search" id="query" placeholder="Například lampa, záloha nebo první spuštění"><p id="count" role="status"></p><div id="results"></div><noscript>Pro hledání zapněte JavaScript. Všechny články jsou dostupné přes hlavní menu.</noscript></section>')
(OUT/'search.json').write_text(json.dumps([{k:p[k] for k in ('title','description','slug')} for p in pages],ensure_ascii=False))
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
print(f'Vytvořeno {len(pages)+len(sections)+2} HTML stránek.')
