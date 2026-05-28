#!/data/data/com.termux/files/usr/bin/bash

# Mobile Companion APK Builder
# This script builds the APK in Termux without Android Studio

set -e

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$APP_DIR/build"
SRC_DIR="$APP_DIR/src"
RES_DIR="$APP_DIR/res"
MANIFEST="$APP_DIR/AndroidManifest.xml"

echo "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—"
echo "â•‘     Mobile Companion APK Builder                â•‘"
echo "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo ""

# Check for required tools
echo "[1/8] Checking dependencies..."
for cmd in java kotlinc aapt d8 apksigner; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: $cmd not found. Run: pkg install $cmd"
        exit 1
    fi
done

# Clean build directory
echo "[2/8] Cleaning build directory..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/classes"
mkdir -p "$BUILD_DIR/dex"

# Compile resources
echo "[3/8] Compiling resources..."
aapt package -f -m \
    -J "$BUILD_DIR/classes" \
    -M "$MANIFEST" \
    -S "$RES_DIR" \
    -I "$ANDROID_HOME/platforms/android-34/android.jar"

# Compile Kotlin source
echo "[4/8] Compiling Kotlin sources..."
KOTLIN_FILES=$(find "$SRC_DIR" -name "*.kt")
kotlinc $KOTLIN_FILES \
    -classpath "$BUILD_DIR/classes:$ANDROID_HOME/platforms/android-34/android.jar" \
    -d "$BUILD_DIR/classes" \
    -no-stdlib

# Convert to DEX
echo "[5/8] Converting to DEX..."
find "$BUILD_DIR/classes" -name "*.class" > "$BUILD_DIR/classes.txt"
d8 --output "$BUILD_DIR/dex" \
    --lib "$ANDROID_HOME/platforms/android-34/android.jar" \
    @"$BUILD_DIR/classes.txt"

# Package APK
echo "[6/8] Packaging APK..."
aapt package -f \
    -M "$MANIFEST" \
    -S "$RES_DIR" \
    -I "$ANDROID_HOME/platforms/android-34/android.jar" \
    -F "$BUILD_DIR/mobile-companion-unsigned.apk"

# Add DEX to APK
cd "$BUILD_DIR/dex"
aapt add "$BUILD_DIR/mobile-companion-unsigned.apk" classes.dex
cd "$APP_DIR"

# Generate keystore (if not exists)
if [ ! -f "$BUILD_DIR/keystore.jks" ]; then
    echo "[7/8] Generating signing key..."
    keytool -genkey -v \
        -keystore "$BUILD_DIR/keystore.jks" \
        -alias mobilecompanion \
        -keyalg RSA \
        -keysize 2048 \
        -validity 10000 \
        -storepass android \
        -keypass android \
        -dname "CN=Mobile Companion, OU=AI, O=MobileCompanion, L=Unknown, ST=Unknown, C=US"
else
    echo "[7/8] Using existing keystore..."
fi

# Sign APK
echo "[8/8] Signing APK..."
apksigner sign \
    --ks "$BUILD_DIR/keystore.jks" \
    --ks-key-alias mobilecompanion \
    --ks-pass pass:android \
    --key-pass pass:android \
    --out "$BUILD_DIR/mobile-companion.apk" \
    "$BUILD_DIR/mobile-companion-unsigned.apk"

# Copy to home directory
cp "$BUILD_DIR/mobile-companion.apk" "$HOME/mobile-companion.apk"

echo ""
echo "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—"
echo "â•‘           BUILD SUCCESSFUL!                     â•‘"
echo "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo ""
echo "APK location: $HOME/mobile-companion.apk"
echo ""
echo "To install:"
echo "  pkg install aapt"
echo "  aapt install $HOME/mobile-companion.apk"
echo ""
echo "Or transfer to your phone and install manually."
echo ""
