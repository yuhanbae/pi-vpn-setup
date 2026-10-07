WIREGUARD VPN AUTO-SETUP SCRIPT
================================

This script sets up the WireGuard VPN configuration files
based on the ws.unja.ac.id credentials and exploration data.

Prerequisites (on a Linux server with root/sudo):
  sudo apt update && sudo apt install -y wireguard-tools iptables

Usage:
  chmod +wg-setup.sh ./wg-setup.sh
  sudo ./wg-setup.sh YOUR_PUBLIC_IP

What it does:
  1. Generates server WireGuard keys (if not present)
  2. Creates wg0.conf with server private key
  3. Sets up basic iptables MASQUERADE for client internet access
  4. Outputs client configuration template
  5. Records authentication credentials mapping

Credits:
  - Original credentials: username=198305052005011001, password=3ntahlaH
  - Derived PSK (base64): M250YWhsYUg=
  - Derived client IP: 10.0.0.219