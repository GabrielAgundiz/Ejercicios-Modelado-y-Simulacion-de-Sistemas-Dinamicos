import csv
import os

def abrir_csv_con_excel(ruta_csv):
    if os.name == 'nt':  # Verifica si el sistema operativo es Windows
        os.system(f'start excel "{ruta_csv}"')
    else:
        print("Este método solo es compatible con Windows.")

def congruencial_hibrido(a, b, c, Xo, m, n):
    resultados = []
    Xn = Xo
    for i in range(n):
        aXn_plus_bc = a * Xn + b * c
        resultado_fraccion_hibrido = f"{aXn_plus_bc // m} + {aXn_plus_bc % m}/{m}"
        Xn_mas_1 = aXn_plus_bc % m
        numero_rectangular = Xn_mas_1 / m
        resultados.append([i+1, Xn, resultado_fraccion_hibrido, Xn_mas_1, numero_rectangular])
        Xn = Xn_mas_1
    return resultados

def guardar_csv(resultados):
    ruta_csv = 'resultados_congruencial_hibrido.csv'
    with open(ruta_csv, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(['n', 'Xn', '(a*Xn + b*c) % m', 'Xn+1', 'NUMEROS RECTANGULARES'])
        escritor_csv.writerows(resultados)
    return ruta_csv

def calcular_periodo_esperado(modulo):
    if isinstance(modulo, int):
        if modulo & (modulo - 1) == 0 and modulo != 0:
            # Módulo es binario
            periodo_binario = modulo // 4
            return periodo_binario, "binario"
        else:
            # Módulo es decimal
            str_modulo = str(modulo)
            potencia = len(str_modulo) - 1
            
            if potencia >= 5:
                # Módulo es un número decimal cuyo exponente es mayor o igual a 5
                return 5 * 10**(potencia - 2), "decimal"
            elif potencia < 5:
                # Módulo es un número decimal cuyo exponente es menor a 5
                return 5**(potencia-1)*4, "decimal"
    else:
        return "Error: El módulo debe ser un número entero."

def es_generador_confiable(Xo, periodo_esperado, resultados):
    primer_Xn = resultados[0][1]  # Primer valor de Xn
    for fila in resultados:
        if fila[3] == primer_Xn:  # Si se repite el mismo valor que la primer Xn en Xn+1
            return False
    # Si Xo es igual a la última iteración de Xn+1 y las iteraciones de la tabla son igual al periodo esperado, entonces es CONFIABLE
    if Xo == resultados[-1][3] and periodo_esperado == len(resultados):
        return True
    else:
        return False

def main():
    a = int(input("Ingrese el valor de 'a': "))
    b = int(input("Ingrese el valor de 'b': "))
    c = int(input("Ingrese el valor de 'c': "))
    Xo = int(input("Ingrese el valor de 'Xo': "))
    m = int(input("Ingrese el valor de 'm': "))
    periodo_esperado, tipo_modulo = calcular_periodo_esperado(m)  # Calcula el periodo esperado

    # El número real de iteraciones se basa en el periodo esperado
    resultados = congruencial_hibrido(a, b, c, Xo, m, periodo_esperado)

    print(f"Periodo esperado: {periodo_esperado} ({tipo_modulo})")

    ruta_csv = guardar_csv(resultados)
    print("Archivo CSV generado con éxito.")

    if es_generador_confiable(Xo, periodo_esperado, resultados):
        print(f"Generador Congruencial Híbrido CONFIABLE")
    else:
        print("Generador Congruencial Híbrido NO CONFIABLE")

    abrir_csv_con_excel(ruta_csv)

if __name__ == "__main__":
    main()