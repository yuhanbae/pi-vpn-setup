SIMPLE WIREGUARD AUTH WRAPPER
=============================

This script provides HTTP BASIC authentication using the
ws.unja.ac.id credentials before allowing access to the
WireGuard VPN status/page.

Usage:
  # Install Caddy (or use with nginx)
  # Create Caddyfile with this config:
  
  yuhanbae.vpn.io {
    basicauth users.json wg-auth.json
    reverse_proxy 127.0.0.1:51820/
  }

  # Or run standalone python HTTP proxy:
  python3 wg-auth-proxy.py

wg-auth-proxy.py:
  - Listens on port 8080
  - Authenticates against username: 198305052005011001
  - Password: 3ntahlaH
  - Forwards authenticated clients to WireGuard host:port
  - Logs all access attempts

Credentials:
  - Username: 198305052005011001
  - Password: 3ntahlaH
  - These are the same credentials provided for ws.unja.ac.id

Security:
  - Password is stored in memory only (no file persistence)
  - Sessions are not persisted (re-auth on each connection)
  - Recommended to use HTTPS termination if exposing publicly