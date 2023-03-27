import requests
import os
from bs4 import BeautifulSoup
from .Ordbøker.Merke_ordbok import merke_ordbok

"""
skrape "merker" og lagre resultatet i buffer tekst filen
"""

def skrape_merker_verdi():
    with open('Bil_skraper/"låner"_fra_finn.html') as fil:  #klarte ikke å requeste finn.no med "vis alle" aktivert, så lagret bare nettside koden i en annen fil
        tekst = fil.read()

        fil.close()
    html_data = BeautifulSoup(tekst, "html.parser")

    liste_elementer = html_data.find_all("li")
    with open('Bil_skraper/Ordbøker/Merke_ordbok.py', "w+") as fil:
        fil.write("merke_ordbok = { \n")

        for element in liste_elementer:
            print(element)
            if element.find_next("input"):
                merke_id = element.find_next("input")["id"].replace("-", "=")
                merke_navn = element.text.split("(")[0][:-1]
                fil.write(f'    "{merke_navn.lower()}": "{merke_id}", \n')
        #finne NoneType erroren

        fil.write("} \n")
        fil.close()

    """
    format:
        make=0.8103
    """

def skrape_model_verdi():
    for merke in merke_ordbok:
        make_kode = merke_ordbok[merke]
        merke = merke.replace(' ', '_').replace('-', '_').lower()

        side = requests.get(f"https://www.finn.no/car/used/search.html?{make_kode}&sort=PUBLISHED_DESC")
        html_data = BeautifulSoup(side.content, "html.parser")

        print(side.url)
        underliste_klasse = html_data.find("ul", class_="list u-ml16")

        if underliste_klasse:
            liste_elementer = underliste_klasse.find_all("div", class_="input-toggle")
            with open(f"Bil_skraper/Ordbøker/Model_ordbøker/{merke}.py", "w") as fil:

                fil.write(f"{merke}_model_bok"+" = { \n")

                for element in liste_elementer:
                    print(element)
                    model_id = element.find_next("input")["id"].replace("-", "=")
                    model_navn = element.text.split("(")[0][:-1]

                    fil.write(f'    "{model_navn}": "{model_id}", \n')

                fil.write("} \n")
                fil.close()
            print(f"ferdig med {merke}")
    """
    format:
        make=model=1.8093.2000436
    """

def skrape_område():
    side = requests.get(f"https://www.finn.no/car/used/search.html?sort=PUBLISHED_DESC")
    html_data = BeautifulSoup(side.content, "html.parser")

    område_heading = html_data.find("h3", text="Område")
    område_liste = område_heading.find_next("ul")

    if område_liste:
        liste_elementer = område_liste.find_all("div", class_="input-toggle")
        with open(f"Bil_skraper/Ordbøker/Område_ordbok.py", "w") as fil:
            fil.write("område_bok = { \n")

            for element in liste_elementer:
                print(element)
                merke_id = element.find_next("input")["id"].replace("-", "=")
                merke_navn = element.text.split("(")[0][:-1]
                fil.write(f'    "{merke_navn.lower()}": "{merke_id}", \n')

            fil.write("} \n")
            fil.close()

    """
    format:
        location=22042
    """
    """
    søke nettsiden for "område", deretter lagre elementet under, en ul liste
    """

def skrive_imports():
    merke_liste = os.listdir("Bil_skraper/Ordbøker/Model_ordbøker")
    with open(f"Bil_skraper/Ordbøker/Alle_model_import_samlet.py", "w") as fil:
        for merke in merke_liste:
            fil.write(f"from .Model_ordbøker.{merke.replace('.py', '').replace('-', '_')} import * \n")

        fil.close()


