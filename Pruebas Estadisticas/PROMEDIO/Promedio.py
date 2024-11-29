import math

def main():
    # Solicitar la cantidad de números
    N = int(input("Ingrese la cantidad de números (N): "))
    
    # Solicitar los números aleatorios
    numeros = []
    print("Ingrese los números aleatorios:")
    for i in range(N):
        numero = float(input(f"Número {i + 1}: "))
        numeros.append(numero)
    
    # Calcular la suma de los números
    suma = sum(numeros)
    
    # Calcular el promedio de los números
    promedio = suma / N
    
    # Mostrar la suma y el promedio
    print(f"Suma de los números: {suma}")
    print(f"Promedio de los números: {promedio}")
    
    # Calcular el estadístico Z0
    Z0 = abs(((promedio - 0.5) * math.sqrt(N)) / math.sqrt(1 / 12))
    
    # Mostrar el valor absoluto de Z0
    print(f"Valor absoluto de Z0: {Z0}")
    
    # Solicitar el valor del estadístico de tablas
    estadistico_tablas = float(input("Ingrese el valor del estadístico de tablas: "))
    
    # Comparar Z0 con el estadístico de tablas
    if Z0 < estadistico_tablas:
        print(f"{Z0}(Z0) < {estadistico_tablas}(Z-TABLAS): LOS NÚMEROS SON ACEPTADOS")
    else:
        print(f"{Z0}(Z0) < {estadistico_tablas}(Z-TABLAS): LOS NÚMEROS NO SON ACEPTADOS")

if __name__ == "__main__":
    main()
