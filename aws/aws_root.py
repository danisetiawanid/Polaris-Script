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
KZJzw/IL0MzX5lHOvNjPyb6NqFc+EyBxTHGV.....
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
