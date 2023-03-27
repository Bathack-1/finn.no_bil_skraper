

def år_model_filter(fra_år=None, til_år=None):
    års_model_filter = ""
    if fra_år:
        års_model_filter += f"year_from={fra_år}&"
    if til_år:
        års_model_filter += f"year_to={til_år}"
    return års_model_filter


def kilometer_filter(fra_km=None, til_km=None):
    km_stand_filter = ""
    if fra_km:
        km_stand_filter += f"mileage_from={fra_km}&"
    if til_km:
        km_stand_filter += f"mileage_to={til_km}"
    return km_stand_filter


def pris_filter(fra_pris=None, til_pris=None):
    pris_filter = ""
    if fra_pris:
        pris_filter += f"price_from={fra_pris}&"
    if til_pris:
        pris_filter += f"price_to={til_pris}"
    return pris_filter
