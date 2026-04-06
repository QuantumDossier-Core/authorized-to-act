import streamlit as st
import requests

st.set_page_config(page_title="Sovereign OS | SCIF Terminal", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #0d0e15; color: #a9b1d6; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3, h4 { color: #00f0ff; font-family: 'Courier New', Courier, monospace; text-transform: uppercase; letter-spacing: 1px; }
    .stButton>button { background-color: #ffb000; color: #000; font-weight: 900; border: none; width: 100%; border-radius: 0px; letter-spacing: 2px;}
    .stButton>button:hover { background-color: #cc8d00; border: 1px solid #00f0ff; color: #fff;}
    .alert-box { border-left: 4px solid #ffb000; background-color: #1a1b26; padding: 15px; margin-bottom: 20px;}
    .system-status { font-size: 0.85em; color: #9ece6a; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 5px;}
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='color:#ffb000;'>🔐 Auth0 Matrix</h2>", unsafe_allow_html=True)
st.sidebar.markdown("Establish Local Authority Profile:")
operator_identity = st.sidebar.radio(
    "ACTIVE CLEARANCE LEVEL",
    ("Mayor Sterling [CLEARANCE: OMEGA]", "Intern June [CLEARANCE: DELTA]")
)

jls_extract_var = "incident_telemetry"
base_payload = {
"system_metadata": {
    "payload_id": "STITCH-9942A",
    "timestamp": "2026-04-01T03:14:05Z",
    "source_system": "Stitch_IoT_Mesh",
    "audit_trace_id": "00-0af7651916cd43dd8448eb211c80319c",
    "fga_routing_policy": "strict_delegation_required",
    "authorized_approver": "MAYOR_OFFICE",
    "operator_email": "admin@your-org.com"
},
    jls_extract_var: {
        "event_type": "INFRASTRUCTURE_FAILURE",
        "location": "Inference Expressway, outbound from Logic Loop",
        "catalyst": "Legacy 36-inch water main structural fatigue.",
        "severity_level": "CRITICAL",
        "impact_zone": "The Civic Archive and two residential blocks"
    },
    "governance_and_compliance": {
        "strategic_messaging_pillars": [
            "A transparent grid is a resilient city.",
            "Securing our resources today so Neo Arcadia thrives tomorrow."
        ]
    }
}

st.title("Sovereign OS // SCIF Terminal Override")
st.markdown("<div class='system-status'>SYSTEM STATUS: LOGIC LOOP (CRITICAL) | CIVIC ARCHIVE (DEPRESSURIZED) | AUTH0 PERIMETER (SECURE)</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📡 Stitch IoT Mesh")
    st.markdown("""
    <div class="alert-box">
        <h4>🚨 CRITICAL ALARM</h4>
        <p><b>Vector:</b> Inference Expressway<br>
        <b>Severity:</b> LEVEL 5 (CRITICAL)<br>
        <b>Status:</b> CONTAINMENT PENDING</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("**Sub-Surface Telemetry Payload:**")
    st.json(base_payload["incident_telemetry"])

with col2:
    st.markdown("### Token Vault: Protocol 11-B Gate")
    st.markdown("Sovereign Engine draft compiled. Zero-Trust handshake required to execute city-wide directive.")
    
    if st.button("EXECUTE CRYPTOGRAPHIC HANDSHAKE"):
        with st.spinner("Negotiating Zero-Trust Auth0 Scope Verification & Workspace Sync..."):
            
            if operator_identity == "Intern June [CLEARANCE: DELTA]":
                base_payload["system_metadata"]["fga_routing_policy"] = "intern_override"
            else:
                base_payload["system_metadata"]["fga_routing_policy"] = "strict_delegation_required"
            
            try:
                response = requests.post("http://127.0.0.1:8000/api/v1/incident/process", json=base_payload)
                data = response.json()
                
                if "POLICY RESTRICTION" in data.get("status", ""):
                    st.error(f"❌ CRYPTOGRAPHIC REJECTION: {data['error_code']}")
                    st.warning(data["mitigation"])
                else:
                    st.success("✅ CLEARANCE ACCEPTED. DIRECTIVE COMPILED AND SYNCED TO WORKSPACE.")
                    
                    if "docs.google.com" in data.get("doc_url", ""):
                        st.markdown(f"🔗 **[OPEN OFFICIAL GOVERNANCE DIRECTIVE IN GOOGLE DOCS]({data['doc_url']})**")
                    else:
                        st.error(f"Workspace Sync Failed: {data.get('doc_url')}")
                        
                    st.markdown("#### 📄 Executive Governance Directive (Local Preview)")
                    st.info(data["internal_directive"])
                    
            except Exception as e:
                st.error(f"Connection severed. Sovereign Engine offline. Details: {e}")