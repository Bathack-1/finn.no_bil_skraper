
class Bil:
    def __init__(self, navn, link, annonse_id):
        self.navn = navn
        self.link = link
        self.annonse_id = annonse_id
        self.ekstra_info = {"hovedbatteri": "ikke nevnt"}

        self.pris = None
        self.år = None
        self.kmstand = None
        self.bilde = None
        self.annonse_opprettelsesdato = None
        self.beskrivelse = None
        self.spesifikasjoner = None
        self.lokasjon = None
