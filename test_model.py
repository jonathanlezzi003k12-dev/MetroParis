#provo il mio build graphlib
from model.fermata import Fermata
from model.model import Model




model=Model()
print("Numero nodi:",model.get_numnodi())
model.buildGraphPesato()
print("Numero nodi:",len(model._grafo.nodes))
print("Numero nodi:",model.get_numarchi())



source=Fermata(2,"Abbesses",2.33855,488843)
#source è un oggetto di tipo fermata
nodiBFS=model.getBFSNodesFromEdge(source)
nodiDFS=model.getDFSNodesFromEdge(source)
for i in range (0,10):
    print(nodiBFS[i])
print("=======================================================================")
for i in range (0,10):
    print(nodiDFS[i])

print("=======================================================================")
print ("Archi con peso 2 ")
archiMaggiori=model.getArchiPesoMaggiore()
for a in archiMaggiori:
    print(a[0],"->",a[1],":",a[2])
