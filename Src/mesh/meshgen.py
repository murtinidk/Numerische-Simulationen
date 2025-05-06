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
    """res_width = round(width*xResolution)
    res_height = round(height*yResolution)
    coords_height, coords_width = np.meshgrid(, )
    coords = np.vstack([coords_height.ravel(), coords_width.ravel()]).T
    for i in coords:
        mesh.append(node.Node(index, i[1], i[0]))
        index += 1"""
    coords_height = np.linspace(0.0, height, yResolution)
    coords_width = np.linspace(0.0, width, xResolution)
    coords_width_grid, coords_height_grid = np.meshgrid(coords_width, coords_height)
    indexes = np.linspace(0, yResolution * xResolution - 1, yResolution * xResolution, dtype= int)
    combinations = np.stack((indexes, coords_width_grid.ravel(), coords_height_grid.ravel()), axis=-1).reshape(-1, 3)
    mesh = np.array(list(map(lambda x: node.Node(*x), combinations)))


    Data.setMesh(mesh)

    #TODO add boundary conditioins here
    
    #IEN
    IEN = dict()
    mesh_size = len(mesh)
    # Total number of possible cells (elements)
    num_cells = (yResolution - 1) * (xResolution - 1)
    cell_indices = np.arange(num_cells)
    # Compute indices of each corner
    i_TL = cell_indices
    i_BL = cell_indices + 1
    i_TR = cell_indices + xResolution
    i_BR = cell_indices + xResolution + 1
    # Filter indices that are in bounds
    valid_TL = i_TL[i_TL < mesh_size]
    valid_BL = i_BL[i_BL < mesh_size]
    valid_TR = i_TR[i_TR < mesh_size]
    valid_BR = i_BR[i_BR < mesh_size]
    IEN.update({(0, i): mesh[i].GetIndex() for i in valid_TL})
    IEN.update({(1, i - 1): mesh[i].GetIndex() for i in valid_BL})
    IEN.update({(2, i - xResolution): mesh[i].GetIndex() for i in valid_TR})
    IEN.update({(3, i - xResolution - 1): mesh[i].GetIndex() for i in valid_BR})
    Data.setIEN(IEN)
    
    #NE
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