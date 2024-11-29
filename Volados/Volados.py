import random

# Generar una lista de números aleatorios para la simulación
random_numbers = [random.uniform(0,1) for _ in range(1000)]  # Generamos suficientes números aleatorios

# Solicitar al usuario el tipo de simulación
modo = input("¿Quieres hacerlo con iteraciones o corridas? (Escribe 'iteraciones' o 'corridas'): ").strip().lower()

# Inicialización de variables
cantidad_inicial = 50
meta = 80
apuesta_inicial = 10

# Variables para estadísticas
veces_meta = 0
veces_quiebra = 0
corridas_realizadas = 0
volados_realizados = 0

# Lista para almacenar las corridas
resultados = []

# Simulación según el modo seleccionado
if modo == 'iteraciones':
    iteraciones_totales = int(input("Ingrese el número de iteraciones: "))
    
    i = 0
    while volados_realizados < iteraciones_totales and i < len(random_numbers):
        corrida = corridas_realizadas + 1
        cantidad_actual = cantidad_inicial
        apuesta = apuesta_inicial
        corrida_resultado = []

        while cantidad_actual > 0 and cantidad_actual < meta and volados_realizados < iteraciones_totales and i < len(random_numbers):
            numero_aleatorio = random_numbers[i]
            resultado_volado = "Sí" if numero_aleatorio <= 0.5 else "No"
            cantidad_antes = cantidad_actual

            if resultado_volado == "Sí":
                cantidad_actual += apuesta
                apuesta = apuesta_inicial
            else:
                cantidad_actual -= apuesta
                apuesta *= 2

            cantidad_despues = cantidad_actual
            se_llego_meta = "Sí" if cantidad_actual >= meta else "No"

            # Registrar en la tabla
            corrida_resultado.append([
                corrida,
                cantidad_antes,
                apuesta if resultado_volado == "No" else apuesta_inicial,  # Apuesta antes del ajuste para la siguiente ronda
                numero_aleatorio,
                resultado_volado,
                cantidad_despues,
                se_llego_meta
            ])

            i += 1
            volados_realizados += 1

        # Actualizar estadísticas
        if cantidad_actual >= meta:
            veces_meta += 1
        else:
            veces_quiebra += 1

        corridas_realizadas += 1
        resultados.append(corrida_resultado)

elif modo == 'corridas':
    corridas_totales = int(input("Ingrese el número de corridas: "))

    i = 0
    while corridas_realizadas < corridas_totales and i < len(random_numbers):
        corrida = corridas_realizadas + 1
        cantidad_actual = cantidad_inicial
        apuesta = apuesta_inicial
        corrida_resultado = []

        while cantidad_actual > 0 and cantidad_actual < meta and i < len(random_numbers):
            numero_aleatorio = random_numbers[i]
            resultado_volado = "Sí" if numero_aleatorio <= 0.5 else "No"
            cantidad_antes = cantidad_actual

            if resultado_volado == "Sí":
                cantidad_actual += apuesta
                apuesta = apuesta_inicial
            else:
                cantidad_actual -= apuesta
                apuesta *= 2

            cantidad_despues = cantidad_actual
            se_llego_meta = "Sí" if cantidad_actual >= meta else "No"

            # Registrar en la tabla
            corrida_resultado.append([
                corrida,
                cantidad_antes,
                apuesta if resultado_volado == "No" else apuesta_inicial,  # Apuesta antes del ajuste para la siguiente ronda
                numero_aleatorio,
                resultado_volado,
                cantidad_despues,
                se_llego_meta
            ])

            i += 1
            volados_realizados += 1

        # Actualizar estadísticas
        if cantidad_actual >= meta:
            veces_meta += 1
        else:
            veces_quiebra += 1

        corridas_realizadas += 1
        resultados.append(corrida_resultado)

else:
    print("Modo no reconocido. Por favor, escribe 'iteraciones' o 'corridas'.")


probabilidad_meta = (veces_meta / corridas_realizadas) * 100 if corridas_realizadas > 0 else 0
probabilidad_quiebra = (veces_quiebra / corridas_realizadas) * 100 if corridas_realizadas > 0 else 0

# Resultados y estadísticas finales
if corridas_realizadas > 0:
    print(f"Probabilidad de llegar a la meta: {probabilidad_meta:.2f}%")
    print(f"Probabilidad de caer en la quiebra: {probabilidad_quiebra:.2f}%")
    print(f"Veces que se llegó a la meta: {veces_meta}")
    print(f"Veces que se llegó a la quiebra: {veces_quiebra}")
    print(f"Total de corridas realizadas: {corridas_realizadas}")
    print(f"Total de volados realizados: {volados_realizados}")

    # Mostrar resultados detallados de las corridas
    for corrida in resultados:
        print("\nCorrida:", corrida[0][0])
        for row in corrida:
            print(f"Cantidad antes del volado: ${row[1]:.2f}")
            print(f"Apuesta: ${row[2]:.2f}")
            print(f"Número aleatorio: {row[3]:.4f}")
            print(f"¿Se ganó el volado?: {row[4]}")
            print(f"Cantidad después del volado: ${row[5]:.2f}")
            print(f"¿Se llegó a la meta?: {row[6]}")
            print()
else:
    print("No se realizaron corridas.")

