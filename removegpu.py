import paramiko
import threading
import io
import tempfile
import os
import stat

# ==== EDIT LIST IP DI SINI ====
IPS = [
    "54.173.224.57",
    "54.82.139.183"
]

USERNAME = "root"
PASSWORD = "Azura042AA"   # ganti sesuai password VPS kamu

# Set True untuk pakai SSH key (paste di PRIVATE_KEY), False untuk pakai password
USE_SSH_KEY = True

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

# ==== COMMAND UNINSTALL SPOOF ====
REMOVE_SCRIPT = r"""
#!/bin/bash
set -e

echo "[1/4] Remove nvidia-utils-550 & build-essential..."
apt purge -y nvidia-utils-550 build-essential || true
apt autoremove -y || true

echo "[2/4] Remove fake libnvidia-ml.so if exists..."
rm -f /usr/local/lib/libnvidia-ml.so.550.120
rm -f /lib/x86_64-linux-gnu/libnvidia-ml.so.1

echo "[3/4] Clean source file libnvidia-ml.c if exists..."
rm -f ~/libnvidia-ml.c
rm -f /root/libnvidia-ml.c

echo "[4/4] Done. Checking leftover..."
ldconfig -p | grep nvidia || echo "✅ No NVIDIA spoof libs found"
"""

def try_load_private_key(key_str, passphrase):
    """
    Coba load private key dari string menjadi PKey object.
    Mengembalikan (pkey_obj, None) jika berhasil,
    atau (None, tmp_filename) jika harus fallback menulis file sementara (untuk unencrypted keys).
    """
    if not key_str or key_str.strip() == "":
        return None, None

    key_io = io.StringIO(key_str)
    # Coba beberapa kelas kunci yang umum
    load_attempts = []
    # Try RSAKey
    try:
        pkey = paramiko.RSAKey.from_private_key(key_io, password=passphrase)
        return pkey, None
    except Exception as e:
        load_attempts.append(("RSAKey", str(e)))
        key_io.seek(0)
    # Try Ed25519Key (paramiko >= 2.9)
    try:
        if hasattr(paramiko, "Ed25519Key"):
            pkey = paramiko.Ed25519Key.from_private_key(key_io, password=passphrase)
            return pkey, None
    except Exception as e:
        load_attempts.append(("Ed25519Key", str(e)))
        key_io.seek(0)
    # Try ECDSAKey
    try:
        pkey = paramiko.ECDSAKey.from_private_key(key_io, password=passphrase)
        return pkey, None
    except Exception as e:
        load_attempts.append(("ECDSAKey", str(e)))
        key_io.seek(0)
    # Try DSAKey
    try:
        pkey = paramiko.DSSKey.from_private_key(key_io, password=passphrase)
        return pkey, None
    except Exception as e:
        load_attempts.append(("DSSKey", str(e)))
        key_io.seek(0)

    # Kalau semua gagal, mungkin key tidak terenkripsi tapi Paramiko gagal parsing from_string.
    # Fallback: tulis file sementara dan gunakan key_filename (berguna untuk unencrypted OpenSSH keys).
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, prefix="tmp_sshkey_", mode="w")
        tmp.write(key_str)
        tmp.flush()
        tmp.close()
        os.chmod(tmp.name, 0o600)
        return None, tmp.name
    except Exception as e:
        load_attempts.append(("file_write", str(e)))
        # Jika tetap gagal, kembalikan None
        return None, None

def clean_vps(ip):
    tmp_keyfile = None
    try:
        print(f"\n🔗 Connecting to {ip} ...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connect_kwargs = dict(hostname=ip, username=USERNAME, timeout=15)

        if USE_SSH_KEY and PRIVATE_KEY and PRIVATE_KEY.strip() != "":
            pkey_obj, tmpfile = try_load_private_key(PRIVATE_KEY, PRIVATE_KEY_PASSPHRASE)
            if pkey_obj:
                connect_kwargs['pkey'] = pkey_obj
            elif tmpfile:
                # fallback ke file-based key (tidak mendukung passphrase di sini)
                tmp_keyfile = tmpfile
                connect_kwargs['key_filename'] = tmp_keyfile
                # Jika key terenkripsi dan paramiko tidak mem-parse, koneksi kemungkinan gagal.
            else:
                print(f"⚠️ Could not load private key for {ip}. Falling back to password (if available).")
                # biarkan pake password jika ada
                if PASSWORD:
                    connect_kwargs['password'] = PASSWORD
        else:
            # pakai password
            connect_kwargs['password'] = PASSWORD

        # Disable look_for_keys/agent agar tidak mencoba agent lokal (opsional)
        connect_kwargs['allow_agent'] = False
        connect_kwargs['look_for_keys'] = False

        ssh.connect(**connect_kwargs)

        stdin, stdout, stderr = ssh.exec_command(REMOVE_SCRIPT)
        print(f"=== {ip} OUTPUT ===")
        for line in stdout:
            print(line.strip())
        for line in stderr:
            print("ERR:", line.strip())

        ssh.close()
        print(f"✅ Finished cleaning {ip}")

    except Exception as e:
        print(f"❌ Failed on {ip}: {e}")
    finally:
        # hapus file sementara kalau dibuat
        if tmp_keyfile and os.path.exists(tmp_keyfile):
            try:
                os.remove(tmp_keyfile)
            except Exception:
                pass

threads = []
for ip in IPS:
    t = threading.Thread(target=clean_vps, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
