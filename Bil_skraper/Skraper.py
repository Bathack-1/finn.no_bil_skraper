import requests
from .Bil_klasse import Bil
from bs4 import BeautifulSoup


def rensk_tekst(tekst, skal_erstatte, erstattning, fjern):
    liste_tekst = tekst.replace(skal_erstatte, erstattning).strip(fjern).split()
    full_tekst = ""
    for delen in liste_tekst:
        full_tekst += delen

    return full_tekst

def skrap():
    lagret_søk = "https://www.finn.no/car/used/search.html?location=22030&location=20061&make=0.8078&mileage_to=200000&price_to=230000&sales_form=1&sort=PUBLISHED_DESC"
    side = requests.get(lagret_søk)

    html_data = BeautifulSoup(side.content, "html.parser")

    alle_annonser = html_data.find_all("a", class_="ads__unit__link")

    alle_biler = []

    for annonse in alle_annonser:
        print(annonse)
        navn = annonse.text
        link = annonse["href"]
        annonse_id = annonse["id"]
        alle_biler.append(Bil(navn, link, annonse_id))

    for bil in alle_biler:
        side = requests.get(bil.link)

        html_data = BeautifulSoup(side.content, "html.parser")

        info_vindu = html_data.find_all("div", class_="u-strong")
        bil.år = info_vindu[0].text
        bil.kmstand = int(rensk_tekst(info_vindu[1].text, " ", "", "km"))

        pris_boks = html_data.find_all("dd")
        bil.pris = int(rensk_tekst(pris_boks[1].text, " ", "", "kr"))

        beskrivelse = html_data.find(id="collapsableTextContent")
        if beskrivelse is not None:
            #print(beskrivelse)
            batteri_relaterte_ord = ["hovedbatteri", "garanti"]
            for ord in batteri_relaterte_ord:
                if ord in beskrivelse.text:
                    bil.byttet_hovedbatteri = True

        print(bil.navn, bil.år, bil.kmstand, bil.pris, "kr", bil.byttet_hovedbatteri)

    print("\n", len(alle_biler))

    sortert_km = sorted(alle_biler, key=lambda bil: bil.kmstand)

    for bil in sortert_km:
        print(bil.kmstand, bil.navn)

    """
    finne link til bil på finn.no:
        <a id="295201897" href="https://www.finn.no/car/used/ad.html?finnkode=295201897" class="ads__unit__link">Tesla Model S 70D - 1 Eier/Gratis SC/Autopilot/NextGen/Skinn/CCS++</a>
        
    finne pris:
        <h2 data-testid="price">229 147 kr</h2>
        
    finne årsmodel:
        <div class="u-strong">2015</div>
    
    finne kilometerstand:
        <div class="u-strong">302&nbsp;350 km</div>
     
    finne beskrivelse:
        <h2 class="u-t3">Beskrivelse</h2>
        
     /*   
    finne farge:
        <dd>Hvit</dd>
    
    finne chassi nr:
        <dd>5YJSA6H14EFP57966</dd>
        */
    """