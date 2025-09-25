import paramiko
import threading
import io

# ==== LIST IP ====
IPS = [
    "34.214.107.125",
    "54.185.89.113",
    "54.212.238.192",
    "54.212.119.115"
]

USERNAME = "root"

# ==== PRIVATE KEY (dummy contoh) ====
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA5ivWiKj2hF4wFhbf1f3ymTmDA0GjU81a5kPm5Nnpl0qDlEiq
s/5IkJw8RUlOFy9vty6KeyB1rX1rAzck+IsfIwIpdGmHQn7t9vJFm9+BPA6BpgEv
NdnX65Q46vG6uTrT0qAd6RdR7qeBDy4Mz2/v/wD3jrg6m9hVdI6xcsM9HGU8j4zY
ERBvZrqLrKGKFHFlVeaUvz3f0UMAsjXj0nxayISbXOnHtu1m5DwoZS/8B4bLDaHx
lhH1SPEK/HeQWqy8pI47lYx5KCp52KOj9w46Hp7bWQQMz6HK5lC+d5SgdcNAbcbd
K/gi10UnO2IbKArFuFkzq5zda648uLBo6SxSuwIDAQABAoIBAGXx9rRSudUI7p1q
Bjv+nUvWWDvB/7gnVWJ1orer+LUksMClqs3MC5HZUSyS+j50qTNmLrm4N8berN4g
t4RKAkF8PKYt81W1aGqfBcuzI8dY2X2QOrvMP8E8xjTxWfWeo6E/f9/0jzp4AEab
69qYxqCYag1Rdcv+9mKIrPmald+T9EXuZx/ecQR9Ge3xf++cnfb8ULm76czqTImN
sauUWSbERDea99VXRs6ELj29Xc45SIqXn7HnG6412ePkpiH09f8ebEwislCECYnL
4mjMm1HKmsG4Sm18AHLqGSDW8M038l8iH087iVQqiU3WppKRCtaQYH5L26yYU2OP
J/sO+mECgYEA86dAr2VSY6SRDkVkbc8hv4gLkNqMx6wPo42ScLLvZe+1kYQgfx6g
R0K+e4mSrO7U4K4jfbDZ5UM6cQQx9/ixjeanw0Skn+ADDDvHG96dhwv3bF4kkVRB
NznEqX6XmlPt3oqe2DeDt77pIDE8+q3NQ4pVs6kMjIGPAuSsh34F+MsCgYEA8dWx
BEneZ7x/vVon4h1jxvfuJ+J/ukF5hJownFMwGX/Mx+WL2AxT91G8x62kffCVbBSm
um/aPKeEhi5vijsqkcqfeGh62t4SS+XSBqN+w+6Xn9YhjAdxWhWQQMvwOu6u8Tyb
XTLM3yknG2r7bx4yIwNqCJk7GD79ppJ0uD0u/9ECgYAB5HGnKxVJutR5lOZjx/EO
KMNWO6xOPLLeZVIW1/zuAL+bQrhx5E4AX69VDEt8VlqG6DNUXZRDqJMCn7K3p1HR
tVHmPVk9+KJtbOVt/PuiOeCREeYczte20xcI7ffFdhNp4A+9xCicu7nZyygbFlB6
zs89lvmG+dafgiEo6DypowKBgQDOdzJ6BtbqmfQ1JROH6K+W33Vkd+u0iNHGdB2s
WRlnq8SZpVCPU3ccX5xcndMh8pSfgcIWygf4YMy0AlEYIwtlDSi5E/pPgej9A2kc
YdmITdsFizt44aHU1zQhHfwrVDvnmWbLWuOuYuQQdHXVmGIVooSUcr4RJTZJUCB2
a0YFAQKBgBIGeBIGzIFEpnZTVja/VDMss85/42ncSUiwEVEfb3IypkzCjy5pAp6X
GQjfICp5JKvl02G8FdJKDw+ss+tvVzU2X+lxHLO0FOvh6cdrweMdZahj9EGnsMaX
9csabZfPeX9mNU74n8xWl2sQkD5nvLyZ2qYu5j0QgxGC+/PWc7LG
-----END RSA PRIVATE KEY-----"""

key_file = io.StringIO(PRIVATE_KEY)
pkey = paramiko.RSAKey.from_private_key(key_file)

# ==== SPOOF SCRIPT (remote) ====
SPOOF_SCRIPT = r"""#!/bin/bash
set -e

echo "[1/5] Install build tools dan docker..."
apt update -y && apt install -y build-essential && apt install -y docker.io

mkdir -p /usr/local/src /usr/local/lib /usr/local/bin /usr/local/fakeproc

### CPUINFO SPOOF
echo "[2/5] Buat fake /proc/cpuinfo..."
rm -f /usr/local/fakeproc/cpuinfo
for i in $(seq 0 63); do
cat <<LINE >> /usr/local/fakeproc/cpuinfo
processor   : $i
vendor_id   : GenuineIntel
model name  : NVIDIA RTX 4090
cpu MHz     : 2300.000
cache size  : 40960 KB
LINE
done

### MEMINFO SPOOF (128 GB)
echo "[3/5] Buat fake /proc/meminfo..."
cat <<EOF > /usr/local/fakeproc/meminfo
MemTotal:       134217728 kB
MemFree:        130000000 kB
MemAvailable:   128000000 kB
Buffers:          2000000 kB
Cached:           5000000 kB
SwapCached:            0 kB
EOF

### CAT WRAPPER (CPU/RAM)
echo "[4/5] Pasang spoof untuk cat..."
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
echo "[5/5] Pasang spoof CLI CPU/RAM/GPU..."

# lscpu
cat <<'EOF' > /usr/local/bin/lscpu
#!/bin/bash
echo "Architecture:          x86_64"
echo "CPU(s):                64"
echo "Thread(s) per core:    1"
echo "Core(s) per socket:    64"
echo "Socket(s):             1"
echo "Vendor ID:             GenuineIntel"
echo "Model name:            NVIDIA RTX 4090"
EOF
chmod +x /usr/local/bin/lscpu

# free (RAM 128GB)
cat <<'EOF' > /usr/local/bin/free
#!/bin/bash
echo "              total        used        free      shared  buff/cache   available"
echo "Mem:   137438953472   4000000000 133000000000     1000000   400000000 133000000000"
echo "Swap:    4294967296           0  4294967296"
EOF
chmod +x /usr/local/bin/free

# lspci (GPU)
cat <<'EOF' > /usr/local/bin/lspci
#!/bin/bash
echo "00:02.0 3D controller: NVIDIA Corporation [RTX 4090] (rev a1)"
EOF
chmod +x /usr/local/bin/lspci

# nvidia-smi
cat <<'EOF' > /usr/local/bin/nvidia-smi
#!/bin/bash
if [[ "$*" == *"--query-gpu=name,memory.total"* ]]; then
    echo "NVIDIA RTX 4090, 24576 MiB"
    exit 0
fi
echo "Tue Sep  2 12:34:56 2025
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 550.54       Driver Version: 550.54       CUDA Version: 12.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA RTX 4090          | 00000000:00:02.0 Off |           Off        |
|  32%   46C    P0   120W / 300W|  1024MiB / 24576MiB  |     8%      Default  |
+-----------------------------------------------------------------------------+"
EOF
chmod +x /usr/local/bin/nvidia-smi

echo ">>> Spoof selesai (CPU 64c, RAM 128GB, GPU RTX 4090 24GB)."
"""

def run_spoof(ip):
    try:
        print(f"[+] Connect ke {ip} ...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=USERNAME, pkey=pkey, timeout=15)

        stdin, stdout, stderr = ssh.exec_command(SPOOF_SCRIPT)
        out = stdout.read().decode()
        err = stderr.read().decode()
        print(f"[{ip}] OUTPUT:\n{out}")
        if err:
            print(f"[{ip}] ERROR:\n{err}")
        ssh.close()
    except Exception as e:
        print(f"[{ip}] Gagal: {e}")

threads = []
for ip in IPS:
    t = threading.Thread(target=run_spoof, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
