# Nasazení HAwiki.cz do Cloudflare

Tento dokument popisuje nasazení statického webu HAwiki.cz na Cloudflare Worker. Zdrojový repozitář je `erikni/HAwiki.cz`, produkční Worker se jmenuje `hawiki-cz` a veřejný web běží na `https://www.hawiki.cz`.

## Konfigurace

Společným zdrojem pravdy pro ruční nasazení i GitHub Actions je `wrangler.jsonc`:

- Worker: `hawiki-cz`
- statická aktiva: `dist/`
- vzor preview URL: `*-hawiki-cz.gemini77.workers.dev`
- produkční URL: `https://www.hawiki.cz`

Používané projektové proměnné jsou v `AGENTS.md`. Správný název proměnné pro náhled je `PREVIEW_URL`.

## Požadavky

- Python podle `.python-version`
- Node.js 22 nebo novější
- Wrangler 4.157.0 nebo novější kompatibilní verze
- přístup do Cloudflare účtu s Workerem `hawiki-cz`
- API token s oprávněním upravovat Workers Scripts pro automatické nasazení

API token ani jiné přihlašovací údaje nepatří do Git repozitáře. GitHub Actions používá repository secret `CLOUDFLARE_API_TOKEN`. ID Cloudflare účtu je veřejná hodnota uvedená ve workflow.

## Sestavení a kontrola

Před každým preview i produkčním nasazením spusťte:

```sh
sh build-cloudflare.sh
```

Skript vytvoří `dist/` a zkontroluje lokální odkazy. Pro úplné ověření spusťte také:

```sh
PYTHONPATH=.vendor python3 check_seo.py
```

Při chybě sestavení, odkazů, SEO nebo JSON-LD nepokračujte v nasazení.

## Přihlášení pro ruční nasazení

Interaktivní přihlášení:

```sh
npx wrangler login
npx wrangler whoami
```

Před nasazením ověřte, že přihlášený účet skutečně obsahuje Worker `hawiki-cz`. Název Workeru neodhadujte a nevytvářejte nový Worker s podobným názvem.

## Preview pull requestu

Preview nesmí změnit produkční provoz. Z kořene sestavené feature větve spusťte:

```sh
npx wrangler preview --name pr-<číslo-PR>
```

Wrangler vrátí skutečnou URL preview. Ověřte, že odpovídá vzoru `PREVIEW_URL`, načítá změny z dané větve a neukazuje produkční nebo starší obsah.

Skutečnou URL následně uveďte:

- v popisu pull requestu;
- v komentáři souvisejícího issue;
- v odpovědi uživateli před žádostí o schválení mergu.

GitHub workflow `.github/workflows/preview-cloudflare-workers.yml` provádí stejný postup automaticky pro pull requesty ze stejného repozitáře. U forků se preview nespouští, aby nebyly zpřístupněny secrets.

## Produkční nasazení

Produkční nasazení proveďte pouze z aktuální schválené větve `main` a až po výslovném schválení mergu a případného ručního nasazení uživatelem.

Automatické nasazení z `main` zajišťuje `.github/workflows/deploy-cloudflare-workers.yml`. Pokud je potřeba schválené ruční nasazení, po sestavení spusťte:

```sh
npx wrangler deploy
```

Příkaz `deploy` směruje novou verzi do produkce. Nepoužívejte jej k vytvoření preview.

## Ověření produkce

Úspěšný výstup Wrangleru sám o sobě nepotvrzuje správné nasazení. Po dokončení ověřte alespoň:

1. změněnou produkční URL a její HTTP stav;
2. viditelný titulek a očekávaný obsah;
3. hlavní obrázky a další změněné statické soubory;
4. canonical URL, Open Graph a JSON-LD;
5. že ostatní důležité stránky nadále fungují.

Výsledek a přímou produkční URL zaznamenejte do souvisejícího issue.

## Návrat k předchozí verzi

Pokud nová produkční verze způsobí chybu, zastavte další změny a zjistěte poslední funkční verzi:

```sh
npx wrangler deployments list --name hawiki-cz
```

Rollback proveďte přes Cloudflare Dashboard v přehledu Workeru `hawiki-cz`, případně dokumentovaným příkazem Wrangleru pro konkrétní ověřenou verzi. Po návratu znovu ověřte produkční URL a výsledek zaznamenejte do issue. ID verze vždy zkopírujte z Cloudflare; neodhadujte je.

## Odkazy

- https://developers.cloudflare.com/workers/static-assets/
- https://developers.cloudflare.com/workers/previews/
- https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/
