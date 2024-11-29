import simpy
import random
import tkinter as tk
from tkinter import messagebox
import math

# Parámetros del problema
LLEGADAS_MEDIA = 20  # media de llegadas por hora (distribución de Poisson)
TIEMPO_SERVICIO_1_MEDIA = 2  # media de servicio en estación 1 en minutos (distribución exponencial)
TIEMPO_SERVICIO_2_MIN = 1  # tiempo mínimo de servicio en estación 2 en minutos (distribución uniforme)
TIEMPO_SERVICIO_2_MAX = 2  # tiempo máximo de servicio en estación 2 en minutos (distribución uniforme)

# Funciones de distribución
def poisson_distribution(lam, num_values=1):
    def poisson_prob(lam, x):
        return (math.exp(-lam) * lam**x) / math.factorial(x)
    
    distribution = []
    cumulative_prob = 0.0
    x = 0
    while cumulative_prob < 0.99995:
        prob = poisson_prob(lam, x)
        cumulative_prob += prob
        distribution.append((x, cumulative_prob))
        x += 1
    
    values = []
    for _ in range(num_values):
        r = random.uniform(0, 1)
        for (x, cumulative_prob) in distribution:
            if r < cumulative_prob:
                values.append(x)
                break
    
    return values[0] if num_values == 1 else values

def uniform_distribution(a, b):
    return random.uniform(a, b)

# Interfaz gráfica
class SimulacionGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Simulación de Sistema de Colas")
        self.canvas = tk.Canvas(self, width=800, height=400, bg="white")
        self.canvas.pack()
        
        self.start_button = tk.Button(self, text="Iniciar Simulación", command=self.run_simulation)
        self.start_button.pack(pady=10)
        
        self.pause_button = tk.Button(self, text="Pausar/Reanudar Simulación", command=self.toggle_pause)
        self.pause_button.pack(pady=10)
        
        self.instant_button = tk.Button(self, text="Ejecutar al Instante", command=self.run_instant)
        self.instant_button.pack(pady=10)
        
        self.servicio_1_area = self.canvas.create_rectangle(150, 100, 250, 200, fill="lightblue")
        self.servicio_2_area = self.canvas.create_rectangle(550, 100, 650, 200, fill="lightgreen")
        
        self.servicio_1_cola_label = tk.Label(self, text="Cola Estación 1: 0")
        self.servicio_1_cola_label.pack()
        self.servicio_1_atendidos_label = tk.Label(self, text="Atendidos Estación 1: 0")
        self.servicio_1_atendidos_label.pack()
        
        self.servicio_2_cola_label = tk.Label(self, text="Cola Estación 2: 0")
        self.servicio_2_cola_label.pack()
        self.servicio_2_atendidos_label = tk.Label(self, text="Atendidos Estación 2: 0")
        self.servicio_2_atendidos_label.pack()

        self.tiempos_totales = []
        self.client_objects = []

        self.servicio_1_cola = 0
        self.servicio_1_atendidos = 0
        self.servicio_2_cola = 0
        self.servicio_2_atendidos = 0

        self.paused = False
        self.instant = False
        
    def run_simulation(self):
        self.env = simpy.Environment()
        self.servicio_1 = simpy.Resource(self.env, capacity=1)
        self.servicio_2 = simpy.Resource(self.env, capacity=1)
        self.env.process(self.llegada_clientes(self.env, self.servicio_1, self.servicio_2))
        self.after(100, self.update_simulation)
        
    def update_simulation(self):
        if not self.paused:
            try:
                self.env.step()
            except RuntimeError:
                tiempo_promedio = sum(self.tiempos_totales) / len(self.tiempos_totales)
                mensaje = f'Tiempo promedio en el sistema: {tiempo_promedio:.2f} minutos\n'
                if self.servicio_1_cola > self.servicio_2_cola:
                    mensaje += "La cola en la Estación 1 es mayor."
                else:
                    mensaje += "La cola en la Estación 2 es mayor."
                messagebox.showinfo("Resultados", mensaje)
                return
        self.after(100, self.update_simulation)
        
    def llegada_clientes(self, env, servicio_1, servicio_2):
        cliente_id = 0
        while True:
            tiempo_llegada = poisson_distribution(60 / LLEGADAS_MEDIA) / 60  # en horas
            yield env.timeout(tiempo_llegada)
            cliente_id += 1
            env.process(self.proceso_cliente(env, cliente_id, servicio_1, servicio_2))
            
    def proceso_cliente(self, env, cliente_id, servicio_1, servicio_2):
        llegada = env.now
        x, y = 50, 150
        cliente_obj = self.canvas.create_oval(x, y, x + 20, y + 20, fill="red")
        self.client_objects.append(cliente_obj)
        
        # Estación 1
        self.servicio_1_cola += 1
        self.update_labels()
        with servicio_1.request() as req1:
            yield req1
            self.servicio_1_cola -= 1
            self.servicio_1_atendidos += 1
            self.update_labels()
            self.move_client(cliente_obj, 200, 150)
            tiempo_servicio_1 = random.expovariate(1 / TIEMPO_SERVICIO_1_MEDIA)
            yield env.timeout(tiempo_servicio_1)
        
        # Estación 2
        self.servicio_2_cola += 1
        self.update_labels()
        with servicio_2.request() as req2:
            yield req2
            self.servicio_2_cola -= 1
            self.servicio_2_atendidos += 1
            self.update_labels()
            self.move_client(cliente_obj, 600, 150)
            tiempo_servicio_2 = uniform_distribution(TIEMPO_SERVICIO_2_MIN, TIEMPO_SERVICIO_2_MAX)
            yield env.timeout(tiempo_servicio_2)
        
        self.canvas.delete(cliente_obj)
        tiempo_total = env.now - llegada
        self.tiempos_totales.append(tiempo_total)
        print(f'Cliente {cliente_id} completó el servicio en {tiempo_total:.2f} minutos.')
        
    def update_labels(self):
        self.servicio_1_cola_label.config(text=f"Cola Estación 1: {self.servicio_1_cola}")
        self.servicio_1_atendidos_label.config(text=f"Atendidos Estación 1: {self.servicio_1_atendidos}")
        self.servicio_2_cola_label.config(text=f"Cola Estación 2: {self.servicio_2_cola}")
        self.servicio_2_atendidos_label.config(text=f"Atendidos Estación 2: {self.servicio_2_atendidos}")
        
    def move_client(self, client_obj, x, y):
        if self.instant:
            self.canvas.coords(client_obj, x, y, x + 20, y + 20)
            self.canvas.update()
        else:
            current_coords = self.canvas.coords(client_obj)
            dx = x - current_coords[0]
            dy = y - current_coords[1]
            steps = 10  # Número de pasos para un movimiento suave
            for _ in range(steps):
                self.canvas.move(client_obj, dx/steps, dy/steps)
                self.canvas.update()
                self.after(10)  # 100 ms por paso para hacer un total de 1 segundo
            self.after(1000)  # Pausa adicional de 1 segundo después de llegar al destino

    def toggle_pause(self):
        self.paused = not self.paused

    def run_instant(self):
        self.instant = True

# Ejecutar la aplicación
if __name__ == "__main__":
    app = SimulacionGUI()
    app.mainloop()
