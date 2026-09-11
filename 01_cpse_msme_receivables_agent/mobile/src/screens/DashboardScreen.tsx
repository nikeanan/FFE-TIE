import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  SafeAreaView,
  RefreshControl,
  Alert,
} from 'react-native';
import { Colors } from '../theme/colors';
import { KpiCard } from '../components/KpiCard';
import { ActionCard } from '../components/ActionCard';
import { ReceivxService } from '../services/api';
import { NextBestAction } from '../types';

export const DashboardScreen: React.FC = () => {
  const [refreshing, setRefreshing] = useState(false);
  const [summary, setSummary] = useState<any>(null);

  const loadData = async () => {
    const data = await ReceivxService.getAdvisorSummary();
    setSummary(data);
  };

  useEffect(() => {
    loadData();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  const handleActionPress = async (action: NextBestAction) => {
    if (action.actionType === 'FIX_INVOICE') {
      const res = await ReceivxService.autoRemediateInvoice(action.invoiceId);
      Alert.alert('✅ Auto-Remediation Applied', res.message);
    } else if (action.actionType === 'ACCEPT_TREDS_BID') {
      const res = await ReceivxService.acceptTredsBid('bid_sbi_01');
      Alert.alert('💰 TReDS Bid Locked', res.message);
    } else if (action.actionType === 'AUTHORIZE_ESCALATION') {
      Alert.alert(
        '⚖️ Legal Notice Authorized',
        'Section 43B(h) disallowance notice digitally generated and dispatched to buyer finance director.'
      );
    } else {
      Alert.alert('📨 Follow-up Dispatched', 'Automated polite WhatsApp nudge sent to CPSE accounts desk.');
    }
  };

  if (!summary) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Initializing RECEIVX Autonomous Engine...</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.content}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.primaryAccent} />}
      >
        {/* Header Profile */}
        <View style={styles.header}>
          <View>
            <Text style={styles.welcome}>⚡ RECEIVX COMMAND</Text>
            <Text style={styles.subWelcome}>Precision Engineering Works (MSME)</Text>
          </View>
          <View style={styles.statusBadge}>
            <Text style={styles.statusText}>🟢 6 AGENTS LIVE</Text>
          </View>
        </View>

        {/* 4 KPI Grid */}
        <View style={styles.kpiGrid}>
          <KpiCard
            label="Active Receivables"
            value="₹46.25 L"
            subtext="3 CPSE contracts"
            accentColor="#38BDF8"
          />
          <KpiCard
            label="MSMED Overdue (>45d)"
            value="₹18.50 L"
            subtext="Non-compliant Sec 15"
            accentColor="#EF4444"
          />
          <KpiCard
            label="Sec 16 Interest Accrued"
            value="₹2.98 L"
            subtext="3x RBI Rate (19.5% p.a.)"
            accentColor="#F59E0B"
          />
          <KpiCard
            label="TReDS Instant Cash"
            value="₹14.75 L"
            subtext="T+1 Factoring ready"
            accentColor="#10B981"
          />
        </View>

        {/* Section 16 Live Interest Accumulation Ticker */}
        <View style={styles.tickerCard}>
          <View style={styles.tickerHeader}>
            <Text style={styles.tickerTitle}>⚖️ Statutory Section 16 Daily Ticker</Text>
            <Text style={styles.tickerRate}>19.5% p.a. Compounding</Text>
          </View>
          <Text style={styles.tickerAmount}>₹ 2,98,540.85</Text>
          <Text style={styles.tickerSub}>Accruing ₹ 988.50 every 24 hours from non-compliant buyers.</Text>
        </View>

        {/* Daily NBA Agenda */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>🎯 Daily Next-Best-Actions (NBA)</Text>
          <Text style={styles.sectionCaption}>Synthesized across CPSE buyer behavior graphs</Text>
        </View>

        {summary.actions.map((act: NextBestAction) => (
          <ActionCard key={act.actionId} action={act} onPressAction={handleActionPress} />
        ))}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  loadingContainer: {
    flex: 1,
    backgroundColor: Colors.background,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: Colors.textMuted,
    fontSize: 14,
  },
  content: {
    padding: 16,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  welcome: {
    fontSize: 18,
    fontWeight: '800',
    color: Colors.text,
    letterSpacing: -0.5,
  },
  subWelcome: {
    fontSize: 12,
    color: Colors.primaryAccent,
    fontWeight: '600',
  },
  statusBadge: {
    backgroundColor: 'rgba(13, 148, 136, 0.2)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: Colors.primary,
  },
  statusText: {
    fontSize: 10,
    fontWeight: '700',
    color: Colors.primaryAccent,
  },
  kpiGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  tickerCard: {
    backgroundColor: '#1E1B4B',
    borderRadius: 14,
    padding: 16,
    marginVertical: 10,
    borderWidth: 1,
    borderColor: '#4338CA',
  },
  tickerHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 6,
  },
  tickerTitle: {
    fontSize: 12,
    fontWeight: '700',
    color: '#C7D2FE',
  },
  tickerRate: {
    fontSize: 10,
    fontWeight: '800',
    color: '#FBBF24',
  },
  tickerAmount: {
    fontSize: 24,
    fontWeight: '800',
    color: '#F8FAFC',
    marginVertical: 4,
  },
  tickerSub: {
    fontSize: 11,
    color: '#A5B4FC',
  },
  sectionHeader: {
    marginTop: 14,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '800',
    color: Colors.text,
  },
  sectionCaption: {
    fontSize: 12,
    color: Colors.textDim,
  },
});
