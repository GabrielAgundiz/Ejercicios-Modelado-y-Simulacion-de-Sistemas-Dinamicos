import math
import numpy as np
import csv

def main():
    # Solicitar la cantidad de números
    N = int(input("Ingrese la cantidad de números (N): "))
    
    # Solicitar los números rectangulares
    numeros = []
    print("Ingrese los números rectangulares:")
    for i in range(N):
        numero = float(input(f"Número {i + 1}: "))
        numeros.append(numero)
    
    # Solicitar la cantidad de subintervalos
    n = int(input("Ingrese la cantidad de subintervalos: "))
    
    # Calcular la frecuencia esperada FEi
    FEi = N / n
    
    # Definir los límites de los subintervalos
    intervalos = np.linspace(0, 1, n + 1)
    
    # Contar la frecuencia observada en cada subintervalo
    FOi = [0] * n
    for numero in numeros:
        for i in range(n):
            if intervalos[i] <= numero < intervalos[i + 1]:
                FOi[i] += 1
                break
        else:
            if numero == 1:  # Incluye el caso especial en que el número sea exactamente 1
                FOi[n - 1] += 1

    # Calcular el estadístico X2
    X2 = sum(((FOi[i] - FEi) ** 2) / FEi for i in range(n))
    
    # Mostrar las frecuencias observadas y esperadas, y el estadístico X2
    print("\nFrecuencias observadas y esperadas por subintervalo:")
    for i in range(n):
        print(f"Intervalo {intervalos[i]:.2f} - {intervalos[i+1]:.2f}: FO = {FOi[i]}, FE = {FEi:.2f}")
    
    print(f"\nValor de X2: {X2:.5f}")
    
    # Solicitar el valor del estadístico de tablas
    estadistico_tablas = float(input("Ingrese el valor del estadístico de tablas: "))
    
    # Comparar X2 con el estadístico de tablas
    if X2 < estadistico_tablas:
        print("Los números son aceptados.")
    else:
        print("Los números NO son aceptados.")
    
    # Guardar los resultados en un archivo CSV
    with open('resultados_frecuencias.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Intervalo', 'FO', 'FE'])
        for i in range(n):
            writer.writerow([f"{intervalos[i]:.2f} - {intervalos[i+1]:.2f}", FOi[i], FEi])

if __name__ == "__main__":
    main()
