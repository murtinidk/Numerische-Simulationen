import numpy as np

def IntegrationPoints(n:int = 2):
  return np.polynomial.legendre.leggauss(n)

def Integrate2d(
  f: callable, n: int = 2,
  xmin: float = -1, xmax: float = 1,
  ymin: float = -1, ymax: float = 1) -> float:
  x_points, x_weights = IntegrationPoints(n)
  y_points, y_weights = IntegrationPoints(n)

  integral = 0.0
  for i in range(n):
    for j in range(n):
      xi = (xmax - xmin) / 2 * x_points[i] + (xmax + xmin) / 2
      eta = (ymax - ymin) / 2 * y_points[j] + (ymax + ymin) / 2
      integral += f(xi, eta) * x_weights[i] * y_weights[j]

  return integral * (xmax - xmin) / 2 * (ymax - ymin) / 2

def Integrate1d(
    f: callable, n: int = 2,
    xmin: float = -1, xmax: float = 1) -> float:
  x_points, x_weights = IntegrationPoints(n)
  integral = 0.0
  for i in range(n):
    xi = (xmax - xmin) / 2 * x_points[i] + (xmax + xmin) / 2
    integral += f(xi) * x_weights[i]
  return integral * (xmax - xmin) / 2