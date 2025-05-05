class Node:
    def __init__(self, index, realX, realY):
        self.index = index
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