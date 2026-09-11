import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, SafeAreaView, ScrollView } from 'react-native';
import { StatusBar } from 'expo-status-bar';

export default function App() {
  const [activeTab, setActiveTab] = useState<'MIX' | 'QC' | 'CARBON' | 'CERT'>('MIX');

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" />
      <View style={styles.header}>
        <Text style={styles.headerTitle}>🏗️ CMI Mobile Plant Twin</Text>
        <Text style={styles.headerSub}>UltraTech Ready-Mix Hub #04 • Gurugram</Text>
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        {activeTab === 'MIX' && (
          <View style={styles.card}>
            <Text style={styles.cardTitle}>🧪 Concrete Mix Design (M30 Grade)</Text>
            <Text style={styles.metric}>Target f'ck: 38.25 MPa</Text>
            <Text style={styles.subtext}>IS 10262:2019 • Severe Exposure Verified</Text>
            <View style={styles.divider} />
            <Text style={styles.detail}>• OPC 53 Cement: 330 kg/m³</Text>
            <Text style={styles.detail}>• Fly Ash (Class F): 80 kg/m³</Text>
            <Text style={styles.detail}>• W/B Ratio: 0.390 (IS 456 PASSED ✅)</Text>
          </View>
        )}

        {activeTab === 'QC' && (
          <View style={styles.card}>
            <Text style={styles.cardTitle}>⚠️ Live SCADA Batch QC (IS 4926)</Text>
            <Text style={[styles.metric, { color: '#10B981' }]}>Status: 100% In Tolerance</Text>
            <Text style={styles.subtext}>Cement Scale: ±0.6% | Moisture Compensated</Text>
            <View style={styles.divider} />
            <Text style={styles.detail}>• Metered Water: 155 L</Text>
            <Text style={styles.detail}>• Sand Moisture: 4.5% (+33.3 L Free Water)</Text>
            <Text style={styles.detail}>• Effective W/C: 0.459</Text>
          </View>
        )}

        {activeTab === 'CARBON' && (
          <View style={styles.card}>
            <Text style={styles.cardTitle}>🌱 Embodied Carbon Intelligence</Text>
            <Text style={[styles.metric, { color: '#38BDF8' }]}>236.4 kg CO₂e / m³</Text>
            <Text style={styles.subtext}>-28.5% CO₂ vs. 100% OPC Baseline</Text>
            <View style={styles.divider} />
            <Text style={styles.detail}>• SCM Replacement: 19.5%</Text>
            <Text style={styles.detail}>• IGBC Tier: GOLD / 4-STAR GREEN CONCRETE</Text>
            <Text style={styles.detail}>• Annual Plant Offset: 2,410 Tonnes CO₂e</Text>
          </View>
        )}

        {activeTab === 'CERT' && (
          <View style={styles.card}>
            <Text style={styles.cardTitle}>📜 Digital Batch QA Certificate</Text>
            <Text style={styles.metric}>SHA256-CMI-TICKET-9081</Text>
            <Text style={styles.subtext}>Client: Larsen & Toubro Ltd (Heavy Civil)</Text>
            <View style={styles.divider} />
            <Text style={styles.detail}>• 28d Predicted Strength: 41.2 MPa</Text>
            <Text style={styles.detail}>• Certified by: Chief Materials Engineer</Text>
            <TouchableOpacity style={styles.button}>
              <Text style={styles.buttonText}>📥 Export ISO 9001 Certificate</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>

      {/* Bottom Tabs */}
      <View style={styles.bottomNav}>
        {[
          { key: 'MIX', label: 'Mix Design', icon: '🧪' },
          { key: 'QC', label: 'Batch QC', icon: '⚠️' },
          { key: 'CARBON', label: 'Carbon', icon: '🌱' },
          { key: 'CERT', label: 'Certificate', icon: '📜' },
        ].map((t) => (
          <TouchableOpacity
            key={t.key}
            style={[styles.navBtn, activeTab === t.key && styles.navBtnActive]}
            onPress={() => setActiveTab(t.key as any)}
          >
            <Text style={styles.navIcon}>{t.icon}</Text>
            <Text style={[styles.navLabel, activeTab === t.key && styles.navLabelActive]}>
              {t.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0B132B' },
  header: { padding: 16, backgroundColor: '#1C2541', borderBottomWidth: 1, borderBottomColor: 'rgba(255,255,255,0.08)' },
  headerTitle: { fontSize: 18, fontWeight: '800', color: '#F8FAFC' },
  headerSub: { fontSize: 12, color: '#38BDF8', marginTop: 2 },
  content: { padding: 16 },
  card: { backgroundColor: '#1E293B', borderRadius: 14, padding: 18, borderWidth: 1, borderColor: 'rgba(255,255,255,0.08)' },
  cardTitle: { fontSize: 16, fontWeight: '700', color: '#F8FAFC', marginBottom: 6 },
  metric: { fontSize: 24, fontWeight: '800', color: '#38BDF8', marginVertical: 4 },
  subtext: { fontSize: 12, color: '#94A3B8' },
  divider: { height: 1, backgroundColor: 'rgba(255,255,255,0.08)', marginVertical: 12 },
  detail: { fontSize: 13, color: '#CBD5E1', marginVertical: 3 },
  button: { backgroundColor: '#0284C7', paddingVertical: 10, borderRadius: 8, alignItems: 'center', marginTop: 12 },
  buttonText: { color: '#FFFFFF', fontWeight: '700', fontSize: 13 },
  bottomNav: { flexDirection: 'row', backgroundColor: '#1C2541', paddingVertical: 10, borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.08)', justifyContent: 'space-around' },
  navBtn: { alignItems: 'center', paddingVertical: 4, paddingHorizontal: 12, borderRadius: 8 },
  navBtnActive: { backgroundColor: 'rgba(2, 132, 199, 0.2)' },
  navIcon: { fontSize: 18, marginBottom: 2 },
  navLabel: { fontSize: 10, color: '#64748B', fontWeight: '600' },
  navLabelActive: { color: '#38BDF8', fontWeight: '800' },
});
