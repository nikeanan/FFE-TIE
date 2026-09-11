import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Colors } from '../theme/colors';

interface CracCountdownTimerProps {
  daysElapsed: number;
  totalLimit?: number;
  contractNo: string;
}

export const CracCountdownTimer: React.FC<CracCountdownTimerProps> = ({
  daysElapsed,
  totalLimit = 10,
  contractNo,
}) => {
  const isDeemedAccepted = daysElapsed >= totalLimit;
  const daysRemaining = Math.max(0, totalLimit - daysElapsed);
  const progressPercent = Math.min(100, (daysElapsed / totalLimit) * 100);

  return (
    <View style={styles.container}>
      <View style={styles.topRow}>
        <Text style={styles.tag}>GeM GFR Rule 149</Text>
        <Text style={styles.contractText}>{contractNo}</Text>
      </View>

      <View style={styles.statusBarContainer}>
        <View
          style={[
            styles.statusBarFill,
            {
              width: `${progressPercent}%`,
              backgroundColor: isDeemedAccepted ? Colors.success : Colors.warning,
            },
          ]}
        />
      </View>

      <View style={styles.bottomRow}>
        <Text style={styles.elapsedText}>
          {daysElapsed} of {totalLimit} days elapsed
        </Text>
        <Text
          style={[
            styles.statusBadge,
            { color: isDeemedAccepted ? Colors.success : Colors.warning },
          ]}
        >
          {isDeemedAccepted ? '🎯 DEEMED ACCEPTED' : `⏳ ${daysRemaining} DAYS REMAINING`}
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: Colors.surfaceCard,
    borderRadius: 12,
    padding: 14,
    borderWidth: 1,
    borderColor: Colors.border,
    marginBottom: 10,
  },
  topRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  tag: {
    color: Colors.primaryAccent,
    fontSize: 11,
    fontWeight: '700',
  },
  contractText: {
    color: Colors.textMuted,
    fontSize: 11,
  },
  statusBarContainer: {
    height: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 8,
  },
  statusBarFill: {
    height: '100%',
    borderRadius: 4,
  },
  bottomRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  elapsedText: {
    fontSize: 11,
    color: Colors.textMuted,
  },
  statusBadge: {
    fontSize: 11,
    fontWeight: '800',
  },
});
