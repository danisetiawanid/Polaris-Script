import paramiko
import io

# ==== List IP Target ====
IPS = [
"107.20.107.57"
]

USERNAME = "ubuntu"

# ==== Private Key Dummy (tempel langsung di sini) ====
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
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

# Buat object RSAKey dari string
key_file = io.StringIO(PRIVATE_KEY)
pkey = paramiko.RSAKey.from_private_key(key_file)

COMMANDS = [
    "sudo mkdir -p /root/.ssh",
    "sudo chmod 700 /root/.ssh",
    "sudo cp /home/ubuntu/.ssh/authorized_keys /root/.ssh/",
    "sudo chmod 600 /root/.ssh/authorized_keys",
    "sudo chown root:root /root/.ssh/authorized_keys",
    "if ! grep -q '^PermitRootLogin yes' /etc/ssh/sshd_config; then echo 'PermitRootLogin yes' | sudo tee -a /etc/ssh/sshd_config; fi",
    "sudo systemctl restart ssh"
]

def run_commands(ip):
    print(f"\n=== Connect ke {ip} ===")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=USERNAME, pkey=pkey, timeout=15)
        for cmd in COMMANDS:
            print(f"[{ip}] Jalankan: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print(f"[{ip}] ✅ Sukses")
            else:
                print(f"[{ip}] ❌ Error: {stderr.read().decode().strip()}")
    except Exception as e:
        print(f"[{ip}] ❌ Gagal connect: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    for ip in IPS:
        run_commands(ip)

    print("\n=== Semua selesai! ===")
    print("Sekarang coba login langsung: ssh root@<EC2-IP>")
