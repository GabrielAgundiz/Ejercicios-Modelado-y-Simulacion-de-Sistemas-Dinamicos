import csv
import os

def abrir_csv_con_excel(ruta_csv):
    if os.name == 'nt':  # Verifica si el sistema operativo es Windows
        os.system(f'start excel "{ruta_csv}"')
    else:
        print("Este método solo es compatible con Windows.")

def congruencial_mixto(a, Xo, c, m, n):
    resultados = []
    Xn = Xo
    for i in range(n):
        aXo_plus_c = a * Xn + c
        resultado_fraccion_mixta = f"{aXo_plus_c // m} + {aXo_plus_c % m}/{m}"
        Xn_mas_1 = (aXo_plus_c) % m
        numero_rectangular = Xn_mas_1 / m
        resultados.append([i+1, Xn, resultado_fraccion_mixta, Xn_mas_1, numero_rectangular])
        Xn = Xn_mas_1
    return resultados

def guardar_csv(resultados):
    with open('resultados_congruencial_mixto.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(['n', 'Xo', '(a*Xo + c) % m', 'Xn+1', 'NUMEROS RECTANGULARES'])
        escritor_csv.writerows(resultados)

def main():
    a = 10
    Xo = 13
    c = 8
    m = 16
    n = m
    
    resultados = congruencial_mixto(a, Xo, c, m, n)
    guardar_csv(resultados)
    print("Archivo CSV generado con éxito.")
    ruta_csv = 'resultados_congruencial_mixto.csv'
    abrir_csv_con_excel(ruta_csv)
    

if __name__ == "__main__":
    main()
