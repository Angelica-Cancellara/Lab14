import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._idMap = {}
        self._edges = []
        self._bestPath = []
        self._bestScore = 0

    def getBestPath(self, partenza):
        self._bestPath = []
        self._bestScore = 0
        source = self._idMap[int(partenza)]

        parziale = [source] #devo partire da questo nodo
        for n in self._graph.successors(source):
            parziale.append(n)
            self.ricorsione(parziale)
            parziale.pop()

        return self._bestPath, self._bestScore

    def ricorsione(self, parziale):
        if self.calcolaPeso(parziale) > self._bestScore:
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = self.calcolaPeso(parziale)

        for s in self._graph.successors(parziale[-1]):
            if s not in parziale and self._graph[parziale[-1]][s]["weight"] < self._graph[parziale[-2]][parziale[-1]]["weight"]:
                parziale.append(s)
                self.ricorsione(parziale)
                parziale.pop()

    def calcolaPeso(self, parziale):
        peso = 0
        for i in range(0, len(parziale)-1):
            peso += self._graph[parziale[i]][parziale[i+1]]['weight']
        return peso

    def buildGraph(self, store, k):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(store)
        self._graph.add_nodes_from(self._nodes)
        self._idMap = {}
        for n in self._nodes:
            self._idMap[n.order_id] = n
        self._edges = DAO.getArchi(store, k, self._idMap)
        for e in self._edges:
            self._graph.add_edge(e[0], e[1], weight=e[2])

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def camminoMassimo(self, nodoPartenza):
        source = self._idMap[int(nodoPartenza)]
        self._camminoMassimo = []
        cammino = []

        #calcola tutti i nodi raggiungibili dal nodoPartenza
        tree = nx.dfs_tree(self._graph, source)
        nodi = list(tree.nodes())

        for n in tree.nodes:
            cammino = [n]

            while cammino[0] != source:
                pred = nx.predecessor(tree, source, cammino[0]) #trova il predecessore di source tra source e cammino[0]
                cammino.insert(0, pred[0])

            if len(cammino) > len(self._camminoMassimo):
                self._camminoMassimo = copy.deepcopy(cammino)

        return self._camminoMassimo

    def getAllStores(self):
        return DAO.getAllStores()

    def getAllNodes(self):
        return self._graph.nodes()