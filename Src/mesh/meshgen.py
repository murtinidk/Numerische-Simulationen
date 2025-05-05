#- this file contains declarations and implementations for generating a FEM simulation mesh
#- Numerische Simulationen für Digital Engineering, SS 2025
#- Gruppe 6: Ram Abhay, Figo Tobias, Thalmayr Martin

#imports
import data.node as node
from main import Data
import numpy as np

# declarations

def meshgen():
    global Data
    
    mesh = []
    index = 0
    width = Data.getWidth()
    height = Data.getHeight()
    xResolution = Data.getXResolution()
    yResolution = Data.getYResolution()
    res_width = round(width*xResolution)
    res_height = round(height*yResolution)
    coords_height, coords_width = np.meshgrid(np.linspace(0.0, height, yResolution), np.linspace(0.0, width, xResolution))
    coords = np.vstack([coords_height.ravel(), coords_width.ravel()]).T
    for i in coords:
        mesh.append(node.Node(index, i[1], i[0]))
        index += 1

    Data.setMesh(mesh)

    #TODO add boundary conditioins here

    nodesWithoutDirichlet = list(filter(lambda x: x.GetBoundary != "Dirichlet" ,mesh))
    #filter for ones without Dirichlet 
    eqId = list(range(nodesWithoutDirichlet.__sizeof__()))
    #select their index value
    nodesWithoutDirichlet = list(map(lambda n: n.GetIndex(), nodesWithoutDirichlet))
    NE = dict(zip(nodesWithoutDirichlet, eqId))
    Data.setNE(NE)



    print(f"Mesh generated with width={Data.getWidth()}, height={Data.getHeight()}, xResolution={Data.getXResolution()}, yResolution={Data.getYResolution()}, boundary={Data.getBoundary()}")
    # Function to generate a mesh for the simulation
    # This function will create a mesh based on the specified parameters and return it