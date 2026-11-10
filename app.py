
import streamlit as st
import matplotlib.pyplot as plt

from agent.controller import SmartFuzzyAgent
from agent.fuzzy_engine import temperature_membership


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Fuzzy Logic Fan Controller",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("Fuzzy Logic Based Fan Speed Controller")

st.write(
    "This system determines the required fan speed "
    "based on room temperature and humidity using "
    "fuzzy logic."
)


# ============================================================
# CREATE AGENT
# ============================================================

agent = SmartFuzzyAgent()


# ============================================================
# ROOM CONDITIONS
# ============================================================

st.header("Room Conditions")

col1, col2 = st.columns(2)

with col1:

    temperature = st.slider(
        "Temperature (°C)",
        min_value=0,
        max_value=40,
        value=25
    )

with col2:

    humidity = st.slider(
        "Humidity (%)",
        min_value=0,
        max_value=100,
        value=50
    )


# ============================================================
# ANALYZE
# ============================================================

if st.button("Calculate Fan Speed"):

    result = agent.analyze(
        temperature,
        humidity
    )

    # ========================================================
    # AGENT DECISION
    # ========================================================

    st.header("Agent Decision")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Temperature",
            f"{temperature} °C"
        )

    with col2:

        st.metric(
            "Humidity",
            f"{humidity} %"
        )

    with col3:

        st.metric(
            "Fan Speed",
            f"{result['fan_speed']}%"
        )


    # ========================================================
    # FAN CATEGORY
    # ========================================================

    st.success(
        f"Fan Category: {result['category']}"
    )


    # ========================================================
    # EXPLANATION
    # ========================================================

    st.info(
        result["explanation"]
    )


    # ========================================================
    # FUZZIFICATION
    # ========================================================

    st.header("Fuzzification")

    col1, col2 = st.columns(2)


    # ---------------- TEMPERATURE ----------------

    with col1:

        st.subheader("Temperature Membership")

        temperature_values = result[
            "fuzzy_values"
        ]["temperature"]

        for name, value in temperature_values.items():

            st.write(
                f"{name}: {value:.2f}"
            )

            st.progress(
                float(value)
            )


    # ---------------- HUMIDITY ----------------

    with col2:

        st.subheader("Humidity Membership")

        humidity_values = result[
            "fuzzy_values"
        ]["humidity"]

        for name, value in humidity_values.items():

            st.write(
                f"{name}: {value:.2f}"
            )

            st.progress(
                float(value)
            )


    # ========================================================
    # RULES FIRED
    # ========================================================

    st.header("Rules Fired")

    if result["fired_rules"]:

        for rule in result["fired_rules"]:

            st.write(
                f"{rule['id']}: "
                f"IF Temperature is "
                f"{rule['temperature']} "
                f"AND Humidity is "
                f"{rule['humidity']} "
                f"THEN Fan is "
                f"{rule['output']}"
            )

            st.write(
                f"Rule Strength: "
                f"{rule['strength']:.2f}"
            )

    else:

        st.write(
            "No rule was fired."
        )


    # ========================================================
    # FAN OUTPUT MEMBERSHIP
    # ========================================================

    st.header("Fan Speed Membership")

    output_values = result[
        "output_memberships"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Slow",
            f"{output_values['Slow']:.2f}"
        )

    with col2:

        st.metric(
            "Medium",
            f"{output_values['Medium']:.2f}"
        )

    with col3:

        st.metric(
            "Fast",
            f"{output_values['Fast']:.2f}"
        )


    # ========================================================
    # TEMPERATURE GRAPH
    # ========================================================

    st.header("Temperature Membership Functions")

    temperatures = list(
        range(0, 41)
    )

    cold_values = []
    warm_values = []
    hot_values = []

    for temp in temperatures:

        values = temperature_membership(
            temp
        )

        cold_values.append(
            values["Cold"]
        )

        warm_values.append(
            values["Warm"]
        )

        hot_values.append(
            values["Hot"]
        )


    fig, ax = plt.subplots(figsize=(3, 1.5))

    ax.plot(
        temperatures,
        cold_values,
        label="Cold"
    )

    ax.plot(
        temperatures,
        warm_values,
        label="Warm"
    )

    ax.plot(
        temperatures,
        hot_values,
        label="Hot"
    )

    ax.axvline(
        temperature,
        linestyle="--",
        label="Current Temperature"
    )

    ax.set_xlabel(
        "Temperature (°C)"
    )

    ax.set_ylabel(
        "Membership Degree"
    )

    ax.set_title(
        "Temperature Fuzzy Sets"
    )

    ax.legend()

    ax.grid()

    st.pyplot(fig, use_container_width=False)


    # ========================================================
    # FINAL DECISION
    # ========================================================

    st.header("Final Decision")

    st.write(
        "Recommended Fan Speed"
    )

    st.subheader(
        f"{result['fan_speed']}%"
    )

    st.write(
        f"The system recommends "
        f"{result['category']} fan speed."
    )