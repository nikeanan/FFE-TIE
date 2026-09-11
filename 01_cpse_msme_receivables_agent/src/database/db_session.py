import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from .models import (
    MSME,
    Buyer,
    BuyerBehaviourStats,
    BuyerLearnedRule,
    FinancingOffer,
    GoodsReceiptNote,
    Invoice,
    InvoiceEvent,
    InvoiceLifecycleStatus,
    PurchaseOrder,
    ValidationFlag,
)


class DatabaseSession:
    """Thread-safe in-memory and file-backed database session for RECEIVX platform."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSession, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.msmes: Dict[str, MSME] = {}
        self.buyers: Dict[str, Buyer] = {}
        self.pos: Dict[str, PurchaseOrder] = {}
        self.grns: Dict[str, GoodsReceiptNote] = {}
        self.invoices: Dict[str, Invoice] = {}
        self.events: List[InvoiceEvent] = []
        self.validation_flags: Dict[str, List[ValidationFlag]] = {}
        self.buyer_stats: Dict[str, BuyerBehaviourStats] = {}
        self.buyer_rules: Dict[str, List[BuyerLearnedRule]] = {}
        self.financing_offers: Dict[str, List[FinancingOffer]] = {}
        self._initialized = True

    def clear(self):
        self.msmes.clear()
        self.buyers.clear()
        self.pos.clear()
        self.grns.clear()
        self.invoices.clear()
        self.events.clear()
        self.validation_flags.clear()
        self.buyer_stats.clear()
        self.buyer_rules.clear()
        self.financing_offers.clear()

    # --- MSME ---
    def save_msme(self, msme: MSME):
        self.msmes[msme.id] = msme

    def get_msme(self, msme_id: str) -> Optional[MSME]:
        return self.msmes.get(msme_id)

    # --- Buyer ---
    def save_buyer(self, buyer: Buyer):
        self.buyers[buyer.id] = buyer

    def get_buyer(self, buyer_id: str) -> Optional[Buyer]:
        return self.buyers.get(buyer_id)

    def list_buyers(self) -> List[Buyer]:
        return list(self.buyers.values())

    # --- Purchase Orders & GRNs ---
    def save_po(self, po: PurchaseOrder):
        self.pos[po.id] = po

    def get_po(self, po_id: str) -> Optional[PurchaseOrder]:
        return self.pos.get(po_id)

    def find_po_by_number(self, po_number: str) -> Optional[PurchaseOrder]:
        for po in self.pos.values():
            if po.po_number.lower().strip() == po_number.lower().strip():
                return po
        return None

    def save_grn(self, grn: GoodsReceiptNote):
        self.grns[grn.id] = grn

    def get_grn_for_po(self, po_id: str) -> Optional[GoodsReceiptNote]:
        for grn in self.grns.values():
            if grn.po_id == po_id:
                return grn
        return None

    # --- Invoices ---
    def save_invoice(self, invoice: Invoice):
        self.invoices[invoice.id] = invoice

    def get_invoice(self, invoice_id: str) -> Optional[Invoice]:
        return self.invoices.get(invoice_id)

    def list_invoices(self) -> List[Invoice]:
        return list(self.invoices.values())

    def update_invoice_status(self, invoice_id: str, new_status: InvoiceLifecycleStatus, actor: str = "SYSTEM"):
        inv = self.get_invoice(invoice_id)
        if inv:
            old_status = inv.status
            inv.status = new_status
            self.log_event(
                invoice_id=invoice_id,
                event_type="STATUS_CHANGE",
                payload={"from": str(old_status), "to": str(new_status)},
                actor=actor,
            )

    # --- Events (Audit Log) ---
    def log_event(self, invoice_id: str, event_type: str, payload: Dict[str, Any], actor: str):
        ev = InvoiceEvent(
            id=len(self.events) + 1,
            invoice_id=invoice_id,
            event_type=event_type,
            payload=payload,
            actor=actor,
            created_at=datetime.utcnow(),
        )
        self.events.append(ev)
        return ev

    def get_events_for_invoice(self, invoice_id: str) -> List[InvoiceEvent]:
        return [e for e in self.events if e.invoice_id == invoice_id]

    # --- Buyer Graph: Stats & Learned Rules ---
    def save_buyer_stats(self, stats: BuyerBehaviourStats):
        self.buyer_stats[stats.buyer_id] = stats

    def get_buyer_stats(self, buyer_id: str) -> Optional[BuyerBehaviourStats]:
        return self.buyer_stats.get(buyer_id)

    def save_buyer_rule(self, rule: BuyerLearnedRule):
        if rule.buyer_id not in self.buyer_rules:
            self.buyer_rules[rule.buyer_id] = []
        self.buyer_rules[rule.buyer_id].append(rule)

    def get_buyer_rules(self, buyer_id: str) -> List[BuyerLearnedRule]:
        return self.buyer_rules.get(buyer_id, [])

    # --- Financing Offers ---
    def save_financing_offer(self, offer: FinancingOffer):
        if offer.invoice_id not in self.financing_offers:
            self.financing_offers[offer.invoice_id] = []
        self.financing_offers[offer.invoice_id].append(offer)

    def get_financing_offers(self, invoice_id: str) -> List[FinancingOffer]:
        return self.financing_offers.get(invoice_id, [])


db = DatabaseSession()
