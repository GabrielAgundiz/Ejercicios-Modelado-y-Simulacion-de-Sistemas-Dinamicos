import math
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
    
    # Ordenar los números en forma ascendente
    numeros.sort()
    
    # Calcular las distancias acumuladas y el estadístico Dn
    Dn = 0
    resultados = []
    
    print("\nDistancias acumuladas y estadísticos de prueba:")
    for i in range(1, N + 1):
        Fxi = i / N
        dist = abs(Fxi - numeros[i - 1])
        resultados.append([i, numeros[i - 1], Fxi, dist])
        print(f"Número: {numeros[i - 1]:.5f}, F(xi): {i}/{N}= {Fxi:.5f}, |F(xi) - xi|: {dist:.5f}")
        if dist > Dn:
            Dn = dist
    
    # Mostrar el valor de Dn
    print(f"\nValor de Dn: {Dn:.5f}")
    
    # Solicitar el valor del estadístico de tablas
    estadistico_tablas = float(input("Ingrese el valor del estadístico de tablas: "))
    
    # Comparar Dn con el estadístico de tablas
    if Dn < estadistico_tablas:
        print("Los números son aceptados.")
    else:
        print("Los números NO son aceptados.")
    
    # Guardar los resultados en un archivo CSV
    with open('resultados_ks.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['i', 'Xi', 'F(Xi)', 'Dn'])
        for resultado in resultados:
            writer.writerow(resultado)

if __name__ == "__main__":
    main()
