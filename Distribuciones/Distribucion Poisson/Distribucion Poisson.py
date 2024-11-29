import math
import random
import csv
import os

def poisson_distribution(lam, num_values):
    # Calcular la distribución de probabilidad de Poisson
    def poisson_prob(lam, x):
        return (math.exp(-lam) * lam**x) / math.factorial(x)
    
    # Generar la tabla de la distribución acumulada
    distribution = []
    cumulative_prob = 0.0
    x = 0
    while cumulative_prob < 0.99995:
        prob = poisson_prob(lam, x)
        cumulative_prob += prob
        distribution.append((x, cumulative_prob, prob))
        x += 1
    
    # Generar valores aleatorios siguiendo la distribución de Poisson
    values = []
    for _ in range(num_values):
        r = random.uniform(0, 1)
        for (x, cumulative_prob, _) in distribution:
            if r < cumulative_prob:
                values.append(r)
                break
    
    return values, distribution

def guardar_csv(values, distribution, ruta_csv='resultados_poisson.csv'):
    with open(ruta_csv, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(['Valor', 'Probabilidad', 'Probabilidad Acumulada'])
        for (x, prob_acumulada, prob) in distribution:
            escritor_csv.writerow([x, prob, prob_acumulada])
        escritor_csv.writerow([])
        escritor_csv.writerow(['Contador', 'Número Generado', 'Valor Obtenido'])
        contador = 1
        for value in values:
            valor_obtenido = next(x for (x, cum_prob, _) in distribution if cum_prob >= value)
            escritor_csv.writerow([contador, value, valor_obtenido])
            contador += 1
        escritor_csv.writerow([])
        escritor_csv.writerow(['Tabla de Rangos'])
        escritor_csv.writerow(['Rango Inicial', 'Rango Final', 'Valor Asignado'])
        for i in range(len(distribution) - 1):
            rango_inicial = 0 if i == 0 else distribution[i - 1][1]
            rango_final = distribution[i][1]
            valor_asignado = distribution[i][0]
            escritor_csv.writerow([rango_inicial, rango_final, valor_asignado])
    return ruta_csv

def abrir_csv_con_excel(ruta_csv):
    if os.name == 'nt':  # Verifica si el sistema operativo es Windows
        os.system(f'start excel "{ruta_csv}"')
    else:
        print("Este método solo es compatible con Windows.")

def main():
    lam = float(input("Ingrese el valor de λ (lambda): "))
    num_values = int(input("Ingrese el número de días: "))
    
    values, distribution = poisson_distribution(lam, num_values)
    
    ruta_csv = guardar_csv(values, distribution)
    print("Archivo CSV generado con éxito.")
    abrir_csv_con_excel(ruta_csv)

if __name__ == "__main__":
    main()
