# CONTENIDO

## ECUACIONES DE LAGRANGE EN 1D
    EL porgrama está pensado para que manualmente se halle la energía cinética y potencial del sistema físico a analizar y que esté te de en formato LaTex, las ecuaciones de Euler-lagrange del sistema (el programa te devuelve la expresión, pero la ecuación hay que igualarla a 0).

### Parámetros del programa
- `T`: Energía cinética total
- `V`: Energía potencial total(gravitatorio, elástica...)

#### Ejemplo
- `T = 0.5 * m * diff(q, t)**2` #diff(q,t) es la derivada de q respecto de t
- `V = 0.5 * k * q**2`

## Como ejecutar
1. Asegurate de tener un entorno virtual activado
2. Instalar las dependencias:
"""
pip install -r requirements.txt
"""
