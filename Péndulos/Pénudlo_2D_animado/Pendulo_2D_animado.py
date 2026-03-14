import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Para crear gráficos 3D
from matplotlib.animation import FuncAnimation #crear videoa animados (evolucion temporat de sistemas...)

####################################################################### FUNCIONES AUXILIARES
def sistema(t, y, L, g):
    """
    Define aquí tu sistema de m ecuaciones diferenciales.
    y: array de tamaño m -> [y1, y2, ..., ym]
    Devuelve: array de derivadas [dy1/dt, dy2/dt, ..., dym/dt]
    """
    dydt = np.zeros_like(y)

    # Ejemplo para un sistema de 2 ecuaciones:
    # dy1/dt = y2
    # dy2/dt = -y1

    dydt[0] = y[1]
    dydt[1] = -g/L*np.sin(y[0])

    return dydt

def rk4_step(f, t, y, h):
    k1 = f(t, y, L, g)
    k2 = f(t + h/2, y + h/2 * k1, L, g)
    k3 = f(t + h/2, y + h/2 * k2, L, g)
    k4 = f(t + h, y + h * k3, L, g)
    
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

    for i in range(1, N): #Partimos de 1 porque en 0 son las condiciones iniciales
        y = rk4_step(f, t, y, h) #hayas solucion para un timepo
        t = t + h #vamos al siguiente tiempo
        t_vals[i] = t 
        for j in range(len(y)): # esto es lo mismo a (y_vals[i] = y.copy())
            y_vals[i, j] = y[j]
       

    return t_vals, y_vals

####################################################################### PROGRAMA PRICIPAL
# === Parámetros del Sistema de EDOs ===
L = float(input("Longitud hilo L: "))
g = 9.81

# === Parámetros del sistema ===
angulo_0 = float(input("angulo inicial: "))
y0 = np.array([np.pi/180*angulo_0, 0.0])  # condiciones iniciales [angulo inicial, velocidad angular]
t0 = 0.0
tf = 2*np.pi*np.sqrt(L/g)*(1 + 1/16*((np.pi/180*angulo_0)**2))*10 # 1 periodo
h = 0.01 # el pendulo avanza 10 ms en la vida real

# === Ejecutar simulación ===
t, ys = resolver_sistema(sistema, y0, t0, tf, h)

#Matriz de resultados
for i in range(len(t)):
    for j in range(len(ys[i])):
        print(f"{ys[i][j]:8.4f}", end="\t")  # imprime con 4 decimales, ancho 8
    print(end="\n")  # salto de línea tras cada fila


# === Graficar resultados ===
tetha = ys[:, 0]
x = L*np.sin(tetha)

v_angular = ys[:, 1]
y = -L*np.cos(tetha)

r = np.max(np.sqrt(x**2 + y**2))*1.2

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
ax.set_title('Péndulo simple - Animación 2D')
ax.grid()

#trayectoria, = ax.plot([], [], lw=1, color='blue')  # línea vacía para ir actualizando | line, = ... == line = ...[0] sacas de la lista un ojeto,

masa, = ax.plot([], [], 'ro', markersize=8)  # la bola (rojo)
Hilo, = ax.plot([], [], 'k-', lw=1)        # el muelle (línea negra)

# Función de inicialización
def init():
    #trayectoria.set_data([], [])
    masa.set_data([],[])
    Hilo.set_data([],[])
    return masa, Hilo, #trayectoria, #volvemos a meter el objeto en una lista (no hace falta la coma al final si tenemos mas de un elemento)

# Función que se llama en cada frame de la animación
def update(num):
    #print(f"Frame {num}: x = {x[num]}, y = {y[num]}") #muestra en que num te llegas
    #trayectoria.set_data(x[:num], y[:num]) #toma desde 0 hasta num (python empiezas en [0]) y mantiene los anteriores = (muestra la trayectoria que se va siguiendo)
    masa.set_data([x[num]], [y[num]]) #toma desde 0 hasta num y borra los anteriores = (bola se muve siguiendo lo trayectoria)
    Hilo.set_data([0, x[num]], [0, y[num]]) #toma fijo el (0, 0) y se va hasta num = (nuelle se estira hasta donde la bola)
    return masa, Hilo, #trayectoria

# Crear la animación
ani = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=h*1000) #FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=1)
plt.show()
