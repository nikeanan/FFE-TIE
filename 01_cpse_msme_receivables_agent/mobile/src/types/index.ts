export type UrgencyLevel = 'IMMEDIATE_ACTION' | 'FINANCING_OPPORTUNITY' | 'ADVISORY' | 'ROUTINE';

export interface NextBestAction {
  actionId: string;
  invoiceId: string;
  invoiceNumber: string;
  buyerName: string;
  title: string;
  rationale: string;
  actionType: 'FIX_INVOICE' | 'ACCEPT_TREDS_BID' | 'AUTHORIZE_ESCALATION' | 'SEND_NUDGE';
  urgency: UrgencyLevel;
  estimatedImpact: string;
}

export interface InvoiceItem {
  id: string;
  invoiceNumber: string;
  buyerName: string;
  amount: number;
  dueDate: string;
  daysPending: number;
  status: 'CLEAN' | 'FLAGGED' | 'ACCEPTED' | 'TREDS_LISTED' | 'OVERDUE' | 'DISPUTED';
  flagsCount: number;
  isGeM: boolean;
  geMDeliveryDate?: string;
  cracDaysElapsed?: number;
}

export interface TredsBid {
  id: string;
  platform: 'RXIL' | 'M1xchange' | 'Invoicemart' | 'C2FO';
  financier: string;
  discountRateApr: number;
  netPayout: number;
  status: 'OPEN' | 'ACCEPTED' | 'EXPIRED';
  savingsVsBankOd: number;
}

export interface LegalEscalationNotice {
  invoiceId: string;
  invoiceNumber: string;
  buyerName: string;
  principalAmount: number;
  accruedSec16Interest: number;
  daysOverdue: number;
  recommendedStep: string;
  draftText: string;
}
