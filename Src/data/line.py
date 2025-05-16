import numpy as np
from sklearn.neighbors import BallTree

#import data.dataStorage as data

class Node:
    def __init__(self, index, realX, realY):
        self.index = int(index)
        self.realX = realX
        self.realY = realY
        self.boundary = None  # Default value for boundary nodes

    def SetBoundary(self, Boundary):
        self.boundary = Boundary
        
    def GetIndex(self):
        return self.index

    def GetCoordinates(self):
        return (self.realX, self.realY)

    def GetBoundary(self):
        return self.boundary
#mesh = data.DataClass.getMesh()

width = 10
height = 10
xResolution = 5
yResolution = 5
node_coords_height = np.linspace(0.0, height, yResolution)
node_coords_width = np.linspace(0.0, width, xResolution)
node_coords_width_grid, node_coords_height_grid = np.meshgrid(node_coords_width, node_coords_height)
indexes = np.linspace(0, yResolution * xResolution - 1, yResolution * xResolution, dtype= int)
mesh = np.stack((indexes, node_coords_width_grid.ravel(), node_coords_height_grid.ravel()), axis=-1).reshape(-1, 3)
mesh1 = np.array(list(map(lambda x: Node(*x), mesh)))

tree = BallTree(mesh[:, 1:3], leaf_size=10, metric='euclidean')
index = tree.query_radius(np.array([[4.7,4.7]]), 1, return_distance=False)
print(index)
print(mesh[index[0]])