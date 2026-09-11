import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Colors } from '../theme/colors';

interface VoiceNoteMicProps {
  onRecordComplete: (text: string) => void;
}

export const VoiceNoteMic: React.FC<VoiceNoteMicProps> = ({ onRecordComplete }) => {
  const [isRecording, setIsRecording] = useState(false);

  const toggleRecording = () => {
    if (isRecording) {
      setIsRecording(false);
      onRecordComplete('नमस्ते, एनटीपीसी वाले बिल का क्या स्टेटस है? (Hindi Voice Audio Query)');
    } else {
      setIsRecording(true);
      setTimeout(() => {
        setIsRecording(false);
        onRecordComplete('भेल वाले बिल में 45 MT को 50 MT करके दोबारा भेजो (Hindi Voice Remediation)');
      }, 2500);
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={[styles.micButton, isRecording && styles.micRecording]}
        onPress={toggleRecording}
        activeOpacity={0.8}
      >
        <Text style={styles.micIcon}>{isRecording ? '⏹️' : '🎙️'}</Text>
      </TouchableOpacity>
      <Text style={styles.hintText}>
        {isRecording
          ? 'Listening in Hindi / English...'
          : 'Hold to speak vernacular command'}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginVertical: 12,
  },
  micButton: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: Colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: Colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 8,
    elevation: 8,
  },
  micRecording: {
    backgroundColor: Colors.danger,
  },
  micIcon: {
    fontSize: 26,
  },
  hintText: {
    fontSize: 11,
    color: Colors.textMuted,
    marginTop: 6,
  },
});
