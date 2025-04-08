import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese!")
            self._view.update_page()
            return

        avgMilano, avgTorino, avgGenova = self._model.get_all_situazioni(self._mese)
        self._view.lst_result.controls.append(ft.Text("L'umidità media del mese selezionato è:"))
        self._view.lst_result.controls.append(ft.Text(f"Milano: {round(avgMilano, 3)}"))
        self._view.lst_result.controls.append(ft.Text(f"Torino: {round(avgTorino, 3)}"))
        self._view.lst_result.controls.append(ft.Text(f"Genova: {round(avgGenova, 3)}"))
        self._view.update_page()
        return



    def handle_sequenza(self, e):
        pass

    def read_mese(self, e):
        self._mese = int(e.control.value)

