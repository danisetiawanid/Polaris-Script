import paramiko
import threading
import os
from io import StringIO

# ==== LIST VPS (IP target) ====
IPS = [
    "107.20.107.57"
]

# ==== USERNAME awal (sebelum root aktif) ====
USERNAME_INIT = "ubuntu"
USERNAME_ROOT = "root"

# ==== SSH KEY DUMMY ====
PRIVATE_KEY_STR = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAqH63bq/6gDbhBcSQYskMB5FvL5gFThpN9aTrfAlCEHsHAqtE
...
-----END RSA PRIVATE KEY-----"""

pkey = paramiko.RSAKey.from_private_key(StringIO(PRIVATE_KEY_STR))

# ==== FILE SPOOF ====
LOCAL_FILE = os.path.join(os.getcwd(), "spoof_4060.c")
REMOTE_FILE = "/root/libnvidia-ml.c"

# ==== STEP 1: enable root login ====
COMMANDS_ROOT_ENABLE = [
    "sudo mkdir -p /root/.ssh",
    "sudo chmod 700 /root/.ssh",
    "sudo cp /home/ubuntu/.ssh/authorized_keys /root/.ssh/",
    "sudo chmod 600 /root/.ssh/authorized_keys",
    "sudo chown root:root /root/.ssh/authorized_keys",
    "if ! grep -q '^PermitRootLogin yes' /etc/ssh/sshd_config; then echo 'PermitRootLogin yes' | sudo tee -a /etc/ssh/sshd_config; fi",
    "sudo systemctl restart ssh"
]

# ==== STEP 2: spoof deploy ====
COMMANDS_SPOOF = [
    "apt update -y",
    "apt install -y build-essential docker.io nvidia-utils-550",
    f"gcc -shared -fPIC -o /usr/local/lib/libnvidia-ml.so.550.120 {REMOTE_FILE}",
    "ln -sf /usr/local/lib/libnvidia-ml.so.550.120 /lib/x86_64-linux-gnu/libnvidia-ml.so.1",
    "nvidia-smi"
]


def run_all(ip):
    print(f"\n===== [ {ip} ] =====")

    # 1. Koneksi awal dengan user ubuntu
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"[{ip}] Login sebagai {USERNAME_INIT}...")
        client.connect(ip, username=USERNAME_INIT, pkey=pkey, timeout=15)

        # enable root login
        for cmd in COMMANDS_ROOT_ENABLE:
            print(f"[{ip}] Jalankan: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            stdout.channel.recv_exit_status()
        client.close()
        print(f"[{ip}] ✅ Root login enabled")

    except Exception as e:
        print(f"[{ip}] ERROR step root enable: {e}")
        return

    # 2. Reconnect pakai root
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"[{ip}] Reconnect sebagai {USERNAME_ROOT}...")
        client.connect(ip, username=USERNAME_ROOT, pkey=pkey, timeout=15)

        # upload spoof file
        sftp = client.open_sftp()
        if not os.path.exists(LOCAL_FILE):
            print(f"[{ip}] ERROR: File {LOCAL_FILE} tidak ditemukan di lokal.")
            return
        print(f"[{ip}] Upload {LOCAL_FILE} -> {REMOTE_FILE}")
        sftp.put(LOCAL_FILE, REMOTE_FILE)
        sftp.close()

        # jalankan spoof commands
        for cmd in COMMANDS_SPOOF:
            print(f"[{ip}] Jalankan: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            if out:
                print(f"[{ip}] OUTPUT:\n{out}")
            if err:
                print(f"[{ip}] ERROR:\n{err}")
            if exit_status != 0:
                print(f"[{ip}] Command gagal (exit {exit_status})")

        client.close()
        print(f"[{ip}] ✅ Spoof selesai")

    except Exception as e:
        print(f"[{ip}] ERROR step spoof deploy: {e}")


# ==== MAIN ====
threads = []
for ip in IPS:
    t = threading.Thread(target=run_all, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("\n🎉 Semua server selesai diproses (root enable + spoof deploy).")
