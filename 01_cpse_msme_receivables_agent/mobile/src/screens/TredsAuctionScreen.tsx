import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Alert,
} from 'react-native';
import { Colors } from '../theme/colors';
import { TredsBidCard } from '../components/TredsBidCard';
import { ReceivxService } from '../services/api';
import { TredsBid } from '../types';

export const TredsAuctionScreen: React.FC = () => {
  const [bids, setBids] = useState<TredsBid[]>([]);

  useEffect(() => {
    ReceivxService.getTredsBids().then(setBids);
  }, []);

  const handleAcceptBid = async (bidId: string) => {
    const res = await ReceivxService.acceptTredsBid(bidId);
    Alert.alert('🎉 Factoring Locked', res.message);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <Text style={styles.title}>💰 TReDS Multi-Exchange Auction</Text>
          <Text style={styles.subTitle}>RXIL • M1xchange • Invoicemart • C2FO</Text>
        </View>

        {/* Comparison Header */}
        <View style={styles.savingsBanner}>
          <View>
            <Text style={styles.savingsLabel}>Net Working Capital Savings</Text>
            <Text style={styles.savingsValue}>₹23,450</Text>
          </View>
          <View style={styles.spreadPill}>
            <Text style={styles.spreadText}>+5.65% APR Spread</Text>
          </View>
        </View>

        <Text style={styles.sectionHeader}>Live Bids for Invoice INV/2026/092 (₹14.75 L):</Text>

        {bids.map((b) => (
          <TredsBidCard key={b.id} bid={b} onAccept={handleAcceptBid} />
        ))}
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
  savingsBanner: {
    backgroundColor: Colors.surfaceCard,
    borderRadius: 14,
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
    borderLeftWidth: 4,
    borderLeftColor: Colors.success,
  },
  savingsLabel: { fontSize: 11, color: Colors.textMuted, textTransform: 'uppercase' },
  savingsValue: { fontSize: 22, fontWeight: '800', color: Colors.success },
  spreadPill: {
    backgroundColor: 'rgba(16, 185, 129, 0.15)',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 20,
  },
  spreadText: { color: Colors.success, fontSize: 11, fontWeight: '800' },
  sectionHeader: { fontSize: 14, fontWeight: '700', color: Colors.text, marginBottom: 10 },
});
