from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from src.database.db_session import db
from src.database.models import InvoiceLifecycleStatus
from src.database.seed_data import seed_database
from src.agents.validator_agent import validator_agent
from src.agents.tracker_agent import tracker_agent, InboundEmailParser
from src.agents.escalator_agent import escalator_agent
from src.agents.financier_agent import financier_agent
from src.agents.forecaster_agent import forecaster_agent
from src.agents.advisor_agent import advisor_agent
from src.agents.orchestrator import orchestrator
from src.integrations.whatsapp_adapter import whatsapp

# Seed database on startup
seed_database()

app = FastAPI(
    title="RECEIVX — CPSE–MSME Receivables Intelligence Platform",
    description=(
        "Production-grade autonomous AI layer taking MSME invoices from created to cash-in-bank. "
        "Encompasses 6 specialized agents: Validator, Tracker, Escalator, Financier, Forecaster, and Advisor."
    ),
    version="2.0.0",
)


# --- Health ---
@app.get("/")
def root():
    return {
        "platform": "RECEIVX",
        "vision": "Autonomous AI Layer for CPSE-MSME Receivables",
        "status": "ONLINE",
        "agents": ["VALIDATOR", "TRACKER", "ESCALATOR", "FINANCIER", "FORECASTER", "ADVISOR"],
        "active_invoices": len(db.list_invoices()),
        "monitored_cpse_buyers": len(db.list_buyers()),
    }


# --- Invoices ---
@app.get("/api/v1/invoices")
def list_invoices():
    return db.list_invoices()


@app.get("/api/v1/invoices/{invoice_id}")
def get_invoice(invoice_id: str):
    inv = db.get_invoice(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    events = db.get_events_for_invoice(invoice_id)
    return {"invoice": inv, "audit_events": events}


# --- Agent 1: Validator ---
@app.post("/api/v1/agents/validate/{invoice_id}")
def validate_invoice(invoice_id: str):
    try:
        res = validator_agent.run_sync(invoice_id)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/agents/remediate/{invoice_id}")
def remediate_invoice(invoice_id: str):
    try:
        return orchestrator.auto_remediate_invoice(invoice_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Agent 2: Tracker ---
@app.get("/api/v1/agents/track/{invoice_id}")
def track_invoice(invoice_id: str):
    return tracker_agent.evaluate_invoice(invoice_id)


@app.post("/api/v1/agents/track/tick")
def run_tracking_tick():
    return tracker_agent.run_daily_tick()


# --- Agent 3: Escalator ---
@app.get("/api/v1/agents/escalate/{invoice_id}")
def get_escalation_recommendation(invoice_id: str):
    try:
        return escalator_agent.recommend_escalation(invoice_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ExecuteEscalationRequest(BaseModel):
    step_number: int
    actor: str = "MSME_USER"


@app.post("/api/v1/agents/escalate/{invoice_id}/execute")
def execute_escalation(invoice_id: str, req: ExecuteEscalationRequest):
    try:
        return escalator_agent.execute_escalation_step(
            invoice_id=invoice_id,
            step_number=req.step_number,
            actor=req.actor,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Agent 4: Financier ---
@app.get("/api/v1/agents/finance/{invoice_id}")
def analyze_financing(invoice_id: str):
    try:
        return financier_agent.evaluate_financing(invoice_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AcceptBidRequest(BaseModel):
    offer_id: str
    actor: str = "MSME_USER"


@app.post("/api/v1/agents/finance/accept")
def accept_treds_bid(req: AcceptBidRequest):
    return financier_agent.execute_bid_acceptance(req.offer_id, req.actor)


# --- Agent 5: Forecaster ---
@app.get("/api/v1/agents/forecast/{invoice_id}")
def forecast_settlement(invoice_id: str):
    try:
        return forecaster_agent.predict_settlement(invoice_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/agents/forecast/cash-flow/{msme_id}")
def simulate_cash_flow(msme_id: str):
    try:
        return forecaster_agent.simulate_cash_flow(msme_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Agent 6: Advisor ---
@app.get("/api/v1/agents/advisor")
def get_daily_advisor_agenda(msme_id: str = Query("msme_precision_01")):
    return advisor_agent.generate_daily_actions(msme_id)


# --- Full Orchestration ---
@app.get("/api/v1/orchestrator/pipeline/{invoice_id}")
def run_full_pipeline(invoice_id: str):
    try:
        return orchestrator.run_full_pipeline(invoice_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Integrations: WhatsApp ---
class InboundWhatsAppRequest(BaseModel):
    sender: str
    message: str


@app.post("/api/v1/whatsapp/webhook")
def whatsapp_webhook(req: InboundWhatsAppRequest):
    return whatsapp.handle_inbound_message(sender=req.sender, text=req.message)


@app.get("/api/v1/whatsapp/history")
def get_whatsapp_history():
    return whatsapp.MESSAGE_HISTORY


# --- Integrations: Inbound Email / IMAP Feedback Loop ---
class InboundEmailRequest(BaseModel):
    from_email: str
    subject: str
    body: str


@app.post("/api/v1/email/inbound")
def parse_inbound_email(req: InboundEmailRequest):
    return InboundEmailParser.process_buyer_email(
        from_email=req.from_email,
        subject=req.subject,
        body=req.body,
    )


# --- Buyer Graph ---
@app.get("/api/v1/buyers")
def list_buyers():
    return db.list_buyers()


@app.get("/api/v1/buyers/{buyer_id}/graph")
def get_buyer_graph(buyer_id: str):
    stats = db.get_buyer_stats(buyer_id)
    rules = db.get_buyer_rules(buyer_id)
    return {
        "buyer": db.get_buyer(buyer_id),
        "stats": stats,
        "learned_rules": rules,
    }
