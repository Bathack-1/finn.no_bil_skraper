from Bil_skraper.Skraper import Skraper
from Bil_skraper.utviklings_verktøy import skrape_merker_verdi, skrape_model_verdi, skrape_område, skrive_imports
from Bil_skraper.finn_no_link_konstruktor import Link_konstruktor


def main():

    """
    Måten du lager et "filter" er ved oppskriften under

    ordbok = {
        "merke": merke,
         "model": [alle modelene],
         "år": (fra, til),
         "km_stand": (fra, til),
         "område": [alle områdene],
         "salgsform": [alle salgsformene],
    }
    Dette er for å gjøre det enklest mulig å endre programmet
    bare vær klar over at jeg ikke kan programmere, så prosessen å skrape alle annonsene tar tid

    under ser du et eksempel på audi A1 i viken, som er bruktbil til salgs
    """

    ordbok = {
        "merke": "audi",
         "model": ["A1"],
         "område": ["viken"],
         "salgsform": ["Bruktbil til salgs"],
    }

    link_1 = Link_konstruktor(ordbok)
    print(link_1.link)
    skraper = Skraper(link_1.link)
    for bil in skraper.alle_biler:
        print(bil.annonse_opprettelsesdato, bil.navn)


if __name__ == '__main__':
    main()
