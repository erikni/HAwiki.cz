# Šablona pro projekt

Git je vždy hostovaný na GitHub.com. Před použitím této šablony doplňte následující čtyři údaje: 
- uživatele nebo organizaci na GitHubu
- název repozitáře
- produkční URL webu
- URL review/preview webu. 


## Kontext repozitáře

- **Uživatel nebo organizace na GitHubu:** `{{GITHUB_USERNAME}}`
- **Název repozitáře:** `{{REPOSITORY_NAME}}`
- **URL repozitáře:** `https://github.com/{{GITHUB_USERNAME}}/{{REPOSITORY_NAME}}`
- **URL issue:** `https://github.com/{{GITHUB_USERNAME}}/{{REPOSITORY_NAME}}/issues/<číslo-issue>`
- **Produkční URL webu:** `{{SITE_URL}}`
- **URL review/preview webu nebo její vzor:** `{{PREVIEW_URL}}`

Ostatní informace o projektu zjistěte z repozitáře a jeho metadat na GitHubu. Ověřte výchozí větev (pokud neni zadana je to "main", existující issues, README a související dokumentaci, nastavení buildu a testů, CI workflows, konfiguraci nasazení a dostupná nastavení hostingu. Produkční a review/preview URL i příkazy pro nasazení ověřte podle konfigurace a dokumentace. Chybějící URL, příkazy ani hranice prostředí neodhadujte; vyžádejte si chybějící údaj, až když je potřebný pro danou úlohu.

## Issues, větve a commity

- Před změnou souborů založte GitHub Issue (pokud jiz neni zalozene) pro **každou implementační úlohu**. Zaznamenejte požadovaný výsledek a ověřitelná akceptační kritéria. Pokud pokračujete v již evidované úloze, použijte odpovídající existující issue.
- Odkazy na issues sestavujte z uživatele nebo organizace na GitHubu, názvu repozitáře a čísla issue: `https://github.com/{{GITHUB_USERNAME}}/{{REPOSITORY_NAME}}/issues/<číslo-issue>`.
- Feature větev pojmenujte `feature/<číslo-issue>-<stručný-popis>`.
- Číslo issue uveďte v každém commit message, například `feat: add vehicle filter (#123)`.
- Změny posílejte pouze do feature větve přiřazené k danému issue. Číslo issue uvádějte také v průběžných zprávách o postupu.

## Pull requesty a schvalování mergů

- Po implementaci a ověření změn ve feature větvi vytvořte pull request do produkční větve repozitáře. Použijte výchozí větev, pokud dokumentace nebo konfigurace nasazení neurčuje jinou produkční větev. K vytvoření PR není potřeba samostatné schválení uživatelem.
- V názvu nebo popisu PR uveďte související issue. Pokud PR dané issue řeší, použijte `Closes #<číslo-issue>`.
- V PR popište změnu a uveďte výsledky ověření.
- Před mergem **každého** pull requestu do produkční větve si vyžádejte výslovné schválení uživatele. Předchozí žádost o implementaci nebo publikaci ani souhlas s vytvořením PR neopravňuje k mergi nebo zapnutí automatického mergování.
- Před žádostí o schválení předložte konkrétní PR, související issue, výsledky ověření a skutečnou review/preview URL.

## Nasazení review/preview

- Před žádostí o schválení mergu nasaďte feature větev do review/preview prostředí nakonfigurovaného pro projekt.
- Postup nasazení a URL review/preview zjistěte z dokumentace repozitáře, konfigurace nasazení a nastavení hostingu. Ověřte, že nasazená stránka odpovídá feature větvi a je podle modelu dané platformy oddělená od produkčního provozu a produkčních dat či zdrojů.
- Jakmile je review/preview nasazené a ověřené, zveřejněte jeho **skutečnou URL** na všech těchto místech:
  - v popisu pull requestu;
  - jako komentář k souvisejícímu GitHub Issue;
  - v závěrečném výstupu AI agenta v chatu.
- Pokud nasazení selže nebo nelze ověřit URL či oddělení od produkce, jasně to uveďte. Netvrďte, že je review/preview připravené ke kontrole, a nežádejte o schválení mergu.
- K vytvoření review/preview nepoužívejte příkaz pro produkční nasazení, pokud nakonfigurovaná platforma výslovně nezaručuje, že tím nelze změnit produkční provoz.

## Ověření

- Příkazy pro build a ověření zjistěte z README, konfigurace balíčků a nástrojů, CI workflows nebo jiné relevantní dokumentace projektu.
- Po změnách zdrojového kódu, obsahu, strukturovaných dat nebo build nástrojů spusťte příslušné příkazy pro build a ověření. Užší kontroly použijte pouze tehdy, pokud dokumentovaný postup projektu potvrzuje, že pro danou změnu postačují.
- U změn pouze v dokumentaci podle situace posuďte, zda je build nebo ověřovací příkaz relevantní, a uveďte, co jste spustili.
- Opravte chyby způsobené změnou a příslušné kontroly spusťte znovu. Nezávislé nebo nevyřešené chyby popište; netvrďte, že ověření prošlo.
- Před žádostí o schválení mergu zkontrolujte, že PR obsahuje výsledky ověření a skutečnou review/preview URL.

## Ověření produkčního nasazení

- Zjistěte, zda se produkce nasazuje automaticky po mergi, nebo zda je potřeba samostatný zdokumentovaný krok. Postupujte podle procesu nasazení v repozitáři; nepředpokládejte, že souhlas s mergem opravňuje také k samostatnému ručnímu nasazení do produkce.
- Po dokončení nasazení zkontrolujte `{{SITE_URL}}` a změněné funkce. Uveďte výsledek kontroly živého webu, případné selhání nasazení a omezení ověření.

## Konvence specifické pro projekt

- Z dokumentace a existujícího kódu zjistěte a zachovávejte zavedenou architekturu projektu, soubory, které jsou hlavním zdrojem pravdy, formáty obsahu, pojmenování a relevantní implementační postupy.
- Dokumentaci projektu konzultujte, pokud se týká úlohy. Před každou změnou nevyžadujte čtení nesouvisejících dokumentů.
