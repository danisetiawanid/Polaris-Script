import paramiko
import threading

# ==== EDIT LIST IP DI SINI ====
IPS = [
"146.190.175.35",
"134.199.227.178"
]

USERNAME = "root"
PASSWORD = "Azura042AA"   # ganti sesuai VPS

# ==== SPOOF SCRIPT (dijalankan remote) ====
SPOOF_SCRIPT = r"""#!/bin/bash
set -e

echo "[1/3] Install build tools..."
apt update -y && apt install -y build-essential && apt install -y docker.io

mkdir -p /usr/local/src /usr/local/lib /usr/local/bin /usr/local/fakeproc

### CPUINFO SPOOF (14 core)
echo "[2/3] Buat fake /proc/cpuinfo..."
rm -f /usr/local/fakeproc/cpuinfo
for i in $(seq 0 13); do
cat <<LINE >> /usr/local/fakeproc/cpuinfo
processor   : $i
vendor_id   : GenuineIntel
model name  : Intel(R) Core(TM) i5-14600K CPU @ 3.50GHz
cpu MHz     : 3500.000
cache size  : 24576 KB
LINE
done

### MEMINFO SPOOF (32 GB)
echo "[3/3] Buat fake /proc/meminfo..."
cat <<EOF > /usr/local/fakeproc/meminfo
MemTotal:       33554432 kB
MemFree:        32000000 kB
MemAvailable:   32000000 kB
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
echo "CPU(s):                14"
echo "Thread(s) per core:    1"
echo "Core(s) per socket:    14"
echo "Socket(s):             1"
echo "Vendor ID:             GenuineIntel"
echo "Model name:            Intel(R) Core(TM) i5-14600K CPU @ 3.50GHz"
EOF
chmod +x /usr/local/bin/lscpu

# free (RAM 32GB)
cat <<'EOF' > /usr/local/bin/free
#!/bin/bash
echo "              total        used        free      shared  buff/cache   available"
echo "Mem:    34359738368   2000000000 32000000000     500000   200000000 32000000000"
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

echo ">>> Spoof selesai (CPU 14c Intel i5-14600K, RAM 32GB)."
echo "Tes dengan:"
echo "  lscpu"
echo "  free -h"
echo "  cat /proc/cpuinfo | head"
echo "  cat /proc/meminfo | head"
"""

def run_spoof(ip):
    try:
        print(f"[+] Connect ke {ip} ...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=USERNAME, password=PASSWORD, timeout=15)

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
