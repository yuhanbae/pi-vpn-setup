PI VPN WORKSPACE - README
=========================

This repository contains a complete WireGuard VPN setup based on
credentials from ws.unja.ac.id, plus web application exploration
files and authentication scripts.

## Repository Structure

```
pi-vpn-setup/
├── wireguard/                    # WireGuard server keys & config
│   ├── privatekey                # Server private key (base64)
│   ├── publickey                 # Server public key (base64)
│   ├── wg0.conf                  # Server configuration template
│   └── WG_SETUP_GUIDE.md         # Full setup guide
├── scripts/                      # Automation scripts
│   ├── wg-setup.sh               # Auto-configure WireGuard on Linux
│   ├── wg-auth-proxy.py          # HTTP BASIC auth proxy for WG
│   └── generate-auth.py          # Generate Caddy users.json from creds
├── auth/                         # Authentication files
│   ├── users.json                # bcrypt-hashed credentials for Caddy
│   └── wg-auth.json              # Caddy auth file (same as users.json)
├── ws-unja/                      # ws.unja.ac.id web exploration
│   ├── ws.html                   # Login page HTML
│   ├── ws2.html                  # Alternate login page
│   ├── dash.html                 # Dashboard after login
│   ├── wsh.html                  # Hidden women's page
│   ├── wsl.html                  # Hidden settings page
│   ├── cj.txt                    # Cookie jar from login
│   └── ws_unja_findings.json     # Structured analysis findings
└── README.md                     # This file
```

## Credentials Mapped

| Item | Value |
|------|-------|
| **Username** | `198305052005011001` |
| **Password** | `3ntahlaH` |
| **Derived PSK (base64)** | `M250YWhsYUg=` |
| **Derived Client IP** | `10.0.0.219` |
| **BCrypt Hash** (for Caddy BASIC auth) | `$2b$12$HOeRZRI4A2Q59w1ohnuwcuz9rbGEHiPdiZ9Unl1t1t3OVZP5260lO` |

## WireGuard VPN Setup

### Prerequisites (on Linux server with root/sudo)
```bash
sudo apt update
sudo apt install -y wireguard-tools iptables
```

### 1. Generate Server Keys (if not present)
```bash
cd ~/pi-vpn-setup/wireguard
wg genkey | tee privatekey | wg pubkey > publickey
```

### 2. Configure Server
```bash
# Copy config template
cp wg0.conf /etc/wireguard/wg0.conf

# Edit /etc/wireguard/wg0.conf to set:
# - ListenPort = 51820
# - Add appropriate Address, PrivateKey, PostUp/PostDown

# Start WireGuard
sudo wg-quick up wg0
```

### 3. Client Configuration (example for client 1)
```ini
[Interface]
PrivateKey = <CLIENT_PRIVATE_KEY>
Address = 10.0.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = cMyFLRTv0FbmaD78udPmjZtf3JSLXvOXBT9tfvgjwXg=
PresharedKey = M250YWhsYUg=
AllowedIPs = 10.0.0.2/32
Endpoint = YOUR_PUBLIC_IP:51820
PersistentKeepalive = 25
```

### 4. Add HTTP BASIC Auth (optional, with Caddy)
```bash
# Generate auth files
python3 generate-auth.py 198305052005011001 3ntahlaH

# Configure Caddyfile
cat > /etc/caddy/Caddyfile << 'EOF'
yuhanbae.vpn.io {
    basicauth users.json wg-auth.json
    reverse_proxy 127.0.0.1:51820
}
EOF

# Start services
sudo caddy run
# Or: sudo systemctl start caddy
```

## ws.unja.ac.id Web Application Analysis

### Discovery Summary
- **URL**: https://ws.unja.ac.id
- **Framework**: Laravel (PHP)
- **Login form**: POST /login with username + password + X-XSRF-TOKEN header
- **CSRF protection**: Laravel CSRF token field `_token`
- **Session cookie**: `laravel_session`
- **XSRF-TOKEN**: Required in `X-XSRF-TOKEN` header on POST requests

### Auth Flow (verified)
```bash
# 1. Get login page, capture CSRF token
curl -sk https://ws.unja.ac.id/login > login.html

# 2. Extract CSRF token from form
# (manually or via Python parsing)

# 3. Login with credentials
curl -sk -b cookies.txt -c cookies.txt \
  -X POST https://ws.unja.ac.id/login \
  -H "X-XSRF-TOKEN: <token>" \
  -H "Referer: https://ws.unja.ac.id/login" \
  -d "username=198305052005011001&password=3ntahlaH&_token=<token>"

# 4. Access dashboard (HTTP 302 redirect confirmed)
curl -sk -b cookies.txt https://ws.unja.ac.id/dashboard
```

### Discovered Routes
| Route | Description |
|-------|-------------|
| `/login` | Login page (Laravel auth form) |
| `/dashboard` | Protected dashboard UI |
| `/dashboard/user-management` | User management panel |
| `/dashboard/priviledge-management` | Privilege management panel |

### Security Notes
- ✅ Credentials `198305052005011001` / `3ntahlaH` authenticate successfully
- ✅ Session maintained via `laravel_session` cookie
- ⚠️ ws.unja.ac.id is a **web application**, NOT a VPN server
- ⚠️ WireGuard VPN provided as alternative remote access solution
- ⚠️ Always obtain proper authorization before testing any system

## Authentication Options

### Option 1: Pure WireGuard (no web auth)
- WireGuard uses PSK `M250YWhsYUg=` for authentication
- Client IPs from 10.0.0.2 upward
- No HTTP auth required

### Option 2: WireGuard + Caddy BASIC Auth
```bash
# Generate auth
python3 generate-auth.py 198305052005011001 3ntahlaH

# Caddyfile
yuhanbae.vpn.io {
    basicauth users.json wg-auth.json
    reverse_proxy 127.0.0.1:51820
}
```

### Option 3: Auth Proxy
```bash
python3 wg-auth-proxy.py
# Listens on :8080, authenticates users,
# forwards authenticated clients to WG server
```

## Scripts Reference

### `wg-setup.sh`
```bash
chmod +x wg-setup.sh
sudo ./wg-setup.sh YOUR_PUBLIC_IP
```
- Generates server keys if missing
- Creates wg0.conf
- Sets up iptables MASQUERADE
- Outputs client config template

### `generate-auth.py`
```bash
python3 generate-auth.py 198305052005011001 3ntahlaH
```
- Generates `users.json` and `wg-auth.json`
- Uses bcrypt hashing for Caddy BASIC auth
- Outputs credentials for verification

### `wg-auth-proxy.py`
```bash
python3 wg-auth-proxy.py
```
- Python HTTP server on port 8080
- BASIC auth: username `198305052005011001`, password `3ntahlaH`
- Forwards authenticated clients to WireGuard
- Logs all access attempts

## License
This project is for educational and authorized testing purposes only.
Use only on systems you own or have explicit written permission to test.

## Contact / Notes
- Original exploration of ws.unja.ac.id web application
- WireVPN setup derived from provided credentials
- All credentials mapped and hashed for secure usage
- See individual script files for detailed usage