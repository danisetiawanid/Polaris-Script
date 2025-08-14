import paramiko
import threading

# --- CONFIGURASI --- #
USERNAME = "root"
PASSWORD = "Azura042AA"
COMMANDS = [
    "apt install -y docker.io",
    "cat <<'EOF' > /tmp/meminfo_fake\n"
    "MemTotal:       33554432 kB\n"
    "MemFree:        33000000 kB\n"
    "MemAvailable:   33000000 kB\n"
    "Buffers:               0 kB\n"
    "Cached:                0 kB\n"
    "SwapCached:            0 kB\n"
    "SwapTotal:      8388608 kB\n"
    "SwapFree:       8388608 kB\n"
    "EOF",
    "sudo mount --bind /tmp/meminfo_fake /proc/meminfo",
    "cat /proc/meminfo | head -3",
    "free -h"
]
MAX_THREADS = 10

SERVER_LIST = [
    "134.199.197.44"
]

print_lock = threading.Lock()

def install_docker(ip):
    try:
        with print_lock:
            print(f"[{ip}] 🔌 Connecting...")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=USERNAME, password=PASSWORD, timeout=10)

        for cmd in COMMANDS:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()
            error = stderr.read().decode()

            with print_lock:
                print(f"[{ip}] 💻 Command: {cmd}")
                if output.strip():
                    print(f"[{ip}] Output:\n{output.strip()}")
                if error.strip():
                    print(f"[{ip}] ❗ Error:\n{error.strip()}")

        with print_lock:
            print(f"[{ip}] ✅ All commands executed")

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

        while threading.active_count() > MAX_THREADS:
            pass

    for t in threads:
        t.join()

    print("\n🎉 Semua VPS sudah diproses!")

if __name__ == "__main__":
    main()
