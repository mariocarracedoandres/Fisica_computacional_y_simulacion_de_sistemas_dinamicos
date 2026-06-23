# CONTENIDO
Contiene lo sigiente:
- Un archivo de código en Python llamado **Atractor_de_Lorenz.py**
- Este mismo archivo copn información llamado **README_atractor.md**
- Un archivo de video en formato mp4 llamado **Atractor _de_Lorenz(mp4).mp4**
- Un archivo de imagen en formato png llamado **Atractor_de_Lorenz(png).png**

## ATRACTOR DE LORENZ
El atractor de Lorentz es un ejemplo de un sistema de EDO, en el que se puede ver la trayectoria de una particula en base a unos parametros y condiciones iniciales.
Dependiendo de los paramatreos a, b, c. Se formaran todo típo de trayectorias.

En el codigo y archvios png y mp4 se representarán una trayectoría caoótica.


### Parámetros del programa
Los parámetros que se usarán en el programa son:
- `a`: primer parametro a
- `b`: segundo parametro b
- `c`: tercer parametro c
- `x0`: condicion inicial x0 (posicion en el eje x)
- `y0`: condicion inicial y0 (posicion en el eje y)
- `z0`: condicion inicial z0 (posicion en el eje z)
- `tf`: tiempo de duración
- `n`: velocidad de la animación (1 = normal ; 2 = algo rápido ; 3 = rápido) el **tiempo de la animacion será tf_real = tf/n**
La cuál se pedirán por pantalla al ejecutar el programa.
### Ejemplo del archivo mp4
- `a = 10`
- `b = 28`
- `c = 8/3`
- `x0 = 1`
- `y0 = 1`
- `z0 = 1`
- `tf = 40`
Para estos valores se obtiene una trayectoria caótica.

## CONSIDERACIONES
El porgrama tal cual no guardará nada, solo mostrará la animación por pantalla.
Si se quiere guardar, habrá un comentario al final del codigo donde se dirá que hay que quitar el # para que se puede guardar en la misma carpeta donde se encuentra el archivo.

Bibliografía:
- [Aractor de Lorenz](https://es.wikipedia.org/wiki/Atractor_de_Lorenz):
    De aquí se obtiene el sistema de EDO. y los valores de los parámetros (a, b, c)

## Como ejecutar
1. Asegurate de crear un entorno virtual y activarlo
2. Instalar las dependencias:
```
pip install -r requirements.txt
```