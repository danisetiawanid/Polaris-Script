import paramiko
import threading

# ==== EDIT LIST IP DI SINI ====
IPS = [
"104.131.190.76",
"162.243.185.14"
]

USERNAME = "root"
PASSWORD = "Azura042AA"   # ganti sesuai VPS

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

echo ">>> Selesai (AMD EPYC 7642, 48 Core @2.3GHz, RAM 48GB)."
echo "Tes dengan:"
echo "  lscpu"
echo "  free -h"
echo "  cat /proc/cpuinfo | head"
echo "  cat /proc/meminfo | head"
"""

def run_cuy(ip):
    try:
        print(f"[+] Connect ke {ip} ...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=USERNAME, password=PASSWORD, timeout=15)

        stdin, stdout, stderr = ssh.exec_command(SCRIPT)
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
    t = threading.Thread(target=run_cuy, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
