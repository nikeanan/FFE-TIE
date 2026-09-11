import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { Colors } from '../theme/colors';
import { VoiceNoteMic } from '../components/VoiceNoteMic';

interface ChatMessage {
  id: string;
  text: string;
  sender: 'BOT' | 'USER';
  time: string;
}

export const VoiceWhatsAppScreen: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      text: '🙏 Namaste! Main RECEIVX AI Assistant hoon. Aapke 3 bills active hain. NTPC Dadri ka bill deemed accepted ho gaya hai.',
      sender: 'BOT',
      time: '10:30 AM',
    },
    {
      id: '2',
      text: 'STATUS',
      sender: 'USER',
      time: '10:32 AM',
    },
    {
      id: '3',
      text: '📊 Active Receivables: ₹46.25 L\n• BHEL: Flagged (Qty discrepancy)\n• PGCIL: TReDS Bid open @ 7.85%\n• NTPC: Overdue (>45d). Reply FIX, ACCEPT, or APPROVE.',
      sender: 'BOT',
      time: '10:32 AM',
    },
  ]);
  const [inputText, setInputText] = useState('');

  const sendMessage = (text: string) => {
    if (!text.trim()) return;
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      text,
      sender: 'USER',
      time: 'Just now',
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputText('');

    setTimeout(() => {
      let reply = 'Command received and executed by Autonomous Agent.';
      if (text.toUpperCase().includes('FIX')) {
        reply = '✅ BHEL Invoice INV/2026/088 quantity updated to 50 MT and re-submitted to CPSE gate.';
      } else if (text.toUpperCase().includes('ACCEPT')) {
        reply = '💰 SBI Factoring Bid @ 7.85% accepted on RXIL. Payout ₹14.52 L scheduled.';
      } else if (text.toUpperCase().includes('STATUS')) {
        reply = '📊 All 6 agents running. Next settlement forecast: NTPC bill payment on Mar 18.';
      }

      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          text: reply,
          sender: 'BOT',
          time: 'Just now',
        },
      ]);
    }, 800);
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        {/* WhatsApp Top Bar */}
        <View style={styles.topBar}>
          <View style={styles.botAvatar}>
            <Text style={styles.avatarText}>RX</Text>
          </View>
          <View>
            <Text style={styles.botName}>RECEIVX Official Assistant</Text>
            <Text style={styles.botStatus}>Vernacular Voice & Text • Online</Text>
          </View>
        </View>

        {/* Chat History */}
        <ScrollView contentContainerStyle={styles.chatArea}>
          {messages.map((m) => (
            <View
              key={m.id}
              style={[
                styles.bubble,
                m.sender === 'USER' ? styles.bubbleUser : styles.bubbleBot,
              ]}
            >
              <Text style={styles.bubbleText}>{m.text}</Text>
              <Text style={styles.timeText}>{m.time}</Text>
            </View>
          ))}
        </ScrollView>

        {/* Vernacular Mic Simulator */}
        <VoiceNoteMic onRecordComplete={(text) => sendMessage(text)} />

        {/* Quick Action Chips */}
        <View style={styles.chipRow}>
          {['FIX', 'STATUS', 'ACCEPT', 'APPROVE'].map((chip) => (
            <TouchableOpacity
              key={chip}
              style={styles.chip}
              onPress={() => sendMessage(chip)}
              activeOpacity={0.7}
            >
              <Text style={styles.chipText}>{chip}</Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Input Bar */}
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Type WhatsApp message..."
            placeholderTextColor={Colors.textDim}
            value={inputText}
            onChangeText={setInputText}
          />
          <TouchableOpacity
            style={styles.sendButton}
            onPress={() => sendMessage(inputText)}
            activeOpacity={0.8}
          >
            <Text style={styles.sendIcon}>📤</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.whatsappDark },
  topBar: {
    backgroundColor: '#202C33',
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    gap: 12,
  },
  botAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: Colors.whatsappGreen,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: { color: '#FFFFFF', fontWeight: '800', fontSize: 14 },
  botName: { fontSize: 14, fontWeight: '700', color: '#E9EDEF' },
  botStatus: { fontSize: 11, color: '#8696A0' },
  chatArea: { padding: 16 },
  bubble: {
    padding: 12,
    borderRadius: 12,
    marginBottom: 10,
    maxWidth: '85%',
  },
  bubbleUser: {
    backgroundColor: Colors.whatsappBubbleOut,
    alignSelf: 'flex-end',
    borderBottomRightRadius: 2,
  },
  bubbleBot: {
    backgroundColor: Colors.whatsappBubbleIn,
    alignSelf: 'flex-start',
    borderBottomLeftRadius: 2,
  },
  bubbleText: { color: '#E9EDEF', fontSize: 13.5, lineHeight: 18 },
  timeText: { fontSize: 9, color: '#8696A0', alignSelf: 'flex-end', marginTop: 4 },
  chipRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: 16,
    paddingVertical: 6,
  },
  chip: {
    backgroundColor: '#2A3942',
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderRadius: 14,
  },
  chipText: { color: Colors.primaryAccent, fontSize: 11, fontWeight: '700' },
  inputContainer: {
    flexDirection: 'row',
    padding: 10,
    backgroundColor: '#202C33',
    alignItems: 'center',
    gap: 8,
  },
  input: {
    flex: 1,
    backgroundColor: '#2A3942',
    color: '#FFFFFF',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 8,
    fontSize: 13,
  },
  sendButton: {
    backgroundColor: Colors.whatsappGreen,
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendIcon: { fontSize: 16 },
});
