
from agent.fuzzy_engine import (
    fuzzify,
    centroid_defuzzification
)

from agent.rules import evaluate_rules


class SmartFuzzyAgent:

    def __init__(self):
        self.last_result = None

    def analyze(self, temperature, humidity):

        # Step 1: Fuzzification
        fuzzy_values = fuzzify(
            temperature,
            humidity
        )

        # Step 2: Rule evaluation
        fired_rules, output_memberships = evaluate_rules(
            fuzzy_values
        )

        # Step 3: Defuzzification
        fan_speed = centroid_defuzzification(
            output_memberships
        )

        # Step 4: Fan category
        if fan_speed < 40:
            category = "SLOW"
        elif fan_speed < 70:
            category = "MEDIUM"
        else:
            category = "FAST"

        # Step 5: Explanation
        if temperature >= 32 and humidity >= 70:
            explanation = (
                "High temperature and high humidity detected. "
                "The agent recommends strong cooling."
            )

        elif temperature >= 32:
            explanation = (
                "High temperature detected. "
                "The agent increases fan speed."
            )

        elif humidity >= 70:
            explanation = (
                "High humidity detected. "
                "The agent increases cooling."
            )

        elif temperature <= 18:
            explanation = (
                "Room temperature is low. "
                "The agent keeps the fan speed low."
            )

        else:
            explanation = (
                "Room conditions are moderate. "
                "The agent selects a comfortable fan speed."
            )

        # Final result
        result = {
            "temperature": temperature,
            "humidity": humidity,
            "fuzzy_values": fuzzy_values,
            "fired_rules": fired_rules,
            "output_memberships": output_memberships,
            "fan_speed": round(fan_speed, 2),
            "category": category,
            "explanation": explanation
        }

        self.last_result = result

        return result