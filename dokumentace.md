# Zápočtový program – převod MarkDownu do HTML

## Úvod

Program řeší zdánlivě jednoduchý problém: ze souboru s textem naformátovaným v MarkDownu vytvoří plnohodnotný soubor HTML, který je zobrazitelný webovým prohlížečem. 

## Vstup programu
Program příjmá jeden soubor *nazev_souboru.md* a z něj vytvoří sloubor *output.html*. Název souboru je konfigurovatelný a pokud jde o platný textový soubor, není nutné dodržet příponu .md, nicméně pro přehlednost to je vřele doporučeno.

Jediným požadavkem na vstupní soubor je jeho platné naformátování, jelikož program je poměrně striktní a jakékoliv i drobné "nesrovnalosti" může vyhodnotit špatně. Platným formátováním se rozumí:

1. Úpravy textu na úrovni řádku (**tučné písmo**, *kurzíva*, ...)
    * každý počátek formátovaného úseku musí být ukončen (a to stejným znakem)
        * `*text*` – toto je platné
        * `_text*` – toto platné není
        * `*text` – toto také není platné
2. Číslované a nečíslované seznamy
    * v celém MarkDown dokumentu musí být dodržen jednotný styl odsazení (je konfigurovatelný)
        * odsazení je provedeno pomocí mezer, a to ve stanovených násobcích (doporučuje se používat 2 nebo 4)
    * prázdná řádek mezi jednotlivými seznamy vytvoří seznamy oddělené (nový element ol či ul)
    * číslované a nečíslované seznamy lze kombinovat, avšak na jedné úrovní smí být pouze jeden druh (nemohou se střídat číslované a nečíslované řádky se stejným odsazením)
3. Odstavce
    * prázdný řáddek označuje odstavec
4. Nadpisy
    * je podporováno 6 úrovní napisů – `# nadpis 1`, `## nadpis 2` atd.
        * pokud je v souboru nadpis úrovně 7 nebo více, program ohlásí výjimku a ukončí se
    * nadpis muže mít své "id" – `## nadpis {#id}`
        * to může být použité např. pro vytvoření odkazu (kotvy) na tento nadpis
        * id není zobrazeno, slouží pouze pro odkazování

