# Quick SOP – Wazuh Vulnerability Remediation

**Platform:** Debian 13 / Proxmox VE

### 1. Identify the vulnerable package

```bash
dpkg -l | grep -i PACKAGE_NAME
apt-cache policy PACKAGE_NAME
```

Record the CVE, severity, installed version and fixed version from Wazuh.

### 2. Check whether the service is running

```bash
sudo systemctl status SERVICE_NAME --no-pager
sudo ss -lntup
```

### 3. Check dependencies and usage

```bash
apt-cache rdepends --installed PACKAGE_NAME
apt-mark showmanual | grep -i PACKAGE_NAME
sudo lsof | grep -i LIBRARY_NAME
```

### 4. Check for security updates

```bash
sudo apt update
apt-cache policy PACKAGE_NAME
```

If a fixed version is available:

```bash
sudo apt install --only-upgrade PACKAGE_NAME
```

### 5. If the package is unnecessary, simulate removal

```bash
sudo apt-get -s remove PACKAGE_NAME
```

Review all proposed removals. Ensure no Proxmox or production dependencies are affected.

### 6. Remove the package

```bash
sudo apt remove PACKAGE_NAME
sudo apt autoremove
```

Review each removal transaction before confirming.

### 7. Clean residual configuration (optional)

```bash
sudo apt purge PACKAGE_NAME
```

### 8. Verify

```bash
dpkg -l | grep -i PACKAGE_NAME
apt-cache policy PACKAGE_NAME
```

### 9. Verify in Wazuh

Search using:

```text
agent.name: "HOSTNAME"
AND vulnerability.id: "CVE-ID"
```

Allow Syscollector and vulnerability detection to refresh before confirming clearance.

---

### Important rules

- Never remove packages blindly.
- Check dependencies before removal.
- Prefer official Debian security updates.
- Never manually install packages from another Debian release.
- Never suppress CVEs globally just to clear alerts.
- Verify Proxmox and production services after remediation.

**Success criteria:** Package upgraded to a fixed version or safely removed, services operational, and Wazuh finding cleared.
