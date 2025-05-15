import calculation.element as element

def calculate():
  from main import Data

  mesh = Data.getMesh()
  for elementId in range((Data.getXResolution() - 1) * (Data.getYResolution()-1)):
    curElement = element.Element(elementId)
    currElementmatrix = curElement.ElementMatrix()
    print("ElementMatrix: ", elementId)
    for line in currElementmatrix:
      print(*line, sep=" ")

    