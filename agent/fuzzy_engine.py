


# ============================================================
# TRIANGULAR MEMBERSHIP FUNCTION
# ============================================================
def fuzzify(temperature, humidity):
    """
    Converts crisp values into fuzzy membership values.
    """
    temperature_values = temperature_membership(temperature)
    humidity_values = humidity_membership(humidity)

    return {
        "temperature": temperature_values,
        "humidity": humidity_values
    }
def triangular_membership(x, a, b, c):
    """
    Triangular membership function.

    a = left point
    b = peak
    c = right point

    Returns a value between 0 and 1.
    """

    if x <= a or x >= c:
        return 0.0

    if x == b:
        return 1.0

    if x < b:
        return (x - a) / (b - a)

    return (c - x) / (c - b)


# ============================================================
# TRAPEZOIDAL MEMBERSHIP FUNCTION
# ============================================================

def trapezoidal_membership(x, a, b, c, d):
    """
    Trapezoidal membership function.

    a = left start
    b = left top
    c = right top
    d = right end

    Returns a value between 0 and 1.
    """

    if x < a or x > d:
        return 0.0

    # Handles left shoulder
    if a == b and x <= b:
        return 1.0

    # Handles right shoulder
    if c == d and x >= c:
        return 1.0

    if b <= x <= c:
        return 1.0

    if x < b:
        return (x - a) / (b - a)

    return (d - x) / (d - c)


# ============================================================
# TEMPERATURE MEMBERSHIP
# ============================================================

def temperature_membership(temperature):
    """
    Converts temperature into fuzzy values.

    Temperature range: 0 to 40°C

    Fuzzy sets:
        Cold
        Warm
        Hot
    """

    cold = trapezoidal_membership(
        temperature,
        0, 0, 16, 22
    )

    warm = triangular_membership(
        temperature,
        18, 24, 30
    )

    hot = trapezoidal_membership(
        temperature,
        26, 32, 40, 40
    )

    return {
        "Cold": cold,
        "Warm": warm,
        "Hot": hot
    }


# ============================================================
# HUMIDITY MEMBERSHIP
# ============================================================

def humidity_membership(humidity):
    """
    Converts humidity into fuzzy values.

    Humidity range: 0 to 100%

    Fuzzy sets:
        Dry
        Normal
        Humid
    """

    dry = trapezoidal_membership(
        humidity,
        0, 0, 30, 45
    )

    normal = triangular_membership(
        humidity,
        35, 50, 65
    )

    humid = trapezoidal_membership(
        humidity,
        55, 70, 100, 100
    )

    return {
        "Dry": dry,
        "Normal": normal,
        "Humid": humid
    }


# ============================================================
# FAN SPEED MEMBERSHIP
# ============================================================

def fan_speed_membership(speed):
    """
    Converts fan speed into fuzzy values.

    Fan speed range: 0 to 100%

    Fuzzy sets:
        Slow
        Medium
        Fast
    """

    slow = trapezoidal_membership(
        speed,
        0, 0, 25, 45
    )

    medium = triangular_membership(
        speed,
        30, 50, 70
    )

    fast = trapezoidal_membership(
        speed,
        55, 75, 100, 100
    )

    return {
        "Slow": slow,
        "Medium": medium,
        "Fast": fast
    }


# ============================================================
# FUZZIFICATION
# ============================================================

def fuzzify(temperature, humidity):
    """
    Converts crisp values into fuzzy membership values.
    """

    temperature_values = temperature_membership(
        temperature
    )

    humidity_values = humidity_membership(
        humidity
    )

    return {
        "temperature": temperature_values,
        "humidity": humidity_values
    }


# ============================================================
# CENTROID DEFUZZIFICATION
# ============================================================

def centroid_defuzzification(output_memberships):
    """
    Converts fuzzy output into a crisp fan speed.

    Uses the centroid method.
    """

    numerator = 0.0
    denominator = 0.0

    # Check every possible fan speed
    for speed in range(0, 101):

        speed_memberships = fan_speed_membership(speed)

        # Clip each output fuzzy set
        slow = min(
            output_memberships["Slow"],
            speed_memberships["Slow"]
        )

        medium = min(
            output_memberships["Medium"],
            speed_memberships["Medium"]
        )

        fast = min(
            output_memberships["Fast"],
            speed_memberships["Fast"]
        )

        # Aggregate using MAX
        aggregated = max(
            slow,
            medium,
            fast
        )

        numerator += speed * aggregated
        denominator += aggregated

    if denominator == 0:
        return 0.0

    return numerator / denominator