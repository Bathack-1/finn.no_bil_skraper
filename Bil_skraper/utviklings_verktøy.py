import requests
from bs4 import BeautifulSoup

"""
skrape "merker" og lagre resultatet i buffer tekst filen
"""

def skrape_merker_verdi():
    tekst = ""
    with open('Bil_skraper/"låner"_fra_finn.html') as fil:
        tekst = fil.read()

        fil.close()
    #side = requests.get('/home/christoffer/Programmering/PycharmProjects/Botter/finn.no_skraper/Bil_skraper/"låner"_fra_finn.html')
    html_data = BeautifulSoup(tekst, "html.parser")

    liste_elementer = html_data.find_all("li")
    with open('Bil_skraper/buffer_tekst_fil', "w+") as fil:
        fil.write("merke = { \n")

        for element in liste_elementer:
            merke_id = element.find_next("input")["id"].replace("-", "=")
            merke_navn = element.text.split(" ")[0]
            fil.write(f'"{merke_navn}": "{merke_id}", \n')

        fil.write("}")
        fil.close()

    """
    format:
    make=0.8103
    """
