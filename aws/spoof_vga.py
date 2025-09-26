#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deploy_spoof_strict_auth.py

Hanya satu metode autentikasi yang boleh aktif:
  - USE_INLINE_KEY = True  -> gunakan PRIVATE_KEY (inline paste)
  - USE_PASSWORD    = True  -> gunakan PASSWORD
Kedua boolean tidak boleh True bersamaan.
"""

import paramiko
import threading
import os
import io
import sys

# ==== LIST VPS ====
IPS = [
"54.173.224.57",
"54.82.139.183",
]

USERNAME = "root"

# -----------------------------
# AUTH TOGGLE (pilih salah satu saja)
# -----------------------------
USE_INLINE_KEY = True   # True = gunakan PRIVATE_KEY (inline paste)
USE_PASSWORD = False    # True = gunakan PASSWORD
# -----------------------------

# Jika pakai password, isi di sini:
PASSWORD = "Azura042AA"  # hanya dipakai jika USE_PASSWORD=True

# Jika pakai inline private key, paste seluruh block private key (termasuk header/footer) di sini:
PRIVATE_KEY = r"""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2DJRmWW9NenwFv3BwRNE7uKUXOjbByuC2hVNWAeqo535YU6p
+e81xwsolMrS//l0CT7N/RjogOp7UfQdt9tyo8TPp5LBScvEt8OMj2/3VZsE4aS7
fB6o16DCmP6nbtSEqx6azvXUCQuNldDXILyMvYC8QZyt0xCRlSEIQTZFFZ2jiJBd
Ddr2vf+Rcef3Hgqyv6FL7Q6go7avXhE9VJNKuIXg4LpfOOAb1WFO1m2eklIXhL5f
G1WQkads7qHziBpkUAkXc5idkyn0PYDeCuhUjYpPVfbUxnRqpPtmrW1qxbhLL6bp
dv2TVO/wd/F/OmkKMOD5CazxVfoPFbM/Qg66EwIDAQABAoIBAGwusbpKuKVzzFoU
3JFarRHEe20KcB9kXHP4WN2F6JM7B4DztgaE9qoFIWdjHrZMAw5lSPovLpjjvJXD
y+MmgnUElMxLmUDuIB+8UGeuJVvG2Gh44AA5708G+JlKREonOcPO6rRJOrLT/yNK
f3u4Hczt0EYcurZ1AgRXpSPMnkEz1mcA2zSP2i5WqG4yITIBlXPjNam65O/LowPa
PGYVVu+7tvkjhF+DI+ffjw3aMsPQgsOnKcsgR0s4tp5BtVxzvBrVG/exJCAwTUED
HkgttnrposyILE3CX/hRooVT92DK7nNxZKHORlJJe8rjNqTl6qImzss+HQ0gBFYx
oeYMnIECgYEA/n365y0q01WufBwmoRkGQQwzlWauFSg8mRvfyrBTxhpBFFOsOKZ4
OpC++arXnkL4Ql28ZBq0CDXdUG7BxhU+ps1QL1iZM5MF0VGSGaodgzoJ2NYLzQc3
zeCYRHXFQFB50nhfFuhQdNvRmhUiUP2/WeqzDiaN0IkU/4uZxl1YDKECgYEA2XpA
QsQ7zY1f4Mq4dQpxyJLXAgko3XVyKj8nkCWdw29dBjeihWkVPzeGEQ6ZYmNnNUcn
mHgRINnQf4XSUQdPZOeV/ZkHmLP+v6F5Ja5vDqXLg9Tf1FnP22ZHCj6Zx/e7WN0A
eOZ9d+XUpTIPEjIitKEojhXfATzUMAsTVfRydjMCgYAgholismsex3ydcBufy0r5
VU3iclUdbx8Pknhvt0l9sC1RI8CHHP+QvJ8r2aHlIDoKgWBqit8njXrTpNQvNNfl
CaiN5IzwAoJj1kEN9qf+9ZP8mp63fYysS2Aqn8KuDZsEQ04j510hElcfkkPohgXG
wDBSRqspU9vTLUxiBdwTAQKBgQCkjJZgrj+diLGZ0Wj9zbhIDaq3NJ0B62JFSuGx
dHTJMdLN6HyEuvzDh0xeTZCK3DF0I3F3MKmtFIFoa6W1f3V4IK3hYs9XoCFJd3DF
rRUEnTe+eOwerRHTrLBltPYAUpYjZ5x63dLjTDe4Aodauip+R037K9s/AXp/G3I2
4C1W9wKBgQCoIH74y0A3DBjke1vEgx7mjI6r6taaSrK75Cf2cR8+D8cnAIU1nopQ
gREiSJO/RR9X7kwhVoX/cTniKXhZDMoGIQkv6sGSkDn4k8KU4VM3/y/k0AugEdiv
xr86KVcyPahmKXklFtQr6U0xSAg+zJhDAgerUywHDiSDsc1OBFObow==
-----END RSA PRIVATE KEY-----"""
PRIVATE_KEY_PASSPHRASE = None  # isi jika private key terenkripsi, atau None

# ==== FILE LOKAL / REMOTE ====
LOCAL_FILE = os.path.join(os.getcwd(), "spoof_a5000.c")  # file hasil upload (harus ada di cwd)
REMOTE_FILE = "/root/libnvidia-ml.c"                    # nama file di server

# ==== PERINTAH REMOTE ====
COMMANDS = [
    "apt update -y",
    "apt install -y nvidia-utils-550",
    f"gcc -shared -fPIC -o /usr/local/lib/libnvidia-ml.so.550.120 {REMOTE_FILE}",
    "ln -sf /usr/local/lib/libnvidia-ml.so.550.120 /lib/x86_64-linux-gnu/libnvidia-ml.so.1",
    "nvidia-smi"
]

# -------------------------
# Validasi opsi auth (STRICT: hanya satu aktif)
# -------------------------
if USE_INLINE_KEY and USE_PASSWORD:
    print("[!] Konfigurasi tidak valid: USE_INLINE_KEY dan USE_PASSWORD tidak boleh keduanya True.")
    sys.exit(1)

if not (USE_INLINE_KEY or USE_PASSWORD):
    print("[!] Konfigurasi tidak valid: aktifkan salah satu USE_INLINE_KEY atau USE_PASSWORD.")
    sys.exit(1)

if USE_PASSWORD and not PASSWORD:
    print("[!] USE_PASSWORD=True tetapi PASSWORD kosong. Isi PASSWORD atau set USE_PASSWORD=False.")
    sys.exit(1)

if USE_INLINE_KEY:
    if not PRIVATE_KEY or "<PASTE_YOUR_PRIVATE_KEY_HERE_INCLUDING_HEADERS>" in PRIVATE_KEY:
        print("[!] USE_INLINE_KEY=True tetapi PRIVATE_KEY belum dipaste. Isi variable PRIVATE_KEY.")
        sys.exit(1)

# -------------------------
# Helper: load private key from string
# -------------------------
def load_pkey_from_string(pem_str, passphrase=None):
    last_exc = None
    for KeyClass in (paramiko.RSAKey, paramiko.Ed25519Key, paramiko.ECDSAKey):
        stream = io.StringIO(pem_str)
        try:
            return KeyClass.from_private_key(stream, password=passphrase)
        except Exception as e:
            last_exc = e
    raise RuntimeError(f"Gagal load private key dari string: {last_exc}")

# Load PKEY jika inline key dipilih
PKEY = None
if USE_INLINE_KEY:
    try:
        PKEY = load_pkey_from_string(PRIVATE_KEY, PRIVATE_KEY_PASSPHRASE)
        print("[*] PRIVATE_KEY berhasil di-load dari variabel.")
    except Exception as e:
        print("[!] Gagal load PRIVATE_KEY:", e)
        sys.exit(1)

# -------------------------
# Fungsi utama untuk tiap IP
# -------------------------
def run_commands(ip):
    print(f"\n===== [ {ip} ] =====")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connect_kwargs = {
            "hostname": ip,
            "username": USERNAME,
            "timeout": 15,
        }

        if USE_INLINE_KEY:
            connect_kwargs.update({
                "pkey": PKEY,
                "allow_agent": False,
                "look_for_keys": False
            })
            auth_mode = "inline-key"
        else:
            connect_kwargs.update({
                "password": PASSWORD,
                "allow_agent": False,
                "look_for_keys": False
            })
            auth_mode = "password"

        print(f"[{ip}] Menghubungkan menggunakan: {auth_mode} ...")
        client.connect(**connect_kwargs)

        # Upload file spoof via SFTP
        sftp = client.open_sftp()
        if not os.path.exists(LOCAL_FILE):
            print(f"[{ip}] ERROR: File lokal {LOCAL_FILE} tidak ditemukan. Melewatkan server ini.")
            sftp.close()
            client.close()
            return
        print(f"[{ip}] Upload {LOCAL_FILE} -> {REMOTE_FILE}")
        sftp.put(LOCAL_FILE, REMOTE_FILE)
        try:
            sftp.chmod(REMOTE_FILE, 0o644)
        except Exception:
            pass
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
                print(f"[{ip}] Command gagal (exit {exit_status}) — lanjutkan ke perintah berikutnya")

        client.close()
        print(f"[{ip}] Selesai.")
    except Exception as e:
        print(f"[{ip}] ERROR koneksi / eksekusi: {e}")

# ==== JALANKAN PARALEL ====
def main():
    threads = []
    for ip in IPS:
        t = threading.Thread(target=run_commands, args=(ip,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\n✅ Semua server selesai diproses.")

if __name__ == "__main__":
    main()
