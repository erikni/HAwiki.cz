# Šablona pro nasazení do Cloudflare Workers

Tento dokument popisuje obecný postup pro nasazení statického webu do Cloudflare Workers. Před použitím doplňte následující projektové údaje:

- uživatele nebo organizaci na GitHubu;
- název repozitáře;
- produkční URL webu;
- URL nebo vzor review/preview webu;
- název produkčního Cloudflare Workeru.

## Kontext projektu

- **GitHub:** `https://github.com/{{GITHUB_USERNAME}}/{{REPOSITORY_NAME}}`
- **Produkční URL:** `{{SITE_URL}}`
- **URL nebo vzor preview:** `{{PREVIEW_URL}}`
- **Cloudflare Worker:** `{{CF_WORKER_URI}}`

Hodnoty mohou být uvedeny v projektovém `AGENTS.md`. Správný název proměnné pro náhled je `PREVIEW_URL`. Wildcard nebo vzor nepovažujte za skutečnou URL konkrétního nasazení.

## Ověření konfigurace

Před prvním nasazením zjistěte z repozitáře a Cloudflare:

- umístění Wrangler konfigurace;
- adresář s vygenerovanými statickými aktivy;
- podporovanou verzi Node.js a Wrangleru;
- příkaz pro sestavení a všechny povinné kontroly;
- Cloudflare účet, ve kterém existuje `{{CF_WORKER_URI}}`;
- způsob připojení produkčních domén;
- zda jsou pro Worker povolené Workers Previews nebo Version URLs.

Chybějící hodnoty, příkazy, názvy Workerů ani hranice prostředí neodhadujte. Wrangler konfigurace má být zdrojem pravdy pro název Workeru a adresář statických aktiv.

## Přihlašovací údaje

API tokeny, refresh tokeny a jiné přihlašovací údaje nepatří do Git repozitáře ani do `AGENTS.md`.

Pro automatické nasazení používejte GitHub repository secrets. Token omezte na nezbytný Cloudflare účet a minimální oprávnění potřebná pro konkrétní nasazení. Veřejné identifikátory lze uchovávat v konfiguraci nebo jako GitHub variables.

Pro ruční přihlášení lze použít:

```sh
npx wrangler login
npx wrangler whoami
```

Před změnou Cloudflare vždy ověřte, že přihlášený účet obsahuje Worker `{{CF_WORKER_URI}}`.

## Sestavení a kontrola

Před preview i produkčním nasazením:

1. sestavte web dokumentovaným příkazem projektu;
2. spusťte kontroly lokálních odkazů, statických souborů a metadat;
3. ověřte SEO, canonical URL a strukturovaná data, pokud je web používá;
4. zkontrolujte, že vygenerovaný adresář neobsahuje staré soubory z předchozího sestavení.

Při chybě nepokračujte v nasazení. Výsledky kontrol uveďte v pull requestu.

## Review/preview nasazení

Před schválením mergu vytvořte oddělené preview, které nemění produkční provoz. Použijte projektový preview workflow nebo zdokumentovaný příkaz odpovídající aktuální verzi Wrangleru, například:

```sh
npx wrangler preview --name pr-<číslo-PR>
```

Příkaz i jeho kompatibilitu ověřte podle Wrangler konfigurace a aktuální dokumentace Cloudflare. Pokud projekt používá Version URLs místo Workers Previews, použijte odpovídající zdokumentovaný postup a jasně uveďte, zda preview sdílí produkční resources.

Po nasazení ověřte, že konkrétní URL:

- odpovídá projektu a očekávanému vzoru `{{PREVIEW_URL}}`;
- obsahuje změny z příslušné feature větve;
- není produkční URL `{{SITE_URL}}`;
- nezměnila produkční provoz ani produkční data.

Skutečnou preview URL uveďte v popisu pull requestu, v komentáři souvisejícího issue a v odpovědi uživateli. Pokud preview nelze vytvořit nebo ověřit, nežádejte o schválení mergu.

Preview workflow nespouštějte pro nedůvěryhodné forky způsobem, který by jim zpřístupnil repository secrets.

## Produkční nasazení

Produkční nasazení proveďte pouze z aktuální schválené produkční větve. Nejdříve ověřte, zda se produkce nasazuje automaticky po mergi, nebo vyžaduje samostatný ruční krok.

Výslovné schválení mergu samo o sobě neopravňuje k ručnímu produkčnímu nasazení, pokud projektový postup nebo uživatel neurčí jinak.

Pokud je schválené ruční nasazení a Wrangler konfigurace je ověřeným zdrojem pravdy, obvyklý příkaz je:

```sh
npx wrangler deploy
```

Příkaz `deploy` nepoužívejte pro review/preview. Před spuštěním znovu ověřte cílový účet, Worker `{{CF_WORKER_URI}}`, produkční větev a obsah sestavení.

## Ověření produkce

Úspěšný výstup nasazovacího příkazu sám o sobě nepotvrzuje správné nasazení. Na `{{SITE_URL}}` ověřte alespoň:

1. HTTP stav změněných URL;
2. viditelný titulek a očekávaný obsah;
3. změněné obrázky a další statické soubory;
4. canonical URL, Open Graph a strukturovaná data;
5. důležité stránky, které změna neměla ovlivnit.

Výsledek, konkrétní produkční URL a případná omezení ověření zaznamenejte do souvisejícího issue. Push nebo úspěšný workflow run nejsou samy o sobě potvrzením funkční produkce.

## Návrat k předchozí verzi

Při chybě zastavte další nasazování a zjistěte poslední ověřenou funkční verzi:

```sh
npx wrangler deployments list --name {{CF_WORKER_URI}}
```

Rollback proveďte přes Cloudflare Dashboard nebo aktuálním dokumentovaným příkazem Wrangleru pro konkrétní ověřené ID verze. ID verze nekopírujte z jiného Workeru a neodhadujte je.

Po rollbacku znovu ověřte `{{SITE_URL}}` a výsledek zaznamenejte do issue.

## Povinné odkazy

Před zavedením nebo změnou procesu ověřte aktuální dokumentaci:

- https://developers.cloudflare.com/workers/static-assets/
- https://developers.cloudflare.com/workers/previews/
- https://developers.cloudflare.com/workers/versions-and-deployments/
- https://github.com/cloudflare/wrangler-action
