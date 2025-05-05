#- this file contains declarations and implementations for storing the data between steps of the simulation
#- it might be extended to load savepoints in the future
#- Numerische Simulationen für Digital Engineering, SS 2025
#- Gruppe 6: Ram Abhay, Figo Tobias, Thalmayr Martin

import interface.gui

class DataClass:
    def __init__(self):
        self.hasSize = False
        self.width = None	
        self.height = None
        self.boundary = None
        self.hasMesh = False
        self.mesh = None
        
    def reset(self):
        if self.hasSize:
            self.__init__()
      
    def setSize(self, width, height, boundary):
        self.width = width
        self.height = height
        self.boundary = boundary
        self.hasSize = True
      
    def hasSize(self):
        return self.hasSize
    def getWidth(self):
        if(not self.hasSize):
            raise Exception("Size not set!")
        return self.width
    def getHeight(self):
        if(not self.hasSize):
            raise Exception("Size not set!")
        return self.height
    def getBoundary(self):
        if(not self.hasSize):
            raise Exception("Size not set!")
        return self.boundary

    def setMesh(self, mesh):
        if(self.hasMesh):
            raise Exception("Mesh already set!")
        self.mesh = mesh
        self.hasMesh = True
        interface.gui.updateGui()
    def hasMesh(self):
        return self.hasMesh
    def getMesh(self):
        if(not self.hasMesh):
            raise Exception("Mesh not set!")
        return self.mesh