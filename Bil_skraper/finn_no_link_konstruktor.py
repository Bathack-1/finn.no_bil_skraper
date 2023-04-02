from .Ordbøker.Alle_model_import_samlet import *
from .Ordbøker.Merke_ordbok import *
from .Ordbøker.Slagsform_ordbok import *
from .Ordbøker.fra_til_filter import *
from .Ordbøker.Område_ordbok import *
"""
ordbøker med "link koden" til til forskjellige parametere:
ordbok for de "viktigste":
    merke
    model
    år
    pris
    km_stand
    område
    drivstoff


få python til å skrive classene selv

"""

"""https://www.finn.no/car/used/search.html?{ekstra info}sort=PUBLISHED_DESC"""



class Link_konstruktor:
    def __init__(self, søk_filter):
        self.søk_filter = søk_filter

        self.link_deler = []
        self.link = ""
        self.skaffe_link()
    def skaffe_link(self):
        base_link = "https://www.finn.no/car/used/search.html?"
        sluttstykke_link = "sort=PUBLISHED_DESC"
        for filter in self.søk_filter:
            self.link += eval(f"self.skaffe_{filter}()")

            """
            gå gjennom alle nøklene
            finne funksjonen på den nøkelen
            kjøre funksjonen 
            legge til resultatet i self.link
            """

        self.link = f"{base_link}{self.link}{sluttstykke_link}"

    def skaffe_merke(self):
        return f"{merke_ordbok[self.søk_filter['merke']]}&"

    def skaffe_model(self):
        model_tekst = ""
        bok = f"{self.søk_filter['merke']}_model_bok"
        ordbok = globals()[bok]
        for model in self.søk_filter["model"]:
            model_tekst += ordbok[model]
            model_tekst += "&"
        return f"{model_tekst}"

    def skaffe_år(self):
        års_model_tekst = år_model_filter(self.søk_filter["år"][0], self.søk_filter["år"][1])
        return f"{års_model_tekst}"

    def skaffe_km_stand(self):
        km_stand_tekst = kilometer_filter(self.søk_filter["km_stand"][0], self.søk_filter["km_stand"][1])
        return f"{km_stand_tekst}&"

    def skaffe_område(self):
        område_tekst = ""
        for område in self.søk_filter["område"]:
            område_tekst += område_bok[område]
            område_tekst += "&"
        return f"{område_tekst}"

    def skaffe_salgsform(self):
        salgsform_tekst = ""
        for form in self.søk_filter["salgsform"]:
            salgsform_tekst += salgsform[form]
            salgsform_tekst += "&"
        return f"{salgsform_tekst}"
