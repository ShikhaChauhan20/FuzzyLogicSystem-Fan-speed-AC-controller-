
# Fuzzy Logic Fan / AC Controller System

A Python-based Artificial Intelligence project that uses **Fuzzy Logic** to intelligently control fan or AC speed based on room temperature and humidity, simulating human-like reasoning.

---

## Features & Tasks Implemented
1. **Input Variables:** Room Temperature (°C) and Humidity (%).
2. **Output Variable:** Fan Speed percentage (0% to 100%).
3. **Fuzzy Sets:** 
   - Temperature: *Cold, Warm, Hot*
   - Humidity: *Low, Moderate, High*
   - Fan Speed: *Slow, Medium, Fast*
4. **Membership Functions:** Triangular (`trimf`) and Trapezoidal (`trapmf`) shapes.
5. **Fuzzy Rules:** Custom IF-THEN logic rules for decision making.
6. **Inference & Defuzzification:** Automatic crisp output calculation using the Centroid method.
7. **Graphical User Interface (GUI):** Interactive desktop window built with `tkinter`.

---

## Prerequisites & Installation

Make sure Python is installed on your system. Open your terminal or command prompt in the project folder and run the following command to install the required libraries:

```bash
pip install numpy scikit-frontend scikit-fuzzy scipy networkx
