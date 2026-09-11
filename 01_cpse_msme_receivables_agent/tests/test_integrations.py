import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database.db_session import db
from src.database.seed_data import seed_database
from src.integrations.gstn_adapter import gstn
from src.integrations.treds_adapter import treds
from src.integrations.samadhaan_adapter import samadhaan
from src.integrations.whatsapp_adapter import whatsapp


def setup_function():
    seed_database()


def test_gstn_adapter():
    # Valid 64-char hex IRN
    valid_irn = "3f8e91a0b5c7d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2"
    res = gstn.validate_gstin("07AAACN0255D1ZQ")
    assert res["valid"] is True
    assert res["state_code"] == "07"

    # Invalid GSTIN
    bad_res = gstn.validate_gstin("INVALID_GSTIN")
    assert bad_res["valid"] is False


def test_treds_adapter():
    # Multi-exchange bid generation
    offers = treds.fetch_live_bids(
        invoice_id="inv_bhel_088",
        invoice_amount=Decimal("1510400.00"),
        days_to_maturity=30,
    )
    assert len(offers) >= 3
    platforms = [o.platform for o in offers]
    assert "RXIL" in platforms
    assert "M1X" in platforms
    assert "INVOICEMART" in platforms

    # Accept bid
    acc = treds.accept_bid(offers[0].id)
    assert acc["success"] is True


def test_samadhaan_adapter():
    inv = db.get_invoice("inv_ntpc_045")
    msme = db.get_msme(inv.msme_id)
    buyer = db.get_buyer(inv.buyer_id)

    petition = samadhaan.generate_msefc_petition(
        msme=msme,
        buyer=buyer,
        invoice=inv,
        statutory_interest=Decimal("45000.00"),
        days_overdue=142,
    )
    assert "STATEMENT OF CLAIM" in petition["petition_text"]
    assert "Section 18" in petition["petition_text"]
    assert "Section 43B(h)" in petition["petition_text"]
    assert len(petition["exhibits"]) == 5


def test_whatsapp_adapter():
    # Inbound message processing
    res = whatsapp.handle_inbound_message(
        sender="+919876543210",
        text="FIX",
    )
    assert "outbound" in res
    assert "Auto-Remediation" in res["outbound"]["message"]

    res_accept = whatsapp.handle_inbound_message(
        sender="+919876543210",
        text="ACCEPT",
    )
    assert "TReDS Bid Confirmed" in res_accept["outbound"]["message"]
