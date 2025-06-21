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
        calculateLineValues(mesh, line, combinations)

    #TODO add boundary conditioins here
    '''def createBoundaryArray(getType, length, floatValue):
        if getType == "neumann":
            raise Exception("Neumann boundary conditions not implemented yet")
        if getType == "none" or floatValue == None:
            return np.full(length, None)
        else:
            if (type(floatValue) == int or type(floatValue) == float) and getType == "dirichlet":
                return np.full(length, floatValue)
            else:
                raise Exception(floatValue + "is not a number")'''
    applyBoundaryConditions(mesh,xResolution,{
        "top":    createBoundaryArray(width, xResolution, Data.getTop()),
        "bottom": createBoundaryArray(width, xResolution, Data.getBottom()),
        "left":   createBoundaryArray(height, yResolution, Data.getLeft()),
        "right":  createBoundaryArray(height, yResolution, Data.getRight())
    })
    
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
    

def createBoundaryArray(length, res, boundary_func):
    section = np.linspace(0, length, res)    
    if callable(boundary_func):
        return np.array([boundary_func(x) for x in section])
    else:
        return np.full(res, boundary_func)


def calculateLineValues(mesh, line, combinations):
    width = Data.getWidth()
    height = Data.getHeight() 
    xRes = Data.getXResolution()
    yRes = Data.getYResolution()
    resolution = 100*int((xRes+yRes)/2)
    xIntervall = width/(xRes-1)
    yIntervall = height/(yRes-1)
    xs = np.linspace(line[0], line[2], resolution)
    ys = np. linspace(line[1], line[3], resolution)
    line_coords = np.column_stack((xs, ys))
    ds = np.sqrt((line[0]- line[2])**2 + (line[1]-line[3])**2)/resolution
    e = 1e-20
    for i in line_coords:
        node_TL_ind = int(np.floor(i[1]/yIntervall)*xRes + np.floor(i[0]/xIntervall))
        node_TR_ind = int(np.floor(i[1]/yIntervall)*xRes + np.ceil(i[0]/xIntervall))
        node_BL_ind = int(np.ceil(i[1]/yIntervall)*xRes + np.floor(i[0]/xIntervall))
        node_BR_ind = int(np.ceil(i[1]/yIntervall)*xRes + np.ceil(i[0]/xIntervall))

        node_TL_coords = combinations[node_TL_ind]
        node_TR_coords = combinations[node_TR_ind]
        node_BL_coords = combinations[node_BL_ind]
        node_BR_coords = combinations[node_BR_ind]

        dist_TL = np.sqrt((i[0]-node_TL_coords[1])**2+(i[1]-node_TL_coords[2])**2)+e
        dist_TR = np.sqrt((i[0]-node_TR_coords[1])**2+(i[1]-node_TR_coords[2])**2)+e
        dist_BL = np.sqrt((i[0]-node_BL_coords[1])**2+(i[1]-node_BL_coords[2])**2)+e
        dist_BR = np.sqrt((i[0]-node_BR_coords[1])**2+(i[1]-node_BR_coords[2])**2)+e

        if callable(line[4]):
            func_value = line[4](np.sqrt((i[0]-line_coords[0,[0]])**2+(i[1]-line_coords[0,[1]])**2))
        else:
            func_value = line[4]
        weight = 1/dist_TL + 1/dist_TR + 1/dist_BL + 1/dist_BR

        weight_TL = 1/dist_TL/weight
        weight_TR = 1/dist_TR/weight
        weight_BL = 1/dist_BL/weight
        weight_BR = 1/dist_BR/weight

        mesh[node_TL_ind].SetLineAddition(float(func_value*weight_TL*ds))
        mesh[node_TR_ind].SetLineAddition(float(func_value*weight_TR*ds))
        mesh[node_BL_ind].SetLineAddition(float(func_value*weight_BL*ds))
        mesh[node_BR_ind].SetLineAddition(float(func_value*weight_BR*ds))
        

    




#Function to get edge and node ids, assuming a rectangular grid with TL = 0,0 , and BR -> last node
#returns corner node ids in a dict
def getCornerNodeIds(num_nodes:int, xres:int) -> dict:
    return {
        "TL" : 0,
        "TR" : xres-1,
        "BL" : num_nodes-xres,
        "BR" : num_nodes-1
    }

#generates edge node ids in a dict, including corners
def getEdgeNodeIds(corners:dict,xres:int) -> dict:
    return {
        "top"    :    np.arange(corners["TL"], corners["TR"]+1),
        "bottom" :    np.arange(corners["BL"], corners["BR"]+1),
        "left"   :    np.arange(corners["TL"], corners["BL"]+1, xres),
        "right"  :    np.arange(corners["TR"], corners["BR"]+1, xres)
    }

#checks if index is in bounds of mesh indexes
def isInBounds(index:int, nodes) -> bool:
    num_nodes = len(nodes)
    #check if index is within bounds of the mesh
    return index >= 0 and index < num_nodes

#function to apply boundary conditions to mesh. expects a dict with values for each edge.
#skips None-Values in arrays, or if boundary condition not set.
#TODO: edgecase: 2x2 domain
def applyBoundaryConditions(mesh,xres:int, value_arrays:dict) -> None:
    if value_arrays is None or len(value_arrays) != 4:
        raise Exception("edge value arrays not correctly initialized")
    edge_idxs_dict = getEdgeNodeIds(getCornerNodeIds(len(mesh),xres), xres)
    
    #create edge dict: location : type, value array with corners, node ids without corners
    edges = {
        "top":    (gui.getTopBoundaryType(),    value_arrays["top"],    edge_idxs_dict["top"]),
        "bottom": (gui.getBottomBoundaryType(), value_arrays["bottom"], edge_idxs_dict["bottom"]),
        "left":   (gui.getLeftBoundaryType(),   value_arrays["left"],   edge_idxs_dict["left"]),
        "right":  (gui.getRightBoundaryType(),  value_arrays["right"],  edge_idxs_dict["right"])
    }
    
    #apply the edge values, excluding corners
    #apply dirichlet values to nodes, average them if they already have a value assigned
    for edge in edges:
        edge_type, value_array, edge_indexes = edges[edge]
        if edge_type == "dirichlet":
            # #apply dirichlet values
            # #value_array[0] is for corner, value_array[1] for the first edge node
            if (edge_indexes.size == 0):
                assert IndexError("no edge indexes?")
            for i, node_mesh_idx in enumerate(edge_indexes):
                value_for_node = value_array[i]
                if value_for_node is not None:
                    #check if node has dirichlet value set:
                    current_dirichlet_value = mesh[node_mesh_idx].GetDirichletBoundary()
                    if(current_dirichlet_value == None):
                        mesh[node_mesh_idx].SetDirichletBoundary(value_for_node)
                    else:
                        #average those values
                        # mesh[node_mesh_idx].SetDirichletBoundary((value_for_node+current_dirichlet_value)/2)
                        mesh[node_mesh_idx].UpdateDirichletBoundary(value_for_node)
    #apply neumann values. if a node already has dirichlet set, do not set neumann value
    for edge in edges:
        edge_type, value_array, edge_indexes = edges[edge]
        if edge_type == "neumann":
            print(value_arrays[edge])
            #TODO: duplicate code -> put into dict 
            if edge == "top" or edge == "bottom":
                #apply neumann values to right von Neumann boundary
                for i, node_mesh_idx in enumerate(edge_indexes-1):
                    value_for_node = value_array[i]
                    if value_for_node is not None:
                        if(mesh[node_mesh_idx].GetDirichletBoundary() is None):
                            mesh[node_mesh_idx].SetRightVonNeumannBoundary(value_for_node)
            if edge == "left" or edge == "right":
                #apply neumann values to right von Neumann boundary
                for i, node_mesh_idx in enumerate(edge_indexes):
                    value_for_node = value_array[i]
                    if value_for_node is not None:
                        if(mesh[node_mesh_idx].GetDirichletBoundary() is None):
                            mesh[node_mesh_idx].SetBelowVonNeumannBoundary(value_for_node)
    return


def removeEdgeNodes(nodes):
    xmin = 0
    xmax = max(nodes[:,1])
    ymin = 0
    ymax = max(nodes[:,2])
    conditions = ((nodes[:,1] > xmin) & (nodes[:,1] < xmax) & (nodes[:,2] > ymin) & (nodes[:,2] < ymax))
    return nodes[conditions]
