import paramiko
import threading
import sys

# ==== EDIT LIST IP DI SINI ====
IPS = [
"143.198.237.246",
"24.199.102.1",
"147.182.206.186",
"64.23.172.7",
"64.23.229.16",
"147.182.245.240",
"146.190.117.74",
"24.144.88.28",
"134.199.221.222",
"146.190.161.111",

]

USERNAME = "root"
PASSWORD = "Azura042AA"   # ganti sesuai VPS
# (Alternatif SSH key –> lihat catatan di bawah)

# ==== SCRIPT CLEANUP (persis seperti yang kamu tulis) ====
CLEANUP_SCRIPT = r"""#!/bin/bash
set -e

echo "[1/3] Hapus file fakeproc..."
rm -rf /usr/local/fakeproc

echo "[2/3] Hapus wrapper palsu..."
rm -f /usr/local/bin/cat
rm -f /usr/local/bin/lscpu
rm -f /usr/local/bin/free

echo "[3/3] Pastikan pakai binary asli..."
hash -r   # reset hash shell agar ambil /bin/cat, /usr/bin/lscpu, /usr/bin/free

echo ">>> Spoof sudah dihapus. Coba cek ulang:"
echo "  which cat"
echo "  which lscpu"
echo "  which free"
echo "  cat /proc/cpuinfo | head"
"""

# ==== (Opsional) VERIFIKASI OTOMATIS ====
VERIFY_CMD = r"""#!/bin/bash
set -e
echo "--- Verifikasi path binary ---"
echo -n "cat   -> "; which cat || true
echo -n "lscpu -> "; which lscpu || true
echo -n "free  -> "; which free || true
echo "--- cpuinfo (head) ---"
(head -n 20 /proc/cpuinfo || true) | sed 's/\t/  /g'
echo "--- meminfo (head) ---"
(head -n 20 /proc/meminfo || true)
"""

def cleanup_host(ip):
    try:
        print(f"[+] Connect ke {ip} ...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # --- Pakai password ---
        ssh.connect(ip, username=USERNAME, password=PASSWORD, timeout=20)
        # --- Kalau mau pakai SSH key, lihat catatan di bawah ---

        # Jalankan cleanup
        print(f"[{ip}] Jalankan cleanup...")
        stdin, stdout, stderr = ssh.exec_command(CLEANUP_SCRIPT)
        out = stdout.read().decode(errors="replace")
        err = stderr.read().decode(errors="replace")
        print(f"\n===== [{ip}] CLEANUP OUTPUT =====\n{out}")
        if err.strip():
            print(f"===== [{ip}] CLEANUP STDERR =====\n{err}")

        # Jalankan verifikasi otomatis
        print(f"[{ip}] Verifikasi otomatis...")
        stdin2, stdout2, stderr2 = ssh.exec_command(VERIFY_CMD)
        out2 = stdout2.read().decode(errors="replace")
        err2 = stderr2.read().decode(errors="replace")
        print(f"\n===== [{ip}] VERIFY OUTPUT =====\n{out2}")
        if err2.strip():
            print(f"===== [{ip}] VERIFY STDERR =====\n{err2}")

        ssh.close()
    except Exception as e:
        print(f"[{ip}] Gagal: {e}", file=sys.stderr)

threads = []
for ip in IPS:
    t = threading.Thread(target=cleanup_host, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("\nSemua host selesai diproses.")
