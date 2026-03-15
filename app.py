import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import hashlib
import time

# --- THE "WINNER" THEME: NEON & DARK ---
st.set_page_config(page_title="Qt-Secure | Quantum Key Distiller", layout="wide")

st.markdown("""
    <style>
    .main { 
        background-color: #0e1117; 
        color: #00ffcc;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Metric Cards with Neon Glow */
    div[data-testid="stMetric"] {
        background: #1a1c24;
        border: 1px solid #00ffcc;
        padding: 20px !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.2);
    }

    /* Professional Status Cards */
    .status-card {
        padding: 20px;
        border-radius: 10px;
        background: #1a1c24;
        border-left: 5px solid #00ffcc;
        margin-bottom: 20px;
    }

    /* Action Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #00ffcc, #008080);
        color: black;
        font-weight: bold;
        border: none;
        height: 3.5rem;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px #00ffcc;
        transform: scale(1.01);
    }

    /* Customizing the Plotly Toolbar */
    .modebar { opacity: 1 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE QUANTUM ENGINE ---
def run_qkd_protocol(n_bits, eve_present, noise_level):
    alice_bits = np.random.randint(2, size=n_bits)
    alice_bases = np.random.randint(2, size=n_bits)
    if eve_present:
        eve_bases = np.random.randint(2, size=n_bits)
        bob_received = np.array([alice_bits[i] if alice_bases[i] == eve_bases[i] else np.random.randint(2) for i in range(n_bits)])
    else:
        bob_received = alice_bits.copy()
        mask = np.random.random(n_bits) < (noise_level/100)
        bob_received[mask] = 1 - bob_received[mask]
    bob_bases = np.random.randint(2, size=n_bits)
    matching_indices = (alice_bases == bob_bases)
    s_alice = alice_bits[matching_indices]
    s_bob = bob_received[matching_indices]
    return alice_bits, alice_bases, bob_bases, s_alice, s_bob, matching_indices

# --- APP LAYOUT ---
st.title("🛡️ QT-SECURE: QUANTUM KEY DISTILLER")
st.caption("Advanced BB84 Simulation Environment v2.2 | SRMIST Kattankulathur")

col_ctrl, col_viz = st.columns([1, 3])

with col_ctrl:
    st.subheader("Command Center")
    n_photons = st.select_slider("Photon Flux", options=[50, 100, 200, 500, 1000], value=200)
    noise = st.slider("Environmental Decoherence (%)", 0, 25, 2)
    eve = st.toggle("Eavesdropper Intercept", value=False)
    st.markdown("---")
    run = st.button("EXECUTE PROTOCOL")
    
    st.markdown("""
        <div style="margin-top: 50px; padding: 10px; border: 1px border-radius: 5px; border: 1px solid #1a1c24; text-align: center;">
            <small style="color: #64748b;">DEVELOPED BY:</small><br>
            <strong style="color: #00ffcc; letter-spacing: 1px;">TEAM QUANTUM PARADOX</strong>
        </div>
    """, unsafe_allow_html=True)
if not run:
    with col_viz:
        st.info("**SYSTEM STATUS: STANDBY** | Awaiting Quantum Channel Initiation...")
        st.markdown("""
        ### Protocol Overview: BB84 Quantum Key Distribution
        This simulator facilitates a secure key exchange between **Alice** and **Bob** using 
        non-orthogonal quantum states. 
        
        **Technical Specifications:**
        * **Heisenberg Uncertainty Principle:** Ensures measurement by Eve is detectable.
        * **Real-time QBER Analysis:** Continuous monitoring of channel decoherence.
        * **SHA-256 Privacy Amplification:** Post-quantum cryptographic hashing.
        """)
        st.markdown(f"""
            <div style="background-color: #0e1117; padding: 10px; border-radius: 5px; border: 1px solid #1a1c24; font-family: monospace; color: #00ffcc;">
                PHOTON STREAM: [ ░░░░░░░░░░░░░░░░ ] 0%
            </div>
        """, unsafe_allow_html=True)

if run:
    a_bits, a_bases, b_bases, s_alice, s_bob, matches = run_qkd_protocol(n_photons, eve, noise)
    qber = (np.sum(s_alice != s_bob) / len(s_alice) * 100) if len(s_alice) > 0 else 0
    is_secure = qber < 11.0

    with col_viz:
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("RAW PHOTONS", n_photons)
        m2.metric("SIFTED KEY SIZE", len(s_alice))
        m3.metric("ERROR RATE (QBER)", f"{qber:.1f}%", delta="UNSAFE" if not is_secure else "SECURE", delta_color="inverse")

        if is_secure:
            st.success("🔒 SECURE CHANNEL ESTABLISHED")
            raw_key_string = "".join(map(str, s_alice))
            secure_hash = hashlib.sha256(raw_key_string.encode()).hexdigest()
            st.markdown(f"""
            <div class="status-card">
                <h4>Final Distilled Key (Privacy Amplified)</h4>
                <code style="color:#00ffcc; word-break: break-all;">{secure_hash}</code>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("PROTOCOL ABORTED: QUANTUM INTERFERENCE DETECTED")

        # Visualization
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=s_alice[:50], mode='markers', name='Alice Bits', marker=dict(color='#00ffcc', size=10)))
        fig.add_trace(go.Scatter(y=s_bob[:50], mode='markers', name='Bob Bits', marker=dict(color='#ff4b4b', size=6, symbol='x')))
        fig.update_layout(
            title="Bit Correlation (First 50 bits)", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font=dict(color="#00ffcc")
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("View Quantum State Log"):
            df = pd.DataFrame({
                "Alice Basis": ["Rect (+)" if b==0 else "Diag (X)" for b in a_bases],
                "Bob Basis": ["Rect (+)" if b==0 else "Diag (X)" for b in b_bases],
                "Status": ["[ VALID ]" if m else "[ DISCARD ]" for m in matches]
            })
            st.download_button("EXPORT FORENSICS (CSV)", df.to_csv(index=False), "qkd_report.csv")
            st.dataframe(df.style.map(
                lambda x: 'color: #00ffcc;' if x == '[ VALID ]' else 'color: #ff4b4b;', 
                subset=['Status']
            ), use_container_width=True)