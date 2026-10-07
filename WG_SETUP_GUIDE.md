WIREGUARD VPN SERVER SETUP
=========================

Based on your credentials:
- Username: 198305052005011001
- Password: 3ntahlaH

SERVER CONFIGURATION (deploy on a Linux server with root/NAT access):

[Server] wg0.conf
-----------------------------------
[Interface]
PrivateKey = WFxUFIXJ/RLf2NDAX8orc7nTuh0f0M0woLLiONvsvGo=
Address = 10.0.0.1/24
ListenPort = 51820
SaveConfig = true

# Client ACL
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT -s 10.0.0.0/24 -j ACCEPT; iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT -s 10.0.0.0/24 -j ACCEPT; iptables -t nat -D POSTROUTING -s 10.0.0.0/24 -j MASQUERADE

[Peer]  # Client 1
PublicKey = YOUR_FIRST_CLIENT_PUBLIC_KEY_HERE
PresharedKey = your_psk_here
AllowedIPs = 10.0.0.2/32
Endpoint = YOUR_PUBLIC_IP:51820

[Peer]  # Client 2
PublicKey = YOUR_SECOND_CLIENT_PUBLIC_KEY_HERE
PresharedKey = your_psk_here
AllowedIPs = 10.0.0.3/32
Endpoint = YOUR_PUBLIC_IP:51820

CLIENT CONFIGURATION (save as client1.conf, client2.conf, etc.):

[Client]
PrivateKey = <CLIENT_PRIVATE_KEY>
Address = 10.0.0.X/24  # unique IP per client, e.g., 10.0.0.2
DNS = 1.1.1.1

[Peer]
PublicKey = <SERVER_PUBLIC_KEY>
PresharedKey = your_psk_here
Endpoint = <SERVER_PUBLIC_IP>:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

USAGE:
1. Install WireGuard on your device/router/server
2. Copy wg0.conf to /etc/wireguard/ on the server
3. Start: wg-quick up wg0
4. Share client configs with authorized users
5. The credentials (username/password above) can be used as PresharedKey or for HTTP auth if you add a TLS gateway

NOTES:
- This is a site-to-site or remote-access VPN tunnel
- Requires a server with public IP and port 51820 forwarded
- Client IPs are assigned from 10.0.0.2 upward
- Keep the username/password secure - they identify authorized users