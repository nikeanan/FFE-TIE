from datetime import datetime
from typing import Any, Dict, List, Optional
from ..database.db_session import db
from ..database.models import Invoice


class WhatsAppAdapter:
    """WhatsApp-first conversational adapter supporting bilingual notifications, quick replies, and voice notes."""

    MESSAGE_HISTORY: List[Dict[str, Any]] = []

    @classmethod
    def send_notification(
        cls,
        to_number: str,
        message: str,
        quick_replies: Optional[List[str]] = None,
        language: str = "en",
    ) -> Dict[str, Any]:
        """Dispatches an outbound WhatsApp business message."""
        payload = {
            "id": f"wam_{len(cls.MESSAGE_HISTORY) + 1:04d}",
            "to": to_number,
            "message": message,
            "quick_replies": quick_replies or [],
            "language": language,
            "timestamp": datetime.utcnow().isoformat(),
            "direction": "OUTBOUND",
            "status": "DELIVERED",
        }
        cls.MESSAGE_HISTORY.append(payload)
        return payload

    @classmethod
    def format_validator_alert(
        cls,
        invoice_no: str,
        buyer_name: str,
        flags: List[Dict[str, Any]],
        current_score: float,
        improved_score: float,
        lang: str = "en",
    ) -> str:
        """Formats the pre-submission validation alert as specified in system vision."""
        buyer_short = buyer_name.split("—")[0].strip() if "—" in buyer_name else buyer_name
        num_issues = len(flags)

        if lang == "hi":
            # Hindi Vernacular Format
            lines = [
                f"⚠️ *चालान {invoice_no} ({buyer_short})* — सबमिट करने से पहले {num_issues} समस्याएं पाई गईं:"
            ]
            for i, f in enumerate(flags, 1):
                lines.append(f"{i}️⃣ {f.get('detail', f.get('code', 'त्रुटि'))}")
            lines.append(
                f"\n✅ इन्हें ठीक करें → पहली बार स्वीकृति की संभावना {int(current_score * 100)}% से बढ़कर {int(improved_score * 100)}% हो जाएगी।"
            )
            lines.append("सुधारे गए ड्राफ्ट के लिए *FIX* लिखकर उत्तर दें।")
            return "\n".join(lines)

        # English Format
        lines = [
            f"⚠️ *Invoice {invoice_no} for {buyer_short}* — {num_issues} issues before you submit:"
        ]
        for i, f in enumerate(flags, 1):
            detail = f.get("detail", f.get("code", "Issue"))
            lines.append(f"{i}️⃣ {detail}")

        lines.append(
            f"\n✅ Fix these → first-pass acceptance chance rises from {int(current_score * 100)}% → {int(improved_score * 100)}%."
        )
        lines.append("Reply *FIX* for a corrected draft.")
        return "\n".join(lines)

    @classmethod
    def format_treds_offer_alert(
        cls,
        invoice_no: str,
        buyer_name: str,
        platform: str,
        apr: float,
        net_amount: float,
        savings_vs_od: float,
        lang: str = "en",
    ) -> str:
        """Formats real-time TReDS discount auction alert to MSME business owner."""
        buyer_short = buyer_name.split("—")[0].strip() if "—" in buyer_name else buyer_name
        if lang == "hi":
            return (
                f"💰 *TReDS डिस्काउंटिंग ऑफर!* चालान {invoice_no} ({buyer_short})\n"
                f"प्लेटफ़ॉर्म: *{platform}* | ब्याज दर: *{apr:.1f}% APR*\n"
                f"तत्काल प्राप्य राशि: *₹{net_amount:,.2f}*\n"
                f"बैंक कैश क्रेडिट की तुलना में बचत: *₹{savings_vs_od:,.2f}*\n\n"
                f"ऑफर स्वीकार करने और T+1 दिन में भुगतान पाने के लिए *ACCEPT* लिखकर जवाब दें।"
            )

        return (
            f"💰 *TReDS Discounting Bid Available!* Invoice {invoice_no} ({buyer_short})\n"
            f"Platform: *{platform}* | Discount APR: *{apr:.1f}%*\n"
            f"Net Payout Today: *INR {net_amount:,.2f}*\n"
            f"Net Savings vs Bank OD: *INR {savings_vs_od:,.2f}*\n\n"
            f"Reply *ACCEPT* to lock this bid and receive settlement in T+1 day."
        )

    @classmethod
    def handle_inbound_message(cls, sender: str, text: str) -> Dict[str, Any]:
        """Processes conversational input from MSME owner via WhatsApp."""
        clean = text.strip().upper()
        inbound_record = {
            "id": f"wam_{len(cls.MESSAGE_HISTORY) + 1:04d}",
            "from": sender,
            "message": text,
            "timestamp": datetime.utcnow().isoformat(),
            "direction": "INBOUND",
        }
        cls.MESSAGE_HISTORY.append(inbound_record)

        if "FIX" in clean:
            reply = (
                "🛠️ *RECEIVX Auto-Remediation Initiated:*\n"
                "1. Invoice quantity adjusted from 480 ➔ 450 NOS to match Store GRN.\n"
                "2. MSME Udyam Number (UDYAM-HR-01-0012345) stamped in header.\n"
                "✅ First-pass acceptance probability updated: *94%*.\n"
                "Corrected PDF generated. Reply *SUBMIT* to dispatch to buyer portal."
            )
            quick_replies = ["SUBMIT", "CANCEL"]
        elif "ACCEPT" in clean:
            reply = (
                "✅ *TReDS Bid Confirmed:*\n"
                "Your acceptance for Invoice INV/2026/088 on RXIL at 7.8% APR is submitted.\n"
                "Funds of INR 1,500,694.00 scheduled for RTGS credit tomorrow by 11:30 AM."
            )
            quick_replies = ["VIEW_SETTLEMENT", "STATUS"]
        elif "APPROVE" in clean or "ESCALATE" in clean:
            reply = (
                "⚖️ *Escalation Step 3 Authorized:*\n"
                "Formal Statutory Demand Notice citing MSMED Act §15/16 and IT Act §43B(h) "
                "has been generated and queued for registered digital dispatch to NTPC General Manager (Finance)."
            )
            quick_replies = ["DOWNLOAD_NOTICE", "STATUS"]
        elif "STATUS" in clean or "PENDING" in clean:
            invoices = db.list_invoices()
            overdue = [i for i in invoices if i.status == "OVERDUE"]
            treds_ready = [i for i in invoices if i.status == "TREDS_LISTED"]
            reply = (
                f"📊 *RECEIVX Daily Portfolio Brief:*\n"
                f"• Total Active Invoices: {len(invoices)}\n"
                f"• Overdue Beyond 45 Days: {len(overdue)} invoices\n"
                f"• TReDS Liquidity Ready: {len(treds_ready)} invoices\n"
                f"Reply *ADVISOR* for your daily Next-Best-Action list."
            )
            quick_replies = ["ADVISOR", "FIX", "STATUS"]
        else:
            reply = (
                "👋 *RECEIVX MSME AI Assistant:*\n"
                "You can reply with:\n"
                "• *STATUS* — Check active receivables & aging\n"
                "• *FIX* — Auto-correct pre-submission invoice flags\n"
                "• *ACCEPT* — Lock best TReDS financing bid\n"
                "• *ESCALATE* — Review & approve legal demand notice"
            )
            quick_replies = ["STATUS", "FIX", "ACCEPT"]

        outbound = cls.send_notification(to_number=sender, message=reply, quick_replies=quick_replies)
        return {
            "inbound": inbound_record,
            "outbound": outbound,
        }


whatsapp = WhatsAppAdapter()
