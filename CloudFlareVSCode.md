# SSH Access to Remote Server via Cloudflare Tunnel (VS Code Remote-SSH)

**Goal:** SSH into `D7070` (self-hosted server, no open ports on the router) from any location, including VS Code Remote-SSH, using an existing Cloudflare Tunnel instead of port forwarding.

**Server:** D7070 (Debian, Proxmox VM) — `youruser` user
**Client tested:** Windows (PowerShell + VS Code), Linux (D5070)
**Hostname:** `ssh.yourdomain.com`

---

## 1. Architecture Decision

Used a **Public Hostname** on the existing Cloudflare Tunnel — just the `cloudflared` CLI binary on each client, used as an SSH `ProxyCommand`. No persistent background client needed, low setup overhead, well suited to occasional access from varying machines/locations.

We initially landed on the wrong screen in the dashboard (a private-network "Create a new hostname route" flow) — that was abandoned in favor of the **Public Hostname** tab under the Tunnel's own settings.

---

## 2. Server-Side: Cloudflare Tunnel Public Hostname

The tunnel was already running as a systemd service (`cloudflared`), managed as a **remotely-managed tunnel** (config lives in the Cloudflare dashboard, not a local `config.yml` — this is now the default Cloudflare pushes for new/edited tunnels).

**Steps taken in the dashboard:**
1. `one.dash.cloudflare.com` → **Networks** → **Tunnels** → select the existing tunnel
2. **Public Hostname** tab (not "Private Network" / hostname routes) → **Add a public hostname**
   - Subdomain: `ssh`
   - Domain: `yourdomain.com`
   - **Service Type: SSH**
   - URL: `localhost:22`
3. Saved — no restart required, propagates live to the running connector

---

## 3. Client-Side Setup

### 3a. Install `cloudflared` on each client machine

`cloudflared` must be installed **separately on every device** you connect from — it's not part of the tunnel/server setup.

**Linux (D5070):** already had it installed.

**Windows:**
- `winget install --id Cloudflare.cloudflared` failed (`winget` not available on this system)
- Manual install used instead:
  1. Downloaded `cloudflared-windows-amd64.exe` from the [cloudflared GitHub releases](https://github.com/cloudflare/cloudflared/releases/latest)
  2. Renamed to `cloudflared.exe`, placed in `C:\Program Files\cloudflare\`
  3. Added `C:\Program Files\cloudflare` to the **`Path`** environment variable (not a custom-named variable — Windows only checks `Path`)
  4. **Fully closed and reopened PowerShell** (and VS Code, separately — both cache PATH at launch)
  5. Verified: `cloudflared --version`

> ⚠️ Common mistake to avoid: creating a variable literally named `cloudflared` pointing at the `.exe` file does nothing. Only the `Path` variable (pointing at the containing **folder**) is checked.

### 3b. SSH keypair per device

Each client machine has its **own separate SSH keypair** (not shared):
- D5070: existing keypair
- Windows: generated fresh with `ssh-keygen -t ed25519`

Each device's **public** key was appended to `~/.ssh/authorized_keys` on the server for the `youruser` user:
```bash
echo "ssh-ed25519 AAAA... device-comment" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

Keeping keys per-device means any one machine's access can be revoked independently by removing its line from `authorized_keys`.

---

## 4. SSH Client Config

`~/.ssh/config` (on each client — `C:\Users\ashis\.ssh\config` on Windows):

```
Host myserver
  HostName ssh.yourdomain.com
  User youruser
  ProxyCommand cloudflared access ssh --hostname %h
  IdentityFile ~/.ssh/id_ed25519
```

Permissions (Linux/macOS clients):
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/config
```

**Important:** the `Host myserver` block only applies when you connect using the alias `myserver`. Running `ssh user@ssh.yourdomain.com` directly (raw hostname) bypasses the whole block, including `IdentityFile` and `ProxyCommand` — always connect via the alias:
```bash
ssh myserver
```

---

## 5. Staged Testing Process

Tested in layers so failures could be isolated to the right component:

**Stage 1 — DNS resolves:**
```bash
dig +short ssh.yourdomain.com
```
→ returned Cloudflare proxy IPs (expected, confirms hostname route is live)

**Stage 2 — Tunnel + sshd reachable (no SSH client involved):**
```bash
cloudflared access ssh --hostname ssh.yourdomain.com
```
→ returned a raw `SSH-2.0-OpenSSH_...` banner, proving DNS → tunnel → sshd all work. (Note: this command is diagnostic only — it's a raw byte proxy, not an actual SSH client. Typing a username/password into it does nothing.)

**Stage 3 — Full SSH login:**
```bash
ssh myserver
```

### Issues hit and resolved along the way

| Symptom | Cause | Fix |
|---|---|---|
| `winget` not recognized | Not installed on this Windows build | Manual binary install |
| `cloudflared --version` still not recognized after PATH edit | PowerShell window was already open before the PATH change | Fully closed and reopened terminal |
| VS Code Remote-SSH: `CreateProcessW failed error:2` / `posix_spawnp: No such file or directory` | VS Code was launched *before* the PATH update, so it inherited the old PATH and couldn't find `cloudflared.exe` | Fully quit VS Code (including background tray process) and relaunched |
| `Permission denied, please try again` (password prompt) under username `ash` | Wrong Unix username — server account is `youruser`, not `ash` | Corrected `User` in SSH config |
| `Permission denied (publickey)` when testing `ssh -o ProxyCommand="..." youruser@ssh.yourdomain.com` directly | Bypassed the `Host myserver` config block by using the raw hostname instead of the alias — `IdentityFile` was never applied | Use the `myserver` alias, or pass `-i ~/.ssh/id_ed25519` explicitly when testing with the raw hostname |

---

## 6. VS Code Remote-SSH

Once `ssh myserver` worked cleanly from a plain terminal:
1. Fully reopen VS Code (fresh process, correct PATH)
2. `Ctrl+Shift+P` → **Remote-SSH: Connect to Host** → `myserver`

VS Code reads the same `~/.ssh/config`, so no separate configuration was needed — it just works once the underlying `ssh myserver` command works.

---

## 7. Security Hardening

### ✅ Completed

- **Per-device SSH keys** — separate keypair per client machine, easy to revoke individually
- **Root login denied** — `PermitRootLogin no` was already set in `/etc/ssh/sshd_config`, confirmed by live test (root login attempt rejected)
- **Password authentication disabled** — a live test proved `youruser` could log in with *just a password*, no key, while password auth was still enabled. Fixed:
  ```
  # /etc/ssh/sshd_config
  PasswordAuthentication no
  PubkeyAuthentication yes
  PermitRootLogin no
  ```
  ```bash
  sudo systemctl restart ssh
  ```
  Verified afterward: password-only login now fails immediately (no prompt), key-based login via `ssh myserver` succeeds.

  ⚠️ **Process note for next time:** always keep a working session open as a fallback *while* restarting sshd after an auth change, and verify the new config actually saved (`grep` the setting) before restarting — we initially restarted sshd without the edit having been saved, which gave a false sense of security.

### 🔲 Outstanding / Not Yet Done

1. **Cloudflare Access policy** — the hostname `ssh.yourdomain.com` is still reachable by anyone on the internet who resolves it; only SSH key auth stands in front of it right now. Plan:
   - Zero Trust → Access → Applications → Add an application → Self-hosted
   - Hostname: `ssh.yourdomain.com`
   - Policy: Allow rule scoped to a specific email (not "anyone with an email")
   - Set a reasonable session duration (e.g. 24h), not indefinite

2. **Firewall / bind-address check** — `sshd` is currently listening on `0.0.0.0:22` (all interfaces), not just localhost. Need to confirm nothing outside the tunnel path can reach it directly:
   ```bash
   sudo ss -tlnp | grep :22
   sudo ufw status
   ```
   If UFW allows port 22 from `Anywhere`, tighten it to localhost/LAN-only, since the tunnel already handles all legitimate remote access.

3. **Nice-to-haves (lower priority):**
   - Fail2ban on sshd (defense in depth even with Access in front)
   - Cloudflare Access login notifications/alerts
   - Periodic audit of `authorized_keys` entries

---

## Quick Reference — Final Working Config

**Server (`D7070`) — `/etc/ssh/sshd_config` (relevant lines):**
```
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
```

**Client — `~/.ssh/config`:**
```
Host myserver
  HostName ssh.yourdomain.com
  User youruser
  ProxyCommand cloudflared access ssh --hostname %h
  IdentityFile ~/.ssh/id_ed25519
```

**Connect:**
```bash
ssh myserver
```
or via VS Code: **Remote-SSH: Connect to Host** → `myserver`
