import calculation.element as element
import scipy.sparse as sparse

def calculate():
  from main import Data

  IENdict = Data.getIEN()
  valuesDict = dict()
  for e in range(Data.getNe()):
    curElement = element.Element(e)
    currElementmatrix = curElement.ElementMatrix()
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
            if(currElementmatrix[a][b] != 0):
              if(valuesDict.get((eq1, eq2)) == None):
                valuesDict[(eq1, eq2)] = 0
              valuesDict[(eq1, eq2)] += currElementmatrix[a][b]
  values = list(valuesDict.values())
  (rows, cols) = zip(*valuesDict.keys()) 
  assert len(values) == len(rows) == len(cols), "values, rows and cols must have the same length"
  systemMatrix = sparse.coo_matrix((values, (rows, cols)), shape=(len(Data.getNE()), len(Data.getNE())), dtype=float).tocsr()
  systemMatrix.eliminate_zeros()
  if(False): #for debug, consttructs a dense matrix
    print("SystemMatrix: \n", systemMatrix.todense())
  


    