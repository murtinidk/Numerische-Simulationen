class Node:
    def __init__(self, index, realX, realY):
        self.index = int(index)
        self.realX = realX
        self.realY = realY
        self.dirichletBoundary = None
        #if self.index == 1:
        #    self.dirichletBoundary = 0
        #if self.index == 8:
        #    self.dirichletBoundary = 2
        self.rightVonNeumannBoundary = None
        self.belowVonNeumannBoundary = None
        # if self.index == 1:
        #     self.belowVonNeumannBoundary = 1
        #if self.realY == 0:
        #    self.dirichletBoundary = 0
        #if self.realY == 1:
        #    self.dirichletBoundary = 2
        self.result = None
        self.lineAddition = 0

    def SetLineAddition(self, additon: float):
        self.lineAddition += additon
    
    def GetLineAddition(self):
        return self.lineAddition

    def SetResult(self, result: float):
        assert self.result is None, "Can't set result: already set"
        assert self.dirichletBoundary is None, "Can't set result: dirichlet is already set"
        self.result = result

    def GetResult(self):
        return self.result

    def GetValue(self):
        assert self.result is not None or self.dirichletBoundary is not None, "Tried accesing Value of Element not set"
        if self.result is not None:
            return self.result
        else:
            return self.dirichletBoundary

    def SetDirichletBoundary(self, Boundary: float):
        #assert self.dirichletBoundary is None, "Can't set dirichlet: already set"
        #assert self.vonNeumannBoundary is None, "Can't set dirichlet: vonNeumann is already set"
        #node has no vonNeumannBoundary attribute
        self.dirichletBoundary = Boundary

    #updates the value: averages old and new given value, used e.g for corner boundary intersections
    def UpdateDirichletBoundary(self, Boundary:float):
        current = self.dirichletBoundary
        self.dirichletBoundary = (current + Boundary) / 2
        print("Multiple dirichlet values for node " + str(self.index)+ ",averaged")
        
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