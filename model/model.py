from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo=nx.DiGraph()
        #================================
        #importantissimo
        #creo un dizionario che ha come chiave l'id della fermata
        #e come oggetto la fermata stessa
        #a cosa mi serve ?
        #riga 45 io mi prendo dal database un oggetto di tipo connessione e poi mi estraggo
        #l'id della fermata in quanto è in comune nella tabella dell'oggetto
        #ora avendo l'id della fermata e il dizionario che ha chiave proprio l'id
        #della fermata posso risalire ai dati della fermata

        self._idMapFermate={}
        for f in self._fermate:
            #quà mi sono salvato tutte le fermate in un dizionario con chiave l'id della fermata
            self._idMapFermate[f.id_fermata]=f


    #creazione di un grafo in cui il numero di collegamenti tra due nodi
    #rappresenta il numero di archi che li collegano; cioè se due vertici
    #sono collegati tra loro attraverso 3 archi distinti il peso sarà pari a tre

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati()

    def addEdgesPesati(self):
         #riutilizzo il principio di funzionamento di add eges tre
        self._grafo.clear_edges()
        alledges=DAO.getAllEdges()
        for conn in alledges:

            u=self._idMapFermate[conn.id_stazP]
            v=self._idMapFermate[conn.id_stazA]
            #se l'arco esiste incrementiamo il peso
            if self._grafo.has_edge(u,v):
                self._grafo[u][v]["weight"]+=1
            #se non esiste lo creiamo
            else:
                self._grafo.add_edge(u,v,weight=1)

    def addEdgesPesatiV2(self):
        #delega il calcolo del peso alla quiry sql per semplificare
        #il codice in python
        self.grafo.crear_edges()
        #lista di tuple con id staz partenza id staz arrivo peso
        allEdgesWPeso=DAO.getAllEdgesPesati()
        for e in allEdgesWPeso:
            #devo recuperare la stazione a partire dall'id
            #e per questo abbiamo l'idmapp
            u=self._idMapFermate[e[0]]
            v=self._idMapFermate[e[1]]
            peso=e[2]
            self._grafo.add(u,v,weight=peso)


    def getArchiPesoMaggiore(self):
        #il data = True serve a salvare tutti gli archi con i propi attributi
        #in questo caso ci serve perchè dobbiamo salvare il peso
        #di defaulti è False
        edges =self._grafo.edges(data=True )
        edgesMaggiori=[]
        for e in edges:
            if self._grafo.get_edge_data(e[0],e[1])["weight"]>1:
                #oppure posso scrivere così
                #self._grafo[e[0]][e[1]]["weight"]
                edgesMaggiori.append(e)
        return edgesMaggiori







    def getBFSNodesFromEdge(self,source):#esploro questo grafo per livelli utilizzando gli archi
        #sono  delle iterable di tuple
        archi=nx.bfs_edges(self._grafo,source)
        #spacchetto una tupla in nodo di partenza e di arrivo
        nodiBFS=[]
        for u,v in archi:
            nodiBFS.append(v)
        return nodiBFS
    def getBFSNodesFromTree(self,source):
        tree=nx.bfs_tree(self._grafo,source)
    def getDFSNodesFromEdge(self,source):#esploro questo grafo per livelli utilizzando gli archi
        #sono  delle iterable di tuple
        archi=nx.dfs_edges(self._grafo,source)
        #spacchetto una tupla in nodo di partenza e di arrivo
        nodiDFS=[]
        for u,v in archi:
            nodiDFS.append(v)
        return nodiDFS
    def buildGraph(self):
        #i nodi sono le varie fermate
        #devo ogni volta svuorae il mio grafo
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addedges3()
    def addedges(self):
        #verificare tra tutte le coppie delle fermate se esiste una
        #connessione oppure no
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u,v):
                    self._grafo.add_edge(u,v)
    def addedges2(self):
        #task metto tutte le coppie di stazioni che sono connesse tra
        #di loro con un adge
        #ciclo su tutte le fermate che ho e per ognuna di esse vado
        #a prendermi i miei vicini
        #molto più semplice perchè devo fare un solo ciclo for
        for u in self._fermate:
            for conn in DAO.getvicini(u):
                v=self._idMapFermate[conn.id_stazA]#accesso al dizionario di fermate attraverso l'id della fermata estratta dall'oggetto
                                                    #di tipo connessione appena creato
                self._grafo.add_edge(u,v)
    def addedges3(self):#terza versione solo con una query
        #e andiamo ad inserire gli archi quando necessario
        alledges=DAO.getAllEdges()
        for conn in alledges:
            #mi ricavo l'id map delle corrispettive fermate
            u=self._idMapFermate[conn.id_stazP]
            v=self._idMapFermate[conn.id_stazA]
            #inserisco nel mio grafo
            self._grafo.add_edge(u,v)

    def get_numnodi(self):
        return len(self._grafo.nodes())
    def get_numarchi(self):
        return len(self._grafo.edges())


    @property
    def fermate(self):
        return self._fermate
