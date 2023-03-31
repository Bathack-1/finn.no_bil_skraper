from Bil_skraper.Skraper import Skraper
from Bil_skraper.utviklings_verktøy import skrape_merker_verdi, skrape_model_verdi, skrape_område, skrive_imports
from Bil_skraper.finn_no_link_konstruktor import Link_konstruktor


def main():
    # skrap()
    # skraper = Skraper("https://www.finn.no/car/used/search.html?location=22030&location=20061&make=0.8078&mileage_to=200000&price_to=230000&sales_form=1&sort=PUBLISHED_DESC")
    # skrape_merker_verdi()
    # skrape_model_verdi()
    # skrape_område()
    # skrive_imports()

    ordbok = {
        "merke": "opel",
         "model": ["Ampera"],#["Model S", "Model 3"],
        # "år": (None, None),
         "km_stand": (None, 200000),
         "område": ["viken", "oslo"],  # ["viken", "oslo"],
         "salgsform": ["Bruktbil til salgs"],  # ["Bruktbil til salgs"],
    }

    link_1 = Link_konstruktor(ordbok)
    print(link_1.link)
    skraper = Skraper(link_1.link)
    for bil in skraper.alle_biler:
        print(bil.annonse_opprettelsesdato, bil.navn)


if __name__ == '__main__':
    main()
