# 📱 RECEIVX Mobile App (Android & iOS)

> **Cross-Platform Native Mobile Application for CPSE–MSME Receivables Intelligence**  
> Built with **React Native / Expo** with full support for **iOS (iPhone/iPad)** and **Android**.

---

## ✨ Mobile Architecture & Capabilities

1. **⚡ Command Center (`DashboardScreen.tsx`)**:
   - Executive dashboard with live Section 16 statutory compound interest ticker (19.5% p.a.).
   - 1-tap Next-Best-Action (NBA) agenda execution.
2. **🔍 Pre-Submission Gatekeeper (`GatekeeperScanScreen.tsx`)**:
   - Camera/document OCR scanning for Purchase Orders & Invoices.
   - Live 4-way match discrepancy badges and automated Udyam MSMED stamp injection.
3. **⏱️ GeM GFR Rule 149 CRAC Tracker (`GemCracTrackerScreen.tsx`)**:
   - Live 10-day deemed acceptance countdown bar.
   - Statutory Deemed CRAC demand notice generator with speed-post tracking.
4. **💰 TReDS Multi-Exchange Auction Room (`TredsAuctionScreen.tsx`)**:
   - Live bid stream from RXIL, M1xchange, Invoicemart.
   - APR comparison and net working capital savings vs. bank overdraft/CC facility.
5. **⚖️ Statutory Escalator Desk (`EscalatorLegalScreen.tsx`)**:
   - Section 43B(h) IT Act tax disallowance notice dispatcher.
   - MSME Samadhaan MSEFC Form 1 XML package generator.
6. **💬 Vernacular Voice & WhatsApp AI Chat (`VoiceWhatsAppScreen.tsx`)**:
   - Hindi & English voice query processor.
   - 1-tap quick action chips (`FIX`, `STATUS`, `ACCEPT`, `APPROVE`).

---

## 🚀 How to Run on Android & iOS

### Prerequisites
- Node.js (v18+)
- Expo CLI (`npx expo install`)
- For iOS physical device / simulator: **Xcode** (macOS) or **Expo Go App** (App Store)
- For Android physical device / emulator: **Android Studio** or **Expo Go App** (Google Play Store)

### 1. Install Dependencies
```bash
cd mobile
npm install
```

### 2. Start Dev Server
```bash
npx expo start
```
- Press **`a`** to open in Android Emulator / connected Android phone.
- Press **`i`** to open in iOS Simulator (macOS).
- Scan QR code using the **Expo Go** app on your iPhone or Android device.

---

## 📦 Production Builds (App Store & Google Play)

### Android APK / AAB Build:
```bash
npx eas-cli build -p android --profile preview
```

### iOS IPA Build:
```bash
npx eas-cli build -p ios --profile preview
```
