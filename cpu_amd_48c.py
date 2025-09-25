import paramiko
import threading
import io
import os
import sys

# ==== EDIT LIST IP DI SINI ====
IPS = [
#     "44.203.56.181",
# "34.207.123.4",
# "18.205.116.18",


"3.83.105.89",
"52.201.227.131",


# "34.239.105.243",
# "35.173.125.250",
]

USERNAME = "root"

# ==== PILIH METODE AUTENTIKASI ====
# Jika True -> gunakan PRIVATE_KEY; jika False -> gunakan PASSWORD
USE_SSH_KEY = True

# Jika menggunakan password, tulis di sini:
PASSWORD = "Azura042AA"  # ganti sesuai VPS (jika USE_SSH_KEY=False)

# -----------------------------
# Paste private key di bawah ini (termasuk -----BEGIN ...----- sampai -----END ...-----)
# Jika tidak pakai key, biarkan string kosong atau tetap tapi set USE_SSH_KEY=False
# -----------------------------
PRIVATE_KEY = r"""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2DJRmWW9NenwFv3BwRNE7uKUXOjbByuC2hVNWAeqo535YU6p
+e81xwsolMrS//l0CT7N/RjogOp7UfQdt9tyo8TPp5LBScvEt8OMj2/3VZsE4aS7
fB6o16DCmP6nbtSEqx6azvXUCQuNldDXILyMvYC8QZyt0xCRlSEIQTZFFZ2jiJBd
Ddr2vf+Rcef3Hgqyv6FL7Q6go7avXhE9VJNKuIXg4LpfOOAb1WFO1m2eklIXhL5f
G1WQkads7qHziBpkUAkXc5idkyn0PYDeCuhUjYpPVfbUxnRqpPtmrW1qxbhLL6bp
dv2TVO/wd/F/OmkKMOD5CazxVfoPFbM/Qg66EwIDAQABAoIBAGwusbpKuKVzzFoU
3JFarRHEe20KcB9kXHP4WN2F6JM7B4DztgaE9qoFIWdjHrZMAw5lSPovLpjjvJXD
y+MmgnUElMxLmUDuIB+8UGeuJVvG2Gh44AA5708G+JlKREonOcPO6rRJOrLT/yNK
f3u4Hczt0EYcurZ1AgRXpSPMnkEz1mcA2zSP2i5WqG4yITIBlXPjNam65O/LowPa
PGYVVu+7tvkjhF+DI+ffjw3aMsPQgsOnKcsgR0s4tp5BtVxzvBrVG/exJCAwTUED
HkgttnrposyILE3CX/hRooVT92DK7nNxZKHORlJJe8rjNqTl6qImzss+HQ0gBFYx
oeYMnIECgYEA/n365y0q01WufBwmoRkGQQwzlWauFSg8mRvfyrBTxhpBFFOsOKZ4
OpC++arXnkL4Ql28ZBq0CDXdUG7BxhU+ps1QL1iZM5MF0VGSGaodgzoJ2NYLzQc3
zeCYRHXFQFB50nhfFuhQdNvRmhUiUP2/WeqzDiaN0IkU/4uZxl1YDKECgYEA2XpA
QsQ7zY1f4Mq4dQpxyJLXAgko3XVyKj8nkCWdw29dBjeihWkVPzeGEQ6ZYmNnNUcn
mHgRINnQf4XSUQdPZOeV/ZkHmLP+v6F5Ja5vDqXLg9Tf1FnP22ZHCj6Zx/e7WN0A
eOZ9d+XUpTIPEjIitKEojhXfATzUMAsTVfRydjMCgYAgholismsex3ydcBufy0r5
VU3iclUdbx8Pknhvt0l9sC1RI8CHHP+QvJ8r2aHlIDoKgWBqit8njXrTpNQvNNfl
CaiN5IzwAoJj1kEN9qf+9ZP8mp63fYysS2Aqn8KuDZsEQ04j510hElcfkkPohgXG
wDBSRqspU9vTLUxiBdwTAQKBgQCkjJZgrj+diLGZ0Wj9zbhIDaq3NJ0B62JFSuGx
dHTJMdLN6HyEuvzDh0xeTZCK3DF0I3F3MKmtFIFoa6W1f3V4IK3hYs9XoCFJd3DF
rRUEnTe+eOwerRHTrLBltPYAUpYjZ5x63dLjTDe4Aodauip+R037K9s/AXp/G3I2
4C1W9wKBgQCoIH74y0A3DBjke1vEgx7mjI6r6taaSrK75Cf2cR8+D8cnAIU1nopQ
gREiSJO/RR9X7kwhVoX/cTniKXhZDMoGIQkv6sGSkDn4k8KU4VM3/y/k0AugEdiv
xr86KVcyPahmKXklFtQr6U0xSAg+zJhDAgerUywHDiSDsc1OBFObow==
-----END RSA PRIVATE KEY-----"""

# Jika private key punya passphrase, tulis di sini. Jika tidak, biarkan None
PRIVATE_KEY_PASSPHRASE = None
# -----------------------------

# Skrip remote (tetap sama seperti yang kamu kirim)
SCRIPT = r"""#!/bin/bash
set -e

echo "[1/3] Install build tools..."
apt update -y && apt install -y build-essential && apt install -y docker.io

mkdir -p /usr/local/src /usr/local/lib /usr/local/bin /usr/local/fakeproc

echo "[2/3] Buat fake /proc/cpuinfo..."
rm -f /usr/local/fakeproc/cpuinfo
for i in $(seq 0 47); do
cat <<LINE >> /usr/local/fakeproc/cpuinfo
processor   : $i
vendor_id   : AuthenticAMD
model name  : AMD EPYC 7642 48-Core Processor
cpu MHz     : 2300.000
cache size  : 256000 KB
LINE
done

### MEMINFO (48 GB)
echo "[3/3] Buat fake /proc/meminfo..."
cat <<EOF > /usr/local/fakeproc/meminfo
MemTotal:       50331648 kB
MemFree:        49000000 kB
MemAvailable:   49000000 kB
Buffers:         1000000 kB
Cached:          2000000 kB
SwapCached:            0 kB
EOF

### CAT WRAPPER (CPU/RAM)
cat <<'EOF' > /usr/local/bin/cat
#!/bin/bash
if [[ "$1" == "/proc/cpuinfo" ]]; then
  /bin/cat /usr/local/fakeproc/cpuinfo
elif [[ "$1" == "/proc/meminfo" ]]; then
  /bin/cat /usr/local/fakeproc/meminfo
else
  /bin/cat "$@"
fi
EOF
chmod +x /usr/local/bin/cat

### CLI WRAPPERS
# lscpu
cat <<'EOF' > /usr/local/bin/lscpu
#!/bin/bash
echo "Architecture:          x86_64"
echo "CPU(s):                48"
echo "Thread(s) per core:    1"
echo "Core(s) per socket:    48"
echo "Socket(s):             1"
echo "Vendor ID:             AuthenticAMD"
echo "Model name:            AMD EPYC 7642 48-Core Processor"
echo "CPU MHz:               2300.000"
echo "CPU max MHz:           3300.000"
EOF
chmod +x /usr/local/bin/lscpu

# free (RAM 48GB)
cat <<'EOF' > /usr/local/bin/free
#!/bin/bash
echo "              total        used        free      shared  buff/cache   available"
echo "Mem:    51539607552   2000000000 49000000000     500000   200000000 49000000000"
echo "Swap:    4294967296           0  4294967296"
EOF
chmod +x /usr/local/bin/free

# lsblk
cat <<'EOF' > /usr/local/bin/lsblk
#!/bin/bash
echo "NAME   SIZE TYPE ROTA"
echo "sda 882147483648K disk 0"
EOF
chmod +x /usr/local/bin/lsblk

echo ">>> Selesai (Intel Xeon Platinum 8268, 24 Core @2.9GHz, RAM 64GB)."
echo "Tes dengan:"
echo "  lscpu"
echo "  free -h"
echo "  cat /proc/cpuinfo | head"
echo "  cat /proc/meminfo | head"
"""

# --- helper: load private key from string, try RSA then Ed25519 then ECDSA ---
def load_pkey_from_string(pem_str, passphrase=None):
    if not pem_str or not pem_str.strip():
        raise RuntimeError("PRIVATE_KEY kosong.")
    stream = io.StringIO(pem_str)
    last_exc = None
    try:
        return paramiko.RSAKey.from_private_key(stream, password=passphrase)
    except Exception as e:
        last_exc = e
    stream = io.StringIO(pem_str)
    try:
        return paramiko.Ed25519Key.from_private_key(stream, password=passphrase)
    except Exception as e:
        last_exc = e
    stream = io.StringIO(pem_str)
    try:
        return paramiko.ECDSAKey.from_private_key(stream, password=passphrase)
    except Exception as e:
        last_exc = e
    raise RuntimeError(f"Gagal load private key: {last_exc}")

# Prepare PKEY jika diminta
PKEY = None
if USE_SSH_KEY:
    try:
        PKEY = load_pkey_from_string(PRIVATE_KEY, PRIVATE_KEY_PASSPHRASE)
        print("[*] Private key berhasil di-load.")
    except Exception as e:
        print(f"[ERROR] Gagal load PRIVATE_KEY: {e}")
        raise

# jika pakai password, pastikan terisi
if not USE_SSH_KEY:
    if not PASSWORD:
        raise RuntimeError("USE_SSH_KEY=False tapi PASSWORD kosong. Isi PASSWORD atau ubah USE_SSH_KEY=True.")

def run_cuy(ip):
    try:
        print(f"[+] Connect ke {ip} ...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connect_kwargs = dict(
            hostname=ip,
            username=USERNAME,
            timeout=20,
            allow_agent=False,
            look_for_keys=False
        )

        if USE_SSH_KEY and PKEY is not None:
            connect_kwargs['pkey'] = PKEY
        else:
            connect_kwargs['password'] = PASSWORD

        ssh.connect(**connect_kwargs)

        # run skrip remote
        stdin, stdout, stderr = ssh.exec_command(SCRIPT)
        out = stdout.read().decode(errors='ignore')
        err = stderr.read().decode(errors='ignore')
        print(f"[{ip}] OUTPUT:\n{out}")
        if err:
            print(f"[{ip}] ERROR:\n{err}")
        ssh.close()
    except Exception as e:
        print(f"[{ip}] Gagal: {e}")

threads = []
for ip in IPS:
    t = threading.Thread(target=run_cuy, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
