import paramiko
import threading
import os
from io import StringIO

# ==== LIST VPS ====
IPS = [
    "107.20.107.57"
]

USERNAME = "root"

# ==== SSH KEY DUMMY ====
PRIVATE_KEY_STR = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAqH63bq/6gDbhBcSQYskMB5FvL5gFThpN9aTrfAlCEHsHAqtE
ISifbBxEeHPILHGwkpQmrmktAL55sWOsSvjKFeInuutuP9FFVpI818QDtqo/EIbz
KZJzw/IL0MzX5lHOvNjPyb6NqFc+EyBxTHGVXaqrpIKHziuPNU50WSZXcthuRR8S
uN03KAd6UGM47G7hAsz7ZT9h8lC4+W4BNJ9Jj5H0hrScw4yw79LmVtld5PFhcYYd
4mkrm/Xz3Wv1KhXyOzELpMZBa5T+RC0M7SMzhruXFgGXZqV2YZOdlEIMKRYPhj90
3bLOULSRDl8GIzKV/X376AMjtDvs/CMn+I4WPwIDAQABAoIBAApCHLzabe/cZ3rI
atn4z4iubAyDvt7wbwqjjcqxbZo/Q0AAWVeDd6FHX0vOEMPT8CIcbvZzZNAEyLfq
D5VI7FTEvhJ9PusXvJb2tEmWn3tBhjFlZeyEBBRL6jg+IG7fUCzjLlNkDI/RL/BO
K1eyGpvnRifv4oDE2iUur5q14OEW/t4EKcdbOqlzHn0Hobit9hUh3OCQUWPL2W9H
PxM3d+PbELCG8xv7VTU2x6QIIaS6Kj1nOilzerh0LXT6Mld2mhMFEg8lbi/MtGtf
ghrTYsfdlI7piNJgKCs2dPjpJ/uunheeD58TaF4nTmTaDf09cXcGRGgxP0y8YcSb
XKhJdMECgYEA2f7KVZXaGurI9jVO3KKE2dm0367yWCMHujQZPejwmSQAZYsWJ+Mv
gckK6/6fHsE1xWVw+2VyqssyUUBnmThoSzVzKDVrRiBnwrjfXP2gzpAbXwdso4kn
nJuHanQguxUkbg1y/Zh31hBLErgMhX2249KS44VqkJnWZ7+uDa/yvi8CgYEAxd61
wzLb+KacEN04oIkRgHtZ76uzsqwsjqymWivS7tPVBTFHvCm8MY3zrjLFwI9oArtG
TzqEB69X2flNSgA/Ec9CoZeuTftNz+DFDyDRNWeGZjiJa7j8Vw4fsU4wZrXYn2dW
VM65ZsOTrQksNX7lIWRLgCrMcuVKzCJV98mwtPECgYAiW3bWQFTssx5TN5mjSnX3
w8kvC+qkG3lHTpi/2iu5ZyQs3Nv0E2lUYjQ3d5zqgvcPkmpZJOcKphXbGnR5gJtn
ZxgsOSccGVVhKjQB+vNSOwIlWw0zRRWaKCUSkRTrh2yDb9k0wMf6U/0RCTLoAyVF
CNYfx9JA0g4psdsjyxxN/wKBgBEf/Usvk6opgUhUXRpHwqQECPydN6g3DoQqnRsg
v9i7rKwOX88BLbB8QKLK8iKARtg1rRgeUF755fiPgwjsjIjWD0Y9AnDtVwauxV9R
z8l3dEJUklAoam5+Ym/N/JJnGqBxKR+d5J3oP1eye4kFun7xVzd4fMlU3uxb7GTN
p+WBAoGAJlcWiDOiMEF34Q+aTO3dvgRBrC9QGOombrgmV5zqadZUWc0hQOthhZg+
FezY9pB1WMljOjyj6F9NsKel+8EfQPJ9g5MKx+aZQXYDeflpzkHfpbz57kk3fZ9k
DaoYaPw0h0mh/avE3HsiHeqbTSZYNsu0RydVVaqld3LaOhVR1ZY=
-----END RSA PRIVATE KEY-----"""

# load key dari string
pkey = paramiko.RSAKey.from_private_key(StringIO(PRIVATE_KEY_STR))

# ==== FILE LOKAL SPOOF ====
LOCAL_FILE = os.path.join(os.getcwd(), "spoof_4060.c")
REMOTE_FILE = "/root/libnvidia-ml.c"

# ==== COMMANDS ====
COMMANDS = [
    "apt update -y",
    "apt install -y build-essential docker.io nvidia-utils-550",
    f"gcc -shared -fPIC -o /usr/local/lib/libnvidia-ml.so.550.120 {REMOTE_FILE}",
    "ln -sf /usr/local/lib/libnvidia-ml.so.550.120 /lib/x86_64-linux-gnu/libnvidia-ml.so.1",
    "nvidia-smi"
]

def run_commands(ip):
    print(f"\n===== [ {ip} ] =====")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=USERNAME, pkey=pkey, timeout=10)

        # upload spoof file
        sftp = client.open_sftp()
        if not os.path.exists(LOCAL_FILE):
            print(f"[{ip}] ERROR: File {LOCAL_FILE} tidak ditemukan di lokal.")
            return
        print(f"[{ip}] Upload {LOCAL_FILE} -> {REMOTE_FILE}")
        sftp.put(LOCAL_FILE, REMOTE_FILE)
        sftp.close()

        # jalankan commands
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
                print(f"[{ip}] Command gagal (exit {exit_status})")

        client.close()
    except Exception as e:
        print(f"[{ip}] ERROR koneksi: {e}")

# ==== JALANKAN PARALEL ====
threads = []
for ip in IPS:
    t = threading.Thread(target=run_commands, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("\n✅ Semua server selesai diproses dengan SSH key.")
