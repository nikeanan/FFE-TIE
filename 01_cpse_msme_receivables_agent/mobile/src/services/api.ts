import { NextBestAction, InvoiceItem, TredsBid, LegalEscalationNotice } from '../types';

export const API_BASE_URL = 'http://localhost:8000/api/v1';

export const MockData = {
  kpis: {
    activeReceivables: 4625000,
    overdueMsmed: 1850000,
    claimableSec16Interest: 298500,
    instantTredsLiquidity: 1475000,
  },
  actions: [
    {
      actionId: 'nba_01',
      invoiceId: 'inv_bhel_01',
      invoiceNumber: 'INV/2026/088',
      buyerName: 'BHEL Trichy',
      title: 'Fix Quantity Discrepancy (45 MT -> 50 MT GRN)',
      rationale: 'Buyer portal rejected due to 5 MT variance with physical Goods Receipt Note.',
      actionType: 'FIX_INVOICE' as const,
      urgency: 'IMMEDIATE_ACTION' as const,
      estimatedImpact: 'Unlocks ₹1,850,000 stuck in validation loop',
    },
    {
      actionId: 'nba_02',
      invoiceId: 'inv_pgcil_01',
      invoiceNumber: 'INV/2026/092',
      buyerName: 'Power Grid Corporation',
      title: 'Accept SBI Factoring Bid @ 7.85% APR on RXIL',
      rationale: 'Bid is 5.65% lower than your 13.5% CC/OD limit. Valid for next 18 hours.',
      actionType: 'ACCEPT_TREDS_BID' as const,
      urgency: 'FINANCING_OPPORTUNITY' as const,
      estimatedImpact: 'Saves ₹23,450 net interest and delivers T+1 liquidity',
    },
    {
      actionId: 'nba_03',
      invoiceId: 'inv_ntpc_01',
      invoiceNumber: 'INV/2026/044',
      buyerName: 'NTPC Dadri',
      title: 'Authorize Section 43B(h) IT Act Disallowance Notice',
      rationale: 'Overdue by 62 days. Buyer faces taxable profit addition unless paid before Mar 31.',
      actionType: 'AUTHORIZE_ESCALATION' as const,
      urgency: 'IMMEDIATE_ACTION' as const,
      estimatedImpact: '94% settlement probability within 7 business days',
    }
  ],
  invoices: [
    {
      id: 'inv_bhel_01',
      invoiceNumber: 'INV/2026/088',
      buyerName: 'BHEL Trichy Boiler Unit',
      amount: 1850000,
      dueDate: '2026-03-25',
      daysPending: 18,
      status: 'FLAGGED' as const,
      flagsCount: 2,
      isGeM: false,
    },
    {
      id: 'inv_pgcil_01',
      invoiceNumber: 'INV/2026/092',
      buyerName: 'Power Grid Corp Northern Hub',
      amount: 1475000,
      dueDate: '2026-04-10',
      daysPending: 8,
      status: 'TREDS_LISTED' as const,
      flagsCount: 0,
      isGeM: false,
    },
    {
      id: 'inv_ntpc_01',
      invoiceNumber: 'INV/2026/044',
      buyerName: 'NTPC Dadri Thermal Station',
      amount: 1300000,
      dueDate: '2026-01-08',
      daysPending: 64,
      status: 'OVERDUE' as const,
      flagsCount: 1,
      isGeM: true,
      geMDeliveryDate: '2026-01-02',
      cracDaysElapsed: 68,
    }
  ],
  tredsBids: [
    {
      id: 'bid_sbi_01',
      platform: 'RXIL' as const,
      financier: 'State Bank of India Factoring',
      discountRateApr: 0.0785,
      netPayout: 1452650,
      status: 'OPEN' as const,
      savingsVsBankOd: 23450,
    },
    {
      id: 'bid_bob_01',
      platform: 'M1xchange' as const,
      financier: 'Bank of Baroda Trade Finance',
      discountRateApr: 0.0820,
      netPayout: 1449800,
      status: 'OPEN' as const,
      savingsVsBankOd: 20120,
    },
    {
      id: 'bid_hdfc_01',
      platform: 'Invoicemart' as const,
      financier: 'HDFC Bank Supply Chain Desk',
      discountRateApr: 0.0845,
      netPayout: 1447200,
      status: 'OPEN' as const,
      savingsVsBankOd: 17500,
    }
  ]
};

export const ReceivxService = {
  async getAdvisorSummary() {
    return { kpis: MockData.kpis, actions: MockData.actions };
  },
  async getInvoices() {
    return MockData.invoices;
  },
  async getTredsBids() {
    return MockData.tredsBids;
  },
  async autoRemediateInvoice(invoiceId: string) {
    return { success: true, message: `Invoice ${invoiceId} quantity aligned with GRN and Udyam MSMED stamped!` };
  },
  async acceptTredsBid(bidId: string) {
    return { success: true, message: `Bid ${bidId} accepted. Factoring settlement scheduled for T+1 11:30 AM.` };
  },
  async generateGeMNotice(contractNo: string) {
    return {
      success: true,
      notice: `STATUTORY NOTICE UNDER GeM GFR RULE 149

Contract No: ${contractNo}
Goods delivered >10 days ago. Consignment is deemed accepted by operation of law. Immediate bill payment mandated.`
    };
  }
};
