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
    applyDirichletBoundaryConditions(mesh, width, height,xResolution, yResolution,{
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
        

    

def calculateLineFunc(line, node_id_array,node_id_dist,resolution,mesh):
    unique_node_ids = np.unique(np.array(node_id_array, dtype=int))
    for i in unique_node_ids:
        if callable(line[4]):
            spec_dist = node_id_dist[node_id_dist[:, 0 ] == i, 1]
            min_id = np.argmin(spec_dist)
            #find original id in array
            indices_node = np.where(node_id_dist[:,0] == i)[0]
            org_id = indices_node[min_id]
            #calulate the function value normal from line to node
            func_value = line[4](np.sqrt((abs(line[2]-line[0])/resolution*org_id)**2+(abs(line[3]-line[1])/resolution*org_id)**2))
            mesh[i].SetDirichletBoundary(func_value)
        else:
            mesh[i].SetDirichletBoundary(line[4])

def applyDirichletBoundaryConditions(nodes, width, height, xres, yres, dirichlet_arrays):
    if dirichlet_arrays is None or len(dirichlet_arrays) != 4:
        raise Exception("dirichlet arrays not correctly initialized")
    
    #calculate the corner node ids
    TL = 0
    TR = xres-1
    BL = len(nodes)-xres
    BR = len(nodes)-1
    
    #calculate the edge node ids excluding corners
    idx_top = np.arange(TL+1, TR)
    idx_bottom = np.arange(BL+1, BR)
    idx_left = np.arange(TL+xres, BL, xres)
    idx_right = np.arange(TR+xres, BR, xres)
    
    #location : type, value array without corners, node ids without corners
    edges = {
        "top":    (gui.getTopBoundaryType(), dirichlet_arrays["top"],idx_top),
        "bottom": (gui.getBottomBoundaryType(), dirichlet_arrays["bottom"],idx_bottom),
        "left":   (gui.getLeftBoundaryType(), dirichlet_arrays["left"],idx_left),
        "right":  (gui.getRightBoundaryType(), dirichlet_arrays["right"],idx_right)
    }
    #print(edges)
    
    #check array lengths
    for edge in edges:
        edge_type, dirichlet_array, idx = edges[edge]
        if len(idx)+2 != len(dirichlet_array):
            raise Exception(edge + "edge array not of correct length")
    
    
    #apply edge values
    for edge in edges:
        edge_type, dirichlet_array, idx = edges[edge]
        if edge_type == "dirichlet":
            #apply dirichlet values
            for i, node_id in enumerate(idx):
                #+1 to skip first value in the array -> corner value
                if dirichlet_array[i+1] is not None:
                    nodes[node_id].SetDirichletBoundary(dirichlet_array[i+1])
    
    #apply corner values
    #check corner intersection -> avg val of neighboring nodes
    corners_values = {
        "TL": (TL,  dirichlet_arrays["top"][0], dirichlet_arrays["left"][0]),
        "TR": (TR,  dirichlet_arrays["top"][-1], dirichlet_arrays["right"][0]),
        "BL": (BL,  dirichlet_arrays["bottom"][0], dirichlet_arrays["left"][-1]),
        "BR": (BR,  dirichlet_arrays["bottom"][-1], dirichlet_arrays["right"][-1])
    }
    corners_neighbors_values = {
        "TL": (nodes[TL+1].GetDirichletBoundary(), nodes[TL+xres].GetDirichletBoundary()),
        "TR": (nodes[TR-1].GetDirichletBoundary(), nodes[TR+xres].GetDirichletBoundary()),
        "BL": (nodes[BL+1].GetDirichletBoundary(), nodes[BL-xres].GetDirichletBoundary()),
        "BR": (nodes[BR-1].GetDirichletBoundary(), nodes[BR-xres].GetDirichletBoundary())
    }
    #print(corners_values)
    #print(corners_neighbors_values)
    for corner in corners_values:
        idx, valA, valB = corners_values[corner]
        neighborA, neighborB = corners_neighbors_values[corner]
        #average: both neighbors are set, two corner values are set
        if neighborA != None and neighborB != None and valA != None and valB != None:
            nodes[idx].SetDirichletBoundary((neighborA + neighborB) / 2)
        # elif valA != None:
        #     nodes[idx].SetDirichletBoundary(valA)
        # elif valB != None:
        #     nodes[idx].SetDirichletBoundary(valB)
        #TODO: needs to be reworked
    

def removeEdgeNodes(nodes):
    xmin = 0
    xmax = max(nodes[:,1])
    ymin = 0
    ymax = max(nodes[:,2])
    conditions = ((nodes[:,1] > xmin) & (nodes[:,1] < xmax) & (nodes[:,2] > ymin) & (nodes[:,2] < ymax))
    return nodes[conditions]
