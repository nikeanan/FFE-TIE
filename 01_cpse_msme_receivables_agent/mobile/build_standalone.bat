@echo off
echo ===============================================================================
echo   RECEIVX Mobile -- Standalone Production Build Generator (Android ^& iOS)
echo ===============================================================================
echo.

echo [1/3] Installing NPM dependencies...
call npm install

echo.
echo [2/3] Choose build target:
echo   1. Android Standalone APK (Direct Sideload on Android Phone)
echo   2. Android Google Play App Bundle (AAB for Play Console)
echo   3. iOS IPA (Ad-hoc / TestFlight for iPhone)
echo   4. iOS Simulator Build (.tar.gz for macOS Xcode Simulator)
echo   5. Local Native Prebuild (Generate raw android/ and ios/ native folders)
echo.

set /p choice="Enter choice [1-5]: "

if "%choice%"=="1" (
    echo.
    echo Building Android Standalone APK via EAS Cloud...
    npx eas-cli build --platform android --profile preview
) else if "%choice%"=="2" (
    echo.
    echo Building Android Play Store AAB Bundle via EAS Cloud...
    npx eas-cli build --platform android --profile production
) else if "%choice%"=="3" (
    echo.
    echo Building iOS IPA via EAS Cloud...
    npx eas-cli build --platform ios --profile preview-device
) else if "%choice%"=="4" (
    echo.
    echo Building iOS Simulator Bundle via EAS Cloud...
    npx eas-cli build --platform ios --profile preview
) else if "%choice%"=="5" (
    echo.
    echo Generating Native Android and iOS projects locally...
    npx expo prebuild --clean
) else (
    echo Invalid choice.
)

pause
