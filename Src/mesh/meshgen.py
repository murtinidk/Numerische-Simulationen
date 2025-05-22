#- this file contains declarations and implementations for generating a FEM simulation mesh
#- Numerische Simulationen für Digital Engineering, SS 2025
#- Gruppe 6: Ram Abhay, Figo Tobias, Thalmayr Martin

#imports
import data.node as node
from main import Data
import numpy as np
from sklearn.neighbors import BallTree
import interface.gui as gui

# declarations

def meshgen():
    global Data
    
    gui.setStep(gui.simStep.meshGen)
    width = Data.getWidth()
    height = Data.getHeight()
    xResolution = Data.getXResolution()
    yResolution = Data.getYResolution()
    node_coords_height = np.linspace(0.0, height, yResolution)
    node_coords_width = np.linspace(0.0, width, xResolution)
    node_coords_width_grid, node_coords_height_grid = np.meshgrid(node_coords_width, node_coords_height)
    indexes = np.linspace(0, yResolution * xResolution - 1, yResolution * xResolution, dtype= int)
    combinations = np.stack((indexes, node_coords_width_grid.ravel(), node_coords_height_grid.ravel()), axis=-1).reshape(-1, 3)
    mesh = np.array(list(map(lambda x: node.Node(*x), combinations)))

    Data.setMesh(mesh)

    #finding nearest neighbours to line
    gui.setStep(gui.simStep.boundaryConditions)
    line = Data.getLine()
    if line is not None:
        resolution = 100
        xs = np.linspace(line[0], line[2], resolution)
        ys = np. linspace(line[1], line[3], resolution)
        line_coords = np.column_stack((xs, ys))
        tree = BallTree(combinations[:, 1:3], leaf_size=1, metric='euclidean')
        index = tree.query_radius(line_coords, 1, return_distance=False)
        flat_indices = np.unique(np.concatenate(index))
        print(flat_indices)

    #TODO add boundary conditioins here
    applyDirichletBoundaryConditions(mesh, width, height)
    
    gui.setStep(gui.simStep.meshTables)
    #IEN
    IEN = dict()
    mesh_size = len(mesh)
    # Total number of possible cells (elements)
    num_cells = (yResolution - 1) * (xResolution - 1)
    cell_indices = np.arange(num_cells)

    # Compute indices of each corner
    grid = np.arange(xResolution*yResolution).reshape(yResolution, xResolution)
    # drop last row and last column, then flatten
    i_TL =  grid[:-1, :-1].ravel()
    cell_index_from_TL = dict(zip(i_TL, cell_indices))
    i_TR = i_TL + 1
    i_BL = i_TL + xResolution
    i_BR = i_TL + xResolution + 1
    # Filter indices that are in bounds
    valid_TL = i_TL[i_TL < mesh_size]
    valid_TR = i_TR[i_TR < mesh_size]
    valid_BL = i_BL[i_BL < mesh_size]
    valid_BR = i_BR[i_BR < mesh_size]
    IEN.update({(0, cell_index_from_TL[i]): mesh[i].GetIndex() for i in valid_TL})
    IEN.update({(1, cell_index_from_TL[i-1]): mesh[i].GetIndex() for i in valid_TR})
    IEN.update({(2, cell_index_from_TL[i - xResolution]): mesh[i].GetIndex() for i in valid_BL})
    IEN.update({(3, cell_index_from_TL[i - xResolution - 1]): mesh[i].GetIndex() for i in valid_BR})
    Data.setIEN(IEN)
    
    #NE
    nodesWithoutDirichlet = list(filter(lambda x: x.GetDirichletBoundary() == None ,mesh))
    #filter for ones without Dirichlet 
    #eqId = list(range(nodesWithoutDirichlet.__sizeof__())) #sizeof is not the same as len, this is mem size
    eqId = list(range(len(nodesWithoutDirichlet))) #len instead of sizeof -> mem size <-> num Elements...
    #select their index value
    nodesWithoutDirichlet = list(map(lambda n: n.GetIndex(), nodesWithoutDirichlet))
    NE = dict(zip(nodesWithoutDirichlet, eqId))
    Data.setNE(NE)

    #print(f"Mesh generated with width={Data.getWidth()}, height={Data.getHeight()}, xResolution={Data.getXResolution()}, yResolution={Data.getYResolution()}, boundary={Data.getBoundary()}")
    # Function to generate a mesh for the simulation
    # This function will create a mesh based on the specified parameters and return it

def applyDirichletBoundaryConditions(nodes, width, height):
    # parse dirichlet boundary condition from GUI
    def getBoundaryData(type_func, value_func) -> tuple[str, float]:
        boundary_type = type_func()
        boundary_value_str = value_func()
        print(boundary_type, boundary_value_str)
        if boundary_type == 'dirichlet':
            return boundary_type, float(boundary_value_str)
        elif boundary_type == 'neumann':
            raise NotImplementedError("Neumann boundary condition is not implemented yet")
            #return boundary_type, float(boundary_value_str)
        else:
            raise TypeError(f"Unknown boundary type: {boundary_type}")
    
    #apply dirichlet boundary conditions to domain

    for node_obj in nodes:
        coordinates = node_obj.GetCoordinates()
        if coordinates is None:
            print(f"Node {node_obj.GetIndex()} has no coordinates")
            continue
        x, y = coordinates
        #left boundary
        if np.isclose(x, 0.0):
            btype, value = getBoundaryData(gui.getLeftBoundaryType, gui.getLeftBoundaryValue)
            if btype == 'dirichlet' and node_obj.GetDirichletBoundary() == None:
                node_obj.SetDirichletBoundary(value)
        #right boundary
        if np.isclose(x, width):
            btype, value = getBoundaryData(gui.getRightBoundaryType, gui.getRightBoundaryValue)
            if btype == 'dirichlet' and node_obj.GetDirichletBoundary() == None:
                node_obj.SetDirichletBoundary(value)
        #top boundary
        if np.isclose(y, height):
            btype, value = getBoundaryData(gui.getTopBoundaryType, gui.getTopBoundaryValue)
            if btype == 'dirichlet' and node_obj.GetDirichletBoundary() == None:
                node_obj.SetDirichletBoundary(value)
        #bottom boundary
        if np.isclose(y, 0.0):
            btype, value = getBoundaryData(gui.getBottomBoundaryType, gui.getBottomBoundaryValue)
            if btype == 'dirichlet' and node_obj.GetDirichletBoundary() == None:
                node_obj.SetDirichletBoundary(value)

