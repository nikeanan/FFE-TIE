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

interface CityPilot {
  id: string;
  name: string;
  authority: string;
  zone: string;
  baseDepthM: number;
  preventedDamageCr: number;
  rechargeMld: number;
  bcrMultiple: number;
}

const CITIES: CityPilot[] = [
  { id: '1', name: 'Bengaluru', authority: 'BBMP', zone: 'Bellandur / ORR Tech Basin', baseDepthM: 1.35, preventedDamageCr: 552.5, rechargeMld: 4.85, bcrMultiple: 31.7 },
  { id: '2', name: 'Mumbai', authority: 'BMC', zone: 'Mithi River / Hindmata Basin', baseDepthM: 1.65, preventedDamageCr: 942.5, rechargeMld: 6.20, bcrMultiple: 23.8 },
  { id: '3', name: 'Chennai', authority: 'GCC', zone: 'Velachery / OMR IT Basin', baseDepthM: 1.45, preventedDamageCr: 637.0, rechargeMld: 5.40, bcrMultiple: 26.8 },
  { id: '4', name: 'Gurugram', authority: 'GMDA', zone: 'Subhash Chowk / Badshahpur', baseDepthM: 1.10, preventedDamageCr: 217.0, rechargeMld: 3.80, bcrMultiple: 18.6 },
  { id: '5', name: 'Hyderabad', authority: 'GHMC', zone: 'Begumpet Nala / Hussain Sagar', baseDepthM: 1.25, preventedDamageCr: 481.0, rechargeMld: 4.20, bcrMultiple: 26.7 },
];

export default function App() {
  const [selected, setSelected] = useState<string>('1');
  const selCity = CITIES.find((c) => c.id === selected) || CITIES[0];

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <ScrollView contentContainerStyle={styles.scroll}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>🌊 WRAI Mobile</Text>
          <Text style={styles.headerSubtitle}>WaterResilience AI • Smart Flood Twin</Text>
          <View style={styles.badge}>
            <Text style={styles.badgeText}>🟢 5 Smart Cities Online</Text>
          </View>
        </View>

        {/* Aggregate KPI Overview */}
        <View style={styles.kpiContainer}>
          <View style={styles.kpiBox}>
            <Text style={styles.kpiLabel}>Damage Prevented</Text>
            <Text style={[styles.kpiValue, { color: '#4ADE80' }]}>₹ 2,830 Cr</Text>
          </View>
          <View style={styles.kpiBox}>
            <Text style={styles.kpiLabel}>Aquifer Recharged</Text>
            <Text style={[styles.kpiValue, { color: '#38BDF8' }]}>24.45 MLD</Text>
          </View>
        </View>

        {/* City Selector */}
        <Text style={styles.sectionTitle}>Select Smart City Catchment</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.selectorRow}>
          {CITIES.map((c) => (
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

        {/* Selected City Card */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>{selCity.name} ({selCity.authority})</Text>
          <Text style={styles.cardSubtitle}>Zone: {selCity.zone}</Text>

          <View style={styles.metricRow}>
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>Baseline Inundation</Text>
              <Text style={styles.metricVal}>{selCity.baseDepthM.toFixed(2)} meters</Text>
            </View>
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>Damage Protected</Text>
              <Text style={[styles.metricVal, { color: '#4ADE80' }]}>₹ {selCity.preventedDamageCr.toFixed(1)} Cr</Text>
            </View>
          </View>

          <View style={styles.metricRow}>
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>Aquifer Recharge Yield</Text>
              <Text style={[styles.metricVal, { color: '#38BDF8' }]}>{selCity.rechargeMld.toFixed(2)} MLD</Text>
            </View>
            <View style={styles.metricItem}>
              <Text style={styles.metricLabel}>Municipal BCR</Text>
              <Text style={[styles.metricVal, { color: '#FBBF24' }]}>{selCity.bcrMultiple.toFixed(1)}x ROI</Text>
            </View>
          </View>

          <TouchableOpacity style={styles.actionBtn}>
            <Text style={styles.actionBtnText}>🌱 View Sponge City SUDS Blueprint</Text>
          </TouchableOpacity>
        </View>

        {/* Quick Actions */}
        <View style={styles.quickActions}>
          <TouchableOpacity style={styles.secondaryBtn}>
            <Text style={styles.secondaryBtnText}>🌧️ Run 50-Year Cloudburst Stress Test</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.secondaryBtn}>
            <Text style={styles.secondaryBtnText}>📜 Download Municipal EAP Directive</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#061C14',
  },
  scroll: {
    padding: 16,
  },
  header: {
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#134E4A',
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
    color: '#99F6E4',
    marginTop: 4,
  },
  badge: {
    alignSelf: 'flex-start',
    backgroundColor: 'rgba(20, 184, 166, 0.2)',
    borderColor: '#14B8A6',
    borderWidth: 1,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    marginTop: 8,
  },
  badgeText: {
    color: '#5EEAD4',
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
    backgroundColor: '#0B2E24',
    padding: 14,
    borderRadius: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#14B8A6',
  },
  kpiLabel: {
    fontSize: 11,
    color: '#99F6E4',
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
    backgroundColor: '#0B2E24',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#134E4A',
  },
  selectorChipActive: {
    backgroundColor: '#0D9488',
    borderColor: '#14B8A6',
  },
  chipText: {
    color: '#99F6E4',
    fontSize: 12,
    fontWeight: '600',
  },
  chipTextActive: {
    color: '#FFFFFF',
  },
  card: {
    backgroundColor: '#0B2E24',
    borderRadius: 16,
    padding: 18,
    borderWidth: 1,
    borderColor: '#134E4A',
    marginBottom: 20,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  cardSubtitle: {
    fontSize: 12,
    color: '#99F6E4',
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
    backgroundColor: '#0D9488',
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
    backgroundColor: '#061C14',
    borderWidth: 1,
    borderColor: '#134E4A',
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
  },
  secondaryBtnText: {
    color: '#CCFBF1',
    fontWeight: '600',
    fontSize: 13,
  },
});
