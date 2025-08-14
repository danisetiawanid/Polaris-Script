import paramiko
import threading

# --- KONFIGURASI --- #
USERNAME = "root"
PASSWORD = "Azura042AA"

COMMANDS = [
    "echo '[STEP 1] Install Docker...'",
    "apt install -y docker.io",

    "echo '[STEP 2] Membuat file spoof RAM...'",
    "cat <<EOF > /tmp/meminfo_fake\n"
    "MemTotal:       67108864 kB\n"
    "MemFree:        66000000 kB\n"
    "MemAvailable:   66000000 kB\n"
    "Buffers:               0 kB\n"
    "Cached:                0 kB\n"
    "SwapCached:            0 kB\n"
    "SwapTotal:      8388608 kB\n"
    "SwapFree:       8388608 kB\n"
    "EOF",

    "echo '[STEP 3] Membuat script /root/ramspoof.sh...'",
    "cat <<EOF > /root/ramspoof.sh\n"
    "#!/bin/bash\n"
    "mount --bind /tmp/meminfo_fake /proc/meminfo\n"
    "EOF",
    "chmod +x /root/ramspoof.sh",

    "echo '[STEP 4] Membuat systemd service...'",
    "cat <<EOF > /etc/systemd/system/ramspoof.service\n"
    "[Unit]\n"
    "Description=Spoof RAM via /proc/meminfo\n"
    "DefaultDependencies=no\n"
    "Before=sysinit.target\n"
    "After=local-fs.target\n\n"
    "[Service]\n"
    "Type=oneshot\n"
    "ExecStart=/bin/bash /root/ramspoof.sh\n"
    "RemainAfterExit=yes\n\n"
    "[Install]\n"
    "WantedBy=sysinit.target\n"
    "EOF",

    "echo '[STEP 5] Enable dan Start Service...'",
    "systemctl daemon-reexec",
    "systemctl daemon-reload",
    "systemctl enable ramspoof",
    "systemctl start ramspoof",

    "echo '[STEP 6] Cek Hasil RAM Spoof...'",
    "head -n 3 /proc/meminfo",
    "free -h"
]

MAX_THREADS = 10

# Ganti dengan IP VPS kamu
SERVER_LIST = [
    "157.230.130.25"
]

print_lock = threading.Lock()

def run_commands(ip):
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
                    print(f"[{ip}] 📥 Output:\n{output.strip()}")
                if error.strip():
                    print(f"[{ip}] ❗ Error:\n{error.strip()}")

        ssh.close()
        with print_lock:
            print(f"[{ip}] ✅ Semua perintah selesai")

    except Exception as e:
        with print_lock:
            print(f"[{ip}] ❌ ERROR: {str(e)}")

def main():
    threads = []
    for ip in SERVER_LIST:
        t = threading.Thread(target=run_commands, args=(ip,))
        threads.append(t)
        t.start()

        while threading.active_count() > MAX_THREADS:
            pass

    for t in threads:
        t.join()

    print("\n🎉 SEMUA VPS SUDAH SELESAI!")

if __name__ == "__main__":
    main()
