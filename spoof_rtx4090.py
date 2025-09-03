import paramiko
import threading

# ==== EDIT LIST IP DI SINI ====
IPS = [
  "146.190.52.203",
"143.198.62.28",
"143.244.184.133",
"64.23.254.145",
"143.198.150.250",


]

USERNAME = "root"
PASSWORD = "Azura042AA"   # ganti sesuai VPS

# ==== SPOOF SCRIPT (dijalankan remote) ====
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
echo "Tes dengan:"
echo "  lscpu"
echo "  free -h"
echo "  lspci"
echo "  nvidia-smi"
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
