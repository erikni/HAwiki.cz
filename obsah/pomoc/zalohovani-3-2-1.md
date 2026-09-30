---
title: "Zálohování 3–2–1: tři kopie pro klidnější domácnost"
description: "Jednoduchý plán, jak nepřijít o nastavení Home Assistant při poruše zařízení nebo problému doma."
cas: "10 minut čtení"
obtiznost: "Snadné"
kontrola_zdroju: "2026-09-30"
stav: "Podle dokumentace; bez ověření na zařízení"
---

## Proč nestačí záloha přímo v Home Assistant

Máte nastavená světla, topení a oblíbená tlačítka. Pak se porouchá zařízení, na kterém Home Assistant běží. Pokud na něm byla i jediná záloha, nemusíte se k ní dostat.

Metoda **3–2–1** pomáhá rozložit toto riziko: mít více kopií, oddělit jejich úložiště a jednu uchovat mimo domácnost.

## Co znamenají čísla 3–2–1

| Číslo | Význam | Příklad pro domácnost |
| --- | --- | --- |
| **3** | Tři kopie důležitých dat celkem | Fungující Home Assistant a dvě záložní kopie |
| **2** | Dva různé druhy úložišť | Úložiště zařízení a samostatný záložní disk; další kopie může být v cloudu |
| **1** | Jedna kopie mimo domov | Šifrovaná kopie v cloudu nebo disk uložený na jiné adrese |

**Běžící systém se počítá jako první kopie.** Nemusíte tedy vytvářet tři další zálohy. Zároveň tři soubory na jednom disku nesplňují tento plán: porucha disku zasáhne všechny.

## Příklad: Home Assistant, domácí disk a cloud

Představte si tuto sestavu:

1. **Home Assistant Green** obsahuje vaše aktuální nastavení.
2. **Samostatný domácí disk nebo síťové úložiště** uchovává zálohy. Síťové úložiště, označované NAS, je krabička s disky dostupná po domácí síti.
3. **Cloudové úložiště** drží další záložní kopii mimo domácnost.

Když selže Green, pomůže domácí kopie. Když problém zasáhne celou domácnost, využijete kopii mimo domov. Při výběru ověřte, že jde o oddělená úložiště; dvě složky na stejném zařízení nejsou dvě nezávislá místa.

Cloud není povinný. Kopii můžete uchovávat také na odpojeném externím disku mimo domov. V takovém případě si nastavte připomínku, abyste ji pravidelně obnovovali.

## Jak začít v Home Assistant

Pokud ještě zálohy nemáte, projděte nejprve [základní návod na zálohování](../zalohovani/).

Následující postup je určený pro Home Assistant OS. Dostupná úložiště se mohou lišit podle instalace a připojených služeb.

1. Otevřete **Nastavení → Systém → Zálohy**.
2. Nastavte automatické zálohování, například každý den.
3. Přidejte nebo připojte podporované záložní úložiště podle jeho dokumentace.
4. V nastavení automatických záloh zapněte požadovaná umístění, včetně kopie mimo domov.
5. Uložte **nouzovou sadu se šifrovacím klíčem** bezpečně mimo samotné zařízení Home Assistant.
6. Vytvořte zálohu a zkontrolujte, že dorazila do vybraných míst.

Názvy tlačítek se mohou podle verze a jazyka mírně lišit. Kopie mimo domov musí být dostupná také v případě, že svůj Home Assistant vůbec nespustíte.

## Kolik starších záloh uchovávat?

Počet míst a počet starších verzí jsou dvě různé věci. Metoda 3–2–1 řeší rozložení kopií; starší verze vám umožní vrátit se před chybu, které jste si všimli až později.

Jako vlastní výchozí plán můžete zvolit **sedm denních záloh** a samostatnou kopii před větší změnou. Počet upravte podle volného místa a toho, jak často nastavení měníte. Ověřte pravidla každého úložiště: Home Assistant Cloud podle aktuální dokumentace uchovává pouze poslední zálohu.

## Šifrovací klíč patří k záloze

Šifrovanou zálohu lze obnovit jen s příslušným klíčem. Uložte nouzovou sadu například do správce hesel, ke kterému se dostanete i bez Home Assistant. Klíč nezveřejňujte.

Pozor na ručně stažené soubory: při stažení přes stránku záloh Home Assistant se záloha podle dokumentace dešifruje. Takový soubor nenahrávejte do veřejné složky; chcete-li ho uchovat šifrovaný, použijte vhodné zabezpečené úložiště nebo jej samostatně zašifrujte.

## Jak poznáte, že plán funguje?

Jednou za čas si položte tyto otázky:

- Vidím čerstvou zálohu na odděleném úložišti?
- Dostanu se ke kopii mimo domov, i když Home Assistant neběží?
- Mám dostupný odpovídající klíč a přihlašovací údaje?
- Vím, které části domácnosti záloha zahrnuje?

Skutečné ověření je zkušební obnova na náhradním zařízení. Obnovený systém nejprve držte oddělený od skutečných zařízení domácnosti, aby nezačal současně spouštět stejná pravidla. Obnovu na běžícím domácím systému neprovádějte jen na zkoušku: přepsala by jeho nastavení.

## Nejčastější omyly

- **„Mám tři zálohy na jednom disku.“** Pomohou při návratu ke starší verzi, ale nepomohou při poruše tohoto disku.
- **„NAS je mimo Home Assistant, takže je mimo domov.“** Stále může být zasažený stejnou událostí jako zbytek domácnosti.
- **„Automatické zálohy už nemusím kontrolovat.“** Úložiště může být nedostupné nebo plné.
- **„Soubor zálohy znamená, že zvládnu obnovu.“** Potřebujete také přístup k souboru, klíč a použitelný postup obnovy.

## Zdroje a další čtení

- [Home Assistant: vysvětlení pravidla 3–2–1](https://www.home-assistant.io/blog/2025/01/03/3-2-1-backup/)
- [Aktuální dokumentace záloh a obnovy](https://www.home-assistant.io/common-tasks/general/)
- [Náš základní návod na zálohování](../zalohovani/)
