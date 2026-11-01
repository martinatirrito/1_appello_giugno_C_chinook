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

    def handleSelezione(self, e):
        self._view._txt_result.controls.clear()

        # validazione 1: grafo creato
        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        # validazione 2: artista scelto
        if self._view._ddArtista.value is None:
            self._view.create_alert("Selezionare un artista.")
            return

        # validazione 3: N intero (anche il campo vuoto "" dà ValueError)
        try:
            N = int(self._view._txtInN.value)
        except (ValueError, TypeError):
            self._view.create_alert("Inserire un numero intero per N.")
            return

        # validazione 4: N positivo (lo chiede il testo)
        if N < 1:
            self._view.create_alert("N deve essere un intero positivo.")
            return

        # stringa -> int -> OGGETTO Artist (il Model vuole l'oggetto)
        start = self._model.getArtistById(int(self._view._ddArtista.value))
        if start is None:
            self._view.create_alert("Artista non presente nel grafo.")
            return

        gruppo, totBrani = self._model.getBestGroup(start, N)  # spacchetto 2 valori

        # nessun gruppo valido (N troppo grande o vincolo peso 1 troppo stretto)
        if len(gruppo) == 0:
            self._view._txt_result.controls.append(
                ft.Text(f"Nessun gruppo di {N} artisti trovato a partire da {start}."))
            self._view.update_page()
            return

        self._view._txt_result.controls.append(ft.Text("Artisti selezionati:"))
        # lista ordinata alfabeticamente per nome
        for a in sorted(gruppo, key=lambda x: x.Name):
            self._view._txt_result.controls.append(
                ft.Text(f"{a.Name} - brani: {len(a.Tracks)} - playlist: {len(a.Playlists)}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di artisti selezionati: {len(gruppo)}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero complessivo di brani: {totBrani}"))
        self._view.update_page()
