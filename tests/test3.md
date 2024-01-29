# Principy počítačů 30. 10.
---
* **bitové posuny:**
  1. SHL `<<` = posun k **MSb**	
    * `1101 SHL 1` -> `1010`
    * `1101 SHL 3` -> `1000`
    * vše, co se posune mimo přesnost se zahodí
    * vzniklá prázdná místa se doplní nulami ∅
  2. SHR `>>` posun k **LSb**
    * `1101 SHR 1` -> `0110`
* **rotace:**
  * jako bit. posun, ale to co se vysune mimo přesnost se připojí zezadu
  * `1101 ROL 2` -> `0111`

## Záporná čísla
### Znaménkový bit
* nefungují žádné základní operace
### Jedničkový doplněk
* nezáporná čísla — unsigned n-bit
* `-` = `NOT(abs(x))`
  * -5 = `1111 1010`
* funguje bezznaménkové porovnání
* máme 2 nuly
### Dvojkový doplněk
* stejně jako jedničkový, ale přičte se jednička
* řeší problém s nulami
* nefunguje porovnávání, ale fungují základní operace

## Čísla v pythonu
* balíček `numpy`
  * přidává unsigned, pevné bitové délky