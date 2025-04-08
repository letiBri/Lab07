from database.meteo_dao import MeteoDao
from model.citta import Citta


class Model:
    def __init__(self):
        self.dao = MeteoDao()
        self.M = []
        self.T = []
        self.G = []

        self.Milano = Citta("Milano", 0, 0, self.M)
        self.Torino = Citta("Torino", 0, 0, self.T)
        self.Genova = Citta("Genova", 0, 0, self.G)

        self.cittaCorrente = None
        self.costo = 0
        self.percorsoMinimo = []

    def get_all_situazioni(self, mese):
        listaTotale = self.dao.get_all_situazioni()
        listaGenova = []
        listaMilano = []
        listaTorino = []

        for s in listaTotale:
            if s.localita == "Milano" and s.creaMese() == mese:
                listaMilano.append(s.umidita)
            elif s.localita == "Torino" and s.creaMese() == mese:
                listaTorino.append(s.umidita)
            elif s.localita == "Genova" and s.creaMese() == mese:
                listaGenova.append(s.umidita)
        mediaMilano = sum(listaMilano) / len(listaMilano)
        mediaTorino = sum(listaTorino) / len(listaTorino)
        mediaGenova = sum(listaGenova) / len(listaGenova)
        return mediaMilano, mediaTorino, mediaGenova

    def getSituazioni_recursion(self, mese):
        self.M.clear()
        self.T.clear()
        self.G.clear()

        lista = self.dao.getSituazioni_recursion(mese)
        for s in lista:
            if s.localita == "Milano":
                self.M.append(s)
            elif s.localita == "Torino":
                self.T.append(s)
            elif s.localita == "Genova":
                self.G.append(s)

    def recursion(self, giorno):
        if giorno == 15:
            #stampa il self.costo
            #stampa la situazione con il to string per s in percorsoMinimo
            pass
        if giorno == 0:
            m = min(self.M[0].umidita, self.T[0].umidita, self.G[0].umidita)
            if m == self.M[0].umidita:
                self.cittaCorrente = self.Milano
                self.cittaCorrente.giorniTot += 1
                self.cittaCorrente.giorniCons += 1
                self.costo += m
                self.percorsoMinimo.append(self.cittaCorrente.listaSituazioni[giorno])
                self.recursion(giorno + 1)

            # if m == self.T[0].umidita:
            #     self.citta = "T"
            #     self.Tt += 1
            #     self.Tc += 1
            #     self.costo += m
            #     self.percorsoMinimo.append(self.T[0])
            #     self.recursion(giorno + 1)
            # elif m == self.G[0].umidita:
            #     self.citta = "G"
            #     self.Gt += 1
            #     self.Gc += 1
            #     self.costo += m
            #     self.percorsoMinimo.append(self.G[0])
            #     self.recursion(giorno + 1)

        elif (self.citta + "c") < 3:
            self.costo += self.citta[giorno]



