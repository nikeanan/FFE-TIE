@echo off
echo =====================================================================
echo  CMI — Construction Material Intelligence Mobile Build Helper
echo =====================================================================
echo.
echo Select build target:
echo [1] Preview / Test Locally in Browser (Expo Web)
echo [2] Build Standalone Android APK (for Direct Device Testing)
echo [3] Build Production Android App Bundle (.AAB for Google Play Store)
echo [4] Build Production iOS App (.IPA via EAS Cloud)
echo [5] Exit
echo.

set /p choice="Enter option [1-5]: "

if "%choice%"=="1" (
    echo.
    echo Starting Expo Web Development Server...
    npx expo start --web
) else if "%choice%"=="2" (
    echo.
    echo Compiling Standalone Android APK via EAS Build...
    npx eas-cli build --profile preview --platform android
) else if "%choice%"=="3" (
    echo.
    echo Compiling Production Android App Bundle (.AAB) for Google Play...
    npx eas-cli build --profile production --platform android
) else if "%choice%"=="4" (
    echo.
    echo Compiling Production iOS App (.IPA) for Apple App Store...
    npx eas-cli build --profile production --platform ios
) else (
    echo Exiting.
)
