#!/usr/bin/env python3
"""Generate Caddy BASIC auth users.json from credentials.

Usage:
    python3 generate-auth.py USERNAME PASSWORD

Example:
    python3 generate-auth.py 198305052005011001 3ntahlaH

Output:
    Creates users.json with bcrypt hash suitable for Caddy basicauth.
    Also creates wg-auth.json (Caddy convention - same content).

    The generated users.json can be referenced in Caddyfile via:
        basicauth users.json wg-auth.json
"""

import sys
import json
import bcrypt


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} USERNAME PASSWORD")
        print(f"Example: {sys.argv[0]} 198305052005011001 3ntahlaH")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2].encode("utf-8")

    # Generate bcrypt hash directly using bcrypt library
    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

    # Build users mapping
    users = {username: hashed}

    # Write users.json
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

    # Write wg-auth.json (Caddy convention - same content)
    with open("wg-auth.json", "w") as f:
        json.dump(users, f, indent=2)

    print(f"\nGenerated users.json and wg-auth.json")
    print(f"Username: {username}")
    print(f"Password hash (bcrypt): {hashed}")
    print(f"\nUpdate your Caddyfile to use:")
    print(f'    basicauth users.json wg-auth.json')
    print(f"\nTest with:")
    print(f'  curl -u "{username}:{password.decode()}" http://your-domain/')


if __name__ == "__main__":
    main()