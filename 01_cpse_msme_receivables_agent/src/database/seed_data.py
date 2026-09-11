from datetime import date, datetime, timedelta
from decimal import Decimal
from .db_session import db
from .models import (
    MSME,
    Buyer,
    BuyerBehaviourStats,
    BuyerLearnedRule,
    BuyerType,
    FinancingOffer,
    FlagSeverity,
    GoodsReceiptNote,
    Invoice,
    InvoiceLifecycleStatus,
    LineItemModel,
    MSMECategory,
    PurchaseOrder,
    ValidationFlag,
)


def seed_database():
    """Seeds realistic production data for CPSE buyers, MSME supplier, historical behavior graphs, and invoices."""
    db.clear()

    # 1. Seed MSME Supplier
    msme = MSME(
        id="msme_precision_01",
        udyam_number="UDYAM-HR-01-0012345",
        gstin="06ABCDE1234F1Z5",
        legal_name="Precision Engineering MSME Ltd",
        category=MSMECategory.SMALL,
        sector="Industrial Valves & Heavy Machining",
        treds_ids={
            "rxil": "RXIL-VEND-8821",
            "m1x": "M1X-MSME-3310",
            "invoicemart": "INV-MART-0912",
        },
        bank_verified=True,
        bank_account="91802003881923",
        bank_ifsc="HDFC0000123",
        whatsapp_number="+919876543210",
        language_pref="en",
        cash_credit_apr=Decimal("0.125"),  # 12.5% Bank OD/CC facility
    )
    db.save_msme(msme)

    # 2. Seed CPSE Buyers
    buyers = [
        Buyer(
            id="cpse_ntpc_dadri",
            name="NTPC Limited — Dadri Thermal Power Station",
            type=BuyerType.CPSE,
            gstin="07AAACN0255D1ZQ",
            division_unit="Dadri Super Thermal Power Project",
            nodal_officer="General Manager (Finance & Stores)",
            escalation_contacts=["gm.finance.dadri@ntpc.co.in", "cfo@ntpc.co.in"],
            treds_registered=True,
            payment_terms_days=45,
            most_effective_channel="EMAIL_FINANCE_HEAD",
        ),
        Buyer(
            id="cpse_bhel_trichy",
            name="Bharat Heavy Electricals Limited (BHEL) — Trichy",
            type=BuyerType.CPSE,
            gstin="33AAAAB4144H1ZW",
            division_unit="Boiler Auxiliaries Plant",
            nodal_officer="Addl. General Manager (Finance & Bills)",
            escalation_contacts=["finance_bills@bhel.in", "agm_materials@bhel.in"],
            treds_registered=True,
            payment_terms_days=45,
            most_effective_channel="PORTAL_TICKET",
        ),
        Buyer(
            id="cpse_ongc_mumbai",
            name="Oil and Natural Gas Corporation (ONGC) — Western Offshore",
            type=BuyerType.CPSE,
            gstin="27AAAPO0055K1Z1",
            division_unit="Western Offshore Basin",
            nodal_officer="Chief General Manager (Finance)",
            escalation_contacts=["cgm_fin_wob@ongc.co.in", "dir_finance@ongc.co.in"],
            treds_registered=True,
            payment_terms_days=45,
            most_effective_channel="EMAIL_FINANCE_HEAD",
        ),
        Buyer(
            id="cpse_iocl_panipat",
            name="Indian Oil Corporation Limited (IOCL) — Panipat Refinery",
            type=BuyerType.CPSE,
            gstin="06AAACI1681G1Z0",
            division_unit="Panipat Refinery & Petrochemical Complex",
            nodal_officer="Deputy General Manager (Finance)",
            escalation_contacts=["dgm_fin_prpc@indianoil.in"],
            treds_registered=False,  # Unregistered on TReDS to test fallback paths
            payment_terms_days=45,
            most_effective_channel="OFFICIAL_STATUTORY_LETTER",
        ),
    ]
    for b in buyers:
        db.save_buyer(b)

    # 3. Seed Buyer Behaviour Stats (The Buyer Graph)
    stats_ntpc = BuyerBehaviourStats(
        buyer_id="cpse_ntpc_dadri",
        period="2026-Q1",
        avg_acceptance_days=18.5,
        avg_payment_days=58.0,
        rejection_rate=0.22,
        top_rejection_reasons=[
            "Quantity on invoice exceeds Store GRN",
            "Missing Udyam registration number on physical invoice header",
            "Discrepancy in Bank IFSC code vs SAP vendor master",
        ],
        on_time_rate=0.38,
        sample_size=142,
        most_effective_channel="EMAIL_FINANCE_HEAD",
        escalation_contacts=["gm.finance.dadri@ntpc.co.in", "cfo@ntpc.co.in"],
    )
    db.save_buyer_stats(stats_ntpc)

    stats_bhel = BuyerBehaviourStats(
        buyer_id="cpse_bhel_trichy",
        period="2026-Q1",
        avg_acceptance_days=14.0,
        avg_payment_days=52.0,
        rejection_rate=0.15,
        top_rejection_reasons=[
            "Missing BHEL internal 6-digit vendor code in subject line/invoice",
            "Inspection Note annexure missing QA signature stamp",
        ],
        on_time_rate=0.55,
        sample_size=98,
        most_effective_channel="PORTAL_TICKET",
        escalation_contacts=["finance_bills@bhel.in"],
    )
    db.save_buyer_stats(stats_bhel)

    stats_ongc = BuyerBehaviourStats(
        buyer_id="cpse_ongc_mumbai",
        period="2026-Q1",
        avg_acceptance_days=11.2,
        avg_payment_days=41.5,
        rejection_rate=0.08,
        top_rejection_reasons=[
            "HSN code 8-digit granularity mismatch",
        ],
        on_time_rate=0.74,
        sample_size=86,
        most_effective_channel="EMAIL_FINANCE_HEAD",
        escalation_contacts=["cgm_fin_wob@ongc.co.in"],
    )
    db.save_buyer_stats(stats_ongc)

    # 4. Seed Buyer Learned Rules ("THE MOAT")
    rules = [
        BuyerLearnedRule(
            id="rule_ntpc_01",
            buyer_id="cpse_ntpc_dadri",
            rule_code="NTPC_DADRI_GRN_QTY",
            rule_name="Store Receipt Quantity Verification",
            human_reason="NTPC Dadri requires invoice billed quantity to strictly match Store GRN. NTPC Dadri rejected 14 similar invoices last quarter due to overbilling vs GRN.",
            severity=FlagSeverity.BLOCKER,
            rejection_count=14,
            check_type="GRN_MATCH",
        ),
        BuyerLearnedRule(
            id="rule_ntpc_02",
            buyer_id="cpse_ntpc_dadri",
            rule_code="NTPC_UDYAM_HEADER",
            rule_name="Udyam Number in Invoice Header",
            human_reason="NTPC Finance accounts require Udyam Number explicitly printed on invoice header to route through MSME priority queue. Missing Udyam weakens 43B(h) statutory enforceability.",
            severity=FlagSeverity.INFO,
            rejection_count=9,
            check_type="UDYAM_HEADER",
        ),
        BuyerLearnedRule(
            id="rule_bhel_01",
            buyer_id="cpse_bhel_trichy",
            rule_code="BHEL_VENDOR_CODE_SUBJECT",
            rule_name="BHEL Vendor Code Header Requirement",
            human_reason="BHEL Trichy billing portal auto-rejects submissions missing the 6-digit SAP Vendor Code in the subject/header. Caused 19 past rejections.",
            severity=FlagSeverity.BLOCKER,
            rejection_count=19,
            check_type="VENDOR_CODE_REQUIRED",
        ),
    ]
    for r in rules:
        db.save_buyer_rule(r)

    # 5. Seed Purchase Orders & GRNs
    po1 = PurchaseOrder(
        id="po_ntpc_0891",
        po_number="PO/NTPC/2026/0891",
        buyer_id="cpse_ntpc_dadri",
        msme_id="msme_precision_01",
        po_date=date(2026, 1, 10),
        delivery_due_date=date(2026, 2, 15),
        line_items=[
            LineItemModel(
                item_code="ITM-FLANGE-150",
                description="Fabricated Steel Flanges 150mm High Pressure",
                quantity=Decimal("450"),
                unit="NOS",
                unit_rate=Decimal("4500.00"),
                gst_rate=Decimal("18.0"),
                hsn_code="7307.29",
                total_taxable=Decimal("2025000.00"),
                total_amount=Decimal("2389500.00"),
            )
        ],
        total_amount=Decimal("2389500.00"),
        payment_terms_days=45,
    )
    db.save_po(po1)

    grn1 = GoodsReceiptNote(
        id="grn_ntpc_4401",
        grn_number="GRN-DADRI-4401",
        po_id=po1.id,
        buyer_id="cpse_ntpc_dadri",
        msme_id="msme_precision_01",
        grn_date=date(2026, 2, 18),
        inspected_by="Senior Manager (Stores - NTPC Dadri)",
        line_items=[
            LineItemModel(
                item_code="ITM-FLANGE-150",
                description="Fabricated Steel Flanges 150mm High Pressure",
                quantity=Decimal("450"),  # Physical receipt was 450
                unit="NOS",
                unit_rate=Decimal("4500.00"),
                gst_rate=Decimal("18.0"),
                hsn_code="7307.29",
                total_taxable=Decimal("2025000.00"),
                total_amount=Decimal("2389500.00"),
            )
        ],
        accepted=True,
    )
    db.save_grn(grn1)

    po2 = PurchaseOrder(
        id="po_bhel_1102",
        po_number="PO/BHEL/2026/1102",
        buyer_id="cpse_bhel_trichy",
        msme_id="msme_precision_01",
        po_date=date(2026, 4, 5),
        delivery_due_date=date(2026, 5, 20),
        line_items=[
            LineItemModel(
                item_code="ITM-VALVE-200",
                description="High Temp Gate Valves 200mm PN40",
                quantity=Decimal("80"),
                unit="NOS",
                unit_rate=Decimal("16000.00"),
                gst_rate=Decimal("18.0"),
                hsn_code="8481.80",
                total_taxable=Decimal("1280000.00"),
                total_amount=Decimal("1510400.00"),
            )
        ],
        total_amount=Decimal("1510400.00"),
        payment_terms_days=45,
    )
    db.save_po(po2)

    # 6. Seed Invoices across lifecycle stages
    today = date.today()

    # Invoice 1: INV-2041 (The one from prompt demo! Currently in DRAFT/Pre-submission review)
    # Quantity on invoice (480) != GRN (450), missing Udyam number
    inv1 = Invoice(
        id="inv_ntpc_2041",
        msme_id="msme_precision_01",
        buyer_id="cpse_ntpc_dadri",
        po_id=po1.id,
        po_number=po1.po_number,
        irn="3f8e91a0b5c7d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2",
        invoice_number="INV/2026/2041",
        invoice_date=today - timedelta(days=2),
        submitted_date=None,
        amount=Decimal("2548800.00"),
        gst_amount=Decimal("388800.00"),
        status=InvoiceLifecycleStatus.DRAFT,
        validation_score=0.41,  # 41% first-pass probability due to quantity mismatch & missing udyam
        line_items=[
            LineItemModel(
                item_code="ITM-FLANGE-150",
                description="Fabricated Steel Flanges 150mm High Pressure",
                quantity=Decimal("480"),  # Overbilled! PO/GRN is 450
                unit="NOS",
                unit_rate=Decimal("4500.00"),
                gst_rate=Decimal("18.0"),
                hsn_code="7307.29",
                total_taxable=Decimal("2160000.00"),
                total_amount=Decimal("2548800.00"),
            )
        ],
        bank_account="91802003881923",
        bank_ifsc="HDFC0000123",
        vendor_code="VEND-NTPC-8812",
        hsn_code="7307.29",
    )
    db.save_invoice(inv1)

    # Invoice 2: Overdue severely (142 days overdue, NTPC Dadri) -> Escalator target
    inv2 = Invoice(
        id="inv_ntpc_045",
        msme_id="msme_precision_01",
        buyer_id="cpse_ntpc_dadri",
        po_id=po1.id,
        po_number=po1.po_number,
        irn="1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
        invoice_number="INV/2026/045",
        invoice_date=today - timedelta(days=187),  # 187 days ago
        submitted_date=today - timedelta(days=185),
        acceptance_date=today - timedelta(days=170),
        amount=Decimal("531000.00"),
        gst_amount=Decimal("81000.00"),
        status=InvoiceLifecycleStatus.OVERDUE,
        due_date=today - timedelta(days=142),  # 142 days overdue
        validation_score=0.96,
        line_items=[
            LineItemModel(
                item_code="ITM-FLANGE-150",
                description="Fabricated Steel Flanges 150mm High Pressure",
                quantity=Decimal("100"),
                unit="NOS",
                unit_rate=Decimal("4500.00"),
                gst_rate=Decimal("18.0"),
                hsn_code="7307.29",
                total_taxable=Decimal("450000.00"),
                total_amount=Decimal("531000.00"),
            )
        ],
        bank_account="91802003881923",
        bank_ifsc="HDFC0000123",
        vendor_code="VEND-NTPC-8812",
        hsn_code="7307.29",
    )
    db.save_invoice(inv2)

    # Invoice 3: Accepted & TReDS listed with competitive factoring bids (BHEL Trichy)
    inv3 = Invoice(
        id="inv_bhel_088",
        msme_id="msme_precision_01",
        buyer_id="cpse_bhel_trichy",
        po_id=po2.id,
        po_number=po2.po_number,
        irn="9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e",
        invoice_number="INV/2026/088",
        invoice_date=today - timedelta(days=15),
        submitted_date=today - timedelta(days=14),
        acceptance_date=today - timedelta(days=8),
        amount=Decimal("1510400.00"),
        gst_amount=Decimal("230400.00"),
        status=InvoiceLifecycleStatus.TREDS_LISTED,
        due_date=today + timedelta(days=30),  # 30 days remaining till buyer payment
        validation_score=0.98,
        treds_ready=True,
        line_items=po2.line_items,
        bank_account="91802003881923",
        bank_ifsc="HDFC0000123",
        vendor_code="BHEL-TR-554201",
        hsn_code="8481.80",
    )
    db.save_invoice(inv3)

    # Seed TReDS Financing Offers for INV-088 across RXIL, M1xchange, Invoicemart
    offers_inv3 = [
        FinancingOffer(
            id="offer_rxil_01",
            invoice_id=inv3.id,
            platform="RXIL",
            financier="State Bank of India (SBI Factoring)",
            discount_rate_apr=Decimal("0.078"),  # 7.8% APR
            net_amount=Decimal("1500694.00"),
            valid_till=datetime.utcnow() + timedelta(hours=36),
            status="OPEN",
        ),
        FinancingOffer(
            id="offer_m1x_01",
            invoice_id=inv3.id,
            platform="M1X",
            financier="ICICI Bank Factoring Unit",
            discount_rate_apr=Decimal("0.082"),  # 8.2% APR
            net_amount=Decimal("1500192.00"),
            valid_till=datetime.utcnow() + timedelta(hours=24),
            status="OPEN",
        ),
        FinancingOffer(
            id="offer_invmart_01",
            invoice_id=inv3.id,
            platform="INVOICEMART",
            financier="Axis Bank TReDS Desk",
            discount_rate_apr=Decimal("0.085"),  # 8.5% APR
            net_amount=Decimal("1499814.00"),
            valid_till=datetime.utcnow() + timedelta(hours=48),
            status="OPEN",
        ),
    ]
    for off in offers_inv3:
        db.save_financing_offer(off)

    # Invoice 4: Submitted to ONGC Western Offshore (Day 8 pending acceptance) -> Tracker target
    inv4 = Invoice(
        id="inv_ongc_112",
        msme_id="msme_precision_01",
        buyer_id="cpse_ongc_mumbai",
        invoice_number="INV/2026/112",
        invoice_date=today - timedelta(days=9),
        submitted_date=today - timedelta(days=8),
        amount=Decimal("850000.00"),
        gst_amount=Decimal("129661.00"),
        status=InvoiceLifecycleStatus.SUBMITTED,
        validation_score=0.92,
        treds_ready=True,
        bank_account="91802003881923",
        bank_ifsc="HDFC0000123",
        vendor_code="ONGC-WOB-9931",
        hsn_code="8481.80",
    )
    db.save_invoice(inv4)

    # Log initial events
    db.log_event(inv1.id, "STATUS_CHANGE", {"from": "CREATED", "to": "DRAFT"}, "MSME_USER")
    db.log_event(inv2.id, "STATUS_CHANGE", {"from": "ACCEPTED", "to": "OVERDUE"}, "SYSTEM")
    db.log_event(inv3.id, "STATUS_CHANGE", {"from": "ACCEPTED", "to": "TREDS_LISTED"}, "AGENT_FINANCIER")
    db.log_event(inv4.id, "STATUS_CHANGE", {"from": "VALIDATED", "to": "SUBMITTED"}, "AGENT_TRACKER")


if __name__ == "__main__":
    seed_database()
    print(f"Seed completed: {len(db.buyers)} buyers, {len(db.invoices)} invoices, {len(db.events)} events.")
