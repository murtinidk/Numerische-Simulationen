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
        self.xResolution = None
        self.yResolution = None
        self.boundary = None
        self.hasMesh = False
        self.mesh = None
        self.line = None
        self.hasLine = False
        self.hasIEN = False
        self.IEN = None
        self.hasNE = False
        self.NE = None
        self.JacobianInverseTransposeMap = dict()
        self.elementMatrixMap = dict()
        
    def reset(self):
        if self.hasSize:
            self.__init__()
    
    def setSize(self, width, height, boundary, xResolution, yResolution):
        self.width = width
        self.height = height
        self.xResolution = xResolution
        self.yResolution = yResolution
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
    def getXResolution(self):
        if(not self.hasSize):
            raise Exception("Size not set!")
        return self.xResolution
    def getYResolution(self):
        if(not self.hasSize):
            raise Exception("Size not set!")
        return self.yResolution
    def getBoundary(self):
        if(not self.hasSize):
            raise Exception("Size not set!")
        return self.boundary
    
    def setLine(self, line):
        if(self.hasLine):
            raise Exception("Line already set!")
        if line is not None:
            self.line = line
            self.hasLine = True
    def hasLine(self):
        return self.hasLine
    def getLine(self):
        if(not self.hasLine):
            return None
        return self.line

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
    
    #Knotengleichungsarray in:"Globale Knotennummer" out:"Gleichungs id"
    def setNE(self, NE) -> None:
        if(self.hasNE):
            raise Exception("NE already set!")
        self.NE = NE
        self.hasNE = True
        interface.gui.updateGui()
    def hasNE(self) -> bool:
        return self.hasNE
    def getNE(self) -> dict:
        if(not self.hasNE):
            raise Exception("NE not set!")
        return self.NE
    def getNEof(self, A) -> int:
        if(not self.hasNE):
            raise Exception("NE not set, when accessing element!")
        if(not A in self.NE):
            raise Exception("A not in NE!")
        return self.NE[A]
    
    #Elementknotenarray in:"a=lokale Knotennummer, c=Elementnummer" out:"globale Knotennummer"
    def setIEN(self, IEN) -> None:
        if(self.hasIEN):
            raise Exception("IEN already set!")
        self.IEN = IEN
        self.hasIEN = True
        interface.gui.updateGui()
    def hasIEN(self) -> bool:
        return self.hasIEN
    def getIEN(self) -> dict:
        if(not self.hasIEN):
            raise Exception("IEN not set!")
        return self.IEN
    def getIENof(self, a, c) -> int:
        if(not self.hasIEN):
            raise Exception("IEN not set, when accessing element!")
        if(not (a,c) in self.IEN):
            raise Exception("(a, c) not in IEN!")
        return self.IEN[(a, c)]
    
    #Gleichungsarray in:"a=lokale Knotennummer, c=Elementnummer" out:"Gleichungs id"
    def getEQof(self, a, c) -> int:
        return self.getNEof(self.getIENof(a, c))

    #number of elements
    def getNe(self) -> int:
        raise NotImplemented
        
    #number of nodes in element
    def getNen(self) -> int:
        return 4
    
    def addJacobianInverseTransposeToMap(self, width, height, JacobianInverseTranspose) -> None:
        self.JacobianInverseTransposeMap.update({(width, height): JacobianInverseTranspose})
    def getJacobianInverseTransposeMap(self) ->dict:
        return self.JacobianInverseTransposeMap
    
    def addElementMatrixToMap(self, id, elementMatrix) -> None:
        self.elementMatrixMap.update({id: elementMatrix})
    def getElementMatrixMap(self) -> dict:
        return self.elementMatrixMap