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

