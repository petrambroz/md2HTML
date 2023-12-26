# Zápočtový program – převod MarkDownu do HTML

## Úvod

Program řeší zdánlivě jednoduchý problém: ze souboru s textem naformátovaným v MarkDownu vytvoří plnohodnotný soubor HTML, který je zobrazitelný webovým prohlížečem. 

### Vstup programu
Program příjmá jeden soubor *nazev_souboru.md* a z něj vytvoří sloubor *output.html*. Název souboru je konfigurovatelný a pokud jde o platný textový soubor, není nutné dodržet příponu .md, nicméně pro přehlednost to je vřele doporučeno. Kódování souboru je vyžadováno utf-8.

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

## Informace pro programátory

### Rozdělení do modulů

Program je vhodně rozdělen do tří hlavních souborů. V kořenovém adresáři se nachází soubor `main.py`, který slouží ke spuštění celého programu. Ten načte nastavení ze souboru `settings.json` a předá je jako parametry k vytvoření objektu třídy `Runner`. Poté je volána funkce `run()`, funkcí `make_file()` je vytvořen nový prázdný soubor a `save_file()` uloží zpracovaná data.

#### runner.py

Tento soubor, který je obsažen v modulu `src` obsahuje hlavní část programu. V jeho konstruktoru je načten text z MarkDown souboru, jsou uůpženy proměnné později použité k nastavení jazyka, názvu dokumentu (html tag "title"), počet mezer označující odsazený blok.

##### funkce `run()`

Hlavní částí je funkce `run()`, která postupně prochází načtený soubor řádek po řádku a každý řádek zpracuje. 

Prvně se testuje, zda je aktuální řádek prázdný – pak jsou "ukončeny" veškeré předchozí rozpracované bloky formátování (seznamy, odstavec, citace), jsou náležtě zprácovány funcí třídy `Convertor` a přidány k výstupu.

Dále se testuje, zda je na řádku horizontální separátor. Poté zda řádek označuje začátek či konec bloku kódu.

Řádek 229 zkouší, zda řádek začíná vykřičníkem a pokud ano, je pomocí regulárního výrazu zjištěno, zda zbytek řádku odpovídá syntaxi vložení obrázku. Pokud ano, je opět regulárním výrazem z řádku načten zvlášť název a odkaz na obrázek, což je potom předáno funkci třídy `Convertor` a přidáno k výstupu.

Řádky 238-274 zkouší, zda je aktuální řádek nějaký seznam a podle jeho úrovně je přidán do patřičné proměnné. Ještě předtím je však pomocí metody `lists()` provedeno zpracování všech předchozích, ještě neukončených částí seznamu.

Pokud se řádek nevyznačuje ničím speciálním, je přidán k aktuálnímu odstavci.