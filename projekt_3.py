"""
projekt_3.py: Třetí projekt do Engeto Online Python Akademie

author: Michal Zemčák
email: michal.zemcak@gmail.com
discord: michal_79719
"""

import sys
import csv
import os
from bs4 import BeautifulSoup as bs
from requests import get


def main(url_district, file_name):
    """
    Tato funkce se spustí jako první při spuštění kódu.
    Spouští funkce v správném pořadí od stažení, zpracování a zápisu dat do souboru CSV.
    Jako volitelné extra, funkce také vypíše cestu k vytvořenému souboru a jeho velikost v bytech.
    """

    print(f"Stahovaní dat z URL: {url_district}")

    # Prefix pro vytvoření úplné URL adresy
    prefix = "https://volby.cz/pls/ps2017nss/"

    unique_urls = get_unique_links(url_district, prefix)
    response = get(unique_urls[0])
    election_parties = extract_party_names(response)

    # Získání kódů obcí pro všechny unikátní URL
    town_codes = []
    for url in unique_urls:
        town_codes.extend(extract_codes_from_url(url))

    # Stáhnutí dat pro všechny obce a zápis do seznamu final_data
    final_data = scrape_data(unique_urls, town_codes)

    # Zápis final_data do CSV souboru
    write_to_csv(final_data, file_name, election_parties)

    # Získání aktuální pracovní složky a výpis cesty souboru
    working_directory = os.getcwd()
    file_path = (working_directory + "/" + file_name)
    print(f"Data v CSV jsou uložená zde:\n{file_path}")



def get_unique_links(url_district, prefix):
    """
    Tato funkce stáhne HTML obsah a filtruje seznam URL adres pro každé město a jejich kódy.
    """
    districts_mix = get(url_district)
    districts_bs = bs(districts_mix.content, "html.parser")
    unique_urls = set()

    # Procházení všech odkazů na stránce a filtrování podle kritérií
    for url in districts_bs.find_all("a", href=True):
        if "ps311" in url["href"]:
            full_url = prefix + url["href"]
            unique_urls.add(full_url)

    # Převedení setu na list a vrácení seznamu unikátních URL adres
    return list(unique_urls)


def extract_party_names(response):
    """
    Tato funkce extrahuje názvy politických stran z URL adresy.
    """
    soup = bs(response.content, "html.parser")
    element_names = soup.find_all('td', class_='overflow_name')
    return [element.get_text(strip=True) for element in element_names]


def extract_codes_from_url(text):
    """
    Tato funkce získává kódy obcí z URL adresy a zajišťuje, že kódy jsou správné.
    """
    codes = []
    for i in range(len(text) - 5):
        substring = text[i:i + 6]
        if substring.isdigit():
            codes.append(substring)
    return codes


def clean_text(text):
    """
    Očišťtění textu získaného z BeautifulSoup pro následné použití v funkcích.
    """
    return text.strip().replace("\xa0", "").replace("&nbsp;", "")


def find_and_append(soup, headers, data_list):
    """
    Tato funkce byla připravena pro filtrování a přidání požadovaných dat.
    """
    td = soup.find("td", {"class": "cislo", "headers": headers})
    if td:
        data_list.append(clean_text(td.text))
    else:
        data_list.append("N/A")


def scrape_data(town_urls, town_codes):
    """
    Tato funkce stahuje, filtruje a agreguje data do formy použitelné pro následující funkce.
    """
    final_data = []
    for index, town_link in enumerate(town_urls):
        towns_data = []
        response = get(town_link)

        if response.status_code == 200:
            soup = bs(response.content, "html.parser")
            town_code = town_codes[index] if index < len(town_codes) else "N/A"
            towns_data.append(town_code)

            # Získání názvu obce
            town_tag = soup.find('h3', string=lambda x: x and 'Obec:' in x)
            town_name = town_tag.text.split(': ')[1].strip() if town_tag else "N/A"
            towns_data.append(town_name)

            # Získání počtu voličů v seznamu, vydaných obálek a platných hlasů
            find_and_append(soup, "sa2", towns_data)  # voliči v seznamu
            find_and_append(soup, "sa3", towns_data)  # vydané obálky
            find_and_append(soup, "sa6", towns_data)  # platné hlasy

            # Získání hlasů pro jednotlivé strany
            for headers in ["t1sa2 t1sb3", "t2sa2 t2sb3"]:
                numbers_td = soup.find_all("td", {"class": "cislo", "headers": headers})
                for cislo_td in numbers_td:
                    towns_data.append(clean_text(cislo_td.text))

            # Přidání dat obce do final_data
            final_data.append(towns_data)
        else:
            print("Chyba při načítání stránky:", response.status_code)
    return final_data


def write_to_csv(final_data, file_name, election_parties):
    """
    Tato funkce zapisuje data do souboru .csv.
    """
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        # Zápis hlavičky souboru
        writer.writerow(['kód', 'obec', 'voliči_v_seznamu', 'vydané_obálky', 'platné_hlasy'] + election_parties)

        # Zápis dat obcí do souboru
        writer.writerows(final_data)


def validate_arguments(url_district, file_name):
    """
    Tato funkce validuje vložené argumenty pro spuštění tohoto skriptu.
    Pokud nejsou splněny podmínky, uživatel je informován v terminálu.
    """
    url_prefix = "https://volby.cz/pls/ps2017nss/"
    suffix = ".csv"
    if url_district.startswith(url_prefix) and file_name.endswith(suffix):
        return True
    elif file_name.startswith(url_prefix) and url_district.endswith(suffix):
        print("Špatné pořadí argumentů!")
        return False
    else:
        print("Špatný formát argumentů!")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    url_district = sys.argv[1]
    file_name = sys.argv[2]

    if not validate_arguments(url_district, file_name):
        sys.exit(1)

    main(url_district, file_name)
