class Element:
  def __init__(self, id: int):
    from main import Data
    self.id = id
    self.nodeTLId = Data.getIENof(0, id)
    self.nodeTRId = Data.getIENof(1, id)
    self.nodeBLId = Data.getIENof(2, id)
    self.nodeBRId = Data.getIENof(3, id)
    self.hX = Data.mesh[self.nodeTLId].getX() - Data.mesh[self.nodeTRId].getX()
    hX2 = Data.mesh[self.nodeBLId].getX() - Data.mesh[self.nodeBRId].getX()
    assert self.hX == hX2, "Element not rectangular"
    assert self.hX != 0, "hX is 0!"
    self.hY = Data.mesh[self.nodeTLId].getY() - Data.mesh[self.nodeBLId].getY()
    hY2 = Data.mesh[self.nodeTRId].getY() - Data.mesh[self.nodeBRId].getY()
    assert self.hY == hY2, "Element not rectangular"
    assert self.hY != 0, "hY is 0!"
    
  def GetJacobianInverseTronspose(self):
    from main import Data
    if (self.hX, self.hY) in Data.getJacobianInverseTransposeMap():
      return Data.getJacobianInverseTransposeMap()[(self.hX, self.hY)]
    else:
      JacobianInverseTranspose = [[0, 0], [0, 0]]
      JacobianInverseTranspose[0][0] = 2 / self.hX #dx/dxi
      JacobianInverseTranspose[1][1] = 2 / self.hY #dy/deta
      JacobianInverseTranspose[0][1] = 0 #dx/deta
      JacobianInverseTranspose[1][0] = 0 #dy/dxi
      Data.addJacobianInverseTransposeToMap(self.hX, self.hY, JacobianInverseTranspose)
      return JacobianInverseTranspose
    
  def GetJacobianDeterminant(self):
    from main import Data
    return self.hX * self.hY / 4
  
  def HutFx(self, a:int, xi: float) -> float:
    
    assert a in range(4), "a not in range(4)"
    assert (xi >= -1 and xi <= 1), "xi not in range (-1, 1)"
    if a == 0 or a == 2:
      return (1 - xi) / 2
    if a == 1 or a == 3:
      return (1 + xi) / 2
    
  def HutFy(self, a:int, eta: float) -> float:
    
    assert a in range(4), "a not in range(4)"
    assert (eta >= -1 and eta <= 1), "eta not in range (-1, 1)"
    if a == 0 or a == 1:
      return (1 - eta) / 2
    if a == 2 or a == 3:
      return (1 + eta) / 2
    
  def HutF2D(self ,a:int ,xi:float, eta:float):
    return self.HutFx(a, xi) * self.HutFy(a, eta)
  
  def HutFderivativeX(self, a:int, xi:float):
    assert a in range(4), "a not in range(4)"
    assert (xi >= -1 and xi <= 1), "xi not in range (-1, 1)"
    if a == 0 or a == 2:
      return -1 / 2
    if a == 1 or a == 3:
      return 1 / 2
    
  def HutFderivativeY(self, a:int, eta:float):
    assert a in range(4), "a not in range(4)"
    assert (eta >= -1 and eta <= 1), "eta not in range (-1, 1)"
    if a == 0 or a == 1:
      return -1 / 2
    if a == 2 or a == 3:
      return 1 / 2
    
  def HutFderivative2D(self, a:int, xi:float, eta:float):
    return (self.HutFderivativeX(a, xi), self.HutFderivativeY(a, eta))