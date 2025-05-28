import calculation.element as element
import scipy.sparse as sparse
import interface.gui as gui
from typing import Type

# This is an optimization, as i notized all element matrixes are the same
calculateIndividualElementMatrixes = False #all of our element matrixes are the same, so we can save time by not calculating them multiple times

def calculate():
  from main import Data

  gui.setStep(gui.simStep.systemMatrix)
  systemMatrix, systemVector = calculateSystemMatrixAndVector()
  
  gui.setStep(gui.simStep.solveSystem)
  result = sparse.linalg.spsolve(systemMatrix, systemVector)
  
  for NodeId in Data.getNE().keys():
    Data.getMesh()[NodeId].SetResult(result[Data.getNE()[NodeId]])
  Data.setHasResult(True)

  gui.setStep(gui.simStep.drawingColors)
  gui.updateGui()
  
#assembles the system matrix and vector
def calculateSystemMatrixAndVector() -> tuple[Type[sparse.csr_matrix], list[float]]:
  from main import Data
  global calculateIndividualElementMatrixes

  if(not calculateIndividualElementMatrixes):
    elementmatrix = element.Element(0).ElementMatrix()
    
  IENdict = Data.getIEN()
  valuesDict = dict()
  systemVector = [0.] * len(Data.getNE())
  
  for e in range(Data.getNe()):
    if(calculateIndividualElementMatrixes):
      elementmatrix = element.Element(e).ElementMatrix()

    elementVector = element.Element(e).ElementVector(elementmatrix)
    
    if(False): #for debug, spams terminal
      print("ElementMatrix: ", e)
      for line in elementmatrix:
        print(*line, sep=" ")

    for a in range(Data.getNen()):
      if(Data.isEQkey(a, e)):
        eq1 = Data.getEQof(a, e)
        #add to systemVector
        systemVector[eq1] += elementVector[a]

        for b in range(Data.getNen()):
          if(Data.isEQkey(b, e)):
            eq2 = Data.getEQof(b, e)
            if(elementmatrix[a][b] != 0):
              
              if(valuesDict.get((eq1, eq2)) == None):
                valuesDict[(eq1, eq2)] = 0
              valuesDict[(eq1, eq2)] += elementmatrix[a][b]

  #add line value to right hand side vector
  for node_id, eq_id in Data.getNE().items():
    node = Data.getMesh()[node_id]
    systemVector[eq_id] += node.GetLineAddition()
  
  #convert to sparse matrix
  values = list(valuesDict.values())
  (rows, cols) = zip(*valuesDict.keys()) 
  assert len(values) == len(rows) == len(cols), "values, rows and cols must have the same length"
  systemMatrix = sparse.coo_matrix((values, (rows, cols)), shape=(len(Data.getNE()), len(Data.getNE())), dtype=float).tocsr()
  systemMatrix.eliminate_zeros()
  
  if(False): #for debug, consttructs a dense matrix
    print("SystemMatrix: \n", systemMatrix.todense())
    print("SystemVector: ", systemVector)
    
  return systemMatrix, systemVector

  

  


    