import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Colors } from '../theme/colors';
import { TredsBid } from '../types';

interface TredsBidCardProps {
  bid: TredsBid;
  onAccept: (bidId: string) => void;
}

export const TredsBidCard: React.FC<TredsBidCardProps> = ({ bid, onAccept }) => {
  const isBest = bid.platform === 'RXIL';

  return (
    <View style={[styles.card, isBest && styles.bestCard]}>
      <View style={styles.header}>
        <View>
          <Text style={styles.platform}>{bid.platform} Exchange</Text>
          <Text style={styles.financier}>{bid.financier}</Text>
        </View>
        <View style={styles.aprPill}>
          <Text style={styles.aprText}>{(bid.discountRateApr * 100).toFixed(2)}% APR</Text>
        </View>
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Instant Net Payout:</Text>
        <Text style={styles.payout}>₹{bid.netPayout.toLocaleString('en-IN')}</Text>
      </View>

      <View style={styles.savingsBox}>
        <Text style={styles.savingsText}>
          ⚡ Saves ₹{bid.savingsVsBankOd.toLocaleString('en-IN')} vs. 13.5% Bank OD facility
        </Text>
      </View>

      <TouchableOpacity
        style={styles.acceptButton}
        onPress={() => onAccept(bid.id)}
        activeOpacity={0.8}
      >
        <Text style={styles.acceptButtonText}>Accept & Lock T+1 Cash</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.surfaceCard,
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    marginBottom: 12,
  },
  bestCard: {
    borderColor: Colors.success,
    borderWidth: 1.5,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  platform: {
    fontSize: 11,
    fontWeight: '700',
    color: Colors.primaryAccent,
    textTransform: 'uppercase',
  },
  financier: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.text,
  },
  aprPill: {
    backgroundColor: '#065F46',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 20,
  },
  aprText: {
    color: '#6EE7B7',
    fontSize: 12,
    fontWeight: '800',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginVertical: 6,
  },
  label: {
    fontSize: 12,
    color: Colors.textMuted,
  },
  payout: {
    fontSize: 16,
    fontWeight: '800',
    color: Colors.text,
  },
  savingsBox: {
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    padding: 8,
    borderRadius: 6,
    marginVertical: 8,
  },
  savingsText: {
    color: Colors.success,
    fontSize: 11,
    fontWeight: '600',
  },
  acceptButton: {
    backgroundColor: Colors.primary,
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 4,
  },
  acceptButtonText: {
    color: '#FFFFFF',
    fontWeight: '700',
    fontSize: 13,
  },
});
