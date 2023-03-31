import requests
from .Bil_klasse import Bil
from bs4 import BeautifulSoup


class Skraper:
    def __init__(self, link):
        self.link = link
        self.alle_biler = []
        self.spesifikasjons_ord = ["Farge", "Chassis", "Effekt", "Batteri",
                                   "WLTP"]  # sepsifikasjoner som kan være greit å få fra annonsen
        self.beskrivelses_ord = ["hovedbatteri"]
        self.skrap_hoved_siden()
        self.skrap_alle_annonser()

    def rensk_tekst(self, tekst, skal_erstatte=None, erstattning=None, fjern=None):
        liste_tekst = tekst.replace(skal_erstatte, erstattning).strip(fjern).split()
        full_tekst = ""
        for delen in liste_tekst:
            full_tekst += delen

        return full_tekst

    def skaffe_dato_fra_bilde(self, annonse_img_element, bil):
        bil.bilde = annonse_img_element["src"]
        splitet_bilde_link = bil.bilde.split("/")  # splittet det opp
        annonse_opprettelsesdato = {  # Ta det 8. 6. og 5. delen av listen. [dag], [måned], [år]
            "dag": splitet_bilde_link[8],
            "måned": splitet_bilde_link[6],
            "år": splitet_bilde_link[5]
        }

        return annonse_opprettelsesdato

    def skaffe_info_fra_titel(self, annonse_a_element):
        navn = annonse_a_element.text
        link = annonse_a_element["href"]
        annonse_id = annonse_a_element["id"]

        return navn, link, annonse_id

    def skaffe_spesifikasjon_fra_annonse(self, annonse_div_element):
        spesifikasjons_tekst = annonse_div_element.find_all("div")
        årsmodel = spesifikasjons_tekst[0].text
        kmstand = self.rensk_tekst(spesifikasjons_tekst[1].text, " ", "", "km")
        pris = self.rensk_tekst(spesifikasjons_tekst[2].text, " ", "", "kr")

        ordbok = {
            "årsmodel": årsmodel,
            "kilometerstand": kmstand,
            "pris": pris
        }

        return ordbok

    def skrap_hoved_siden(self):
        side = requests.get(self.link)
        html_data = BeautifulSoup(side.content, "html.parser")

        alle_annonser = html_data.find_all("article", class_="ads__unit")

        for annonse in alle_annonser:
            annonse_a_element = annonse.find_next("a")
            info_fra_titel = self.skaffe_info_fra_titel(annonse_a_element)
            bil = Bil(info_fra_titel[0], info_fra_titel[1], info_fra_titel[2])
            self.alle_biler.append(bil)

            annonse_img_element = annonse.find_next("img")
            bil.annonse_opprettelsesdato = self.skaffe_dato_fra_bilde(annonse_img_element, bil)

            annonse_div_element = annonse.find_next("div", class_="ads__unit__content__keys")
            spesifikasjons_ordbok = self.skaffe_spesifikasjon_fra_annonse(annonse_div_element)
            bil.år = spesifikasjons_ordbok["årsmodel"]
            bil.kmstand = spesifikasjons_ordbok["kilometerstand"]
            bil.pris = spesifikasjons_ordbok["pris"]

    def skarp_beskrivelse(self, bil):
        if bil.beskrivelse is not None:
            bil.beskrivelse = bil.beskrivelse.text
            for ord in self.beskrivelses_ord:
                if ord.lower() in bil.beskrivelse.lower():
                    bil.ekstra_info[ord] = "nevnt"

    def skrape_spesifikasjoner(self, bil):
        for index, spesifikasjon in enumerate(bil.spesifikasjoner):
            if index % 2 != 0:
                continue
            for ord in self.spesifikasjons_ord:
                if ord.lower() in spesifikasjon.text.lower():
                    bil.ekstra_info[spesifikasjon] = bil.spesifikasjoner[index + 1].text

    def skrape_steds_info(self, html_parser, bil):
        steds_vindu = html_parser.find("span", class_="u-mh16")  # lette etter der lokasjonen står
        if steds_vindu:  # Hvis verdien finnes
            bil.lokasjon = steds_vindu.text  # lagre den
        else:  # ellers
            steds_vindu = html_parser.find("p", class_="u-mh16")  # så er lokasjonen en full adresse
            bil.lokasjon = steds_vindu.text

    def skrap_annonse(self, bil):
        side = requests.get(bil.link)
        html_data = BeautifulSoup(side.content, "html.parser")

        bil.beskrivelse = html_data.find(id="collapsableTextContent")  # finne beskrivelsen
        self.skarp_beskrivelse(bil)

        spesifikasjons_boks_info = html_data.find_all("dt")  # nederst på side med navent til spesifikasjonene
        spesifikasjons_boks_data = html_data.find_all("dd")  # nedesrt på siden med spesifikajsonene til bilen

        bil.spesifikasjoner = [item for par in zip(spesifikasjons_boks_info, spesifikasjons_boks_data) for item in
                               par]  # Tvinne datanene sammen, så du får navnet på spesifikasjonen og deretter dataen til spesifikasjonen
        self.skrape_spesifikasjoner(bil)

        self.skrape_steds_info(html_data, bil)

    def skrap_alle_annonser(self):
        for bil in self.alle_biler:
            self.skrap_annonse(bil)

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
