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

def density_of_states(E):
    return np.sqrt(E)

def electron_concentration(Ef):
    Ef_joules = Ef * e
    n = (1/(3*np.pi**2)) * ((2*m*Ef_joules)/(hbar**2))**(3/2)
    return n

# ------------------ SIDEBAR ------------------

st.sidebar.title("Controls")

metal = st.sidebar.selectbox("Select Metal", list(fermi_energies.keys()))
Ef = fermi_energies[metal]

st.sidebar.subheader("Temperature Curves")
T0 = st.sidebar.checkbox("0 K", value=True)
T100 = st.sidebar.checkbox("100 K")
T300 = st.sidebar.checkbox("300 K")
T500 = st.sidebar.checkbox("500 K")
T800 = st.sidebar.checkbox("800 K")

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

# -------- RIGHT PANEL (FERMI-DIRAC) --------
with col2:
    st.subheader("Fermi–Dirac Distribution")

    E = np.linspace(0, Ef + 5, 500)

    fig, ax = plt.subplots()

    if T0:
        ax.plot(E, fermi_dirac(E, Ef, 0), label="0 K")
    if T100:
        ax.plot(E, fermi_dirac(E, Ef, 100), label="100 K")
    if T300:
        ax.plot(E, fermi_dirac(E, Ef, 300), label="300 K")
    if T500:
        ax.plot(E, fermi_dirac(E, Ef, 500), label="500 K")
    if T800:
        ax.plot(E, fermi_dirac(E, Ef, 800), label="800 K")

    ax.set_xlabel("Energy (eV)")
    ax.set_ylabel("Probability f(E)")
    ax.set_ylim(0, 1.1)
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# -------- DOS GRAPH --------
st.subheader("Density of States (DOS)")

E_dos = np.linspace(0.01, Ef + 5, 500)
DOS = density_of_states(E_dos)

fig2, ax2 = plt.subplots()
ax2.plot(E_dos, DOS)
ax2.set_xlabel("Energy (eV)")
ax2.set_ylabel("DOS ∝ √E")
ax2.grid(True)

st.pyplot(fig2)
