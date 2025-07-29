import paramiko
import threading

# --- CONFIGURASI --- #
USERNAME = "root"
PASSWORD = "Azura042AA"  # Ganti sesuai password VPS
COMMAND = "apt install -y docker.io"
MAX_THREADS = 10

# Ganti ini dengan daftar IP kamu
SERVER_LIST = [
    "164.92.104.24",
    "159.223.196.223",
    "143.198.67.108",
    "143.198.140.58",
    "146.190.157.159",
    "146.190.132.29",
    "146.190.140.135",
    "146.190.151.75",
    "24.199.97.85",
    "164.92.74.46"
]

print_lock = threading.Lock()  # Untuk mencegah print tumpang tindih

def install_docker(ip):
    try:
        with print_lock:
            print(f"[{ip}] 🔌 Connecting...")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=USERNAME, password=PASSWORD, timeout=10)

        stdin, stdout, stderr = ssh.exec_command(COMMAND)
        output = stdout.read().decode()
        error = stderr.read().decode()

        with print_lock:
            print(f"[{ip}] ✅ INSTALL DONE")

            if output.strip():
                print(f"[{ip}] Output:\n{output.strip()}")
            if error.strip():
                print(f"[{ip}] ❗ Error:\n{error.strip()}")

        ssh.close()

    except Exception as e:
        with print_lock:
            print(f"[{ip}] ❌ FAILED: {str(e)}")

def main():
    threads = []
    for ip in SERVER_LIST:
        t = threading.Thread(target=install_docker, args=(ip,))
        threads.append(t)
        t.start()

        # Batasi jumlah thread aktif
        while threading.active_count() > MAX_THREADS:
            pass

    for t in threads:
        t.join()

    print("\n🎉 Semua VPS sudah diproses!")

if __name__ == "__main__":
    main()
