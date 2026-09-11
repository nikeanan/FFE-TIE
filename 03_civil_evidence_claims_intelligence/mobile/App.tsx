import React, { useState } from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
  StatusBar,
} from 'react-native';

interface ContractorAudit {
  id: string;
  name: string;
  project: string;
  variationCr: number;
  eotDays: number;
  ldShieldCr: number;
  totalCr: number;
}

const CONTRACTORS: ContractorAudit[] = [
  { id: '1', name: 'L&T Heavy Civil', project: 'Delhi-Meerut RRTS Viaduct', variationCr: 1.78, eotDays: 68, ldShieldCr: 1.50, totalCr: 4.57 },
  { id: '2', name: 'Tata Projects', project: 'Mumbai Coastal Road Sea-Link', variationCr: 4.97, eotDays: 45, ldShieldCr: 1.13, totalCr: 6.39 },
  { id: '3', name: 'Dilip Buildcon', project: 'Delhi-Mumbai Expressway PKG-14', variationCr: 7.36, eotDays: 82, ldShieldCr: 1.56, totalCr: 11.46 },
  { id: '4', name: 'Afcons Marine', project: 'Vizag Deepwater Berth', variationCr: 10.56, eotDays: 54, ldShieldCr: 1.51, totalCr: 14.01 },
  { id: '5', name: 'Megha Engineering', project: 'Himalayan Hydroelectric HRT', variationCr: 10.75, eotDays: 95, ldShieldCr: 2.95, totalCr: 16.51 },
];

export default function App() {
  const [selected, setSelected] = useState<string>('1');
  const selContractor = CONTRACTORS.find((c) => c.id === selected) || CONTRACTORS[0];

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <ScrollView contentContainerStyle={styles.scroll}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>⚖️ CECI Mobile</Text>
          <Text style={styles.headerSubtitle}>Civil Evidence & Claims Intelligence</Text>
          <View style={styles.badge}>
            <Text style={styles.badgeText}>🟢 5 Pilot Portfolios Active</Text>
          </View>
        </View>

        {/* Aggregate KPI Overview */}
        <View style={styles.kpiContainer}>
          <View style={styles.kpiBox}>
            <Text style={styles.kpiLabel}>Portfolio Value</Text>
            <Text style={styles.kpiValue}>₹ 7,590 Cr</Text>
          </View>
          <View style={styles.kpiBox}>
            <Text style={styles.kpiLabel}>Total Value Unlocked</Text>
            <Text style={[styles.kpiValue, { color: '#38BDF8' }]}>₹ 52.93 Cr</Text>
          </View>
        </View>

        {/* Contractor Selector */}
        <Text style={styles.sectionTitle}>Select Infrastructure Project</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.selectorRow}>
          {CONTRACTORS.map((c) => (
            <TouchableOpacity
              key={c.id}
              style={[styles.selectorChip, selected === c.id && styles.selectorChipActive]}
              onPress={() => setSelected(c.id)}
            >
              <Text style={[styles.chipText, selected === c.id && styles.chipTextActive]}>
                {c.name}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>

        {/* Selected Contractor Card */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>{selContractor.name}</Text>
          <Text style={styles.cardSubtitle}>Project: {selContractor.project}</Text>

          <View style={styles.metricRow}>
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>Approved Variation</Text>
              <Text style={styles.metricVal}>₹ {selContractor.variationCr.toFixed(2)} Cr</Text>
            </View>
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>EoT Extension</Text>
              <Text style={styles.metricVal}>{selContractor.eotDays} Days</Text>
            </View>
          </View>

          <View style={styles.metricRow}>
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>LD Risk Shielded</Text>
              <Text style={[styles.metricVal, { color: '#4ADE80' }]}>₹ {selContractor.ldShieldCr.toFixed(2)} Cr</Text>
            </View>
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>Net Financial Gain</Text>
              <Text style={[styles.metricVal, { color: '#38BDF8' }]}>₹ {selContractor.totalCr.toFixed(2)} Cr</Text>
            </View>
          </View>

          <TouchableOpacity style={styles.actionBtn}>
            <Text style={styles.actionBtnText}>📑 View Multi-Modal Evidence Dossier</Text>
          </TouchableOpacity>
        </View>

        {/* Quick Actions */}
        <View style={styles.quickActions}>
          <TouchableOpacity style={styles.secondaryBtn}>
            <Text style={styles.secondaryBtnText}>📸 Capture Site Photo Evidence</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.secondaryBtn}>
            <Text style={styles.secondaryBtnText}>⏱️ Log Hindrance Register Entry</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B0F17',
  },
  scroll: {
    padding: 16,
  },
  header: {
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#1E293B',
    marginBottom: 16,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '800',
    color: '#FFFFFF',
    letterSpacing: -0.5,
  },
  headerSubtitle: {
    fontSize: 13,
    color: '#94A3B8',
    marginTop: 4,
  },
  badge: {
    alignSelf: 'flex-start',
    backgroundColor: 'rgba(99, 102, 241, 0.2)',
    borderColor: '#6366F1',
    borderWidth: 1,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    marginTop: 8,
  },
  badgeText: {
    color: '#A5B4FC',
    fontSize: 11,
    fontWeight: '700',
  },
  kpiContainer: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 20,
  },
  kpiBox: {
    flex: 1,
    backgroundColor: '#1E293B',
    padding: 14,
    borderRadius: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#6366F1',
  },
  kpiLabel: {
    fontSize: 11,
    color: '#94A3B8',
    textTransform: 'uppercase',
  },
  kpiValue: {
    fontSize: 18,
    fontWeight: '700',
    color: '#F8FAFC',
    marginTop: 4,
  },
  sectionTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#F8FAFC',
    marginBottom: 10,
  },
  selectorRow: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  selectorChip: {
    backgroundColor: '#1E293B',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#334155',
  },
  selectorChipActive: {
    backgroundColor: '#4338CA',
    borderColor: '#6366F1',
  },
  chipText: {
    color: '#94A3B8',
    fontSize: 12,
    fontWeight: '600',
  },
  chipTextActive: {
    color: '#FFFFFF',
  },
  card: {
    backgroundColor: '#1E293B',
    borderRadius: 16,
    padding: 18,
    borderWidth: 1,
    borderColor: '#334155',
    marginBottom: 20,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  cardSubtitle: {
    fontSize: 12,
    color: '#94A3B8',
    marginTop: 2,
    marginBottom: 16,
  },
  metricRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 14,
  },
  metricItem: {
    flex: 1,
  },
  metricLabel: {
    fontSize: 11,
    color: '#94A3B8',
  },
  metricVal: {
    fontSize: 16,
    fontWeight: '700',
    color: '#F8FAFC',
    marginTop: 2,
  },
  actionBtn: {
    backgroundColor: '#4F46E5',
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 8,
  },
  actionBtnText: {
    color: '#FFFFFF',
    fontWeight: '700',
    fontSize: 13,
  },
  quickActions: {
    gap: 10,
  },
  secondaryBtn: {
    backgroundColor: '#0F172A',
    borderWidth: 1,
    borderColor: '#334155',
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
  },
  secondaryBtnText: {
    color: '#CBD5E1',
    fontWeight: '600',
    fontSize: 13,
  },
});
