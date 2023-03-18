
class Sorterer:
    def __init__(self, bil_liste):
        self.bil_liste = bil_liste

    def sorter_pris_per_gått_km(self, bil):
        return bil.kmstand

    def sorter_liste(self):
        self.bil_liste.sort(reverse=True, key=lambda bil: bil.kmstand)