import re
from datetime import date
from decimal import Decimal
from typing import Any, Dict, Optional


class InvoicePDFParser:
    """Extracts structured invoice metadata, line items, and statutory identifiers from raw OCR text or digital PDF streams."""

    @classmethod
    def parse_raw_text(cls, text: str) -> Dict[str, Any]:
        extracted = {
            "invoice_number": None,
            "invoice_date": None,
            "po_number": None,
            "buyer_gstin": None,
            "seller_gstin": None,
            "irn": None,
            "total_amount": None,
            "line_items": [],
            "raw_text_length": len(text),
        }

        # 1. Extract Invoice Number
        inv_match = re.search(r"\b(?:Invoice\s*(?:No\.?|Number|#)|Inv\s*No\.?)\s*[:\-]?\s*([A-Z0-9/\-_]+)", text, re.IGNORECASE)
        if inv_match:
            extracted["invoice_number"] = inv_match.group(1).strip()

        # 2. Extract PO Number (Word boundary + explicit PO / Purchase Order tag)
        po_match = re.search(r"\b(?:P\.?O\.?\s*(?:No\.?|Number|#|Ref)|Purchase\s*Order\s*(?:No\.?|Number|#|Ref)?)\s*[:\-]?\s*([A-Z0-9/\-_]+)", text, re.IGNORECASE)
        if po_match:
            extracted["po_number"] = po_match.group(1).strip()

        # 3. Extract 64-char IRN Hash
        irn_match = re.search(r"\b([a-f0-9]{64})\b", text, re.IGNORECASE)
        if irn_match:
            extracted["irn"] = irn_match.group(1).lower().strip()

        # 4. Extract GSTINs (Format: 2 digits + 10 alphanumeric PAN + 1 entity + Z + 1 check digit)
        gstin_matches = re.findall(r"\b([0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1})\b", text)
        if len(gstin_matches) >= 2:
            extracted["seller_gstin"] = gstin_matches[0]
            extracted["buyer_gstin"] = gstin_matches[1]
        elif len(gstin_matches) == 1:
            extracted["seller_gstin"] = gstin_matches[0]

        # 5. Extract Total Amount
        amt_match = re.search(r"(?:Total\s*(?:Amount|Value)?\s*[:\-]?\s*(?:INR|Rs\.?|₹)?\s*)([0-9,]+(?:\.[0-9]{2})?)", text, re.IGNORECASE)
        if amt_match:
            cleaned_amt = amt_match.group(1).replace(",", "")
            extracted["total_amount"] = Decimal(cleaned_amt)

        return extracted


pdf_parser = InvoicePDFParser()
InvoicePDFExtractor = InvoicePDFParser
InvoicePDFParser.extract_from_text = InvoicePDFParser.parse_raw_text
