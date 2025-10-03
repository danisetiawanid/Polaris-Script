import paramiko
import threading
import sys
import io
import tempfile
import os

# ==== EDIT LIST IP DI SINI ====
IPS = [
   "134.199.203.144",
"64.225.117.62",
]

USERNAME = "root"
PASSWORD = "Azura042AA"   # ganti sesuai password VPS kamu

# Set True untuk pakai SSH key (paste ke PRIVATE_KEY), False untuk pakai password
USE_SSH_KEY = False

# Paste private key di bawah ini (termasuk -----BEGIN ...----- sampai -----END ...-----)
# Jika tidak ingin menggunakan key, biarkan string kosong ""
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

# Jika private key punya passphrase, tulis di sini. Jika tidak, biarkan None
PRIVATE_KEY_PASSPHRASE = None

# ==== SCRIPT CLEANUP (persis seperti yang kamu tulis) ====
CLEANUP_SCRIPT = r"""#!/bin/bash
set -e

echo "[1/3] Hapus file fakeproc..."
rm -rf /usr/local/fakeproc

echo "[2/3] Hapus wrapper palsu..."
rm -f /usr/local/bin/cat
rm -f /usr/local/bin/lscpu
rm -f /usr/local/bin/free
rm -f /usr/local/bin/lsblk

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

def try_load_private_key(key_str, passphrase):
    """
    Coba load private key dari string menjadi PKey object.
    Mengembalikan tuple (pkey_obj, tmp_filename).
    - Jika pkey_obj bukan None: gunakan pkey langsung (Paramiko PKey)
    - Jika tmp_filename bukan None: gunakan key_filename=tmp_filename sebagai fallback
    - Jika keduanya None: gagal
    """
    if not key_str or key_str.strip() == "":
        return None, None

    key_io = io.StringIO(key_str)

    # Coba RSA
    try:
        key_io.seek(0)
        pkey = paramiko.RSAKey.from_private_key(key_io, password=passphrase)
        return pkey, None
    except Exception:
        pass

    # Coba Ed25519 (jika tersedia)
    try:
        key_io.seek(0)
        if hasattr(paramiko, "Ed25519Key"):
            pkey = paramiko.Ed25519Key.from_private_key(key_io, password=passphrase)
            return pkey, None
    except Exception:
        pass

    # Coba ECDSA
    try:
        key_io.seek(0)
        pkey = paramiko.ECDSAKey.from_private_key(key_io, password=passphrase)
        return pkey, None
    except Exception:
        pass

    # Coba DSS (DSA)
    try:
        key_io.seek(0)
        pkey = paramiko.DSSKey.from_private_key(key_io, password=passphrase)
        return pkey, None
    except Exception:
        pass

    # Fallback: tulis file sementara (berguna untuk unencrypted OpenSSH keys)
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, prefix="tmp_sshkey_", mode="w")
        tmp.write(key_str)
        tmp.flush()
        tmp.close()
        os.chmod(tmp.name, 0o600)
        return None, tmp.name
    except Exception:
        return None, None

def cleanup_host(ip):
    tmp_keyfile = None
    ssh = None
    try:
        print(f"[+] Connect ke {ip} ...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connect_kwargs = dict(hostname=ip, username=USERNAME, timeout=20)

        if USE_SSH_KEY and PRIVATE_KEY and PRIVATE_KEY.strip() != "":
            pkey_obj, tmpfile = try_load_private_key(PRIVATE_KEY, PRIVATE_KEY_PASSPHRASE)
            if pkey_obj:
                connect_kwargs['pkey'] = pkey_obj
                print(f"[{ip}] Menggunakan PKey object untuk autentikasi.")
            elif tmpfile:
                tmp_keyfile = tmpfile
                connect_kwargs['key_filename'] = tmp_keyfile
                print(f"[{ip}] Menggunakan key file sementara: {tmp_keyfile}")
            else:
                print(f"[{ip}] ⚠️ Gagal memuat private key. Akan coba pakai password jika tersedia.")
                if PASSWORD:
                    connect_kwargs['password'] = PASSWORD
        else:
            connect_kwargs['password'] = PASSWORD

        # Jangan mencoba agent/key lain dari environment
        connect_kwargs['allow_agent'] = False
        connect_kwargs['look_for_keys'] = False

        ssh.connect(**connect_kwargs)

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
        print(f"[{ip}] Selesai.")
    except Exception as e:
        print(f"[{ip}] Gagal: {e}", file=sys.stderr)
        try:
            if ssh:
                ssh.close()
        except Exception:
            pass
    finally:
        # Hapus file sementara kalau dibuat
        if tmp_keyfile and os.path.exists(tmp_keyfile):
            try:
                os.remove(tmp_keyfile)
            except Exception:
                pass

threads = []
for ip in IPS:
    t = threading.Thread(target=cleanup_host, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("\nSemua host selesai diproses.")
