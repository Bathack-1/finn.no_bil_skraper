import requests
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
                merke_navn = element.text.split("(")[0]
                fil.write(f'    "{merke_navn}": "{merke_id}", \n')
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

        side = requests.get(f"https://www.finn.no/car/used/search.html?{make_kode}&sort=PUBLISHED_DESC")
        html_data = BeautifulSoup(side.content, "html.parser")

        print(side.url)
        underliste_klasse = html_data.find("ul", class_="list u-ml16")
        if not underliste_klasse:
            continue
        if underliste_klasse.find("div", class_="input-toggle"):

            liste_elementer = underliste_klasse.find_all("div", class_="input-toggle")
            with open(f"Bil_skraper/Ordbøker/Model_ordbøker/{merke}.py", "w") as fil:
                fil.write("model_bok = { \n")

                for element in liste_elementer:
                    print(element)
                    merke_id = element.find_next("input")["id"].replace("-", "=")
                    merke_navn = element.text.split("(")[0]
                    fil.write(f'    "{merke_navn}": "{merke_id}", \n')
                # finne NoneType erroren

                fil.write("} \n")
                fil.close()
            print(f"ferdig med {merke}")
"""
requeste finn.no med hver av model-IDene. se alle svarene den får. 
lage en ny fil, eller overskrive hvis den finnes, og lagre resultatene med filnavn {merke}.py
"""
