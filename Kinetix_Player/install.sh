#!/bin/bash

echo "==============================================="
echo "   KINETIX PLAYER - AUTOMATED INSTALLER v1.0   "
echo "==============================================="
echo "Designed for the Low-End PC Community."
echo ""

# 1. Install System Dependencies (Requires user to enter their password)
echo "[*] Step 1: Installing highly optimized core packages..."
sudo pacman -Syu --needed docker android-tools scrcpy tk python --noconfirm

# 2. Configure Docker Permissions (So the app can run without root/sudo)
echo "[*] Step 2: Configuring engine permissions..."
sudo systemctl enable --now docker
sudo usermod -aG docker $USER

# 3. Create the Hidden Application Directory
echo "[*] Step 3: Moving core files into system storage..."
APP_DIR="$HOME/.local/share/kinetix_player"
mkdir -p "$APP_DIR"

# Copy the python script into the hidden folder
cp kinetix_player.py "$APP_DIR/"
chmod +x "$APP_DIR/kinetix_player.py"

# 4. Generate the Desktop Shortcut (Terminal=false ensures it runs silently)
echo "[*] Step 4: Building the desktop application shortcut..."
DESKTOP_FILE="$HOME/.local/share/applications/kinetixplayer.desktop"

cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=Kinetix Player
Comment=Ultra Low-End Performance Android Engine
Exec=python3 $APP_DIR/kinetix_player.py
Icon=input-gaming
Terminal=false
Categories=Game;Emulator;
EOF

chmod +x "$DESKTOP_FILE"

echo ""
echo "==============================================="
echo "[+] INSTALLATION SUCCESSFUL!"
echo "==============================================="
echo "[!] CRITICAL: You MUST restart your PC right now."
echo "    Restarting applies the Docker user permissions so the engine"
echo "    can boot smoothly and securely without asking for passwords."
echo ""
echo "After restarting, open your app menu, search for 'Kinetix Player',"
echo "and click it to start gaming!"
