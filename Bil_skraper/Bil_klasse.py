
class Bil:
    def __init__(self, navn, link, annonse_id):
        self.navn = navn
        self.link = link
        self.annonse_id = annonse_id

        self.pris = None
        self.år = None
        self.kmstand = None
        self.byttet_hovedbatteri = False
