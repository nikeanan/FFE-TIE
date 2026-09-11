import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Colors } from '../theme/colors';
import { NextBestAction } from '../types';

interface ActionCardProps {
  action: NextBestAction;
  onPressAction: (action: NextBestAction) => void;
}

export const ActionCard: React.FC<ActionCardProps> = ({ action, onPressAction }) => {
  const isUrgent = action.urgency === 'IMMEDIATE_ACTION';
  const isFinancing = action.urgency === 'FINANCING_OPPORTUNITY';
  const borderColor = isUrgent ? Colors.danger : isFinancing ? Colors.success : Colors.info;

  const buttonText =
    action.actionType === 'FIX_INVOICE'
      ? '🛠️ Fix Quantity Discrepancy'
      : action.actionType === 'ACCEPT_TREDS_BID'
      ? '💰 Lock SBI Factoring Bid'
      : action.actionType === 'AUTHORIZE_ESCALATION'
      ? '⚖️ Sign Legal Disallowance Notice'
      : '📨 Dispatch Follow-up Nudge';

  return (
    <View style={[styles.card, { borderLeftColor: borderColor }]}>
      <View style={styles.header}>
        <Text style={styles.badge}>{action.buyerName}</Text>
        <Text style={[styles.urgency, { color: borderColor }]}>
          {action.urgency.replace('_', ' ')}
        </Text>
      </View>
      <Text style={styles.title}>{action.title}</Text>
      <Text style={styles.rationale}>{action.rationale}</Text>
      <View style={styles.impactContainer}>
        <Text style={styles.impactLabel}>⚡ Impact:</Text>
        <Text style={styles.impactText}>{action.estimatedImpact}</Text>
      </View>
      <TouchableOpacity
        style={[styles.button, { backgroundColor: isUrgent ? '#B91C1C' : Colors.primary }]}
        onPress={() => onPressAction(action)}
        activeOpacity={0.8}
      >
        <Text style={styles.buttonText}>{buttonText}</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.surfaceCard,
    borderRadius: 14,
    padding: 16,
    borderLeftWidth: 5,
    borderWidth: 1,
    borderColor: Colors.border,
    marginBottom: 12,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  badge: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    color: Colors.text,
    fontSize: 11,
    fontWeight: '600',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  urgency: {
    fontSize: 10,
    fontWeight: '700',
    textTransform: 'uppercase',
  },
  title: {
    fontSize: 15,
    fontWeight: '700',
    color: Colors.text,
    marginBottom: 6,
  },
  rationale: {
    fontSize: 12,
    color: Colors.textMuted,
    lineHeight: 17,
    marginBottom: 10,
  },
  impactContainer: {
    flexDirection: 'row',
    backgroundColor: 'rgba(13, 148, 136, 0.12)',
    padding: 8,
    borderRadius: 6,
    marginBottom: 12,
  },
  impactLabel: {
    fontSize: 11,
    fontWeight: '700',
    color: Colors.primaryAccent,
    marginRight: 4,
  },
  impactText: {
    fontSize: 11,
    color: Colors.primaryAccent,
    flex: 1,
  },
  button: {
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontWeight: '700',
    fontSize: 13,
  },
});
