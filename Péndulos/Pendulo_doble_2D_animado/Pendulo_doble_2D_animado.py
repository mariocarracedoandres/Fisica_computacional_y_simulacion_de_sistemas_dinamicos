####################################################
# Penudlo_doble_2D_animado
# Author: Mario Carracedo Andres
# Year: 2026
# License: MIT
# Description: Resuelve las ecuaciones del movimiento del péndulo doble y lo anima
####################################################

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Para crear gráficos 3D
from matplotlib.animation import FuncAnimation #crear videoa animados (evolucion temporat de sistemas...)
from matplotlib.animation import FFMpegWriter #Guardar animaciones
import os

####################################################################### FUNCIONES AUXILIARES
def sistema(t, y, L1, L2, m1, m2, g):
    """
    Define aquí tu sistema de m ecuaciones diferenciales.
    y: array de tamaño m -> [y1, y2, ..., ym]
    Devuelve: array de derivadas [dy1/dt, dy2/dt, ..., dym/dt]
    """
    dydt = np.zeros_like(y)

    # Ejemplo para un sistema de 2 ecuaciones:
    # dy1/dt = y2
    # dy2/dt = -y1
    delta = y[0] - y[1]  # θ1 - θ2

    theta_1 = y[0]
    theta_2 = y[1]
    d_tetha_1 = y[2]
    d_tetha_2 = y[3]
    
    #resolvemos sistema acoplado

    M = np.array([
        [(m1 + m2) * L1, m2 * L2 * np.cos(theta_1 - theta_2)],
        [L1 * np.cos(theta_1 - theta_2), L2]
    ])

    b = np.array([
        -m2 * L2 * d_tetha_2**2 * np.sin(theta_1 - theta_2) - (m1 + m2) * g * np.sin(theta_1),
        L1 * d_tetha_1**2 * np.sin(theta_1 - theta_2) - g * np.sin(theta_2)
    ])

    aceleraciones = np.linalg.solve(M,b)

    dydt[0] = d_tetha_1
    dydt[1] = d_tetha_2
    dydt[2] = aceleraciones[0] #derivada 2º de theta_1
    dydt[3] = aceleraciones[1] #derivada 2º de theta_2

    return dydt

def rk4_step(f, t, y, h): #f es en nuestro caso sistema
    k1 = f(t, y, L1, L2, m1, m2, g)
    k2 = f(t + h/2, y + h/2 * k1, L1, L2, m1, m2, g)
    k3 = f(t + h/2, y + h/2 * k2, L1, L2, m1, m2, g)
    k4 = f(t + h, y + h * k3, L1, L2, m1, m2, g)
    
    # z = y + (h/6)*(k1 + 2*k2 + 2*k3 + k4) #es lo mismo que lo de abajo
    # return z
    return y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

def resolver_sistema(f, y0, t0, tf, h): #f=nombre de la funcion auxiliar correspondiente a nuestro sistema de ecuaciones diferenciales
    N = int(np.ceil((tf - t0)/h)) + 1  # número total de pasos | np.ceil=redondea(devuelve numero float=real) | int()=transforma lo de dentro en entero
    t_vals = np.zeros(N)  # predefinir vector para tiempos
    y_vals = np.zeros((N, len(y0)))  # predefinir matriz para soluciones |len(y0) = tamaño del vector (ej matriz_de_zeros(1000,4))

    # Inicio las variables con los valores iniciales
    t_vals[0] = t0
    y_vals[0,:] = y0 #puedes poner tambien  y_vals[0] = y0, esto es 1º fila y todas las columnas

    t = t0
    y = y0

    for i in range(1, N): #Partimos de 1 porque n 0 son las condiciones iniciales
        y = rk4_step(f, t, y, h) #hayas solucion para un timepo
        t = t + h #vamos al siguiente tiempo
        t_vals[i] = t 
        for j in range(len(y)): # esto es lo mismo a (y_vals[i] = y.copy())
            y_vals[i, j] = y[j]
       

    return t_vals, y_vals

####################################################################### PROGRAMA PRICIPAL
# === Parámetros del Sistema de EDOs ===
L1 = float(input("Longitud Hilo 1, L1 (m): "))
L2 = float(input("Longitud Hilo 2, L2 (m): "))
m1 = float(input("masa 1 (Kg): "))
m2 = float(input("masa 2 (Kg): "))

g = +9.81

# === Parámetros del sistema === o condiciones iniciales
angulo1_0 = int(input("angulo inicial 1ºpendulo: "))
angulo2_0 = int(input("angulo inicial 2ºpenudlo: "))
y0 = np.array([np.pi/180*angulo1_0, np.pi/180*angulo2_0, 0.0, 0.0])  # condiciones iniciales [angulo inicial, velocidad angular]

t0 = 0.0
tf = 10
h = 0.02 # h = en segundos, interval en milisegundos, hacer interval = h*1000 || h = 0,02 = 50 fps || por limitaciones de RK4, H < 0.1

# === Ejecutar simulación ===
t, ys = resolver_sistema(sistema, y0, t0, tf, h)

#Matriz de resultados
for i in range(len(t)):
    for j in range(len(ys[i])):
        print(f"{ys[i][j]:8.4f}", end="\t")  # imprime con 4 decimales, ancho 8
    print(end="\n")  # salto de línea tras cada fila


# === Graficar resultados ===
#Veamos que representa cada columna de la matriz solucion ys
tetha1 = ys[:, 0]
tetha2 = ys[:,1]

v1_angular = ys[:, 2]
v2_angular = ys[:, 3]

#Parametrizemos
x1 = L1*np.sin(tetha1)
y1 = -L1*np.cos(tetha1)

x2 = x1 + L2*np.sin(tetha2)
y2 = y1 + (-L2*np.cos(tetha2))

r = np.max(np.sqrt(x1**2 + y1**2) + np.sqrt(x2**2 + y2**2))*1.2

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
#ax.set_aspect('equal')  # 👈 ¡Esto fuerza escala igual en x e y!

# Configuramos los límites para que no cambien durante la animación
#xmin = np.min([np.min(x), np.min(y)])*1.2
#xmax = np.max([np.max(x), np.max(y)])*1.2

ax.set_xlim(-r, r)
ax.set_ylim(-r, r)
ax.set_aspect("equal")

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title(rf'$\theta_{{1,o}}={angulo1_0}º;\theta_{{2,o}}={angulo2_0}º; m_{{1}}={m1};m_{{2}}={m2};l_{{1}}={L1};l_{{2}}={L2}$') # r = para que no pasen cosas raras al poner latex || $aqui poner algo en latex y sub indices {{}}$
ax.grid()

#trayectoria, = ax.plot([], [], lw=1, color='blue')  # línea vacía para ir actualizando | line, = ... == line = ...[0] sacas de la lista un ojeto,
Hilo1, = ax.plot([], [], 'k-', lw=1, label = "Hilo 1")        
masa1, = ax.plot([], [], 'ro', markersize=8, label = "masa 1") 
Hilo2, = ax.plot([], [], color = "gray", linestyle = "-", lw=1, label = "Hilo 2")
masa2, = ax.plot([], [], 'bo', markersize=8, label = "masa 2") 

# Legenda
ax.legend(handles=[Hilo1, Hilo2, masa1, masa2])

# Función de inicialización
def init():
    #trayectoria.set_data([], [])
    Hilo1.set_data([],[])
    masa1.set_data([],[])
    Hilo2.set_data([],[])
    masa2.set_data([],[])
    return masa1, Hilo1, Hilo2, masa2 #trayectoria, #volvemos a meter el objeto en una lista (no hace falta la coma al final si tenemos mas de un elemento)

# Función que se llama en cada frame de la animación
def update(num):
    #print(f"Frame {num}: x = {x[num]}, y = {y[num]}") #muestra en que num te llegas
    #trayectoria.set_data(x[:num], y[:num]) #toma desde 0 hasta num (python empiezas en [0]) y mantiene los anteriores = (muestra la trayectoria que se va siguiendo)
    Hilo1.set_data([0, x1[num]], [0, y1[num]]) #toma fijo el (0, 0) y se va hasta num = (nuelle se estira hasta donde la bola)
    masa1.set_data([x1[num]], [y1[num]]) #toma desde 0 hasta num y borra los anteriores = (bola se muve siguiendo lo trayectoria)
    Hilo2.set_data([x1[num], x2[num]], [y1[num], y2[num]]) #toma desde 0 hasta num y borra los anteriores = (bola se muve siguiendo lo trayectoria)
    masa2.set_data([x2[num]],[y2[num]])
    return masa1, Hilo1, Hilo2, masa2 #trayectoria

# Crear la animación
ani = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=h*1000) #FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=1)


#Guardo la animacion: quitar el # a lo de abajo si quiero guardar la animacion en la carpeta donde esta el .py
directorio_del_script = os.path.dirname(os.path.abspath(__file__)) #nos da la ruta donde esta el .py

nombre_archivo = "Pendulo_doble_2D_animado(mp4).mp4" #nombre de archivo a guardar
ruta_guardado = os.path.join(directorio_del_script, nombre_archivo) #para guardar el archivo en la carpeta donde esta el .py

writer = FFMpegWriter(fps=int(1/h), metadata=dict(artist='Yo'), bitrate=1800)
ani.save(ruta_guardado, writer=writer)
print(f"Animación guardada como: {nombre_archivo}")
print(f"Archivo guardado en: {ruta_guardado}")

plt.show() # siempre despues de ani.save