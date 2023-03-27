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
        self.merke = søk_filter["merke"]
        self.model = søk_filter["model"]
        self.år = søk_filter["år"]
        self.km_stand = søk_filter["km_stand"]
        self.område = søk_filter["område"]
        self.salgsform = søk_filter["salgsform"]

        self.link_deler = []
        self.link = ""
        self.skaffe_link()
    def skaffe_link(self):
        base_link = "https://www.finn.no/car/used/search.html?"
        sluttstykke_link = "sort=PUBLISHED_DESC"
        if self.model:
            self.link += self.skaffe_model()
        else:
            self.link += f"{merke_ordbok[self.merke]}&"

        self.link += self.skaffe_års_model()
        self.link += self.skaffe_km_stand()
        self.link += self.skaffe_område()
        self.link += self.skaffe_salgsform()

        self.link = f"{base_link}{self.link}{sluttstykke_link}"

    def skaffe_model(self):
        model_tekst = ""
        bok = f"{self.merke}_model_bok"
        ordbok = globals()[bok]
        for model in self.model:
            print(self.model)
            model_tekst += ordbok[model]
            model_tekst += "&"
        return f"{model_tekst}"
        #self.link_deler.append(model_tekst)

    def skaffe_års_model(self):
        års_model_tekst = år_model_filter(self.år[0], self.år[1])
        return f"{års_model_tekst}"
        #self.link_deler.append(års_model_tekst)

    def skaffe_km_stand(self):
        km_stand_tekst = kilometer_filter(self.km_stand[0], self.km_stand[1])
        return f"{km_stand_tekst}&"
        #self.link_deler.append(km_stand_tekst)

    def skaffe_område(self):
        område_tekst = ""
        for område in self.område:
            område_tekst += område_bok[område]
            område_tekst += "&"
        return f"{område_tekst}"
        #self.link_deler.append(område_tekst)

    def skaffe_salgsform(self):
        salgsform_tekst = ""
        for form in self.salgsform:
            salgsform_tekst += salgsform[form]
            salgsform_tekst += "&"
        return f"{salgsform_tekst}"

        #self.link_deler.append(salgsform_tekst)
