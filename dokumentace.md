# Zápočtový program – převod MarkDownu do HTML

## Obsah
1. [Úvod](#uvod)
2. [Vstup programu](#vstup)
3. [Informace pro programátory](#programatori)
4. [Informace pro uživatele](#uzivatele)
5. [Nastavení](#nastaveni)
6. [Průběh práce](#prace)

## Úvod {#uvod}
Program řeší následující problém: ze souboru s textem naformátovaným v MarkDownu vytvoří plnohodnotný soubor HTML, který je zobrazitelný webovým prohlížečem.

## Vstup programu {#vstup}
Program přijímá jeden soubor *nazev_souboru.md* a z něj vytvoří sloubor *output.html*. Název souboru je konfigurovatelný a pokud jde o platný textový soubor, není nutné dodržet příponu .md, nicméně pro přehlednost to je vřele doporučeno. Výchozí název vstupního souboru je *input.md*. Kódování souboru je vyžadováno utf-8.

Jediným požadavkem na vstupní soubor je jeho platné naformátování, jelikož program je poměrně striktní a jakékoliv i drobné "nesrovnalosti" může vyhodnotit špatně. Platným formátováním se rozumí:

1. Úpravy textu na úrovni řádku (**tučné písmo**, *kurzíva*, ...)
    * každý počátek formátovaného úseku musí být ukončen (a to stejným znakem)
        * `*text*` – toto je platné
        * `_text*` – toto platné není
        * `*text` – toto také není platné (znak `*` se zobrazí)
    * pokud je před kterýmkoli znakem \\, je následující znak zpracován jako běžný (tj. pokud je operátor, je chápán jako běžný znak)
2. Číslované a nečíslované seznamy
    * program podporuje maximálně 4 úrovně odsazení
        * tzn. první "neindentovaný" řádek, poté jednou, dvakrát a třikrát "indentovaný"
    * další řádek může být odsazený pouze o 1 více než předchozí (jednou odsazený řádek může následovat řádek jednou či dvakrát odsazený, ale ne třikrát)
    * v celém MarkDown dokumentu musí být dodržen jednotný styl odsazení (je konfigurovatelný)
        * odsazení je provedeno pomocí mezer, a to ve stanovených násobcích (doporučuje se používat 2 nebo 4)
    * prázdná řádek mezi jednotlivými seznamy vytvoří seznamy oddělené (nový element ol či ul)
        * prázdný řádek musí být i mezi začátkem seznamu a případným předchozím odstavcem či jiným elementem
    * číslované a nečíslované seznamy lze kombinovat, avšak na jedné úrovní smí být pouze jeden druh (nemohou se střídat číslované a nečíslované řádky se stejným odsazením)
    * nečíslované seznamy lze označit znakem *, + nebo -
        * lze tyto možnosti kombinovat, avšak je doporučeno se držet pouze jednoho znaku
    * u číslovaných seznamů není brán ohled na to, jakou číslicí je označen, vždy se čísluje 1,2,...,n (vlastnost HTML)
3. Odstavce
    * prázdný řáddek označuje odstavce
    * pokud je text rozdělen na více řádků, je chápán jako jeden odstavec (a v HTML je zobrazen na jednom řádku)
    * 1 či více mezer na konci řádku přidá HTML tag &lt;br&gt;
4. Nadpisy
    * je podporováno 6 úrovní napisů – `# nadpis 1`, `## nadpis 2` atd.
        * pokud je v souboru nadpis úrovně 7 nebo více, program ohlásí výjimku a ukončí se
    * nadpis muže mít své "id" – `## nadpis {#id}`
        * to může být použité např. pro vytvoření odkazu (kotvy) na tento nadpis
        * id není zobrazeno, slouží pouze pro odkazování
5. Odkazy
    * odkaz je ve formátu `[název odkazu](odkaz)`, kdy odkaz může být jak relativní, tak absolutní
    * je možné se odkazovat na atribut "id" některého z nadpisů
6. Obrázky
    * obrázek je ve formátu `![název obrázku](odkaz)`, odkaz je relativní či absolutní.
    * obrázek lze vložit pouze na nový řádek (tedy ne doprostřed textu)
    * název obrázku je v HTML uložen jako atribut "alt"

## Informace pro programátory {#programatori}

### Rozdělení do modulů
Program je vhodně rozdělen do tří hlavních souborů. V kořenovém adresáři se nachází soubor `main.py`, který slouží ke spuštění celého programu. Ten načte nastavení ze souboru `settings.json` a předá je jako parametry k vytvoření objektu třídy `Runner`. Poté je volána funkce `run()`, funkcí `make_file()` je vytvořen nový prázdný soubor a `save_file()` uloží zpracovaná data.

### Postup zpracování souboru
Po spuštění programu main.py je nejprve načteno nastavení ze souboru settings.json, které je předáno konstruktoru třídy Runner při vytváření nové instance. Do proměnné `data` je funkcí `run()` z objektu třídy Runner je uložen naformátovaný text v HTML, poté je metodou `make_file()` do souboru output.html uložena hlavička (či je vytvořen soubor nový) a metodou `save_file()` je do tohoto souboru uložen text z proměnné data. Tím běh celého programu končí.

#### Modul runner.py
Tento soubor, který je obsažen v modulu `src` obsahuje hlavní část programu. V konstruktoru jsou uloženy proměnné později použité k nastavení jazyka, názvu dokumentu (html tag "title"), počet mezer označující odsazený blok.

##### Funkce `run()`
Hlavní částí je funkce `run()`, která postupně prochází načtený soubor řádek po řádku a každý řádek zpracuje.

Prvně se testuje, zda je aktuální řádek prázdný – pak jsou "ukončeny" veškeré předchozí rozpracované bloky formátování (seznamy, odstavec, citace), jsou náležitě zpracovány funckí třídy `Convertor` a přidány k výstupu.

Dále se testuje, zda je na řádku horizontální separátor. Poté zda řádek označuje začátek či konec bloku kódu.

Řádek 254 zkouší, zda řádek začíná vykřičníkem a pokud ano, je pomocí regulárního výrazu zjištěno, zda zbytek řádku odpovídá syntaxi vložení obrázku. Pokud ano, je opět regulárním výrazem z řádku načten zvlášť název a odkaz na obrázek, což je potom předáno funkci třídy `Convertor` a přidáno k výstupu.

Řádky 264-305 zkouší, zda je aktuální řádek nějaký seznam a podle jeho úrovně je přidán do patřičné proměnné. Ještě předtím je však pomocí metody `lists()` provedeno zpracování všech předchozích, ještě neukončených částí seznamu.

Pokud se řádek nevyznačuje ničím speciálním, je přidán k aktuálnímu odstavci.

##### Funce `parse_heading()`
Funkce slouží k naformátovnání nadpisu. Spočítá si, jaké je nadpis úrovně a zbytek stringu (bez znaků #) předá funkci `heading()` ze třídy *Convertor*.
Také je regulárním výrazem zjištěno, zda nadpis obsahuje *id* a pokud ano, je předáno funkci `heading()` zvlášť.

##### Funkce `lists()`
Jde o pomocnou funkci, která postupně zpracuje seznamy vyšší úrovně, pokud nějaké existují. Jako argument přijímá úroveň seznamu, od které se mají případné seznamy zpracovat. Např. parametr s hodnotu 1 znamená, že budou zpracovány pouze seznamy s indentací "2" a vyšší, jelikož bude následovat seznam s indentací "1". Hodnota -1 pak znamená, že se má zpracovat vše.

##### Funkce `parseline()`
*pozn.: slovem "operátor" je myšlen některý ze znaků, který nastavuje formátování na úrovni řádků, např. "`**`"

Funkce zpracovává jeden řádek ze souboru. Prochází ho znak po znaku (for cyklem) a vyhodnocuje, jak bude se znakem naloženo. Seznam operátorů je uložen v členské proměnné `syntax_inline` typu pole.

Pokud je daný znak operátor, je přidán na konec datové struktury zásobník (implementovaný pomocí pole), pokud v ní ještě takový operátor není. Pokud je, porovná se s posledním prvkem zásobníku a pokud se shodují, je textový řetězec ohraničený těmito operátory předán k dalšímu zpracování. Pokud se neshodují, jsou oba tyto operátory zahozeny, jelikož jde o chybu ve formátovní MarkDownu. Tomuto problému se však snaží předejít podmínka na řádku 91, kdy je otestováno, zda (pokud aktuálně načtený operátor ještě nebyl použit) k aktuálnímu operátoru existuje "párový" operátor, který jeho platnost ukončuje. Pokud tomu tak není, je operátor vyhodnocen jako klasický znak. Pokud tedy na řádku bude výraz např. 2*3, je zobrazen správně. Potom je však vhodné používat znaky "`_`" pro případné formátování, jelikož by mohlo docházet k chybám při určování, co má přesně který operátor ohraničovat.

##### Funkce `send_to_edit()`
Funkce volá podle druhu operátoru, který jí byl předán funkcí `parseline()` některou z funkcí třídy Convertor, která vrací příslušně naformátovaný text v HTML. Zde je také možné snadno přidat další znaky, které budou v toku textu chápány jako operátory. V takovém případě je navíc nutné je přidat do seznamu `self.syntax_inline` v konstruktoru a také zavést jejich patřičné zpracování v modulu `Convertor`.

##### Metody `make_file()` a `save_file()`
První z těchto metod uloží do prázdného souboru output.html hlavičku html souboru s doplněnými atributy jako je jazyk a title.

Druhá metoda ukládá do již vytvořeného souboru již zpracovaný text naformátovaný do html, ke kterému přidá uzavření tagů body a html.

#### Modul html_convertor {#html_convertor}
Obsahuje jediný soubor s třídou Convertor, která obsahuje triviální funkce vracející naformátovaný text v html.

## Informace pro uživatele {#uzivatele}
Do kořenového adresáře programu (tam, kde je soubor main.py) vložte textový soubor ve formátu MarkDown, který chcete přeložit do HTML. Název souboru by měl být "input.md" (výchozí název), avšak to lze změnit pomocí nastavení (viz [níže](#nastaveni)). Program se spustí pomocí hlavního skriptu main.py (pomocí terminálu či ve vámi preferovaném IDE). Výstup bude uložen do souboru output.html. Po zobrazení kladného hlášení je soubor připraven k použití.
**Pozor:** je důležité, aby byl vstupní soubor v MarkDownu platně naformátovaný, viz [vstup programu](#vstup).

## Nastavení {#nastaveni}
Program nabízí možnost nastavení některých parametrů, které mohou uživateli usnadnit práci. Nastavení se nachází v souboru settings.json, který lze upravit běžným textovým editorem. Měnit je možné pouze hodnoty za dvojtečkou, mezi uvozovkami.

1. "language" = jazyk – uložený v html souboru jako parametr "lang", určuje jazyk dokumentu kvůli správné interpretaci prohlížečem
    * výchozí hodnota (čeština): "cs"
2. "title" = název dokumentu, je poté zobrazen v prohlížeči jako název panelu
    * výchozí hodnota: "dokument"
3. "indentation" =  počet mezer, které určují odsazený úsek textu (důležité u seznamů)
    * výchozí hodnota: "4"
4. "input-file" =  název vstupního souboru, lze nastavit na libovolný textový řetězec, **musí** se však shodovat s názvem vstupního souboru (včetně přípony)
    * výchozí hodnota: "input.md"
5. "output-file" = název výstupního souboru
    * výchozí hodnota: "output.html"

## Průběh práce {#prace}
Nejprve jsem začal tím nejjednoduším – modulem html_convertor, viz [html_convertor](#html_convertor). Již ze začátku jsem chtěl mít funkce, které pouze přijímají string a vrací patřičně naformátovaný text v HTML (a vůbec neřeší, co je ve stringu obsaženo), mít oddělené od zbytku programu. Věděl jsem, že procházení celého souboru řádek po řádku a každý řádek znak po znaku bude samo o sobě místy dost nepřehledné, jelikož půjde o spoustu vnořených "ifů" zkoušejících, zda aktuální znak náhodou neznačí začátek nějakého formátovaného úseku. Toto oddělení od zbytku programu také považuji za výhodné proto, že lze třídu Convertor snadno vyjmout a použít bez výrazných změn v takřka jakémkoli jiném programu, který převádí jiný druh formátování do HTML.

Druhým krokem pak bylo napsat program, který bude procházet text a hledat v něm znaky nastavující formátování. Zde bylo důležité určit, které znaky bude program rozeznávat, jelikož MarkDown kromě běžné syntaxe může podporovat některé složitější struktury, jako např. tabulky a poznámky pod čarou, které jsem se rozhodl neimplementovat kvůli jejich složitosti a ne zcela snadnému použití v HTML. Naopak jsem chtěl implementovat věci jako horní a dolní idex, id nadpisů a víceřádkový codeblock. Pro inspiraci a ověření platnosti syntaxe jsem využíval webovou stránku [markdownguide.org](https://www.markdownguide.org).

Původně jsem měl také v plánu program udělat tak, aby výstupní kód v HTML vypadal "hezky", čímž myslím správné odsazení jednotlivých elementů.
Výstpu programu nyní vypadá takto:

```
&lt;body&gt;
&lt;h1&gt;Zápočtový program – převod MarkDownu do HTML&lt;/h1&gt;
&lt;h2&gt;Obsah&lt;/h2&gt;
&lt;ol&gt;
&lt;li&gt;&lt;a href="#uvod"&gt;Úvod&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;a href="#vstup"&gt;Vstup programu&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;a href="#programatori"&gt;Informace pro programátory&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;a href="#uzivatele"&gt;Informace pro uživatele&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;a href="#nastaveni"&gt;Nastavení&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;&lt;a href="#prace"&gt;Průběh práce&lt;/a&gt;&lt;/li&gt;
&lt;/ol&gt;
&lt;/body&gt;
```
Ale bylo by hezčí, kdyby vypadal takto:
```
&lt;body&gt;
    &lt;h1&gt;Zápočtový program – převod MarkDownu do HTML&lt;/h1&gt;
    &lt;h2&gt;Obsah&lt;/h2&gt;
    &lt;ol&gt;
        &lt;li&gt;&lt;a href="#uvod"&gt;Úvod&lt;/a&gt;&lt;/li&gt;
        &lt;li&gt;&lt;a href="#vstup"&gt;Vstup programu&lt;/a&gt;&lt;/li&gt;
        &lt;li&gt;&lt;a href="#programatori"&gt;Informace pro programátory&lt;/a&gt;&lt;/li&gt;
        &lt;li&gt;&lt;a href="#uzivatele"&gt;Informace pro uživatele&lt;/a&gt;&lt;/li&gt;
        &lt;li&gt;&lt;a href="#nastaveni"&gt;Nastavení&lt;/a&gt;&lt;/li&gt;
        &lt;li&gt;&lt;a href="#prace"&gt;Průběh práce&lt;/a&gt;&lt;/li&gt;
    &lt;/ol&gt;
&lt;/body&gt;
```
Nicméně to by vyžadovalo další procházení celého HTML souboru a jeho úpravy, případně použití některé externí knihovny. Taková implementace by však byla v rozporu s mým původním plánem – napsat program takový, aby používal naprosté minumum "cizího kódu". To se mi také povedlo dodržet, jediný import je balíček "re", který umožňuje interpretovat regulární výrazy a je součástí běžné instalace pythonu.
Také jsem jednotlivé výstupy převodu do HTML testoval v [HTML validátoru](https://validator.w3.org) a snažil se pro případné nalezené chyby opravit kód tak, aby (ideálně) vždy generoval validní HTML výstup. 