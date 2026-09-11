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
import { CracCountdownTimer } from '../components/CracCountdownTimer';
import { ReceivxService } from '../services/api';

export const GemCracTrackerScreen: React.FC = () => {
  const handleGenerateNotice = async () => {
    const res = await ReceivxService.generateGeMNotice('GEMC-51168772910293');
    Alert.alert(
      '🏛️ Statutory Deemed CRAC Demand Notice Generated',
      res.notice + '\n\n[Dispatched via Email & Registered Speed Post]'
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <Text style={styles.title}>⏱️ GeM GFR Rule 149 Tracker</Text>
          <Text style={styles.subTitle}>10-Day Deemed Acceptance (CRAC) Automation</Text>
        </View>

        <View style={styles.infoBox}>
          <Text style={styles.infoTitle}>⚖️ GFR 2017 Rule 149 Statutory Mandate:</Text>
          <Text style={styles.infoText}>
            Public buyers on GeM must issue CRAC within 10 days of delivery. On day 11, the system auto-deems goods accepted, barring subsequent deductions or delay rejections.
          </Text>
        </View>

        <Text style={styles.sectionHeader}>Active GeM Consignments:</Text>

        <CracCountdownTimer
          contractNo="GEMC-51168772910293 (NTPC Dadri)"
          daysElapsed={12}
          totalLimit={10}
        />

        <View style={styles.actionCard}>
          <Text style={styles.actionTitle}>⚡ Deemed Acceptance Triggered!</Text>
          <Text style={styles.actionDesc}>
            NTPC Dadri delivery took place 12 days ago. Since no dispute was lodged within 10 days, this bill of ₹13,00,000 is deemed accepted by law.
          </Text>
          <TouchableOpacity style={styles.demandButton} onPress={handleGenerateNotice} activeOpacity={0.8}>
            <Text style={styles.demandButtonText}>📜 Dispatch Statutory CRAC Demand Notice</Text>
          </TouchableOpacity>
        </View>

        <CracCountdownTimer
          contractNo="GEMC-99482710481023 (Power Grid North)"
          daysElapsed={6}
          totalLimit={10}
        />
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
  infoBox: {
    backgroundColor: 'rgba(13, 148, 136, 0.12)',
    borderRadius: 10,
    padding: 12,
    marginBottom: 16,
    borderLeftWidth: 3,
    borderLeftColor: Colors.primary,
  },
  infoTitle: { fontSize: 11, fontWeight: '700', color: Colors.primaryAccent, marginBottom: 4 },
  infoText: { fontSize: 11, color: Colors.textMuted, lineHeight: 16 },
  sectionHeader: { fontSize: 14, fontWeight: '700', color: Colors.text, marginBottom: 10 },
  actionCard: {
    backgroundColor: '#064E3B',
    borderRadius: 12,
    padding: 14,
    marginBottom: 16,
  },
  actionTitle: { fontSize: 14, fontWeight: '800', color: '#6EE7B7', marginBottom: 4 },
  actionDesc: { fontSize: 12, color: '#D1FAE5', lineHeight: 17, marginBottom: 10 },
  demandButton: {
    backgroundColor: Colors.primary,
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
  },
  demandButtonText: { color: '#FFFFFF', fontWeight: '700', fontSize: 12 },
});
