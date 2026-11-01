import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapA = {}

    def buildGraph(self):
        self._graph.clear()
        artisti = DAO.getAllNodes()
        for a in artisti:
            self._idMapA[a.ArtistId] = a
        self._graph.add_nodes_from(artisti)

        edges = DAO.getAllEdges(self._idMapA)
        for e in edges:
            self._graph.add_edge(e.a1, e.a2, weight = e.peso)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getBestArtistDegree(self): #GRADO MAGGIORE NODO
        if len(self._graph.nodes) == 0:
            return None, 0

        max_degree = -1
        best_artist = None
        for node, degree in self._graph.degree():
            if degree > max_degree:
                max_degree = degree
                best_artist = node
        return best_artist, max_degree

    def getSommaPesiIncidenti(self): #PESI INCIDENTI MASSIMA
        if len(self._graph.nodes) == 0:
            return None, 0

        max_sum = -1
        best_artist = None
        for node in self._graph.nodes:
            weight_sum = sum(
                self._graph[node][neighbor]['weight']
                for neighbor in self._graph.neighbors(node)
            )
            if weight_sum > max_sum:
                max_sum = weight_sum
                best_artist = node
        return best_artist, max_sum

    def top10Archi(self):
        if len(self._graph.edges) == 0:
            return []

        edges_with_weights = []
        for u, v in self._graph.edges:
            u, v = sorted((u, v), key=lambda a: a.Name)
            edges_with_weights.append((u, v, self._graph[u][v]['weight']))

        edges_sorted = sorted(edges_with_weights,
                      key=lambda x: (-x[2], x[0].Name, x[1].Name))

        return edges_sorted[:10]

    def getArtist(self):
        return self._graph.nodes()

    def getBestGroup(self, starting_artist, N):
        # AZZERO tutto a ogni ricerca
        self._bestGroup = []
        self._maxTracks = 0
        self._visti = set()
        if starting_artist not in self._graph.nodes or N < 1:
            return [], 0  # sempre DUE valori
        # per la potatura: gli artisti che posso davvero raggiungere (stessa
        # componente connessa del primo), da quello con più brani
        componente = nx.node_connected_component(self._graph, starting_artist)
        self._artistiOrdinati = sorted(componente, key=lambda a: len(a.Tracks), reverse=True)
        parziale = [starting_artist]  # il primo artista è quello scelto
        self._ricorsione(parziale, N)
        return self._bestGroup, self._maxTracks

    def _ricorsione(self, parziale, N):
        # (0) OTTIMIZZAZIONE: il gruppo è un INSIEME. [A,B,C] e [A,C,B] sono la
        #     stessa soluzione e hanno le stesse estensioni: lo esploro una volta sola.
        #     frozenset = set immutabile, quindi può stare dentro un set
        chiave = frozenset(parziale)
        if chiave in self._visti:
            return
        self._visti.add(chiave)

        # (1) CASO TERMINALE: esattamente N artisti -> valuto e mi fermo
        if len(parziale) == N:
            tot = self._getTotalTracks(parziale)
            if tot > self._maxTracks:
                self._maxTracks = tot
                self._bestGroup = copy.deepcopy(parziale)  # COPIA: parziale cambia
            return

        # (2) POTATURA: anche aggiungendo gli artisti con più brani tra quelli
        #     non ancora nel gruppo (stima ottimistica: ignoro adiacenza e vincoli)
        #     non supererei il migliore -> inutile continuare.
        #     Senza, con N >= 4 ci mette minuti (il grafo è quasi completo)
        if self._stima(parziale, N) <= self._maxTracks:
            return

        # (3) provo ad aggiungere ogni candidato valido, PRIMA quelli con più brani:
        #     così trovo subito una soluzione buona e la potatura taglia di più
        candidati = sorted(self._getCandidati(parziale), key=lambda a: len(a.Tracks), reverse=True)
        for candidate in candidati:
            parziale.append(candidate)
            self._ricorsione(parziale, N)
            parziale.pop()  # backtracking

    def _stima(self, parziale, N):
        # brani del gruppo + brani dei (N - len) artisti più "grossi" fuori dal gruppo
        stima = self._getTotalTracks(parziale)
        mancanti = N - len(parziale)
        for a in self._artistiOrdinati:
            if mancanti == 0:
                break
            if a not in parziale:
                stima += len(a.Tracks)
                mancanti -= 1
        return stima

    def _getCandidati(self, parziale):
        # Candidati = vicini di QUALSIASI membro del gruppo (non solo dell'ultimo:
        # non è un cammino). Così il vincolo "adiacente ad almeno uno" è garantito.
        res = set()  # set: un vicino di due membri lo conto una volta
        for membro in parziale:
            for v in self._graph.neighbors(membro):
                if v not in parziale and self._ammissibile(v, parziale):
                    res.add(v)
        return res

    def _ammissibile(self, candidate, parziale):
        # vincolo: nessuna coppia del gruppo collegata da un arco di PESO 1
        for membro in parziale:
            if self._graph.has_edge(candidate, membro) and \
                    self._graph[candidate][membro]['weight'] == 1:
                return False
        return True

    def _getTotalTracks(self, artists):
        # somma del numero di brani di ogni artista
        return sum(len(a.Tracks) for a in artists)


