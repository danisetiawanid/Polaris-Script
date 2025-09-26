import paramiko
import io

# ==== List IP Target ====
IPS = [
"3.81.103.228",
"3.90.143.165",
"3.94.251.20",
"54.166.210.101",
"54.89.80.234",
"54.173.224.57",
"54.82.139.183",
]

USERNAME = "ubuntu"

# ==== Private Key Dummy (tempel langsung di sini) ====
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
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
