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
    # Function to generate a mesh for the simulation
    # This function will create a mesh based on the specified parameters and return it

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

#generates edge node ids in a dict, excluding corners
def getEdgeNodeIds(corners:dict,xres:int) -> dict:
    return {
        "top"    :    np.arange(corners["TL"]+1, corners["TR"]),
        "bottom" :    np.arange(corners["BL"]+1, corners["BR"]),
        "left"   :    np.arange(corners["TL"]+xres, corners["BL"], xres),
        "right"  :    np.arange(corners["TR"]+xres, corners["BR"], xres)
    }


'''
---------------------- Dirichlet Corner intersection logic ----------------------------------
function that averages dirichlet values of neighboring nodes, ignores none values, example:
(T) ... Target node with intersection, averages values of non-None neighboring nodes
(L,R,T,B) ... Neighboring nodes

    (T) 
(L) (T) (R)
    (B) 

-> if for example only (L) is set, it returns the value of (L) 
-> if (L) and (R) are set, it returns the average of (L) and (R)
-> for example BR corner, if (L) and (T) are none returns None   
'''
def getDirichletCornerValue(target_idx:int, nodes, xres:int) -> float:
 
    
    neighbor_indexes_dict = getNeighboringIndexes(target_idx, xres, nodes)

    neighbor_values = []
    
    for neighbor_key in neighbor_indexes_dict:
        index = neighbor_indexes_dict[neighbor_key]         #isInBounds check already in getNeighboringIndexes -> only valid indexes
        value = nodes[index].GetDirichletBoundary()         #get the dirichlet value of the neighbor node
        if value is not None:                               #ignore None values
            neighbor_values.append(value)                   #add to the list if not None
    if len(neighbor_values) > 0:                     
        # if one -> return the value (sum = value, len = 1)
        # if more than one (should be 2)-> return the average
        return sum(neighbor_values) / len(neighbor_values)
    else:
        return None                                             #for example no edges from corner set, return None 

'''
returns indexes of neighboring nodes, as defined in function above 
-> since mesh is 1d array, check if truly a neighbor using (x,y)-coords
'''
def getNeighboringIndexes(target_idx:int, xres:int, nodes):
    target_x, target_y = nodes[target_idx].GetX(), nodes[target_idx].GetY()
    #use array of dict to define neighbors, with offset and expected coordinate
    #example: left neighbor has offset -1, and must have the same y-coordinate as target node
    neighbor_definitions = [
        {"offset": -1,   "coord": lambda node: node.GetY(), "expected_coord": target_y},  #left
        {"offset": +1,   "coord": lambda node: node.GetY(), "expected_coord": target_y},  #right
        {"offset": -xres,"coord": lambda node: node.GetX(), "expected_coord": target_x},  #top
        {"offset": +xres,"coord": lambda node: node.GetX(), "expected_coord": target_x}   #bottom
    ]
    neighbor_definition_dict = {
        "left":   {"offset": -1,   "coord": lambda node: node.GetY(), "expected_coord": target_y},  #left
        "right":  {"offset": +1,   "coord": lambda node: node.GetY(), "expected_coord": target_y},  #right
        "top":    {"offset": -xres,"coord": lambda node: node.GetX(), "expected_coord": target_x},  #top
        "bottom": {"offset": +xres,"coord": lambda node: node.GetX(), "expected_coord": target_x}   #bottom
    }
    neighbor_indexes = {} #empty dict
    for definition_key in neighbor_definition_dict:
        definition_dict = neighbor_definition_dict[definition_key]
        potential_idx = target_idx + definition_dict["offset"]
        if isInBounds(potential_idx, nodes):
            potential_neighbor_node = nodes[potential_idx]
            #check if potential idx matches the expected coordinate (float comparison)
            if  np.isclose(definition_dict["expected_coord"],
                            definition_dict["coord"](potential_neighbor_node)):
                neighbor_indexes[definition_key] = potential_idx
                
    return neighbor_indexes

#checks if index is in bounds of mesh indexes
def isInBounds(index:int, nodes) -> bool:
    num_nodes = len(nodes)
    #check if index is within bounds of the mesh
    return index >= 0 and index < num_nodes

#function to apply boundary conditions to mesh. expects a dict with values for each edge.
#skips None-Values in arrays, or if boundary condition not set.
def applyBoundaryConditions(mesh,xres:int, value_arrays:dict) -> None:
    if value_arrays is None or len(value_arrays) != 4:
        raise Exception("edge value arrays not correctly initialized")
    corner_idxs_dict = getCornerNodeIds(len(mesh), xres)
    edge_idxs_dict = getEdgeNodeIds(corner_idxs_dict, xres)
    #create edge dict: location : type, value array with corners, node ids without corners
    edges = {
        "top":    (gui.getTopBoundaryType(), value_arrays["top"], edge_idxs_dict["top"]),
        "bottom": (gui.getBottomBoundaryType(), value_arrays["bottom"], edge_idxs_dict["bottom"]),
        "left":   (gui.getLeftBoundaryType(), value_arrays["left"], edge_idxs_dict["left"]),
        "right":  (gui.getRightBoundaryType(), value_arrays["right"], edge_idxs_dict["right"])
    }
    #apply the edge values, excluding corners
    for edge in edges:
        edge_type, value_array, edge_indexes = edges[edge]
        if edge_type == "dirichlet":
            #apply dirichlet values
            #value_array[0] is for corner, value_array[1] for the first edge node
            for i, node_mesh_idx in enumerate(edge_indexes):
                value_for_node = value_array[i+1]
                if value_for_node is not None:
                    mesh[node_mesh_idx].SetDirichletBoundary(value_for_node)
        if edge_type == "neumann":
            print(value_arrays[edge])
            #TODO: duplicate code -> put into dict 
            if edge == "top" or edge == "bottom":
                #apply neumann values to right von Neumann boundary
                for i, node_mesh_idx in enumerate(edge_indexes):
                    value_for_node = value_array[i+1]
                    if value_for_node is not None:
                        mesh[node_mesh_idx].SetRightVonNeumannBoundary(value_for_node)
            if edge == "left" or edge == "right":
                #apply neumann values to right von Neumann boundary
                for i, node_mesh_idx in enumerate(edge_indexes):
                    value_for_node = value_array[i+1]
                    if value_for_node is not None:
                        mesh[node_mesh_idx].SetBelowVonNeumannBoundary(value_for_node)
            else:
                print("Neumann boundary not implemented yet:"+ edge + " edge application skipped")
    
    #apply corner logic

    #dirichlet corner logic application
    for corner in corner_idxs_dict:
        corner_idx = corner_idxs_dict[corner]
        value = getDirichletCornerValue(corner_idx, mesh, xres)
        if value is not None:
            mesh[corner_idx].SetDirichletBoundary(value)
        else:
            print("No dirichlet value intersection for corner " + corner + ", skipping")
    #neumann corner logic application
    for corner in corner_idxs_dict:
        corner_idx = corner_idxs_dict[corner]
        if(mesh[corner_idx].GetDirichletBoundary() != None):
            continue
        print("CORNER: " + corner + " with index " + str(corner_idx))
        neumannCornerLogic(corner_idx, mesh, xres) 
    return


'''
-------------------Neumann Corner Logic-------------------
Assumes preprocessed mesh state: 
    !-neumann boundaries applied to the domain edges
    !-dirichlet logic already applied to corners -> 
        -> corners can already have dirichlet values (one of 2 intersecting edges or avg val),
        in wich case nothing is done -> handled in function above
'''
def neumannCornerLogic(target_corner_idx:int, mesh, xres:int) -> None:
    neighbors = getNeighboringIndexes(target_corner_idx,xres,mesh)
    print(neighbors)
    #check if corner has a neumann boundary set, depending on direction of neighbor 
    neighbor_funcs = {
        "right":  lambda: (mesh[neighbors["right"]].GetRightVonNeumannBoundary(),  mesh[target_corner_idx].SetRightVonNeumannBoundary),
        "bottom": lambda: (mesh[neighbors["bottom"]].GetBelowVonNeumannBoundary(), mesh[target_corner_idx].SetBelowVonNeumannBoundary)
    }
    
    for key in neighbor_funcs:
        if key in neighbors:
            value, setter = neighbor_funcs[key]()
            if value is not None:
                setter(value)

def removeEdgeNodes(nodes):
    xmin = 0
    xmax = max(nodes[:,1])
    ymin = 0
    ymax = max(nodes[:,2])
    conditions = ((nodes[:,1] > xmin) & (nodes[:,1] < xmax) & (nodes[:,2] > ymin) & (nodes[:,2] < ymax))
    return nodes[conditions]
