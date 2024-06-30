## ENGETO-Python-3-projekt
Třetí projekt na Python Akademii od Engeta.

## Popis projektu
Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí najdete [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

### Instalace knihoven
Knihovny, které jsou použity v kódu jsou uložené v souboru requirements.txt. Pro instalaci doporučuji použít nové virtuálníprostředí s nainstalovaným manažerem spustit následovně:

    $ pip3 --version			        --- ověřím verzi manažeru
    $ pip install -r requirements.txt       	--- nainstaluje knihovny

### Spuštění projektu
Spuštění souboru projekt_3.py v rámci příkazového řádku požaduje dva povinné argumenty.
python soubor.py URL adresu: "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" a název souboru "vysledky_Praha.csv"

    python Projekt_3.py <odkaz-uzemniho-celku> <vysledny-soubor.csv>
Následně se stáhnou výsledky jako .csv soubor.

### Ukázka projektu
Výsledky hlasování pro hl. město Praha:
1. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100
2. argument: vysledky_Praha.csv

### Spuštění programu:
    python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "vysledky_Praha.csv"

### Průběh stahování:
    Stahovaní dat z URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100 
    Data v CSV jsou uložená zde:
    C:\Users\micha\PycharmProjects\test\.venv/vysledky_Praha.csv

### Částečný výstup:
    ...
    kód;obec;voliči_v_seznamu;vydané_obálky;platné_hlasy;Občanská demokratická strana;Řád národa - Vlastenecká 
    539007;Praha-Vinoř;2945;2166;2158;337;8;4;107;1;2;201;85;35;8;1;40;2;2;318;1;0;0;204;486;1;1;138;1;11;2;2;154;6
    539635;Praha-Řeporyje;2947;2074;2069;405;7;0;107;2;0;105;49;43;5;5;55;1;3;372;0;1;1;235;425;1;4;109;0;20;4;1;105;4
    547301;Praha-Dolní Chabry;3020;2276;2253;483;0;2;85;0;1;125;72;36;7;1;47;2;4;392;0;0;1;309;412;1;2;112;1;24;5;1;117;11
    ...
