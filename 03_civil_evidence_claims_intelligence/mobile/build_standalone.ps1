# CECI — Civil Evidence & Claims Intelligence Mobile Build Helper (PowerShell)
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host " CECI — Civil Evidence & Claims Intelligence Mobile Build Helper" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Select build target:"
Write-Host "[1] Preview / Test Locally in Browser (Expo Web)"
Write-Host "[2] Build Standalone Android APK (for Direct Device Testing)"
Write-Host "[3] Build Production Android App Bundle (.AAB for Google Play Store)"
Write-Host "[4] Build Production iOS App (.IPA via EAS Cloud)"
Write-Host "[5] Exit"
Write-Host ""

$choice = Read-Host "Enter option [1-5]"

switch ($choice) {
    "1" {
        Write-Host "`nStarting Expo Web Development Server..." -ForegroundColor Green
        npx expo start --web
    }
    "2" {
        Write-Host "`nCompiling Standalone Android APK via EAS Build..." -ForegroundColor Yellow
        npx eas-cli build --profile preview --platform android
    }
    "3" {
        Write-Host "`nCompiling Production Android App Bundle (.AAB) for Google Play..." -ForegroundColor Green
        npx eas-cli build --profile production --platform android
    }
    "4" {
        Write-Host "`nCompiling Production iOS App (.IPA) for Apple App Store..." -ForegroundColor Magenta
        npx eas-cli build --profile production --platform ios
    }
    Default {
        Write-Host "Exiting."
    }
}
