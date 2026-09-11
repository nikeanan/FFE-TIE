"""Real-World MSME Supplier Personas & CPSE Invoices for Live Pilot Evaluation."""
from decimal import Decimal
from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import date, timedelta


class PilotInvoiceBundle(BaseModel):
    invoice_number: str
    buyer_name: str
    buyer_sector: str
    target_cpse_portal: str
    po_reference: str
    po_amount: Decimal
    invoice_amount: Decimal
    grn_amount: Decimal
    grn_number: str
    grn_date: date
    days_pending: int
    raw_ocr_text: str
    known_traps: List[str]
    treds_eligible: bool
    is_gem_contract: bool


class PilotSupplierProfile(BaseModel):
    supplier_id: str
    company_name: str
    sector: str
    udyam_registration: str
    annual_turnover: Decimal
    bank_cash_credit_apr: float
    monthly_receivables_volume: Decimal
    invoices: List[PilotInvoiceBundle]


PILOT_SUPPLIERS: Dict[str, PilotSupplierProfile] = {
    "pilot_bhel_turbine": PilotSupplierProfile(
        supplier_id="pilot_bhel_turbine",
        company_name="Precision Heavy Engineering Works",
        sector="Turbine & Boiler Components",
        udyam_registration="UDYAM-TN-33-0098471",
        annual_turnover=Decimal("24000000.00"),  # ₹2.4 Cr
        bank_cash_credit_apr=0.135,  # 13.5% Bank OD
        monthly_receivables_volume=Decimal("4500000.00"),  # ₹45 Lakhs
        invoices=[
            PilotInvoiceBundle(
                invoice_number="INV/2026/BHEL-091",
                buyer_name="BHEL Trichy (High Pressure Boiler Plant)",
                buyer_sector="Power Equipment Manufacturing (Maharatna)",
                target_cpse_portal="BHEL Sambandh Vendor Portal",
                po_reference="PO-BHEL-TR-2025-9918",
                po_amount=Decimal("1850000.00"),
                invoice_amount=Decimal("1850000.00"),
                grn_amount=Decimal("1665000.00"),  # 10% discrepancy
                grn_number="GRN-BHEL-2026-4412",
                grn_date=date.today() - timedelta(days=22),
                days_pending=22,
                raw_ocr_text="""TAX INVOICE
Invoice No: INV/2026/BHEL-091
Supplier: Precision Heavy Engineering Works
Buyer: BHARAT HEAVY ELECTRICALS LIMITED, TRICHY - 620014
PO Ref: PO-BHEL-TR-2025-9918 | Date: 12-Nov-2025
Item Description: High-Pressure Boiler Alloy Tubes (Grade P91)
Quantity Billed: 50.00 MT @ INR 37,000 / MT
Total Taxable Amount: INR 15,67,796.61 | GST 18%: INR 2,82,203.39
Total Payable: INR 18,50,000.00
""",
                known_traps=[
                    "GRN recorded 45.00 MT accepted (5 MT rejected at gate due to mill test certificate typo)",
                    "BHEL Sambandh portal rejects invoices lacking explicit Udyam Certificate QR footer",
                    "Vendor code 330089 not included in invoice subject line format",
                ],
                treds_eligible=True,
                is_gem_contract=False,
            )
        ],
    ),
    "pilot_pgcil_transformers": PilotSupplierProfile(
        supplier_id="pilot_pgcil_transformers",
        company_name="Apex Electricals & Transformers Pvt Ltd",
        sector="EHV Transmission Equipment & Isolators",
        udyam_registration="UDYAM-UP-28-0041289",
        annual_turnover=Decimal("48000000.00"),  # ₹4.8 Cr
        bank_cash_credit_apr=0.142,  # 14.2% Bank OD
        monthly_receivables_volume=Decimal("7500000.00"),  # ₹75 Lakhs
        invoices=[
            PilotInvoiceBundle(
                invoice_number="INV/2026/PGCIL-442",
                buyer_name="Power Grid Corporation of India Ltd (Northern Region-1)",
                buyer_sector="Electric Power Transmission (Maharatna)",
                target_cpse_portal="PowerGrid PRANIT Portal",
                po_reference="PGCIL-NR1-SUBST-2025-108",
                po_amount=Decimal("2850000.00"),
                invoice_amount=Decimal("2850000.00"),
                grn_amount=Decimal("2850000.00"),
                grn_number="GRN-PGCIL-2026-8901",
                grn_date=date.today() - timedelta(days=14),
                days_pending=14,
                raw_ocr_text="""TAX INVOICE
Invoice No: INV/2026/PGCIL-442
Supplier: Apex Electricals & Transformers Pvt Ltd
Buyer: POWER GRID CORPORATION OF INDIA LTD, GURUGRAM
PO Ref: PGCIL-NR1-SUBST-2025-108
Item: 400kV Motorized Disconnector Isolator Switches (Set of 6)
Total Invoice Amount: INR 28,50,000.00
IRN: 8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b
""",
                known_traps=[
                    "Routine bureaucratic acceptance queue (Median acceptance 28 days)",
                    "High financing cost under Bank OD (₹33,725/mo interest burn)",
                ],
                treds_eligible=True,
                is_gem_contract=False,
            )
        ],
    ),
    "pilot_ntpc_boilers": PilotSupplierProfile(
        supplier_id="pilot_ntpc_boilers",
        company_name="Vanguard Boiler Spares & Fabrications",
        sector="Thermal Power Plant Consumables",
        udyam_registration="UDYAM-DL-08-0019284",
        annual_turnover=Decimal("32000000.00"),  # ₹3.2 Cr
        bank_cash_credit_apr=0.138,  # 13.8% Bank OD
        monthly_receivables_volume=Decimal("5000000.00"),  # ₹50 Lakhs
        invoices=[
            PilotInvoiceBundle(
                invoice_number="INV/2026/NTPC-08",
                buyer_name="NTPC Limited (Dadri Super Thermal Power Station)",
                buyer_sector="Power Generation & Utilities (Maharatna)",
                target_cpse_portal="Government e-Marketplace (GeM) / NTPC GePNIC",
                po_reference="GEMC-51168772910293",
                po_amount=Decimal("1300000.00"),
                invoice_amount=Decimal("1300000.00"),
                grn_amount=Decimal("1300000.00"),
                grn_number="CRAC-PENDING-STAGE",
                grn_date=date.today() - timedelta(days=64),
                days_pending=64,
                raw_ocr_text="""TAX INVOICE
Invoice No: INV/2026/NTPC-08 | Date: 08-Jan-2026
Supplier: Vanguard Boiler Spares & Fabrications
Buyer: NTPC DADRI POWER STATION, GAUTAM BUDH NAGAR, UP
GeM Order Ref: GEMC-51168772910293
Item: Economizer Cast Iron Bends & Expansion Joints
Total Value: INR 13,00,000.00
Delivery Date: 02-Jan-2026
""",
                known_traps=[
                    "Overdue by 64 days without formal dispute (Violates MSMED Section 15 45-day limit)",
                    "Consignee failed to issue CRAC on GeM within 10 days (Deemed Accepted by law under GFR Rule 149)",
                    "Statutory Section 16 Interest accrued: ₹45,620 at 3x RBI bank rate",
                    "Section 43B(h) IT Act disallowance triggered on buyer corporate tax liability",
                ],
                treds_eligible=False,
                is_gem_contract=True,
            )
        ],
    ),
    "pilot_ongc_petrochem": PilotSupplierProfile(
        supplier_id="pilot_ongc_petrochem",
        company_name="Bharat Petrochem Valving & Gauges",
        sector="Oil & Gas High-Pressure Valves",
        udyam_registration="UDYAM-GJ-01-0078122",
        annual_turnover=Decimal("56000000.00"),  # ₹5.6 Cr
        bank_cash_credit_apr=0.130,  # 13.0% Bank OD
        monthly_receivables_volume=Decimal("9000000.00"),  # ₹90 Lakhs
        invoices=[
            PilotInvoiceBundle(
                invoice_number="INV/2026/ONGC-112",
                buyer_name="Oil and Natural Gas Corporation Ltd (Hazira Plant)",
                buyer_sector="Hydrocarbon Exploration & Refining (Maharatna)",
                target_cpse_portal="ONGC e-Procurement Portal",
                po_reference="PO-ONGC-HAZ-2025-781",
                po_amount=Decimal("3450000.00"),
                invoice_amount=Decimal("3450000.00"),
                grn_amount=Decimal("3450000.00"),
                grn_number="GRN-ONGC-2026-339",
                grn_date=date.today() - timedelta(days=38),
                days_pending=38,
                raw_ocr_text="""TAX INVOICE
Invoice No: INV/2026/ONGC-112
Supplier: Bharat Petrochem Valving & Gauges
Buyer: ONGC HAZIRA GAS PROCESSING COMPLEX, SURAT, GUJARAT
PO Ref: PO-ONGC-HAZ-2025-781
Item: API 6D Forged Steel Ball Valves (Class 600)
Total Invoice Amount: INR 34,50,000.00
""",
                known_traps=[
                    "Buyer email alleged ₹85,000 Liquidated Damages deduction for transit delay without joint inspection",
                    "Requires AI Evidence Rebuttal referencing force majeure transit strike note",
                ],
                treds_eligible=True,
                is_gem_contract=False,
            )
        ],
    ),
    "pilot_railways_forgings": PilotSupplierProfile(
        supplier_id="pilot_railways_forgings",
        company_name="Shakti Rail Forgings & Track Systems",
        sector="Railway Track Components & Fasteners",
        udyam_registration="UDYAM-PB-12-0055410",
        annual_turnover=Decimal("62000000.00"),  # ₹6.2 Cr
        bank_cash_credit_apr=0.145,  # 14.5% Bank OD
        monthly_receivables_volume=Decimal("11000000.00"),  # ₹1.1 Cr
        invoices=[
            PilotInvoiceBundle(
                invoice_number="INV/2026/NR-RAIL-88",
                buyer_name="Northern Railway (Stores & Procurement Division)",
                buyer_sector="Indian Railways / Ministry of Railways",
                target_cpse_portal="IREPS (Indian Railways E-Procurement System)",
                po_reference="IREPS-PO-2025-NR-9901",
                po_amount=Decimal("4100000.00"),
                invoice_amount=Decimal("4100000.00"),
                grn_amount=Decimal("4100000.00"),
                grn_number="RITES-IC-2026-8812",
                grn_date=date.today() - timedelta(days=19),
                days_pending=19,
                raw_ocr_text="""TAX INVOICE
Invoice No: INV/2026/NR-RAIL-88
Supplier: Shakti Rail Forgings & Track Systems
Buyer: SENIOR DIVISIONAL CONTROLLER OF STORES, NORTHERN RAILWAY, NEW DELHI
PO Ref: IREPS-PO-2025-NR-9901
Item: Elastic Rail Clips (Mark III) & GFN-66 Insulating Liners
Total Value: INR 41,00,000.00
RITES Inspection Certificate: RITES-IC-2026-8812
""",
                known_traps=[
                    "RITES inspection certificate number format missing from e-invoice line item description",
                    "IREPS portal auto-rejects billing without matching digital RITES IC token",
                ],
                treds_eligible=True,
                is_gem_contract=False,
            )
        ],
    ),
}
