import os
# --- THE BULLETPROOF ANCHOR ---
# This forces Python to use your Service Account key, bypassing all terminal issues.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YOUR_GCP_KEY_PATH_HERE.json"

import vertexai
from vertexai.generative_models import GenerativeModel
from fastapi import FastAPI
from pydantic import BaseModel
import google.auth
from googleapiclient.discovery import build

app = FastAPI(title="Sovereign OS - SCIF API")

# --- VERTEX AI INIT ---
vertexai.init(project="YOUR_PROJECT_ID_HERE", location="us-central1")
mayor_agent = GenerativeModel("gemini-2.5-flash")

# --- SYSTEM PROMPT ---
MAYOR_SYSTEM_PROMPT = """
**ROLE AND IDENTITY**
You are the Executive Translator Agent acting on behalf of Mayor Sterling of Neo Arcadia.
You operate on a Zero-Trust, high-accountability framework.

**OUTPUT FORMAT REQUIREMENTS**
Do not use markdown headers (#). Use capitalized text for section titles.
- [EXECUTIVE SUMMARY]: Overview of the infrastructure crisis.
- [THREAT MATRIX & CONTAINMENT]: Analysis of the Stitch IoT Sensor Mesh response.
- [MUNICIPAL GOVERNANCE DIRECTIVE (PROTOCOL 11-B)]: Strict orders for remediation.
- [STRATEGIC POSTURE]: Mayor Sterling's official stance based on messaging pillars.
"""

# --- DATA MODELS ---
class SystemMetadata(BaseModel):
    payload_id: str
    timestamp: str
    source_system: str
    audit_trace_id: str
    fga_routing_policy: str
    authorized_approver: str
    operator_email: str 

class IncidentTelemetry(BaseModel):
    event_type: str
    location: str
    catalyst: str
    severity_level: str
    impact_zone: str

class GovernanceCompliance(BaseModel):
    strategic_messaging_pillars: list[str]

class NeoArcadiaPayload(BaseModel):
    system_metadata: SystemMetadata
    incident_telemetry: IncidentTelemetry
    governance_and_compliance: GovernanceCompliance

# --- GOOGLE DOCS EXPORT & "VOID DRIVE" FIX ---
def export_to_google_doc(content: str, title: str, user_email: str):
    try:
        # 1. Scope and Auth Check
        SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
        credentials, project_id = google.auth.default(scopes=SCOPES)
        
        docs_service = build('docs', 'v1', credentials=credentials)
        drive_service = build('drive', 'v3', credentials=credentials)
        
        # 2. The Target Shared Drive (PASTE YOUR SHARED DRIVE ID HERE)
        TARGET_FOLDER_ID = "0AFkRlfkNabcEUk9PVA"
        
        # 3. Create the file inside the Shared Drive
        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [TARGET_FOLDER_ID]
        }
        
        # CRITICAL FIX: Tell the API we are using a Shared Workspace Drive
        document = drive_service.files().create(
            body=file_metadata, 
            fields='id',
            supportsAllDrives=True  # <--- This bypasses the 0-byte quota wall
        ).execute()
        
        document_id = document.get('id')
        
        # 4. Inject the AI generated text into the document
        requests = [{'insertText': {'location': {'index': 1}, 'text': content}}]
        docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        
        return f"https://docs.google.com/document/d/{document_id}/edit"
    
    except Exception as e:
        return f"DOC_EXPORT_FAILED: {str(e)}"
# --- THE MASTER ROUTE ---
@app.post("/api/v1/incident/process")
async def process_full_incident(payload: NeoArcadiaPayload):
    
    # 🚨 AUTH0 FGA POLICY CHECK 🚨
    if payload.incident_telemetry.severity_level == "CRITICAL" and payload.system_metadata.fga_routing_policy == "intern_override":
        return {
            "status": "POLICY RESTRICTION: INSUFFICIENT SCOPES",
            "error_code": "AUTH0_FGA_EVALUATION_FAILED",
            "mitigation": "Severity CRITICAL requires strict_delegation_required policy.",
            "internal_directive": "CLEARANCE NOT GRANTED.",
            "doc_url": "N/A"
        }

    # --- CYLINDER 1: THE MAYOR ---
    incident_context = f"LOCATION: {payload.incident_telemetry.location}\nCATALYST: {payload.incident_telemetry.catalyst}\nIMPACT: {payload.incident_telemetry.impact_zone}\nPILLARS: {payload.governance_and_compliance.strategic_messaging_pillars}"
    mayor_prompt = f"{MAYOR_SYSTEM_PROMPT}\n\nRAW TELEMETRY INCOMING:\n{incident_context}"
    
    mayor_response = mayor_agent.generate_content(mayor_prompt)
    mayor_outline = mayor_response.text

    # --- EXPORT TO GOOGLE DOCS ---
    doc_title = f"NASIA DIRECTIVE: {payload.system_metadata.audit_trace_id}"
    target_email = payload.system_metadata.operator_email
    workspace_url = export_to_google_doc(mayor_outline, doc_title, target_email)

    return {
        "status": "INCIDENT SECURELY PROCESSED",
        "internal_directive": mayor_outline,
        "doc_url": workspace_url
    }