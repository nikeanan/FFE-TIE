Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  RECEIVX Mobile -- Standalone Production Build Generator (Android & iOS)     " -ForegroundColor Yellow
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Checking dependencies..." -ForegroundColor Green
npm install

Write-Host ""
Write-Host "[2/3] Choose Standalone Build Target:" -ForegroundColor Yellow
Write-Host "  1. Android Direct-Install APK (Sideload directly on Android phone)"
Write-Host "  2. Android Google Play App Bundle (AAB for Google Play Store upload)"
Write-Host "  3. iOS IPA (Ad-Hoc / TestFlight distribution for iPhone)"
Write-Host "  4. iOS Simulator Build (.tar.gz for Xcode iOS Simulator)"
Write-Host "  5. Local Native Prebuild (Export raw native Android Studio & Xcode projects)"
Write-Host ""

$choice = Read-Host "Enter choice [1-5]"

switch ($choice) {
    "1" {
        Write-Host "Building Android Standalone APK..." -ForegroundColor Green
        npx eas-cli build --platform android --profile preview
    }
    "2" {
        Write-Host "Building Android Production AAB..." -ForegroundColor Green
        npx eas-cli build --platform android --profile production
    }
    "3" {
        Write-Host "Building iOS IPA..." -ForegroundColor Green
        npx eas-cli build --platform ios --profile preview-device
    }
    "4" {
        Write-Host "Building iOS Simulator Build..." -ForegroundColor Green
        npx eas-cli build --platform ios --profile preview
    }
    "5" {
        Write-Host "Generating local native Android Studio and Xcode directories..." -ForegroundColor Green
        npx expo prebuild --clean
    }
    Default {
        Write-Host "Invalid choice." -ForegroundColor Red
    }
}
