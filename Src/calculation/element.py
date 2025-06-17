import numpy as np
import calculation.gauss as gauss

# This class does only store references to the nodes, and does not contain any data
# It is used to calculate the elementmatrix and the elementvector
class Element:
  def __init__(self, id: int):
    from main import Data
    self.id = id
    self.nodeTLId = Data.getIENof(0, id)
    self.nodeTRId = Data.getIENof(1, id)
    self.nodeBLId = Data.getIENof(2, id)
    self.nodeBRId = Data.getIENof(3, id)
    self.hX = Data.mesh[self.nodeTLId].GetX() - Data.mesh[self.nodeTRId].GetX()
    hX2 = Data.mesh[self.nodeBLId].GetX() - Data.mesh[self.nodeBRId].GetX()
    assert self.hX == hX2, "Element not rectangular"
    assert self.hX != 0, "hX is 0!"
    self.hY = Data.mesh[self.nodeTLId].GetY() - Data.mesh[self.nodeBLId].GetY()
    hY2 = Data.mesh[self.nodeTRId].GetY() - Data.mesh[self.nodeBRId].GetY()
    assert self.hY == hY2, "Element not rectangular"
    assert self.hY != 0, "hY is 0!"

  def GetNodeTL(self):
    from main import Data
    return Data.mesh[self.nodeTLId]
  def GetNodeTR(self):
    from main import Data
    return Data.mesh[self.nodeTRId]
  def GetNodeBL(self):
    from main import Data
    return Data.mesh[self.nodeBLId]
  def GetNodeBR(self):
    from main import Data
    return Data.mesh[self.nodeBRId]
    
  def GetJacobianInverseTronspose(self):
    from main import Data
    if (self.hX, self.hY) in Data.getJacobianInverseTransposeMap():
      return Data.getJacobianInverseTransposeMap()[(self.hX, self.hY)]
    else:
      JacobianInverseTranspose = [[0., 0.], [0., 0.]]
      JacobianInverseTranspose[0][0] = 2. / self.hX #dx/dxi
      JacobianInverseTranspose[1][1] = 2. / self.hY #dy/deta
      JacobianInverseTranspose[0][1] = 0. #dx/deta
      JacobianInverseTranspose[1][0] = 0. #dy/dxi
      Data.addJacobianInverseTransposeToMap(self.hX, self.hY, JacobianInverseTranspose)
      return JacobianInverseTranspose
    
  def GetJacobianDeterminant(self):
    from main import Data
    return self.hX * self.hY / 4
  
  def LocHutFx(self, a:int, xi: float) -> float:
    assert a in range(4), "a not in range(4)"
    assert (xi >= -1 and xi <= 1), "xi not in range (-1, 1)"
    if a == 0 or a == 2:
      return (1 - xi) / 2
    if a == 1 or a == 3:
      return (1 + xi) / 2
    
  def LocHutFy(self, a:int, eta: float) -> float:
    assert a in range(4), "a not in range(4)"
    assert (eta >= -1 and eta <= 1), "eta not in range (-1, 1)"
    if a == 0 or a == 1:
      return (1 - eta) / 2
    if a == 2 or a == 3:
      return (1 + eta) / 2
    
  def LocHutF2D(self ,a:int ,xi:float, eta:float):
    return self.HutFx(a, xi) * self.HutFy(a, eta)
  
  def LocHutFderivativeX(self, a:int, xi:float):
    assert a in range(4), "a not in range(4)"
    assert (xi >= -1 and xi <= 1), "xi not in range (-1, 1)"
    if a == 0 or a == 2:
      return -1 / 2
    if a == 1 or a == 3:
      return 1 / 2
    
  def LocHutFderivativeY(self, a:int, eta:float):
    assert a in range(4), "a not in range(4)"
    assert (eta >= -1 and eta <= 1), "eta not in range (-1, 1)"
    if a == 0 or a == 1:
      return -1 / 2
    if a == 2 or a == 3:
      return 1 / 2
    
  def LocHutFderivative2D(self, a:int, xi:float, eta:float):
    return [self.LocHutFderivativeX(a, xi) * self.LocHutFy(a=a, eta=eta), self.LocHutFderivativeY(a, eta) * self.LocHutFx(a=a, xi=xi)]
  
  def LhsIntegrationPoint(self, a:int, b:int, xi:float, eta:float):
    from main import Data
    material_tensor = Data.getTensor()
    NiTerm = (np.dot(self.GetJacobianInverseTronspose(), self.LocHutFderivative2D(a=a, xi=xi, eta=eta)))
    NjTerm = (np.dot(self.GetJacobianInverseTronspose(), self.LocHutFderivative2D(a=b, xi=xi, eta=eta)))
    return np.dot(NiTerm, np.dot(material_tensor,NjTerm)) * self.GetJacobianDeterminant()
  
  def ElementMatrix(self):
    ElementMatrix = []
    for a in range(4):
      K_a = []
      for b in range(4):
        K_ab = gauss.Integrate2d(lambda xi, eta: self.LhsIntegrationPoint(a, b, xi, eta), n=2)
        K_a.append(K_ab)
      ElementMatrix.append(K_a)
    return ElementMatrix
  
  #edge is the index of the node in the counterclockwise direction of the edge
  def RhsIntegrationPoint(self, a:int, edge:int, location:float):
    #we will always have to integrate along the two neighbouring edges of the node
    
    vonNeumannBoundary = None
    if(edge == 0 and (a == 0 or a == 1)):
      vonNeumannBoundary = self.GetNodeTL().GetRightVonNeumannBoundary()
    elif(edge == 1 and (a == 1 or a == 3)):
      vonNeumannBoundary = self.GetNodeTR().GetBelowVonNeumannBoundary()
    elif(edge == 2 and (a == 0 or a == 2)):
      vonNeumannBoundary = self.GetNodeTL().GetBelowVonNeumannBoundary()
    elif(edge == 3 and (a == 2 or a == 3)):
      vonNeumannBoundary = self.GetNodeBL().GetRightVonNeumannBoundary()
    elif(edge >= 0 and edge <= 4):
      vonNeumannBoundary == None
    else:
      raise ValueError("Edge not in range(4)")
    
    if(vonNeumannBoundary == None):
      return 0
    
    if(edge == 0 or edge == 1):
      vonNeumannBoundary = -vonNeumannBoundary

    if(edge == 0 or edge == 3):
      return self.LocHutFx(a=a, xi=location) * \
             vonNeumannBoundary / self.hX * \
             self.GetJacobianDeterminant() * 2
    elif(edge == 1 or edge == 2):
      return self.LocHutFy(a=a, eta=location) * \
             vonNeumannBoundary / self.hY * \
             self.GetJacobianDeterminant() * 2
    
  def ElementVector(self, ElementMatrix):
    ElementVector = []
    for a in range(4):
      f_a = 0.

      #vonNeumann boundary conditions
      for edge in range(4):
        f_a += gauss.Integrate1d(lambda location: self.RhsIntegrationPoint(a=a, edge=edge, location=location), n=2)

      #dirichlet boundary conditions
      if(self.GetNodeTL().GetDirichletBoundary() != None):
        f_a -= self.GetNodeTL().GetDirichletBoundary() * ElementMatrix[a][0]
      if(self.GetNodeTR().GetDirichletBoundary() != None):
        f_a -= self.GetNodeTR().GetDirichletBoundary() * ElementMatrix[a][1]
      if(self.GetNodeBL().GetDirichletBoundary() != None):
        f_a -= self.GetNodeBL().GetDirichletBoundary() * ElementMatrix[a][2]
      if(self.GetNodeBR().GetDirichletBoundary() != None):
        f_a -= self.GetNodeBR().GetDirichletBoundary() * ElementMatrix[a][3]
        
      ElementVector.append(f_a)
    return ElementVector
  
