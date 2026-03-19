####################################################
# Atractor de Lorentz
# Author: Mario Carracedo Andres
# Year: 2026
# License: MIT
# Description: Muestra la trayectoria de una particula en base a unos parametros y condiciones iniciales
####################################################

import numpy as np #cada vez que quier usar alguna función de numpy, debes hacer np.algo()
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Para crear gráficos 3D ||| al importar una funcion en concreto, puedes poner directamente Axes3D() en lugar mpl_toolkits.mplot3d.Axes3D() cada vez que quieras usar esa función, pero es mas común importar el módulo completo y luego usar la función con el prefijo del módulo, para evitar confusiones con otras funciones que puedan tener el mismo nombre en otros módulos
from matplotlib.animation import FuncAnimation #crear videoa animados (evolucion temporat de sistemas...)
from matplotlib.animation import FFMpegWriter #Guardar animaciones
import os # sirve para trabajar con rutas de archivos
from fractions import Fraction #para trabajar con fracciones
import math # toma e, pi...

####################################################################### FUNCIONES AUXILIARES
def sistema(t, y, a, b, c):
    """
    Define aquí tu sistema de m ecuaciones diferenciales.
    y: array de tamaño m -> [y1, y2, ..., ym]
    Devuelve: array de derivadas [dy1/dt, dy2/dt, ..., dym/dt]
    """
    dydt = np.zeros_like(y)

    # Ejemplo para un sistema de 2 ecuaciones:
    # dy1/dt = y2
    # dy2/dt = -y1

    x = y[0]
    y_ = y[1]
    z = y[2]

    # sistema
    # Ecuaciones del atractor de Lorentz
    # Variables: x, y, z (posición); dx/dt, dy/dt, dz/dt (velocidades)
    # Parámetros clásicos de Lorentz

    dydt[0] = a * (y_ - x)         # dx/dt
    dydt[1] = x * (b - z) - y_      # dy/dt
    dydt[2] = x * y_ - c * z        # dz/dt
    
    return dydt

def rk4_step(f, t, y, h): #f es en nuestro caso sistema
    k1 = f(t, y, a, b, c)
    k2 = f(t + h/2, y + h/2 * k1, a, b, c)
    k3 = f(t + h/2, y + h/2 * k2, a, b, c)
    k4 = f(t + h, y + h * k3, a, b, c) 
    
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

def input_parametro(parametro): #sirve para poner cualquier numero en parametros, condcioones iniciales, etc (cualquier numero real)
    while True:
        try:       
            entrada = input(f"{parametro}: ").strip() #el strip es para eliminar espacios al principio y al final
            txt_original = entrada

            if entrada == "pi":
                valor = math.pi
                break
            elif entrada == "e":
                valor = math.e
                break
            elif entrada == Fraction(entrada):
                valor = Fraction(entrada)
                break
            else:
                valor = float(Fraction(entrada))
                break
        except ValueError:
            print("Debes introducir un número real (entero, decimal, fraccion, pi o e) \n")
    return valor, txt_original

####################################################################### PROGRAMA PRICIPAL

###############-----############### Parámetros 
# Parámetros del Sistema de EDOs
a, a_txt = input_parametro("Introduce el primer parámetro: a")
b, b_txt = input_parametro("Introduce el segundo parámetro: b")
c, c_txt = input_parametro("Introduce el tercer parámetro: c")

# Parámetros del sistema (condiciones iniciales y tiempo de simulación)
x0, x0_txt = input_parametro("Introduce la condición inicial de x0: ")
y0_, y0__txt = input_parametro("Introduce la condición inicial de y0: ")
z0, z0_txt = input_parametro("Introduce la condicion inicial z0")
y0 = np.array([x0, y0_, z0])  # condiciones iniciales [x0, y0, z0] en vector
tf, tf_txt = input_parametro("Timepo de duración (ej: 40)")

t0 = 0.0
h = 0.01 # h = en segundos, interval en milisegundos, hacer interval = h*1000 || h = 0,02 = 50 fps || por limitaciones de RK4, H < 0.1

###############-----############### Resolver sistema
t, ys = resolver_sistema(sistema, y0, t0, tf, h)

#Matriz de resultados
for i in range(len(t)):
    for j in range(len(ys[i])):
        print(f"{ys[i][j]:8.4f}", end="\t")  # imprime con 4 decimales, ancho 8. \t es para que se añada una tabulación
    print(end="\n")  # salto de línea tras cada fila


###############-----############### Graficar resultados 
#Veamos que representa cada columna de la matriz solucion ys
x = ys[:, 0]
y = ys[:,1]
z = ys[:,2]

r = max(np.max(np.abs(x)), np.max(np.abs(y)), np.max(np.abs(z)))*0.75

###############-----############### Creamos la figura y los subplots
fig = plt.figure()
fig_img = plt.figure()

fig.suptitle("Atractor de Lorenz\n"
                rf"$a={a}, b={b}, c={c_txt} ; x_{{0}}={x0}, y_{{0}}={y0_}, z_{{0}}={z0}$")

ax = fig.add_subplot(1, 2, 1, projection="3d")  # Añade un subplot (1 fila, 1 columna, posición 1) de tipo 3D al 'fig', para graficar trayectorias en 3D
ay = fig.add_subplot(1, 2, 2, projection="3d")  # Crea un subplot 3D en la posición 2 de la figura 
fig_img_ax = fig_img.add_subplot(1, 1 ,1, projection="3d")  # Crea un subplot 3D en la posición 2 de la figura para mostrar solo la imagen sin animación
#ax.set_aspect('equal')  # fuerza escala igual en x e y

# Configuramos los límites para que no cambien durante la animación
#xmin = np.min([np.min(x), np.min(y)])*1.2
#xmax = np.max([np.max(x), np.max(y)])*1.2

# Para el subplot de la trayectoria completa
ax.set_xlim((np.min(x), np.max(x)))
ax.set_ylim((np.min(y), np.max(y)))
ax.set_zlim((np.min(z), np.max(z)))
#ay.set_aspect("equal")
ay.set_xlabel('X')
ay.set_ylabel('Y')
ay.set_zlabel('Z')
#ay.set_title(rf'a={a}, b={b}, c={c_input} ; x_{{0}}={x0}, y_{{0}}={y0_}, z_{{0}}={z0}')
ay.grid()

# Para el subplot de la animación
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
#ax.set_title(rf'a={a}, b={b}, c={c_input} ; x_{{0}}={x0}, y_{{0}}={y0_}, z_{{0}}={z0}')
ax.grid()

# Para solo la imagen
fig_img.suptitle("Atractor de Lorenz\n"
                rf"$a={a}, b={b}, c={c_txt} ; x_{{0}}={x0}, y_{{0}}={y0_}, z_{{0}}={z0}$")
fig_img_ax.set_xlabel('X')
fig_img_ax.set_ylabel('Y')
fig_img_ax.set_zlabel('Z')
fig_img_ax.set_aspect("equal")
fig_img_ax.grid()
###############-----############### CREAMOS LOS OBJETOS DE LA ANIMACIÓN Y LA IMAGEN ESTÁTICA
# Para fig_img solo la imagen
trrayectoria_estatico_img, = fig_img_ax.plot(x, y, z, lw=1, color='blue', label = "trayectoria") # solo para mostrar la imagen sin animación (trayectoria)
bola_estatico_img, = fig_img_ax.plot(x[-1], y[-1], z[-1], 'ro', markersize=4, label = "Último punto") # solo para mostrar el último punto recorrido

# Para el fig subplot de la animación (animada)
trayectoria_anim, = ax.plot([], [], [], lw=1, color='blue', label = "trayectoria") #es [] porque al iniciar la animacion no hay datos, se van añadiendo a medida que avanza la animacion, el lw es el grosor de la linea
bola_anim, = ax.plot([], [], [], 'ro', markersize=4, label = "Frente de trayectoria") 

# Para el fig subplot de la trayectoria completa (estática)
trayectoria_estatico_ay, = ay.plot(x, y, z, lw=1, color='blue', label = "trayectoria") # Aquí pasamos de pasar listas vacías [] (que se usan al inicializar una animación para partir sin datos) a pasar los arrays completos x, y, z, porque queremos graficar toda la trayectoria estática de una vez
bola_estatico_ay, = ay.plot([x[-1]], [y[-1]], [z[-1]], 'ro', markersize=4, label = "Frente de trayectoria") # los -1 indican el último valor de x, y, z, es decir, el final de la trayectoria (si pusieras 0 sería el punto inicial, y 1 sería el segundo punto, pero queremos mostrar el último punto recorrido)

###############-----############### LEGENDAS
fig.legend(handles=[trayectoria_anim, bola_anim], loc="lower left",bbox_to_anchor=(0.375, 0.75), borderaxespad=0) # con ese loc = legenda abajo a la izquierda(coorndeadas = 0,0), con bbox_to_anchor se ajusta la posición de la legenda, borderaxespad=0 para que no haya espacio entre la legenda y el borde del gráfico
fig_img.legend(handles=[trayectoria_estatico_ay, bola_estatico_ay], loc="lower left",bbox_to_anchor=(0.375, 0.75), borderaxespad=0) # con ese loc = legenda abajo a la izquierda(coorndeadas = 0,0), con bbox_to_anchor se ajusta la posición de la legenda, borderaxespad=0 para que no haya espacio entre la legenda y el borde del gráfico

###############-----############### ANIMACIÓN
# Función de inicialización 
def init():
    trayectoria_anim.set_data_3d([], [], [])
    bola_anim.set_data_3d([], [], [])
    return trayectoria_anim, bola_anim #volvemos a meter el objeto en una lista (no hace falta la coma al final si tenemos mas de un elemento)

# Función que se llama en cada frame de la animación
def update(num):
    #print(f"Frame {num}: x = {x[num]}, y = {y[num]}") #muestra en que num te llegas
    trayectoria_anim.set_data_3d(x[:num], y[:num], z[:num]) #muestra la trayectoria que se va siguiendo, el : sirve para que se tome desde 0 hasta numero
    bola_anim.set_data_3d([x[num]], [y[num]], [z[num]]) #toma desde 0 hasta num y borra los anteriores = (bola se muve siguiendo lo trayectoria)
    return trayectoria_anim, bola_anim

# Crear la animación (es como hacer img =plt.figure(), pero con la animación)
ani = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=0.1) #FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval= h*1000 = sea mismo tiempo físico)



# vemos rapidez de la animacion a exportar
n, n_txt = input_parametro("Velocidad de la animación (ej: 1=normal, 2=algo, 3=rápido)")


###############-----############### Guardo la animacion : quitar el # a lo de abajo si quiero guardar la animacion en la carpeta donde esta el .py
#directorio_del_script = os.path.dirname(os.path.abspath(__file__)) #nos da la ruta donde esta el .py
#Guardamos imagen (no quitar este #)
#nombre_archivo_imagen = "Atractor_de_Lorenz(png).png" #nombre de archivo a guardar como imagen
#ruta_guardado_imagen = os.path.join(directorio_del_script, nombre_archivo_imagen) #para guardar el archivo en la carpeta donde esta el .py
#fig_img.savefig(ruta_guardado_imagen, dpi=200) #esto es para guardar la imagen, con el nombre y la ruta que hemos definido antes, y con el dpi(pixeles por pulgada)
#print(f"Imagen guardada como: {nombre_archivo_imagen}")
#print(f"Archivo guardado en: {ruta_guardado_imagen}")

#Guardamos video (no quitar este #)
#nombre_archivo_video = "Atractor_de_Lorenz(mp4).mp4" #nombre de archivo a guardar
#ruta_guardado = os.path.join(directorio_del_script, nombre_archivo_video) #para guardar el archivo en la carpeta donde esta el .py

#writer = FFMpegWriter(fps=int(n*1/h), metadata=dict(artist="Mario Carracedo Andrés"), bitrate=2500) #
#ani.save(ruta_guardado, writer=writer, dpi=200) #esto es para guardar la animacion, con el nombre y la ruta que hemos definido antes, y con el writer que hemos configurado con los fps, el artista y el bitrate(calidad del video)
#print(f"Animación guardada como: {nombre_archivo_video}")
#print(f"Archivo guardado en: {ruta_guardado}")

###############-----############### Graficar resultados
plt.show() # siempre despues de ani.save 

 