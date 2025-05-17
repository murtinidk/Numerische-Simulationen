class Node:
    def __init__(self, index, realX, realY):
        self.index = int(index)
        self.realX = realX
        self.realY = realY
        self.dirichletBoundary = None
        self.rightVonNeumannBoundary = None
        self.belowVonNeumannBoundary = None

    def SetDirichletBoundary(self, Boundary: float):
        assert self.dirichletBoundary is None, "Can't set dirichlet: already set"
        assert self.vonNeumannBoundary is None, "Can't set dirichlet: vonNeumann is already set"
        self.gaussBoundary = Boundary

    def GetDirichletBoundary(self):
        return self.dirichletBoundary

    #the vonNeumann is the flux over the edge in the clockwise x, and then y direction
    def SetRightVonNeumannBoundary(self, Boundary: float):
        assert self.rightVonNeumannBoundary is None, "Can't set vonNeumann: already set"
        assert self.dirichletBoundary is None, "Can't set vonNeumann: dirichlet is already set"
        self.rightVonNeumannBoundary = Boundary

    def GetRightVonNeumannBoundary(self):
        return self.rightVonNeumannBoundary
    
    def SetBelowVonNeumannBoundary(self, Boundary: float):
        assert self.belowVonNeumannBoundary is None, "Can't set vonNeumann: already set"
        assert self.dirichletBoundary is None, "Can't set vonNeumann: dirichlet is already set"
        self.belowVonNeumannBoundary = Boundary

    def GetBelowVonNeumannBoundary(self):
        return self.belowVonNeumannBoundary
        
    def GetIndex(self):
        return self.index

    def GetCoordinates(self):
        return (self.realX, self.realY)
    
    def GetX(self):
        return self.realX
    
    def GetY(self):
        return self.realY