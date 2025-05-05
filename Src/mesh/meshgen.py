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
    resolution = Data.getResolution()
    res_height = round(height*resolution)
    res_width = round(width*resolution)
    coords_height, coords_width = np.meshgrid(np.linspace(0.0, height - (height/resolution), resolution), np.linspace(0.0, width - (width/resolution), resolution))
    coords = np.vstack([coords_height.ravel(), coords_width.ravel()]).T
    for i in coords:
        print(i)
        mesh.append(node.Node(index, i[0], i[1]))
        index += 1
    """"
    for x in range( Data.getWidth()):
        for y in range(0, Data.getHeight()):
            mesh.append(node.Node(index, float(x)/ (Data.getWidth()-1), float(y)/ (Data.getHeight()-1)))
            index += 1
    """
    Data.setMesh(mesh)
    print(f"Mesh generated with width={Data.getWidth()}, height={Data.getHeight()}, resolution={Data.getResolution()}, boundary={Data.getBoundary()}")
    # Function to generate a mesh for the simulation
    # This function will create a mesh based on the specified parameters and return it