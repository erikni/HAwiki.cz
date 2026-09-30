# HAwiki.cz

Statický český průvodce Home Assistant pro běžné domácnosti.

## Sestavení

```sh
python3 -m pip install --target .vendor -r requirements.txt
python3 build.py
python3 -m http.server 8000 --directory dist
```

Otevřete http://localhost:8000. Výstup v `dist/` lze hostovat jako běžný statický web v kořeni domény. Obsah se nepřipravuje za běhu na serveru.

## Úpravy obsahu

Články jsou v `obsah/`. Adresář a název Markdown souboru určují adresu článku. Každý článek začíná YAML metadaty: title, description, cas, obtiznost, kontrola_zdroju a stav. Nepoužívejte označení „otestováno“, pokud postup nebyl skutečně ověřen na zařízení.

Šablonu článku najdete v `sablony/navod.md`. Vzhled a vyhledávání jsou v `assets/`. Společné rozložení a rozcestníky vytváří `build.py`. Po úpravě znovu spusťte sestavení. Hlavní stránka používá zvolený seznam článků; nové články se automaticky objeví v příslušné sekci a vyhledávání.

Vyhledávání používá malý JavaScript a neodesílá dotazy na server. Bez JavaScriptu zůstává navigace a čtení článků funkční.

## Obsahová omezení první verze

Devět úvodních článků vychází z odkazované dokumentace. Postupy nebyly vyzkoušeny na fyzickém zařízení. Produktová srovnání, ceny pro ČR/SR, fotografie kroků a další praktické scénáře vyžadují doplnění a ověření. Web je česky; samostatná slovenská verze zatím není součástí.

## Doména a barvy

Cílová adresa je https://www.hawiki.cz a je nastavena v `site.json`. Generátor ji používá v kanonických adresách jednotlivých stránek. DNS a hosting musí být připojeny samostatně. Současný Sites náhled zůstává soukromý.

Hlavní barva je Home Assistant modrá `#18BCF2`; textové odkazy používají tmavší `#0879A6` pro lepší čitelnost. Zdroj palety: https://github.com/home-assistant/frontend/blob/dev/src/resources/theme/color/core.globals.ts

## Zdrojový repozitář

https://github.com/erikni/HAwiki.cz obsahuje pouze zdroje, Markdown články a podklady. `dist/` s hotovým HTML, stažené knihovny `.vendor/` a lokální hostingové nastavení se do něj nenahrávají.
