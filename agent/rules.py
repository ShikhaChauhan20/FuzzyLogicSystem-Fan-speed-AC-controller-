


# ============================================================
# FUZZY RULES
# ============================================================

RULES = [

    {
        "id": "R1",
        "temperature": "Cold",
        "humidity": "Dry",
        "output": "Slow"
    },

    {
        "id": "R2",
        "temperature": "Cold",
        "humidity": "Normal",
        "output": "Slow"
    },

    {
        "id": "R3",
        "temperature": "Cold",
        "humidity": "Humid",
        "output": "Medium"
    },

    {
        "id": "R4",
        "temperature": "Warm",
        "humidity": "Dry",
        "output": "Medium"
    },

    {
        "id": "R5",
        "temperature": "Warm",
        "humidity": "Normal",
        "output": "Medium"
    },

    {
        "id": "R6",
        "temperature": "Warm",
        "humidity": "Humid",
        "output": "Fast"
    },

    {
        "id": "R7",
        "temperature": "Hot",
        "humidity": "Dry",
        "output": "Fast"
    },

    {
        "id": "R8",
        "temperature": "Hot",
        "humidity": "Normal",
        "output": "Fast"
    },

    {
        "id": "R9",
        "temperature": "Hot",
        "humidity": "Humid",
        "output": "Fast"
    }
]


# ============================================================
# RULE EVALUATION
# ============================================================

def evaluate_rules(fuzzy_values):
    """
    Evaluates all fuzzy rules.

    AND operation:
        MIN

    Aggregation:
        MAX
    """

    temperature_values = fuzzy_values["temperature"]
    humidity_values = fuzzy_values["humidity"]

    output_memberships = {
        "Slow": 0.0,
        "Medium": 0.0,
        "Fast": 0.0
    }

    fired_rules = []

    for rule in RULES:

        temperature_strength = temperature_values[
            rule["temperature"]
        ]

        humidity_strength = humidity_values[
            rule["humidity"]
        ]

        # AND = MIN
        firing_strength = min(
            temperature_strength,
            humidity_strength
        )

        # Store rules that fired
        if firing_strength > 0:

            fired_rules.append({
                "id": rule["id"],
                "temperature": rule["temperature"],
                "humidity": rule["humidity"],
                "output": rule["output"],
                "strength": firing_strength
            })

        # MAX aggregation
        if firing_strength > output_memberships[
            rule["output"]
        ]:

            output_memberships[
                rule["output"]
            ] = firing_strength

    return fired_rules, output_memberships