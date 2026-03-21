# 🛡️ QT-SECURE PRO: Quantum Visual Simulator
**Advanced BB84 Simulation Environment v2.2** *Developed by Team Quantum Paradox for QtHack 4.0*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://qt-secure-pro.streamlit.app/)

## 🌐 Overview
QT-SECURE PRO is a high-fidelity simulation suite designed to model **BB84 Quantum Key Distribution (QKD)**. Unlike theoretical models, this environment simulates real-world quantum channel dynamics, including environmental noise (decoherence) and active eavesdropping attempts.

## ✨ Key Features
* **Real-time QBER Analysis:** Continuous monitoring of the Quantum Bit Error Rate.
* **Environmental Decoherence Modeling:** Simulates signal loss and atmospheric noise.
* **SHA-256 Privacy Amplification:** Post-quantum cryptographic hashing to ensure maximum entropy in the final distilled key.
* **Eavesdropper Detection:** Built-in module to demonstrate how the Heisenberg Uncertainty Principle reveals measurement by "Eve."

## 🚀 Phase 2: Dynamic Lab Features (Newly Added)
* **Variable Photon Flux:** High-capacity simulation supporting up to 1000 photons.
* **Real-time Stream Processing:** Live visual feedback of photon measurement and basis reconciliation.
* **Simulation Speed Control:** Toggle between Slow (Educational), Normal (Standard), and Fast (Stress-test) processing modes.
* **End-to-End Secure Messaging:** Integrated XOR-encryption module to demonstrate final key utility.
* **Forensic Analytics:** Exportable CSV reports for deep-dive quantum state analysis.

## 🔬 The Science (BB84 Protocol)
The simulator follows the four-stage quantum cryptography process:
1.  **Quantum Exchange:** Alice sends photons in random bases.
2.  **Sifting:** Bob and Alice compare bases over a classical channel.
3.  **Error Estimation:** QBER is calculated to detect interference.
4.  **Privacy Amplification:** A secure, high-entropy hex key is distilled.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Frontend:** Streamlit (Custom CSS/Neon-Dark Theme)
* **Analytics:** NumPy, Pandas
* **Visualization:** Plotly Interactive Bit-Correlation Graphs

## 🚀 Deployment
The project is live at: [qt-secure-pro.streamlit.app](https://qt-secure-pro.streamlit.app/)

---
**Team Quantum Lockbreakers** *SRMIST Kattankulathur* *Members: Nayanika Prusty & Team*
