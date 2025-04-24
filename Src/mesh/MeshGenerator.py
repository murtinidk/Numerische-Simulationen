import numpy as np


def meshGenerator(l, w, nl, nw):
  l_coords = np.linspace(0.0, l, nl + 1)
  w_coords = np.linspace(0.0, w, nw + 1)
  lv, wv = np.meshgrid(l_coords, w_coords, indexing='ij')
  coord = np.vstack([lv.ravel(), wv.ravel()]).T
  return coord

def validInput(type):
  while True:
    try:
      x = int(input("Please select the " + type + " of your rectangular:"))
    except ValueError:
      print("The entered value was not a number!")
    else:
      return x

def numberOfElements():
  while True:
    try:
      x = int(input("Please select the desired number of Elements for generating the mesh:"))
    except ValueError:
      print("The entered value was not a number!")
    else:
      return x

def findRatio(l, w, n):
  r=l/w
  nl = round((n/r)**(1/2))
  nw = round(n/nl)
  return nl, nw
  

l = validInput('length')
w = validInput('width')
n = numberOfElements()

nl, nw = findRatio(l, w, n)
coord = meshGenerator(l, w, nl, nw)
print(coord)

print(l , w, n , nl, nw)
