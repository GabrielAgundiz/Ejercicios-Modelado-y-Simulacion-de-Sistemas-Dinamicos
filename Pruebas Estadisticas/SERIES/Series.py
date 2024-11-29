import numpy as np
import csv

def main():
    # Solicitar la cantidad de números
    N = int(input("Ingrese la cantidad de números (N): "))
    
    # Solicitar los números rectangulares
    numeros = []
    print("Ingrese los números rectangulares:")
    for i in range(N):
        while True:
            try:
                numero = float(input(f"Número {i + 1}: "))
                numeros.append(numero)
                break
            except ValueError:
                print("Entrada no válida. Ingrese un número.")
    
    # Mostrar los pares generados (x_i, x_{i+1})
    print("\nPares generados:")
    pares = [(numeros[i], numeros[i + 1]) for i in range(N - 1)]
    for i, (x, y) in enumerate(pares):
        print(f"Par {i + 1}: ({x}, {y})")
    
    # Solicitar la cantidad de subintervalos
    n = int(input("Ingrese la cantidad de subintervalos: "))
    
    # Calcular la frecuencia esperada FEi
    FEi = (N - 1) / (n * n)
    
    # Definir los límites de los subintervalos en el plano bidimensional
    intervalos = np.linspace(0, 1, n + 1)
    
    # Inicializar la matriz de frecuencias observadas
    FOij = np.zeros((n, n))
    
    # Formar las parejas y contar las frecuencias observadas
    for x1, y2 in pares:
        for ix in range(n):
            if intervalos[ix] <= x1 < intervalos[ix + 1]:
                for iy in range(n):
                    if intervalos[iy] <= y2 < intervalos[iy + 1]:
                        FOij[ix, iy] += 1
                        break
                break
        else:
            if x1 == 1:  # Caso especial cuando x1 es exactamente 1
                for iy in range(n):
                    if intervalos[iy] <= y2 < intervalos[iy + 1]:
                        FOij[n - 1, iy] += 1
                        break
    
    # Calcular el estadístico X0^2
    X0_2 = ((n * n) / (N - 1)) * sum((FOij[i, j] - FEi) ** 2 for i in range(n) for j in range(n))
    
    # Mostrar las frecuencias observadas y esperadas, y el estadístico X0^2
    print("\nFrecuencias observadas y esperadas por subintervalo:")
    for i in range(n):
        for j in range(n):
            print(f"Celda ({i}, {j}): FO = {FOij[i, j]}, FE = {FEi:.2f}")
    
    print(f"\nValor de X0^2: {X0_2:.5f}")
    
    # Solicitar el valor del estadístico de tablas
    estadistico_tablas = float(input("Ingrese el valor del estadístico de tablas: "))
    
    # Comparar X0^2 con el estadístico de tablas
    if X0_2 < estadistico_tablas:
        print("Los números son aceptados.")
    else:
        print("Los números NO son aceptados.")
    
    # Guardar los resultados en un archivo CSV
    with open('resultados_series.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Celda', 'FO', 'FE'])
        for i in range(n):
            for j in range(n):
                writer.writerow([f"({i}, {j})", FOij[i, j], FEi])

if __name__ == "__main__":
    main()
