import paramiko
import threading

# --- KONFIGURASI --- #
USERNAME = "root"
PASSWORD = "Azura042AA"

COMMANDS = [
    ("Install Docker dan GCC", "apt update && apt install -y docker.io gcc make"),
    ("Buat file spoof RAM 128 GB", """cat << 'EOF' > ~/ramspoof.c
#define _GNU_SOURCE
#include <sys/sysinfo.h>
#include <unistd.h>
#include <dlfcn.h>
long fake_totalram = 128L * 1024 * 1024 * 1024;
int sysinfo(struct sysinfo *info) {
    int (*original_sysinfo)(struct sysinfo *);
    original_sysinfo = dlsym(RTLD_NEXT, "sysinfo");
    int result = original_sysinfo(info);
    if (result == 0) {
        info->totalram = fake_totalram;
        info->freeram = fake_totalram - (1024 * 1024 * 512);
        info->bufferram = 1024 * 1024 * 128;
    }
    return result;
}
long sysconf(int name) {
    if (name == _SC_PHYS_PAGES) {
        return fake_totalram / getpagesize();
    }
    if (name == _SC_AVPHYS_PAGES) {
        return (fake_totalram - (1024 * 1024 * 512)) / getpagesize();
    }
    long (*original_sysconf)(int);
    original_sysconf = dlsym(RTLD_NEXT, "sysconf");
    return original_sysconf(name);
}
EOF"""),
    ("Compile libfake128.so", "gcc -shared -fPIC -o /usr/local/lib/libfake128.so ~/ramspoof.c -ldl"),
    ("Pasang spoof ke bashrc", "echo 'export LD_PRELOAD=/usr/local/lib/libfake128.so' >> ~/.bashrc"),
    ("Pasang spoof ke profile", "echo 'export LD_PRELOAD=/usr/local/lib/libfake128.so' >> ~/.profile"),
    ("Cek hasil spoof RAM", "LD_PRELOAD=/usr/local/lib/libfake128.so free -h")
]

SERVER_LIST = [
    "YOUR.VPS.IP.ADDRESS"  # Ganti dengan IP VPS kamu
]

MAX_THREADS = 10
print_lock = threading.Lock()

def run_commands(ip):
    try:
        with print_lock:
            print(f"\n[{ip}] 🔌 Connecting...")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=USERNAME, password=PASSWORD, timeout=10)

        for idx, (desc, cmd) in enumerate(COMMANDS, start=1):
            with print_lock:
                print(f"\n[{ip}] ▶️ STEP {idx}: {desc}")
                print(f"[{ip}] 💻 Command: {cmd.splitlines()[0]}{' ...' if len(cmd.splitlines()) > 1 else ''}")

            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()
            error = stderr.read().decode()

            with print_lock:
                if output.strip():
                    print(f"[{ip}] 📤 Output:\n{output.strip()}")
                if error.strip():
                    print(f"[{ip}] ⚠️ Error:\n{error.strip()}")

        ssh.close()
        with print_lock:
            print(f"\n[{ip}] ✅ ALL STEPS DONE.")

    except Exception as e:
        with print_lock:
            print(f"\n[{ip}] ❌ ERROR: {e}")

# Multi-threaded deploy
threads = []
for ip in SERVER_LIST:
    t = threading.Thread(target=run_commands, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
