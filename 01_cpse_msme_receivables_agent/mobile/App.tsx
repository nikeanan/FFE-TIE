import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, SafeAreaView } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Colors } from './src/theme/colors';

import { DashboardScreen } from './src/screens/DashboardScreen';
import { GatekeeperScanScreen } from './src/screens/GatekeeperScanScreen';
import { GemCracTrackerScreen } from './src/screens/GemCracTrackerScreen';
import { TredsAuctionScreen } from './src/screens/TredsAuctionScreen';
import { EscalatorLegalScreen } from './src/screens/EscalatorLegalScreen';
import { VoiceWhatsAppScreen } from './src/screens/VoiceWhatsAppScreen';

type TabName = 'DASHBOARD' | 'SCAN' | 'GEM' | 'TREDS' | 'LEGAL' | 'WHATSAPP';

export default function App() {
  const [activeTab, setActiveTab] = useState<TabName>('DASHBOARD');

  const renderActiveScreen = () => {
    switch (activeTab) {
      case 'DASHBOARD':
        return <DashboardScreen />;
      case 'SCAN':
        return <GatekeeperScanScreen />;
      case 'GEM':
        return <GemCracTrackerScreen />;
      case 'TREDS':
        return <TredsAuctionScreen />;
      case 'LEGAL':
        return <EscalatorLegalScreen />;
      case 'WHATSAPP':
        return <VoiceWhatsAppScreen />;
      default:
        return <DashboardScreen />;
    }
  };

  const navItems = [
    { key: 'DASHBOARD' as TabName, label: 'Command', icon: '⚡' },
    { key: 'SCAN' as TabName, label: 'OCR Scan', icon: '🔍' },
    { key: 'GEM' as TabName, label: 'GeM CRAC', icon: '⏱️' },
    { key: 'TREDS' as TabName, label: 'TReDS', icon: '💰' },
    { key: 'LEGAL' as TabName, label: 'Legal 43B', icon: '⚖️' },
    { key: 'WHATSAPP' as TabName, label: 'WhatsApp', icon: '💬' },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" />
      <View style={styles.screenContainer}>{renderActiveScreen()}</View>

      {/* Bottom Navigation Bar */}
      <View style={styles.bottomNav}>
        {navItems.map((item) => {
          const isActive = activeTab === item.key;
          return (
            <TouchableOpacity
              key={item.key}
              style={[styles.tabButton, isActive && styles.tabButtonActive]}
              onPress={() => setActiveTab(item.key)}
              activeOpacity={0.7}
            >
              <Text style={styles.tabIcon}>{item.icon}</Text>
              <Text style={[styles.tabLabel, isActive && styles.tabLabelActive]}>
                {item.label}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  screenContainer: {
    flex: 1,
  },
  bottomNav: {
    flexDirection: 'row',
    backgroundColor: Colors.surface,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
    paddingVertical: 8,
    paddingHorizontal: 4,
    justifyContent: 'space-around',
  },
  tabButton: {
    alignItems: 'center',
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 8,
  },
  tabButtonActive: {
    backgroundColor: 'rgba(13, 148, 136, 0.15)',
  },
  tabIcon: {
    fontSize: 18,
    marginBottom: 2,
  },
  tabLabel: {
    fontSize: 10,
    color: Colors.textDim,
    fontWeight: '600',
  },
  tabLabelActive: {
    color: Colors.primaryAccent,
    fontWeight: '800',
  },
});
