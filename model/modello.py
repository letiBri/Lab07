import copy

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []

    def get_all_situazioni(self, mese):
        listaTotale = MeteoDao.get_all_situazioni()
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

    def calcola_sequenze(self, mese):
        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []
        situazioni = MeteoDao.get_situazioni_meta_mese(mese)
        self._ricorsione([], situazioni)
        return self.soluzione_ottima, self.costo_ottimo

    def trova_possibili_step(self, parziale, lista_situazioni):
        giorno = len(parziale) + 1  # a me serve cercare per il giorno successivo alla lunghezza del parziale
        candidati = []
        for situazione in lista_situazioni:
            if situazione.data.day == giorno:
                candidati.append(situazione)
        return candidati

    def is_admissible(self, candidate, parziale):
        if len(parziale) == 0:  # posso andare dove voglio il giorno 0
            return True
        # vincolo sui 6 giorni
        counter = 0
        for situazione in parziale:
            if situazione.localita == candidate.localita:
                counter += 1
        if counter >= 6:
            return False

        # vincolo sulla permanenza
        # guardo i tre giorni precedenti
        # 1) lunghezza di parziale minore di 3
        # se non ci sono 3 giorni precedenti, allora sono all'inizio e quindi devo per forza mettere l'ultima città visitata
        if len(parziale) < 3:
            if candidate.localita != parziale[0].localita:
                return False

        # 2) le tre situazioni precedenti non sono tutte uguali
        # se invece non sono tutti nella stessa città, allora devo per forza mettere la città dell'ultimo di quei 3 gg
        else:
            if (parziale[-3].localita != parziale[-2].localita) or (parziale[-3].localita != parziale[-1].localita) or (parziale[-2].localita != parziale[-1].localita):
                if parziale[-1].localita != candidate.localita:
                    return False
        # 3)
        # se sono tutti nelle stessa città, allora posso mettere qualsiasi città, sempre considerando il vincolo precedente
        return True

    def calcola_costo(self, parziale):
        costo = 0
        # 1) costo umidita
        for situazione in parziale:
            costo += situazione.umidita

        # 2) costo su spostamenti
        for i in range(1, len(parziale)):
            # se devo cambiare città in due giorni successivi, pago 100
            if parziale[i-1].localita != parziale[i].localita:
                costo += 100
            # se i due giorni precedenti non sono stato nella stessa città in cui sono ora, pago 100
            # if i >= 2 and (parziale[i-1].localita != parziale[i].localita or parziale[i-2].localita != parziale[i].localita):
            #     costo += 100
        return costo

    def _ricorsione(self, parziale, lista_situazioni):
        # condizione terminale
        if len(parziale) == 15:
            self.n_soluzioni += 1
            costo = self.calcola_costo(parziale)
            if self.costo_ottimo == -1 or self.costo_ottimo > costo:
                self.costo_ottimo = costo
                self.soluzione_ottima = copy.deepcopy(parziale)
            #print(f"{costo} ||| {parziale}")

        # condizione ricorsivo
        else:
            # cercare le città per il giorno che mi serve
            # provo ad aggiungere una di queste città e vado avanti
            candidates = self.trova_possibili_step(parziale, lista_situazioni)
            for candidate in candidates:
                # verifica vincoli
                if self.is_admissible(candidate, parziale):
                    parziale.append(candidate)
                    self._ricorsione(parziale, lista_situazioni)
                    parziale.pop()  # backtracking


if __name__ == '__main__':
    my_model = Model()
    print(my_model.calcola_sequenze(1))
    print(f"costo ottimo: {my_model.costo_ottimo}")
    print(f"numero iterazioni: {my_model.n_soluzioni}")






