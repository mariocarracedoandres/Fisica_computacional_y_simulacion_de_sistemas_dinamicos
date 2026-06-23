import sympy as sp
from sympy import symbols, Function, diff, simplify, latex
from IPython.display import display, Math

####################################################
# Ecuaciones de Euler Lagrange en 1D
# Author: Mario Carracedo Andres
# Year: 2025
# License: MIT
# Description: Halla las ecuaciones de Euler-Lagrange en base a ciertos parámetros
####################################################

# sympy: biblioteca para cálculo simbólico.

# symbols: para definir variables simbólicas (como 𝑡, t, 𝑚, m, 𝑘, k).

# Function: para definir funciones simbólicas (como 𝑞(𝑡),).

# diff: para derivar simbólicamente.

# simplify: para simplificar expresiones simbólicas.

# latex: para convertir expresiones simbólicas en código LaTeX.

# display, Math: funciones de IPython/Jupyter para mostrar matemáticas formateadas en notebooks.

# Defino los símbolos
t = symbols('t') # Variable independiete
q = Function('q')(t) # Funcion independiente == coordenada generalizada
m, k = symbols('m k') # Constantes

# Energías + Lagragiano
T = 0.5 * m * diff(q, t)**2 #diff(q,t) es la derivada de q respecto de t
V = 0.5 * k * q**2
L = T - V

#Ecuaciones de Euler Lagrange
EL = simplify(diff(diff(L, diff(q, t)), t) - diff(L, q))

latex_str = latex(EL) #convierte EL en cadena de caracteres de Latex, la guardo en latex_str

display(Math(latex_str))

#print en .py 
print("Resultado en LaTeX:")
print(latex_str)