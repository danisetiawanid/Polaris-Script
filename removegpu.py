import paramiko
import threading

# ==== EDIT LIST IP DI SINI ====
IPS = [
# "129.212.190.17",
# "129.212.176.211",
"134.199.201.163",
"134.199.194.52",
"134.199.206.254",
"129.212.177.90",
"129.212.180.149",
"134.199.193.190",
"134.199.202.73",

]

USERNAME = "root"
PASSWORD = "Azura042AA"   # ganti sesuai password VPS kamu

# ==== COMMAND UNINSTALL SPOOF ====
REMOVE_SCRIPT = r"""
#!/bin/bash
set -e

echo "[1/4] Remove nvidia-utils-550 & build-essential..."
apt purge -y nvidia-utils-550 build-essential || true
apt autoremove -y || true

echo "[2/4] Remove fake libnvidia-ml.so if exists..."
rm -f /usr/local/lib/libnvidia-ml.so.550.120
rm -f /lib/x86_64-linux-gnu/libnvidia-ml.so.1

echo "[3/4] Clean source file libnvidia-ml.c if exists..."
rm -f ~/libnvidia-ml.c
rm -f /root/libnvidia-ml.c

echo "[4/4] Done. Checking leftover..."
ldconfig -p | grep nvidia || echo "✅ No NVIDIA spoof libs found"
"""

def clean_vps(ip):
    try:
        print(f"\n🔗 Connecting to {ip} ...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=USERNAME, password=PASSWORD, timeout=15)

        stdin, stdout, stderr = ssh.exec_command(REMOVE_SCRIPT)
        print(f"=== {ip} OUTPUT ===")
        for line in stdout:
            print(line.strip())
        for line in stderr:
            print("ERR:", line.strip())

        ssh.close()
        print(f"✅ Finished cleaning {ip}")
    except Exception as e:
        print(f"❌ Failed on {ip}: {e}")

threads = []
for ip in IPS:
    t = threading.Thread(target=clean_vps, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
