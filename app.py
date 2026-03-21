import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import hashlib
import time

# --- THE "WINNER" THEME & STYLING ---
st.set_page_config(page_title="Qt-Secure | Quantum Visual Simulator", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ffcc; font-family: 'Segoe UI', sans-serif; }
    div[data-testid="stMetric"] { background: #1a1c24; border: 1px solid #00ffcc; padding: 20px !important; border-radius: 10px !important; box-shadow: 0 0 15px rgba(0, 255, 204, 0.1); }
    .status-card { padding: 20px; border-radius: 10px; background: #1a1c24; border-left: 5px solid #00ffcc; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(45deg, #00ffcc, #008080); color: black; font-weight: bold; border: none; height: 3.5rem; border-radius: 8px; transition: 0.3s; width: 100%; }
    .stButton>button:hover { box-shadow: 0 0 20px #00ffcc; transform: scale(1.02); }
    
    /* Hiding the Copy to Clipboard button globally */
    button[title="Copy to clipboard"] { display: none !important; }
    
    .quantum-pipe { height: 80px; width: 100%; background: rgba(0, 255, 204, 0.03); border: 1px solid rgba(0, 255, 204, 0.1); border-radius: 40px; position: relative; overflow: hidden; margin-bottom: 25px; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
    .photon { width: 12px; height: 12px; background: #00ffcc; border-radius: 50%; box-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc; position: absolute; animation: travel 3s linear infinite; }
    @keyframes travel { 0% { left: 5%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { left: 92%; opacity: 0; } }
    .node-label { color: #00ffcc; font-family: monospace; font-weight: bold; font-size: 0.85rem; z-index: 2; }
    .eve-glow { color: #ff4b4b; text-shadow: 0 0 10px #ff4b4b; font-size: 0.9rem; font-weight: 900; }
    .photon-stream-box { background-color: #0e1117; padding: 12px; border-radius: 5px; border: 1px solid #1a1c24; font-family: monospace; color: #00ffcc; margin-top: 10px; }
    
    /* Custom Terminal Styling */
    .terminal-output {
        background: #10121a;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #1a1c24;
        font-family: monospace;
        font-size: 0.85rem;
        line-height: 1.5;
    }
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
    return alice_bits, alice_bases, bob_bases, bob_received

# --- APP LAYOUT ---
st.title("🛡️QT-SECURE PRO: QUANTUM VISUAL SIMULATOR")
st.caption("Advanced BB84 Simulation Environment v2.2 | SRMIST Kattankulathur")

col_ctrl, col_viz = st.columns([1, 3])

with col_ctrl:
    st.subheader("Command Center")
    n_photons = st.select_slider("Photon Flux", options=[50, 100, 200, 500, 1000], value=100)
    noise = st.slider("Environmental Decoherence (%)", 0, 25, 2)
    eve = st.toggle("Eavesdropper Intercept", value=False)
    sim_speed = st.select_slider("Simulation Speed", options=["Slow", "Normal", "Fast"], value="Normal")
    secret_msg = st.text_input("Message for Encryption", "QUANTUM")
    st.markdown("---")
    run = st.button("EXECUTE PROTOCOL")
    
    st.markdown(f"""
        <div style="margin-top: 50px; padding: 15px; border-radius: 8px; border: 1px solid rgba(0, 255, 204, 0.3); background-color: rgba(26, 28, 36, 0.5); text-align: center;">
            <p style="font-size: 0.7rem; letter-spacing: 2px; color: #00ffcc; margin-bottom: 5px; opacity: 0.8;">DEVELOPED BY</p>
            <p style="font-size: 1rem; font-weight: bold; color: #ffffff; margin: 0;">TEAM QUANTUM PARADOX</p>
        </div>
    """, unsafe_allow_html=True)

with col_viz:
    # --- QUANTUM CHANNEL VISUAL ---
    eve_label = '<span class="node-label eve-glow">EVE INTERCEPTING</span>' if eve else '<span class="node-label" style="opacity:0.4;">VACUUM CHANNEL</span>'
    st.markdown(f'<div class="quantum-pipe"><span class="node-label">ALICE (TX)</span><div class="photon" style="animation-delay: 0s;"></div><div class="photon" style="animation-delay: 1s;"></div>{eve_label}<span class="node-label">BOB (RX)</span></div>', unsafe_allow_html=True)

    if not run:
        st.info("SYSTEM STATUS: STANDBY | Awaiting Quantum Channel Initiation...")
        st.markdown("""
        ### Protocol Overview: BB84 Quantum Key Distribution
        This simulator facilitates a secure key exchange between **Alice** and **Bob** using non-orthogonal quantum states.
        
        **Technical Specifications:**
        * **Heisenberg Uncertainty Principle:** Ensures measurement by Eve is detectable.
        * **Real-time QBER Analysis:** Continuous monitoring of channel decoherence.
        * **SHA-256 Privacy Amplification:** Post-quantum cryptographic hashing.
        """)
        st.markdown('<div class="photon-stream-box">PHOTON STREAM: [ ░░░░░░░░░░░░░░░░ ] 0%</div>', unsafe_allow_html=True)
    else:
        # Processing simulation
        a_bits, a_bases, b_bases, b_received = run_qkd_protocol(n_photons, eve, noise)
        delay = {"Slow": 0.2, "Normal": 0.05, "Fast": 0.001}[sim_speed]
        
        st.subheader("Quantum Measurement")
        stream_placeholder = st.empty()
        progress_bar = st.progress(0)
        status_box = st.empty()
        
        s_alice, s_bob, matches = [], [], []
        log_entries = []
        
        for i in range(n_photons):
            time.sleep(delay)
            match = (a_bases[i] == b_bases[i])
            matches.append(match)
            if match:
                s_alice.append(a_bits[i])
                s_bob.append(b_received[i])
            
            # Progress bar simulation
            pct = int(((i + 1) / n_photons) * 100)
            filled = int(pct / 5)
            bar_graph = "█" * filled + "░" * (20 - filled)
            stream_placeholder.markdown(f'<div class="photon-stream-box">PHOTON STREAM: [ {bar_graph} ] {pct}%</div>', unsafe_allow_html=True)
            progress_bar.progress((i + 1) / n_photons)
            
            # Color-coded status line
            status_text = "[ ACCEPTED ]" if match else "[ DISCARDED ]"
            status_color = "#00ffcc" if match else "#ff4b4b"
            
            log_line = f'<div>PHOTON {i+1:03} | Alice: {a_bits[i]} | Bob: {b_received[i]} | Status: <span style="color:{status_color}; font-weight:bold;">{status_text}</span></div>'
            log_entries.insert(0, log_line)
            
            # Show only the last 5 logs for cleanliness
            status_box.markdown(f'<div class="terminal-output">{"".join(log_entries[:5])}</div>', unsafe_allow_html=True)

        s_alice, s_bob, matches = np.array(s_alice), np.array(s_bob), np.array(matches)
        qber = (np.sum(s_alice != s_bob) / len(s_alice) * 100) if len(s_alice) > 0 else 0
        is_secure = qber < 11.0

        # Metrics Row
        m1, m2, m3 = st.columns(3)
        m1.metric("RAW PHOTONS", n_photons)
        m2.metric("SIFTED KEY SIZE", len(s_alice))
        m3.metric("ERROR RATE (QBER)", f"{qber:.1f}%", delta="UNSAFE" if not is_secure else "SECURE", delta_color="inverse")

        # Basis Statistics Section
        st.subheader("ANALYSIS: BASIS STATISTICS")
        c1, c2 = st.columns([1, 2])
        total_matches = np.sum(matches)
        total_mismatches = n_photons - total_matches
        with c1:
            st.write(f"🟢Basis Match: {(total_matches/n_photons)*100:.2f}%")
            st.write(f"🔴Basis Mismatch: {(total_mismatches/n_photons)*100:.2f}%")
        with c2:
            fig_bar = go.Figure(data=[go.Bar(x=['Matches', 'Mismatches'], y=[total_matches, total_mismatches], marker_color=['#00ffcc', '#ff4b4b'])])
            fig_bar.update_layout(title="Photon Basis Comparison", height=200, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#00ffcc"), margin=dict(l=0,r=0,t=30,b=0))
            st.plotly_chart(fig_bar, use_container_width=True)
            # --- NEW: QUANTUM PHYSICS PROBABILITY SECTION ---
        st.markdown("---")
        st.subheader("QUANTUM PHYSICS: MEASUREMENT PROBABILITY")
        p1, p2 = st.columns([1, 2])
        with p1:
            st.info("""
            **The Physics:**
            According to the **Heisenberg Uncertainty Principle**, measuring a quantum state in a non-orthogonal basis (mismatch) causes a probabilistic wavefunction collapse.
            
            * **Matched Basis:** 100% Deterministic (Certainty).
            * **Mismatched Basis:** 50% Random (Collapse).
            """)
        with p2:
            prob_fig = go.Figure(go.Bar(
                x=['Matched Basis', 'Mismatched Basis'],
                y=[100, 50],
                marker_color=['#00ffcc', '#ff4b4b'],
                text=['100% Certainty', '50% Probability'],
                textposition='auto'
            ))
            prob_fig.update_layout(
                title="Probability of Correct State Measurement",
                height=250,
                margin=dict(t=30, b=0, l=0, r=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#00ffcc"),
                yaxis=dict(range=[0, 110], showgrid=False)
            )
            st.plotly_chart(prob_fig, use_container_width=True)

        # STATUS: CHANNEL SECURITY SECTION
        st.subheader("STATUS: CHANNEL SECURITY")
        if is_secure:
            st.success(f"STATUS: SECURE CHANNEL ESTABLISHED | QBER: {qber:.3f}%")
            raw_key_string = "".join(map(str, s_alice))
            secure_hash = hashlib.sha256(raw_key_string.encode()).hexdigest()
            
            # Message Encryption Display
            sc1, sc2 = st.columns(2)
            ciphertext = hashlib.md5((secret_msg + raw_key_string).encode()).hexdigest()[:16]
            sc1.info(f"**Ciphertext (Hex):**\n{ciphertext}")
            sc2.success(f"**Decrypted Message:**\n{secret_msg}")

            st.markdown(f"""
            <div class="status-card">
                <h4 style="margin-top:0;">Final Distilled Key (Privacy Amplified)</h4>
                <code style="color:#00ffcc; word-break: break-all;">{secure_hash}</code>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"CRITICAL: SECURITY BREACH DETECTED | QBER: {qber:.2f}%")

        # Visualization
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=s_alice[:50], mode='markers', name='Alice Bits', marker=dict(color='#00ffcc', size=10)))
        fig.add_trace(go.Scatter(y=s_bob[:50], mode='markers', name='Bob Bits', marker=dict(color='#ff4b4b', size=6, symbol='x')))
        fig.update_layout(title="Bit Correlation Analysis", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#00ffcc"), margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Quantum State Forensics"):
            df = pd.DataFrame({
                "Alice Basis": ["Rect (+)" if b==0 else "Diag (X)" for b in a_bases],
                "Bob Basis": ["Rect (+)" if b==0 else "Diag (X)" for b in b_bases],
                "Status": ["[ VALID ]" if m else "[ DISCARD ]" for m in matches]
            })
            st.download_button("EXPORT FORENSICS (CSV)", df.to_csv(index=False).encode('utf-8'), "quantum_forensics.csv", "text/csv")
            st.dataframe(df.style.map(lambda x: 'color: #00ffcc;' if x == '[ VALID ]' else 'color: #ff4b4b;', subset=['Status']), use_container_width=True)
