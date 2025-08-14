import paramiko
import threading

# --- CONFIGURASI --- #
USERNAME = "root"
PASSWORD = "Azura042AA"

COMMANDS = [
    # 0. Install Docker dan gcc
    "apt update && apt install -y docker.io gcc make",

    # 1. Buat file spoof RAM 128 GB
    "cat << 'EOF' > ~/ramspoof.c\n"
    "#define _GNU_SOURCE\n"
    "#include <sys/sysinfo.h>\n"
    "#include <unistd.h>\n"
    "#include <dlfcn.h>\n"
    "long fake_totalram = 128L * 1024 * 1024 * 1024;\n"
    "int sysinfo(struct sysinfo *info) {\n"
    "    int (*original_sysinfo)(struct sysinfo *);\n"
    "    original_sysinfo = dlsym(RTLD_NEXT, \"sysinfo\");\n"
    "    int result = original_sysinfo(info);\n"
    "    if (result == 0) {\n"
    "        info->totalram = fake_totalram;\n"
    "        info->freeram = fake_totalram - (1024 * 1024 * 512);\n"
    "        info->bufferram = 1024 * 1024 * 128;\n"
    "    }\n"
    "    return result;\n"
    "}\n"
    "long sysconf(int name) {\n"
    "    if (name == _SC_PHYS_PAGES) {\n"
    "        return fake_totalram / getpagesize();\n"
    "    }\n"
    "    if (name == _SC_AVPHYS_PAGES) {\n"
    "        return (fake_totalram - (1024 * 1024 * 512)) / getpagesize();\n"
    "    }\n"
    "    long (*original_sysconf)(int);\n"
    "    original_sysconf = dlsym(RTLD_NEXT, \"sysconf\");\n"
    "    return original_sysconf(name);\n"
    "}\n"
    "EOF",

    # 2. Compile jadi .so
    "gcc -shared -fPIC -o /usr/local/lib/libfake128.so ~/ramspoof.c -ldl",

    # 3. Pasang agar spoof aktif otomatis setiap shell
    "echo 'export LD_PRELOAD=/usr/local/lib/libfake128.so' >> ~/.bashrc",
    "echo 'export LD_PRELOAD=/usr/local/lib/libfake128.so' >> ~/.profile",

    # 4. Test RAM output
    "LD_PRELOAD=/usr/local/lib/libfake128.so free -h"
]

# Maksimum jumlah koneksi paralel
MAX_THREADS = 10

# Daftar IP VPS target
SERVER_LIST = [
    "YOUR.VPS.IP.ADDRESS"  # ganti dengan IP kamu
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
            with print_lock:
                print(f"[{ip}] ▶️ Running: {cmd[:60]}...")
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
            print(f"[{ip}] ✅ DONE.")

    except Exception as e:
        with print_lock:
            print(f"[{ip}] ❌ ERROR: {e}")

# Jalankan multi-threaded deployment
threads = []
for ip in SERVER_LIST:
    t = threading.Thread(target=run_commands, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
