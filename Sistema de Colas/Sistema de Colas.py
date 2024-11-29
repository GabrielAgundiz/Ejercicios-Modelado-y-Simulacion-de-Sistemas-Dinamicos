import random
import csv
import os
from datetime import datetime, timedelta

# Distribuciones de probabilidad para camiones y tiempos
distribucion_camiones = [
    (0, 0.50),
    (1, 0.25),
    (2, 0.15),
    (3, 0.10)
]

distribucion_llegadas = [
    (20, 0.02),
    (25, 0.03),
    (30, 0.25),
    (35, 0.20),
    (40, 0.20),
    (45, 0.15),
    (50, 0.10),
    (55, 0.05),
    (60, 0.03)
]

distribuciones_servicio = {
    3: [
        (20, 0.05),
        (25, 0.10),
        (30, 0.20),
        (35, 0.25),
        (40, 0.12),
        (45, 0.10),
        (50, 0.08),
        (55, 0.06),
        (60, 0.04)
    ],
    4: [
        (15, 0.05),
        (20, 0.15),
        (25, 0.20),
        (30, 0.20),
        (35, 0.15),
        (40, 0.12),
        (45, 0.08),
        (50, 0.05),
        (55, 0.01)
    ],
    5: [
        (10, 0.10),
        (15, 0.18),
        (20, 0.22),
        (25, 0.18),
        (30, 0.10),
        (35, 0.08),
        (40, 0.06),
        (45, 0.05),
        (50, 0.03)
    ],
    6: [
        (5, 0.12),
        (10, 0.15),
        (15, 0.26),
        (20, 0.15),
        (25, 0.12),
        (30, 0.08),
        (35, 0.06),
        (40, 0.04),
        (45, 0.02)
    ]
}

# Función para calcular la probabilidad acumulada y los rangos
def calcular_acumulada_y_rango(distribucion):
    acumulada = 0
    distribucion_con_rango = []
    for valor, prob in distribucion:
        acumulada += prob
        distribucion_con_rango.append((valor, prob, acumulada))
    return distribucion_con_rango

# Función para asignar valores según el rango
def asignar_valores_segun_rango(random_values, distribucion_con_rango):
    valores_asignados = []
    for r in random_values:
        for valor, _, acum in distribucion_con_rango:
            if r <= acum:
                valores_asignados.append(valor)
                break
    return valores_asignados

# Función para guardar resultados en CSV
def guardar_csv(tiempo_llegadas, tiempo_servicio, num_camiones, distribucion_camiones, distribucion_llegadas, distribucion_servicio, resultados, ruta_csv='resultados_sistema_colas.csv'):
    with open(ruta_csv, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        
        # Guardar distribución de camiones
        escritor_csv.writerow(['Num de Camiones', 'Probabilidad', 'Probabilidad Acumulada'])
        for valor, prob, acum in distribucion_camiones:
            escritor_csv.writerow([valor, prob, acum])
        
        escritor_csv.writerow([])
        
        # Guardar distribución de llegadas
        escritor_csv.writerow(['Tiempo entre Llegadas', 'Probabilidad', 'Probabilidad Acumulada'])
        for valor, prob, acum in distribucion_llegadas:
            escritor_csv.writerow([valor, prob, acum])
        
        escritor_csv.writerow([])
        
        # Guardar distribución de servicio
        escritor_csv.writerow(['Tiempo de Servicio', 'Probabilidad', 'Probabilidad Acumulada'])
        for valor, prob, acum in distribucion_servicio:
            escritor_csv.writerow([valor, prob, acum])
        
        escritor_csv.writerow([])
        
        # Guardar tiempos generados
        escritor_csv.writerow(['Contador', 'Tiempo Entre Llegadas', 'Tiempo de Servicio'])
        for i, (llegada, servicio) in enumerate(zip(tiempo_llegadas, tiempo_servicio)):
            escritor_csv.writerow([i + 1, llegada, servicio])
        
        escritor_csv.writerow([])
        
        # Guardar resultados finales
        escritor_csv.writerow(['Numero aleatorio', 'Tiempo entre llegadas', 'Hora de llegada', 'Hora de inicio del servicio', 'Numero aleatorio', 'Tiempo de servicio', 'Hora de fin del servicio', 'Ocio del personal', 'Tiempo de espera del camion', 'Longitud de la cola'])
        for resultado in resultados:
            escritor_csv.writerow(resultado)
    return ruta_csv

def abrir_csv_con_excel(ruta_csv):
    if os.name == 'nt':  # Verifica si el sistema operativo es Windows
        os.system(f'start excel "{ruta_csv}"')
    else:
        print("Este método solo es compatible con Windows.")

# Función principal para ejecutar el programa
def main():
    hora_inicio_str = input("Ingrese la hora de inicio del servicio (en formato HH:MM, 24 horas): ")
    hora_cierre_str = input("Ingrese la hora de cierre del servicio (en formato HH:MM, 24 horas): ")
    
    hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M')
    hora_cierre = datetime.strptime(hora_cierre_str, '%H:%M')
    
    # No recibir camiones 30 minutos antes del cierre
    hora_cierre -= timedelta(minutes=30)
    
    num_personas = int(input("Ingrese el número de personas en servicio (entre 3 y 6): "))
    
    if num_personas < 3 or num_personas > 6:
        print("Número de personas en servicio debe estar entre 3 y 6.")
        return
    
    # Calcular distribuciones acumuladas y rangos
    dist_camiones_acumulada = calcular_acumulada_y_rango(distribucion_camiones)
    dist_llegadas_acumulada = calcular_acumulada_y_rango(distribucion_llegadas)
    dist_servicio_acumulada = calcular_acumulada_y_rango(distribuciones_servicio[num_personas])
    
    # Generar números aleatorios
    random_llegadas = [random.uniform(0, 1) for _ in range(20)]
    random_servicio = [random.uniform(0, 1) for _ in range(20)]
    
    # Asignar valores según el rango
    tiempo_llegadas = asignar_valores_segun_rango(random_llegadas, dist_llegadas_acumulada)
    tiempo_servicio = asignar_valores_segun_rango(random_servicio, dist_servicio_acumulada)
    
    # Generar resultados del sistema de colas
    resultados = []
    hora_llegada = hora_inicio
    hora_inicio_servicio = hora_inicio
    
    for i in range(len(tiempo_llegadas)):
        if i > 0:
            hora_llegada += timedelta(minutes=tiempo_llegadas[i])
        if hora_llegada < hora_inicio_servicio:
            hora_inicio_servicio = hora_llegada
        hora_fin_servicio = hora_inicio_servicio + timedelta(minutes=tiempo_servicio[i])
        
        if hora_llegada >= hora_cierre:
            break
        
        ocio_personal = max(timedelta(0), hora_inicio_servicio - hora_llegada)
        tiempo_espera_camion = max(timedelta(0), hora_llegada - hora_inicio_servicio)
        
        # Convertir hora_fin_servicio a datetime para la comparación
        longitud_cola = max(0, i - len([r for r in resultados if datetime.strptime(r[6], '%H:%M') <= hora_inicio_servicio]))
        
        resultados.append([
            random_llegadas[i], tiempo_llegadas[i], hora_llegada.strftime('%H:%M'), hora_inicio_servicio.strftime('%H:%M'), 
            random_servicio[i], tiempo_servicio[i], hora_fin_servicio.strftime('%H:%M'), 
            ocio_personal.total_seconds() / 60, tiempo_espera_camion.total_seconds() / 60, longitud_cola
        ])
        
        hora_inicio_servicio = hora_fin_servicio
    
    # Guardar resultados en CSV
    ruta_csv = guardar_csv(tiempo_llegadas, tiempo_servicio, num_personas, dist_camiones_acumulada, dist_llegadas_acumulada, dist_servicio_acumulada, resultados)
    print("Archivo CSV generado con éxito.")
    abrir_csv_con_excel(ruta_csv)

if __name__ == "__main__":
    main()
