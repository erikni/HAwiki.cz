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

Šablonu článku najdete v `sablony/navod.md`. Vzhled a vyhledávání jsou v `assets/`. Zdrojové HTML šablony společného rozložení, článků, karet a rozcestníků jsou v `sablony/`; nejde o vygenerované stránky. Jejich naplnění obsahem zajišťuje `build.py`. Po úpravě znovu spusťte sestavení. Hlavní stránka používá zvolený seznam článků; nové články se automaticky objeví v příslušné sekci a vyhledávání.

Vyhledávání používá malý JavaScript a neodesílá dotazy na server. Bez JavaScriptu zůstává navigace a čtení článků funkční.

## Obsahová omezení první verze

Deset úvodních článků vychází z odkazované dokumentace. Postupy nebyly vyzkoušeny na fyzickém zařízení. Produktová srovnání, ceny pro ČR/SR, fotografie kroků a další praktické scénáře vyžadují doplnění a ověření. Web je česky; samostatná slovenská verze zatím není součástí.

## Doména a barvy

Cílová adresa je https://www.hawiki.cz a je nastavena v `site.json`. Generátor ji používá v kanonických adresách jednotlivých stránek. DNS a hosting musí být připojeny samostatně. Produkční hosting bude Cloudflare Pages; původní Sites náhled slouží pouze k prohlížení rozpracované verze.

Hlavní barva je Home Assistant modrá `#18BCF2`; textové odkazy používají tmavší `#0879A6` pro lepší čitelnost. Zdroj palety: https://github.com/home-assistant/frontend/blob/dev/src/resources/theme/color/core.globals.ts

## Zdrojový repozitář

https://github.com/erikni/HAwiki.cz obsahuje pouze zdroje, Markdown články a podklady. `dist/` s hotovým HTML, stažené knihovny `.vendor/` a lokální hostingové nastavení se do něj nenahrávají.

## Cloudflare Pages

Projekt: `hawiki-cz`. Připojte repozitář `erikni/HAwiki.cz` přes Git integration.

| Nastavení | Hodnota |
| --- | --- |
| Production branch | `main` |
| Framework preset | `None` |
| Root directory | kořen repozitáře (prázdné pole) |
| Build command | `sh build-cloudflare.sh` |
| Build output directory | `dist` |
| Python | `3.13.3` přes `.python-version` |

Sestavení nainstaluje knihovny, převede Markdown do HTML a zkontroluje místní odkazy. Při chybě skončí s nenulovým návratovým kódem. Výstup zůstává mimo Git; Pages ho vytvoří při každém nasazení.

V projektu Pages otevřete **Custom domains** a připojte `www.hawiki.cz` podle průvodce Cloudflare. Samotná hodnota v `site.json` nenastavuje DNS. Pro doménu bez `www` lze samostatně nastavit přesměrování na `https://www.hawiki.cz`.

Pokud je existující `hawiki-cz` projektem Workers, tato nastavení se na něj nevztahují: použijte skutečný projekt Pages. Dashboardová adresa obsahující `/workers/services/view/` sama o sobě nepotvrzuje typ projektu.

Dokumentace: https://developers.cloudflare.com/pages/get-started/git-integration/ a https://developers.cloudflare.com/pages/configuration/build-image/

## Kontrola Python skriptů

Funkce v `build.py` a `check.py` mají dokumentaci a standardní formátování. Oba skripty lze bezpečně importovat; sestavení a kontrola se spustí pouze při jejich přímém spuštění.

```sh
python3 -m pip install pylint
python3 -m pylint build.py check.py
```
