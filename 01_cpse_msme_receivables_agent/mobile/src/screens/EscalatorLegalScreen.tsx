import React from 'react';
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

export const EscalatorLegalScreen: React.FC = () => {
  const handleAuthorizeNotice = () => {
    Alert.alert(
      '🔒 Biometric Authorization Confirmed',
      'Section 43B(h) Disallowance Notice signed with digital timestamp and dispatched to NTPC Chief Financial Officer & Statutory Auditors.'
    );
  };

  const handleExportSamadhaan = () => {
    Alert.alert(
      '📥 MSME Samadhaan Form 1 Generated',
      'XML Claim Bundle with statement of compound interest exported for MSEFC conciliation filing.'
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <Text style={styles.title}>⚖️ Statutory Escalator & Section 43B(h)</Text>
          <Text style={styles.subTitle}>MSMED Act 2006 Rights & Tax Disallowance Leverage</Text>
        </View>

        {/* Claim Summary */}
        <View style={styles.claimCard}>
          <Text style={styles.claimBuyer}>NTPC Dadri Thermal Station</Text>
          <Text style={styles.claimInv}>Invoice: INV/2026/044 • Overdue by 64 days</Text>

          <View style={styles.divider} />

          <View style={styles.statRow}>
            <Text style={styles.statLabel}>Principal Outstanding:</Text>
            <Text style={styles.statVal}>₹ 13,00,000.00</Text>
          </View>
          <View style={styles.statRow}>
            <Text style={styles.statLabel}>Accrued Sec 16 Interest (3x RBI):</Text>
            <Text style={[styles.statVal, { color: Colors.warning }]}>₹ 45,620.00</Text>
          </View>
          <View style={styles.statRow}>
            <Text style={styles.statLabel}>Total Statutory Claim:</Text>
            <Text style={[styles.statVal, { color: Colors.primaryAccent, fontSize: 16 }]}>
              ₹ 13,45,620.00
            </Text>
          </View>
        </View>

        {/* Escalator Stepper */}
        <View style={styles.stepCard}>
          <Text style={styles.stepTitle}>Recommended Legal Step: Step 4 of 6</Text>
          <Text style={styles.stepName}>Formal Section 43B(h) IT Act Disallowance Notice</Text>
          <Text style={styles.stepDesc}>
            Informs the buyer that unpaid MSME dues beyond 45 days cannot be deducted from taxable profits in FY26, creating immediate corporate tax liability.
          </Text>

          <TouchableOpacity style={styles.authButton} onPress={handleAuthorizeNotice} activeOpacity={0.8}>
            <Text style={styles.authButtonText}>✍️ Authorize & Dispatch Notice</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.exportButton} onPress={handleExportSamadhaan} activeOpacity={0.8}>
            <Text style={styles.exportButtonText}>📥 Download MSME Samadhaan Form 1 XML</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.background },
  content: { padding: 16 },
  header: { marginBottom: 14 },
  title: { fontSize: 20, fontWeight: '800', color: Colors.text },
  subTitle: { fontSize: 12, color: Colors.primaryAccent, marginTop: 2 },
  claimCard: {
    backgroundColor: Colors.surfaceCard,
    borderRadius: 14,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: Colors.border,
  },
  claimBuyer: { fontSize: 16, fontWeight: '800', color: Colors.text },
  claimInv: { fontSize: 12, color: Colors.textMuted, marginTop: 2 },
  divider: { height: 1, backgroundColor: Colors.border, marginVertical: 12 },
  statRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginVertical: 4,
  },
  statLabel: { fontSize: 12, color: Colors.textMuted },
  statVal: { fontSize: 14, fontWeight: '700', color: Colors.text },
  stepCard: {
    backgroundColor: '#1E293B',
    borderRadius: 14,
    padding: 16,
    borderLeftWidth: 4,
    borderLeftColor: Colors.danger,
  },
  stepTitle: { fontSize: 11, fontWeight: '700', color: Colors.danger, textTransform: 'uppercase' },
  stepName: { fontSize: 15, fontWeight: '800', color: Colors.text, marginVertical: 4 },
  stepDesc: { fontSize: 12, color: Colors.textMuted, lineHeight: 17, marginBottom: 14 },
  authButton: {
    backgroundColor: Colors.danger,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 8,
  },
  authButtonText: { color: '#FFFFFF', fontWeight: '800', fontSize: 13 },
  exportButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.08)',
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
  },
  exportButtonText: { color: Colors.text, fontWeight: '600', fontSize: 12 },
});
