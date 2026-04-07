# Sovereign OS: Edge-Node Governance Engine
**Built for the Authorized to Act: Auth0 for AI Agents Hackathon**

Sovereign OS is a Zero-Trust, hardware-bound AI orchestration engine designed for high-stakes municipal incident response in Neo Arcadia. It proves that autonomous infrastructure can run in parallel with a secure, Auth0-governed AI orchestration layer—allowing agents to execute governance at machine speed, but *only* after a verified, cryptographic handshake with a human.

## 🛡️ Architectural Note on Public Access (Devpost Rules Compliance)
*Per the Hackathon rules regarding dev tools and internal systems:* **There is intentionally no public, interactive application URL for this codebase.** Sovereign OS is a proprietary GovTech infrastructure platform designed as a headless edge node hosted within a highly restricted private VPC (utilizing GCP Private Service Connect). 

It requires strict, hardware-bound authentication and is not exposed via a public URL. In the context of critical municipal infrastructure, a public testing link is a critical vulnerability. Our lack of a public web URL is not a missing feature—it is the core thesis of our Zero-Trust architecture. Please refer to our demo video and project site to see the Token Vault authorization flow in action.

## 🏛️ Why "Authorized to Act" Matters
In municipal crisis management, immediate physical response (e.g., shutting off water mains) must be decoupled from multi-agent governance. When it comes to the *agentic systems* that follow—the AI orchestrating communications and issuing official directives—authorization cannot be an afterthought. We built Sovereign OS to demonstrate that agentic patterns *can* hold up to rigorous enterprise boundaries without becoming synchronous bottlenecks.

## ⚙️ Core Architecture: The Governance Layer
Sovereign OS receives simulated incident payloads from our IoT Mesh and utilizes **Auth0 FGA (Fine-Grained Authorization)** to enforce strict clearance boundaries:

1. **Identity & FGA (Auth0 Token Vault):** Auth0 acts as the sovereign gatekeeper. If a low-clearance user (Intern June [DELTA Clearance]) attempts to authorize an action, the Auth0 matrix instantly blocks the payload at the FastAPI layer, proving graceful failure at the boundary.
2. **AI Orchestration (Vertex AI):** When the executive (Mayor Sterling [OMEGA Clearance]) authenticates via hardware-bound credentials, the backend passes the telemetry to Gemini 2.5 Flash to draft an actionable Governance Directive. 
3. **Machine-to-Machine Execution (GCP Service Accounts):** The FastAPI backend uses a restricted SCIF bot Service Account to execute an M2M handshake, syncing the finalized directive directly into a secure Google Workspace Shared Drive.

## 🚀 Local Deployment Instructions (Steps for Judges)
Because Sovereign OS is a backend-heavy edge node, deploying it locally requires specific infrastructure configurations to simulate the VPC.

1. **Download the Codebase:** Click the `<> Code` button at the top of this repository and select **Download ZIP**.
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Configure the Auth0 Identity Layer:** * Create an Auth0 Sandbox Tenant.
   * Define a custom API and configure the Token Vault.
   * Create custom scopes (e.g., `execute:critical_infrastructure`) to test FGA rejections vs. approvals.
4. **Configure the GCP Execution Layer:** * Generate a GCP Service Account JSON key with `Google Docs` and `Google Drive` APIs enabled.
   * Save it to the root directory.
   * **The Void Drive Fix:** To prevent 0-byte quota API crashes, create a Workspace Shared Drive, add the Service Account as a Contributor, and update the `TARGET_FOLDER_ID` in `main.py` with `supportsAllDrives=True`.
5. **Set the Security Anchor:** * Mac/Linux: `export GOOGLE_APPLICATION_CREDENTIALS="your-gcp-key.json"`
   * Windows: `set GOOGLE_APPLICATION_CREDENTIALS="your-gcp-key.json"`
6. **Spin up the Edge Node:**
   * Terminal 1 (Orchestrator): `fastapi dev main.py`
   * Terminal 2 (HITL UI): `streamlit run app.py`
