import numpy as np
import calculation.gauss as gauss

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
    return [self.LocHutFderivativeX(a, xi), self.LocHutFderivativeY(a, eta)]
  
  def LhsIntegrationpoint(self, a:int, b:int, xi:float, eta:float):
    from main import Data
    return np.dot((np.dot(self.GetJacobianInverseTronspose(), self.LocHutFderivative2D(a=a, xi=xi, eta=eta))), \
           (np.dot(self.GetJacobianInverseTronspose(),  self.LocHutFderivative2D(a=b, xi=xi, eta=eta)))) * \
           self.GetJacobianDeterminant()
  
  def ElementMatrix(self):
    ElementMatrix = []
    for a in range(4):
      K_a = []
      for b in range(4):
        K_ab = gauss.Integrate2d(lambda xi, eta: self.LhsIntegrationpoint(a, b, xi, eta), n=2)
        K_a.append(K_ab)
      ElementMatrix.append(K_a)
    return ElementMatrix
  
