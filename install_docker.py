import paramiko
import threading

# --- CONFIGURASI --- #
USERNAME = "root"
PASSWORD = "Azura042AA"  # Ganti sesuai password VPS
COMMAND = "apt install -y docker.io"
SERVER_FILE = "servers.txt"
MAX_THREADS = 10

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
    with open(SERVER_FILE, 'r') as f:
        ips = [line.strip() for line in f if line.strip()]

    threads = []
    for ip in ips:
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
