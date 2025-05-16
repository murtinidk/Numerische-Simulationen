import calculation.element as element
import scipy.sparse as sparse
import interface.gui as gui

calculateIndividualElementMatrixes = False #all of our element matrixes are the same, so we can save time by not calculating them multiple times

def calculate():
  from main import Data
  global calculateIndividualElementMatrixes

  if(not calculateIndividualElementMatrixes):
    elementmatrix = element.Element(0).ElementMatrix()
  gui.setStep(gui.simStep.systemMatrix)
  IENdict = Data.getIEN()
  valuesDict = dict()
  for e in range(Data.getNe()):
    if(calculateIndividualElementMatrixes):
      elementmatrix = element.Element(e).ElementMatrix()
    if(False): #for debug, spams terminal
      print("ElementMatrix: ", e)
      for line in currElementmatrix:
        print(*line, sep=" ")

    for a in range(Data.getNen()):
      eq1 = IENdict[(a, e)]
      if(eq1 > 0):
        for b in range(Data.getNen()):
          eq2 = IENdict[(b, e)]
          if(eq2 > 0):
            if(elementmatrix[a][b] != 0):
              if(valuesDict.get((eq1, eq2)) == None):
                valuesDict[(eq1, eq2)] = 0
              valuesDict[(eq1, eq2)] += elementmatrix[a][b]
  values = list(valuesDict.values())
  (rows, cols) = zip(*valuesDict.keys()) 
  assert len(values) == len(rows) == len(cols), "values, rows and cols must have the same length"
  systemMatrix = sparse.coo_matrix((values, (rows, cols)), shape=(len(Data.getNE()), len(Data.getNE())), dtype=float).tocsr()
  systemMatrix.eliminate_zeros()
  if(False): #for debug, consttructs a dense matrix
    print("SystemMatrix: \n", systemMatrix.todense())
  

  


    