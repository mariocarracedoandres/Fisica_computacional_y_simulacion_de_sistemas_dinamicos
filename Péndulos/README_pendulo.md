# CONTENIDO
Contiene 2 programas en los que se usa el método de RK4 (aprenidos en Física Computacional en la UVa), para resolver varios sistemas de interés. Hallar las ecuaciones del movimiento se mostrarán en 2 archivos realizados en LaTex, donde se usó la conservación de la energía. (Aún los estoy pasando a LaTex por ende si no se encuentran es por eso).

El péndulo consiste de una masa que cuelga de una cuerda y por acción de la gravedad, esté oscilaría si la condición del ángulo inicial es disitnto de 0 o PI. Sin embargo, no solo se queda ahí la cosa, nosotros podemos acoplar tantos péndulos como queramos. En este caso los programas represetnarán un péndulo y el otro un péndulo doble.
## Péndulo_2D_animado
### Parámetros del programa
- `L`: longitud de la cuerda inexstensible
- `angulo_0`: angulo inicial(grados) entre 0 y 180

### Como ejecutar el
1. Asegurate de tener un entorno virtual activado
2. Instalar las dependencias:
```
pip install -r requirements.txt
```

## Péndulo_doble_2D_animado
Los siguientes datos son pedidos al ejecutar el código. Por lo que no es necesario modificar nada.
### Parámetros del programa
- `L1`: longitud de la cuerda inexstensible 1(metros) (conecta sujeccion al techo con la masa 1)
- `L2`: longitud de la cuerda inexstensible 2(metros) (conecta las 2 masas)
- `m1`: masa 1(Kg) (masa (roja) mas cercana al punto de sujección)
- `m2`: masa 2(Kg) (masa (azul))
- `angulo1_0`: angulo inicial(grados) entre 0 y 180 de la masa 1 (respecto a la normal al techo/suelo)
- `angulo1_0`: angulo inicial(grados) entre 0 y 180 de la masa 2 (respecto a la normal al techo/suelo)

### Ejemplo del archivo mp4
- `L1 = 1`
- `L2 = 1`
- `m1 = 1`
- `m2 = 1`
- `angulo1_0 = 100`
- `angulo1_0 = 30`

### Como ejecutar el
1. Asegurate de tener un entorno virtual activado
2. Instalar las dependencias:
```
pip install -r requirements.txt
```
