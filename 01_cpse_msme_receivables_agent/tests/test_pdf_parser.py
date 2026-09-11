import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decimal import Decimal
from src.integrations.pdf_parser import pdf_parser


def test_pdf_invoice_extraction():
    raw_ocr_sample = """
    TAX INVOICE
    Seller: Precision Engineering MSME Ltd
    GSTIN: 06ABCDE1234F1Z5
    Buyer: NTPC Limited - Dadri Thermal Power Station
    Buyer GSTIN: 07AAACN0255D1ZQ
    Invoice No: INV/2026/2041
    PO Number: PO/NTPC/2026/0891
    IRN: 3f8e91a0b5c7d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2
    Description: Fabricated Steel Flanges 150mm High Pressure
    Total Amount: INR 2,548,800.00
    """
    extracted = pdf_parser.parse_raw_text(raw_ocr_sample)

    assert extracted["invoice_number"] == "INV/2026/2041"
    assert extracted["po_number"] == "PO/NTPC/2026/0891"
    assert extracted["seller_gstin"] == "06ABCDE1234F1Z5"
    assert extracted["buyer_gstin"] == "07AAACN0255D1ZQ"
    assert extracted["irn"] == "3f8e91a0b5c7d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2"
    assert extracted["total_amount"] == Decimal("2548800.00")
