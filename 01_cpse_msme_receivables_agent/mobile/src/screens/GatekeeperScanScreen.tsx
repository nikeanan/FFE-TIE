import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { Colors } from '../theme/colors';
import { ReceivxService } from '../services/api';

export const GatekeeperScanScreen: React.FC = () => {
  const [scanned, setScanned] = useState(true);
  const [fixed, setFixed] = useState(false);

  const handleScanInvoice = () => {
    Alert.alert(
      '📸 Camera Scanner Simulated',
      'Invoice INV/2026/088 captured and passed through Pre-Submission 4-Way Match Engine.'
    );
    setScanned(true);
    setFixed(false);
  };

  const handleRemediate = async () => {
    const res = await ReceivxService.autoRemediateInvoice('inv_bhel_01');
    setFixed(true);
    Alert.alert('✅ Invoice Remediation Successful', res.message);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <Text style={styles.title}>🔍 Pre-Submission Gatekeeper</Text>
          <Text style={styles.subTitle}>Agent 1: 4-Way Match & Moat Validator</Text>
        </View>

        {/* Viewfinder Mock */}
        <TouchableOpacity style={styles.scannerBox} onPress={handleScanInvoice} activeOpacity={0.8}>
          <Text style={styles.scannerIcon}>📷</Text>
          <Text style={styles.scannerText}>Tap to Scan Tax Invoice / GRN Receipt</Text>
          <Text style={styles.scannerSub}>Instant OCR extraction + GSTIN + Udyam MSMED check</Text>
        </TouchableOpacity>

        {/* Audit Results Card */}
        <View style={styles.auditCard}>
          <View style={styles.auditHeader}>
            <View>
              <Text style={styles.invNo}>INV/2026/088</Text>
              <Text style={styles.buyer}>BHEL Trichy (Boiler Division)</Text>
            </View>
            <View
              style={[
                styles.verdictBadge,
                { backgroundColor: fixed ? '#065F46' : '#991B1B' },
              ]}
            >
              <Text style={styles.verdictText}>{fixed ? 'PASSED (100%)' : 'FLAGGED (42%)'}</Text>
            </View>
          </View>

          <View style={styles.pipeline}>
            <Text style={styles.pipeStep}>1. Extract Docs ✅</Text>
            <Text style={styles.pipeStep}>2. 3-Way Match ⚠️</Text>
            <Text style={styles.pipeStep}>3. GST / IRN ✅</Text>
            <Text style={styles.pipeStep}>4. BHEL Moat Rules ⚠️</Text>
          </View>

          {/* Discrepancies */}
          <Text style={styles.sectionLabel}>Detected Gatekeeper Discrepancies:</Text>

          {!fixed ? (
            <>
              <View style={[styles.flagItem, { borderLeftColor: Colors.danger }]}>
                <Text style={styles.flagSeverity}>BLOCKER: QTY_MISMATCH</Text>
                <Text style={styles.flagDetail}>
                  Invoice billed 45.00 MT but GRN records physical delivery of 50.00 MT.
                </Text>
              </View>

              <View style={[styles.flagItem, { borderLeftColor: Colors.warning }]}>
                <Text style={styles.flagSeverity}>WARN: BHEL_UDYAM_STAMP_REQUIRED</Text>
                <Text style={styles.flagDetail}>
                  BHEL Trichy accounts portal rejects invoices lacking explicit MSMED registration footer.
                </Text>
              </View>

              <TouchableOpacity style={styles.fixButton} onPress={handleRemediate} activeOpacity={0.8}>
                <Text style={styles.fixButtonText}>⚡ Auto-Remediate Invoice (Align Qty & Stamp MSMED)</Text>
              </TouchableOpacity>
            </>
          ) : (
            <View style={styles.cleanBox}>
              <Text style={styles.cleanText}>
                🎉 All discrepancies remediated! Invoice is 100% compliant and ready for BHEL portal upload.
              </Text>
            </View>
          )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: 16 },
  header: { marginBottom: 16 },
  title: { fontSize: 20, fontWeight: '800', color: Colors.text },
  subTitle: { fontSize: 12, color: Colors.primaryAccent, marginTop: 2 },
  scannerBox: {
    backgroundColor: Colors.surfaceCard,
    borderRadius: 16,
    borderWidth: 2,
    borderColor: Colors.primary,
    borderStyle: 'dashed',
    padding: 24,
    alignItems: 'center',
    marginBottom: 16,
  },
  scannerIcon: { fontSize: 36, marginBottom: 8 },
  scannerText: { fontSize: 14, fontWeight: '700', color: Colors.text },
  scannerSub: { fontSize: 11, color: Colors.textMuted, marginTop: 4, textAlign: 'center' },
  auditCard: {
    backgroundColor: Colors.surfaceCard,
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  auditHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  invNo: { fontSize: 16, fontWeight: '800', color: Colors.text },
  buyer: { fontSize: 12, color: Colors.textMuted },
  verdictBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  verdictText: { color: '#FFFFFF', fontSize: 11, fontWeight: '800' },
  pipeline: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    padding: 10,
    borderRadius: 8,
    marginBottom: 14,
  },
  pipeStep: { fontSize: 11, color: Colors.textMuted },
  sectionLabel: { fontSize: 13, fontWeight: '700', color: Colors.text, marginBottom: 8 },
  flagItem: {
    backgroundColor: '#0F172A',
    borderLeftWidth: 4,
    padding: 10,
    borderRadius: 6,
    marginBottom: 8,
  },
  flagSeverity: { fontSize: 11, fontWeight: '800', color: '#F8FAFC', marginBottom: 2 },
  flagDetail: { fontSize: 12, color: Colors.textMuted },
  fixButton: {
    backgroundColor: Colors.primary,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  fixButtonText: { color: '#FFFFFF', fontWeight: '700', fontSize: 13 },
  cleanBox: {
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    padding: 14,
    borderRadius: 8,
    marginTop: 6,
  },
  cleanText: { color: Colors.success, fontSize: 13, fontWeight: '600', lineHeight: 18 },
});
