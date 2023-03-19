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

    #samle alle bilene, og lagrer de i en liste
    for annonse in alle_annonser:
        print(annonse)
        navn = annonse.text
        link = annonse["href"]
        annonse_id = annonse["id"]
        alle_biler.append(Bil(navn, link, annonse_id))

    #Går gjennom listen for å finne ekstra informasjon om hver bil
    for bil in alle_biler:
        side = requests.get(bil.link)

        html_data = BeautifulSoup(side.content, "html.parser")                     #bare vanlig kode for å gjøre siden leslig for python

            ###Info vindu relatert###
        info_vindu = html_data.find_all("div", class_="u-strong")                  #Finne vinduet som forteller årsmodel, kilometerstand, girkasse og drivstoff
        bil.år = info_vindu[0].text                                                #Den første verdien i listen er årsmodel
        bil.kmstand = int(rensk_tekst(info_vindu[1].text, " ", "", "km"))          #andre er kilometerstand. Her returneres det en string, så den må fikses


            ###Beskrivelse relatert###
        beskrivelse = html_data.find(id="collapsableTextContent")       #finne beskrivelsen
        if beskrivelse is not None:                                     #ignorere hvis den ikke finnes
            batteri_relaterte_ord = ["hovedbatteri"]
            for ord in batteri_relaterte_ord:                           #søke etter ord i beskrivelsen som kan være nyttig
                if ord.lower() in beskrivelse.text.lower():
                    bil.ekstra_info[ord] = "nevnt"


            ###Spesifikasjoner relatert###
        spesifikasjons_boks_info = html_data.find_all("dt")     # nederst på side med navent til spesifikasjonene
        spesifikasjons_boks_data = html_data.find_all("dd")     # nedesrt på siden med spesifikajsonene til bilen

        bil.pris = int(rensk_tekst(spesifikasjons_boks_data[1].text, " ", "", "kr"))  # finne prisen på bilen i den boksen

        spesifikasjons_ord = ["Farge", "Chassis", "Effekt", "Batteri", "WLTP"]     # Info som kan være greit å få fra annonsen

        for index, spesifikasjoner in enumerate(spesifikasjons_boks_info):      # Går gjennom alle "dt" deler
            for ord in spesifikasjons_ord:
                if ord.lower() in spesifikasjoner.text.lower():                 #sammenligner det i annonsen med nyttig info
                    bil.ekstra_info[ord] = spesifikasjons_boks_data[index].text     #lagrer det, hvis det er nyttig


            ###finne lokasjon###
        steds_vindu = html_data.find("span", class_="u-mh16")       #lette etter der lokasjonen står
        if steds_vindu:                                             #Hvis verdien finnes
            bil.ekstra_info["Lokasjon"] = steds_vindu.text          #lagre den
        else:                                                       #ellers
            steds_vindu = html_data.find("p", class_="u-mh16")      #så er lokasjonen en full adresse
            bil.ekstra_info["Lokasjon"] = steds_vindu.text          #lagre den


            ###finne opplastningsdato###
        """
        skrape for det første bilde, dele det opp i en liste, beholde delene som forteller dato, lagre det til bilen
        
        """
        bilde = html_data.find("img", class_="img-format__img u-border-radius-8px")     #det er hva bildene er lagret som i html
        bilde_link = bilde["src"]                                                       #kun ta "src" elementet
        splitet_bilde_link = bilde_link.split("/")                                      #splittet det opp
        bilde_dato = f"{splitet_bilde_link[8]} {splitet_bilde_link[6]} {splitet_bilde_link[5]}"    #Ta det 8. 6. og 5. delen av listen. [dag], [måned], [år]
        bil.annonse_opprettelsesdato = bilde_dato
        print(bilde_dato)

    print("\n", len(alle_biler))

    sortert_km = sorted(alle_biler, key=lambda bil: bil.kmstand)    #sorterer listen etter kmstand

    for bil in sortert_km:
        print(bil.kmstand, "km", bil.navn)

    """
    her er noen eksempler på hvordan elementer kan se ut i html koden:
    
    link til en bil på finn.no:
        <a id="295201897" href="https://www.finn.no/car/used/ad.html?finnkode=295201897" class="ads__unit__link">Tesla Model S 70D - 1 Eier/Gratis SC/Autopilot/NextGen/Skinn/CCS++</a>
        
    pris:
        <h2 data-testid="price">229 147 kr</h2>
        
    årsmodel:
        <div class="u-strong">2015</div>
    
    kilometerstand:
        <div class="u-strong">302&nbsp;350 km</div>
     
    beskrivelse:
        <h2 class="u-t3">Beskrivelse</h2>
        
    farge:
        <dd>Hvit</dd>
    
    chassi nr:
        <dd>5YJSA6H14EFP57966</dd>
    """