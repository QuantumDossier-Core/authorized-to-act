# Sovereign OS: Edge-Node Governance Engine
**Built for the Authorized to Act: Auth0 for AI Agents Hackathon**

Sovereign OS is a Zero-Trust, hardware-bound AI orchestration engine designed for high-stakes municipal incident response in Neo Arcadia. It leverages **Auth0 Token Vault** to enforce Fine-Grained Authorization (FGA) over Gemini 2.5 Flash agents, ensuring that autonomous systems only execute critical infrastructure directives when a cryptographically verified Human-in-the-Loop (HITL) grants clearance.

## 🛡️ Architectural Note on Public Access (Devpost Rules Compliance)
*Per the Hackathon rules regarding dev tools and internal systems:* **There is intentionally no public, interactive application URL for this codebase.** Sovereign OS is designed as a Dev Tool / Internal System to run on a hardened, headless Cloud Workstation Edge Node inside a private VPC. Municipal infrastructure tools cannot be publicly accessible web apps. Access is restricted to device-bound authentication via Auth0. The application UI (Streamlit) and Orchestrator (FastAPI) are gated within this secure perimeter to prevent public endpoint exploitation. 

* **Project Artifacts:** A static landing page hosting the video demonstration, architectural diagrams, and project artifacts is available at the URL provided in our submission. 
* **Evaluation:** Please review the video demonstration and the local deployment architecture outlined below to see the Token Vault in action.

## ⚙️ Core Architecture
1. **Identity & FGA (Auth0 Token Vault):** Auth0 acts as the sovereign gatekeeper. If a user (e.g., an Intern) lacks the specific custom scopes for a "CRITICAL" severity event, the request is physically blocked at the FastAPI layer before the AI is ever invoked.
2. **AI Orchestration (Gemini 2.5 Flash):** Once Auth0 verifies a high-clearance user (e.g., the Mayor), the telemetry is passed to Vertex AI to draft an actionable Governance Directive. *(Note: specific agent persona prompts have been excluded from this public repo to protect proprietary logic).*
3. **Machine-to-Machine Execution (GCP Service Accounts):** The FastAPI backend uses a restricted, backend-only GCP Service Account to execute a Machine-to-Machine (M2M) handshake, dropping the finalized directive directly into a secure Google Workspace Shared Drive.

## 🚀 Local Deployment Instructions (Steps for Judges)
Because Sovereign OS is a backend-heavy edge node, deploying it locally requires specific infrastructure configurations.

1. **Download the Codebase:** Click the green `<> Code` button at the top of this repository and select **Download ZIP**.
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Configure the Auth0 Identity Layer:** * Create an Auth0 Sandbox Tenant.
   * Define a custom API and configure the Token Vault.
   * Create custom scopes (e.g., `execute:critical_infrastructure`) to test FGA rejections vs. approvals.
4. **Configure the GCP Execution Layer:** * Generate a GCP Service Account JSON key with `Google Docs` and `Google Drive` API enabled.
   * Save it to the root directory.
   * **The Void Drive Fix:** To prevent 0-byte quota API crashes, create a Workspace Shared Drive, add the Service Account as a Contributor, and update the `TARGET_FOLDER_ID` in `main.py`.
5. **Set the Security Anchor:** `export GOOGLE_APPLICATION_CREDENTIALS="your-gcp-key.json"`
6. **Spin up the Edge Node:**
   * Terminal 1 (Orchestrator): `fastapi dev main.py`
   * Terminal 2 (UI): `streamlit run app.py`
