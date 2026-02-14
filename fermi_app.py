import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Fermi Energy Visualizer", layout="wide")

# ------------------ CONSTANTS ------------------
hbar = 1.054571817e-34
m = 9.10938356e-31
k_B = 8.617333262e-5  # eV/K
e = 1.602176634e-19

# Fermi energies (eV)
fermi_energies = {
    "Cu": 7.044,
    "Ag": 5.48,
    "Au": 5.53,
    "Al": 11.7,
    "Na": 3.24
}

# ------------------ FUNCTIONS ------------------

def fermi_dirac(E, Ef, T):
    if T == 0:
        return np.where(E < Ef, 1, 0)
    return 1 / (1 + np.exp((E - Ef) / (k_B * T)))

def electron_concentration(Ef):
    Ef_joules = Ef * e
    n = (1/(3*np.pi**2)) * ((2*m*Ef_joules)/(hbar**2))**(3/2)
    return n

# ------------------ SIDEBAR ------------------

st.sidebar.title("Controls")

metal = st.sidebar.selectbox("Select Metal", list(fermi_energies.keys()))
Ef = fermi_energies[metal]

temperature = st.sidebar.slider(
    "Select Temperature (K)",
    min_value=0,
    max_value=1000,
    value=300,
    step=10
)

# ------------------ MAIN PAGE ------------------

st.title("Fermi Energy Visualizer")
st.markdown("### Quantum Free Electron Theory")

col1, col2 = st.columns(2)

# -------- LEFT PANEL --------
with col1:
    st.subheader(f"{metal} - Properties")

    st.metric("Fermi Energy (eV)", Ef)

    n = electron_concentration(Ef)
    st.metric("Electron Concentration (m⁻³)", f"{n:.2e}")

    st.metric("Selected Temperature (K)", temperature)

# -------- RIGHT PANEL (FERMI-DIRAC) --------
with col2:
    st.subheader("Fermi–Dirac Distribution")

    E = np.linspace(0, Ef + 5, 500)

    fig, ax = plt.subplots()

    f_values = fermi_dirac(E, Ef, temperature)

    ax.plot(E, f_values, label=f"T = {temperature} K")

    # Mark Fermi energy line
    ax.axvline(Ef, linestyle="--", label="Fermi Energy")

    ax.set_xlabel("Energy (eV)")
    ax.set_ylabel("Probability f(E)")
    ax.set_ylim(0, 1.1)
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
