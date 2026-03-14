# CONTENIDO
    Contiene 2 programas en los que se usa el método de RK4 (aprenidos en Física Computacional en la UVa), para resolver varios sistemas de interés. Hallar las ecuaciones del movimiento se mostrarán en 2 archivos realizados en LaTex, donde se usó la conservación de la energía. (Aún los estoy pasando a LaTex por ende si no se encuentran es por eso).

    El péndulo consiste de una masa que cuelga de una cuerda y por acción de la gravedad, esté oscilaría si la condición del ángulo inicial es disitnto de 0 o PI. Sin embargo, no solo se queda ahí la cosa, nosotros podemos acoplar tantos péndulos como queramos. En este caso los programas represetnarán un péndulo y el otro un péndulo doble.
## Péndulo_2D_animado
### Parámetros del programa
- `L`: longitud de la cuerda inexstensible
- `angulo_0`: angulo inicial(grados) entre 0 y 180

#### Ejemplo
- `T = 0.5 * m * diff(q, t)**2` #diff(q,t) es la derivada de q respecto de t
- `V = 0.5 * k * q**2`

## Péndulo_doble_2D_animado
    Aún tengo que preprar el pdf con el desarrollo teórico