import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):

        try:
            self._model.buildGraph()
            self._view._txt_result.controls.clear()
            Nnodi, Narchi = self._model.getGraphDetails()
            self._view._txt_result.controls.append(
                ft.Text("Grafo correttamente creato.")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di nodi: {Nnodi}")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di archi: {Narchi}")
            )

            self.fillDDArtist()

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella creazione del grafo: {ex}")


    def handleStampaInfo(self,e):
        self._view._txt_result.controls.clear()

        nNodi, nArchi = self._model.getGraphDetails()
        if nNodi == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        try:
            best_degree, max_degree = self._model.getBestArtistDegree()
            if best_degree:
                self._view._txt_result.controls.append(
                    ft.Text(f"Artista con grado maggiore: {best_degree} (grado: {max_degree})")
                )

            best_weight, max_weight = self._model.getSommaPesiIncidenti()
            if best_weight:
                self._view._txt_result.controls.append(
                    ft.Text(f"Artista con somma pesi incidenti massima: {best_weight} (somma: {max_weight})")
                )

            top10 = self._model.top10Archi()
            if top10:
                self._view._txt_result.controls.append(
                    ft.Text("Top 10 archi con peso maggiore:")
                )
                for i, (u, v, weight) in enumerate(top10, 1):
                    self._view._txt_result.controls.append(
                        ft.Text(f"{i}. {u} -- {v} (peso: {weight})")
                    )
            else:
                self._view._txt_result.controls.append(
                    ft.Text("Nessun arco trovato.")
                )

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella stampa delle info: {ex}")

    def fillDDArtist(self):
        self._view._ddArtista.options.clear()
        artisti = self._model.getArtist()
        for a in artisti:
            self._view._ddArtista.options.append(ft.dropdown.Option(str(a.ArtistId), text=str(a)))

        self._view.update_page()

    def handleSelezione(self,e):
        pass