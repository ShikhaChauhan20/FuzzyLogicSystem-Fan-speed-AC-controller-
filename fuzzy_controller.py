import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk

temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')

temperature['Cold'] = fuzz.trapmf(temperature.universe, [0, 0, 10, 20])
temperature['Warm'] = fuzz.trimf(temperature.universe, [15, 25, 35])
temperature['Hot'] = fuzz.trapmf(temperature.universe, [30, 35, 40, 40])

humidity['Low'] = fuzz.trapmf(humidity.universe, [0, 0, 20, 40])
humidity['Moderate'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['High'] = fuzz.trapmf(humidity.universe, [60, 80, 100, 100])

fan_speed['Slow'] = fuzz.trapmf(fan_speed.universe, [0, 0, 20, 40])
fan_speed['Medium'] = fuzz.trimf(fan_speed.universe, [30, 50, 70])
fan_speed['Fast'] = fuzz.trapmf(fan_speed.universe, [60, 80, 100, 100])

rule1 = ctrl.Rule(temperature['Cold'] & humidity['Low'], fan_speed['Slow'])
rule2 = ctrl.Rule(temperature['Warm'] & humidity['Moderate'], fan_speed['Medium'])
rule3 = ctrl.Rule(temperature['Hot'] | humidity['High'], fan_speed['Fast'])
rule4 = ctrl.Rule(temperature['Warm'] & humidity['High'], fan_speed['Fast'])
rule5 = ctrl.Rule(temperature['Cold'] & humidity['High'], fan_speed['Medium'])

fan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
fan_simulation = ctrl.ControlSystemSimulation(fan_ctrl)

def compute_fan_speed(input_temp, input_hum):
    fan_simulation.input['temperature'] = input_temp
    fan_simulation.input['humidity'] = input_hum
    fan_simulation.compute()
    return fan_simulation.output['fan_speed']

app = tk.Tk()
app.title("Fuzzy Fan / AC Controller System")
app.geometry("400x350")

ttk.Label(app, text="Room Temperature (°C):", font=("Arial", 10)).pack(pady=5)
temp_entry = ttk.Entry(app)
temp_entry.pack(pady=5)
temp_entry.insert(0, "30")

ttk.Label(app, text="Humidity (%):", font=("Arial", 10)).pack(pady=5)
hum_entry = ttk.Entry(app)
hum_entry.pack(pady=5)
hum_entry.insert(0, "70")

result_label = ttk.Label(app, text="Fan Speed Output: --", font=("Arial", 12, "bold"))
result_label.pack(pady=20)

def on_calculate():
    try:
        t = float(temp_entry.get())
        h = float(hum_entry.get())
        speed = compute_fan_speed(t, h)
        
        if speed < 35:
            category = "Slow"
        elif speed < 70:
            category = "Medium"
        else:
            category = "Fast"
            
        result_label.config(text=f"Fan Speed: {speed:.1f}% ({category})")
    except ValueError:
        result_label.config(text="Please enter valid numeric values!")

calc_button = ttk.Button(app, text="Calculate Fan Speed", command=on_calculate)
calc_button.pack(pady=10)

app.mainloop()