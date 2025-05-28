#- this file contains declarations and implementations for storing the data between steps of the simulation
#- it might be extended to load savepoints in the future
#- Numerische Simulationen für Digital Engineering, SS 2025
#- Gruppe 6: Ram Abhay, Figo Tobias, Thalmayr Martin

import interface.gui
import external.exportRes as CFSwriter
import numpy as np
class DataClass:
    def __init__(self):
        self.hasSize = False
        self.width = None	
        self.height = None
        self.xResolution = None
        self.yResolution = None
        self.hasMesh = False
        self.mesh = None
        self.line = None
        self.hasLine = False
        self.left = None
        self.hasLeft = False
        self.top = None
        self.hasTop = False
        self.right = None
        self.hasRight = False
        self.bottom = None
        self.hasBottom = False
        self.hasIEN = False
        self.IEN = None
        self.hasNE = False
        self.NE = None
        self.JacobianInverseTransposeMap = dict()
        self.elementMatrixMap = dict()
        self.hasResult = False


        
    def reset(self):
        if self.hasSize:
            self.__init__()
    
    def setSize(self, width, height, xResolution, yResolution):
        self.width = width
        self.height = height
        self.xResolution = xResolution
        self.yResolution = yResolution
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
    
    
    
    def setLeftBoundary(self, left):
        if(self.hasLeft):
            raise Exception("Left Boundary already set!")
        if left is not None:
            self.left = left
            self.hasLeft = True
    def hasLeft(self):
        return self.hasLeft
    def getLeft(self):
        if(not self.hasLeft):
            return None
        return self.left
    
    def setTopBoundary(self, top):
        if(self.hasTop):
            raise Exception("Top Boundary already set!")
        if top is not None:
            self.top = top
            self.hasTop= True
    def hasTop(self):
        return self.hasTop
    def getTop(self):
        if(not self.hasTop):
            return None
        return self.top
    
    def setRightBoundary(self, right):
        if(self.hasRight):
            raise Exception("Left Boundary already set!")
        if right is not None:
            self.right = right
            self.hasRight = True
    def hasRight(self):
        return self.hasRight
    def getRight(self):
        if(not self.hasRight):
            return None
        return self.right
    
    def setBottomBoundary(self, bottom):
        if(self.hasBottom):
            raise Exception("Left Boundary already set!")
        if bottom is not None:
            self.bottom = bottom
            self.hasBottom = True
    def hasBottom(self):
        return self.hasBottom
    def getBottom(self):
        if(not self.hasBottom):
            return None
        return self.bottom
    
    def setBoundary(self, left, top, bottom, right):
        self.setLeftBoundary(left)
        self.setTopBoundary(top)
        self.setRightBoundary(right)
        self.setBottomBoundary(bottom)

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
    
    def isEQkey(self, a, c) -> bool:
        if(not self.hasIEN):
            raise Exception("IEN not set, when accessing element!")
        if(not (a,c) in self.IEN):
            return False
        if(not self.IEN[(a, c)] in self.NE):
            return False
        return True

    #number of elements
    def getNe(self) -> int:
        return (self.xResolution -1) * (self.yResolution - 1)
        
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
    
    def setHasResult(self, hasResult) -> None:
        self.hasResult = hasResult

    def getHasResult(self) -> bool:
        return self.hasResult
    
    #translates data for h5 export writer, as in interface description for the writer
    # writer.writeResuls writes into workingdir/result.cfs
    def exportCFS(self):
        nodesPerEl = self.getNen()
        nElements = self.getNe()
        mesh = self.getMesh()
        nNodes = len(mesh)
        dim = 2 #only 2D xy domains
        n_dof_p_node = 1 #only one degree of freedom per node -> scalar value per node
        if self.getHasResult() == False:
            raise Exception("No result to export!")
        #reult vector
        U = np.zeros((nNodes,))
        for i in range(len(mesh)):
            #get the result from node if dirichlet is not set
            if mesh[i].GetDirichletBoundary() == None:
                U[i] = mesh[i].GetResult()
            else:
                U[i] = mesh[i].GetDirichletBoundary()
        
        #geom: node coordinate matrix
        geom = np.zeros((nNodes,2))
        for i, node in enumerate(mesh):
            geom[i][0] = node.GetX()
            geom[i][1] = node.GetY()

        #connec plot - node connectivity matrix
        connec_plot = np.zeros((nElements, nodesPerEl),dtype=int)
        for element in range(nElements):
            #remap element connectivity
            connec_plot[element, 0] = self.getIENof(2, element) 
            connec_plot[element, 1] = self.getIENof(3, element)
            connec_plot[element, 2] = self.getIENof(0, element)
            connec_plot[element, 3] = self.getIENof(1, element)
        #create instance of writer class
        writer = CFSwriter.EXPORT(
                nodesPerEl=nodesPerEl,
                nElements=nElements,
                nNodes=nNodes,
                dim=dim,
                U=U,
                geom=geom,
                connec_plot=connec_plot,
                n_dof_p_node=n_dof_p_node
        )
        #write results to file
        writer.writeResults()


