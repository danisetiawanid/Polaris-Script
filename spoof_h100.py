import paramiko
import threading
import os

# ==== LIST VPS ====
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
PASSWORD = "Azura042AA"

# ==== FILE LOKAL ====
LOCAL_FILE = os.path.join(os.getcwd(), "spoof_h100.c")  # file hasil upload
REMOTE_FILE = "/root/libnvidia-ml.c"                    # nama file di server

# ==== PERINTAH REMOTE ====
COMMANDS = [
    "apt update -y",
    "apt install -y nvidia-utils-550",
    f"gcc -shared -fPIC -o /usr/local/lib/libnvidia-ml.so.550.120 {REMOTE_FILE}",
    "ln -sf /usr/local/lib/libnvidia-ml.so.550.120 /lib/x86_64-linux-gnu/libnvidia-ml.so.1",
    "nvidia-smi"
]

def run_commands(ip):
    print(f"\n===== [ {ip} ] =====")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=USERNAME, password=PASSWORD, timeout=10)

        # Upload file spoof
        sftp = client.open_sftp()
        if not os.path.exists(LOCAL_FILE):
            print(f"[{ip}] ERROR: File lokal {LOCAL_FILE} tidak ditemukan.")
            return
        print(f"[{ip}] Upload {LOCAL_FILE} -> {REMOTE_FILE}")
        sftp.put(LOCAL_FILE, REMOTE_FILE)
        sftp.close()

        # Jalankan semua perintah
        for cmd in COMMANDS:
            print(f"[{ip}] Jalankan: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if output:
                print(f"[{ip}] OUTPUT:\n{output}")
            if error:
                print(f"[{ip}] ERROR:\n{error}")

            if exit_status != 0:
                print(f"[{ip}] Command gagal (exit {exit_status})")

        client.close()
    except Exception as e:
        print(f"[{ip}] ERROR koneksi: {e}")

# ==== JALANKAN PARALEL ====
threads = []
for ip in IPS:
    t = threading.Thread(target=run_commands, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("\n✅ Semua server selesai diproses.")
