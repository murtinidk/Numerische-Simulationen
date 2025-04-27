#- this file contains declarations and implementations for generating a FEM simulation mesh
#- Numerische Simulationen für Digital Engineering, SS 2025
#- Gruppe 6: Ram Abhay, Figo Tobias, Thalmayr Martin

#imports
import data.node as node
from main import Data

# declarations

def meshgen():
    global Data
    
    mesh = []
    index = 0
    for x in range(0, Data.getWidth()):
        for y in range(0, Data.getHeight()):
            mesh.append(node.Node(index, float(x)/ (Data.getWidth()-1), float(y)/ (Data.getHeight()-1)))
            index += 1
    
    Data.setMesh(mesh)
    print(f"Mesh generated with width={Data.getWidth()}, height={Data.getHeight()}, boundary={Data.getBoundary()}")
    # Function to generate a mesh for the simulation
    # This function will create a mesh based on the specified parameters and return it