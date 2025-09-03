import paramiko
import io

# ==== List IP Target ====
IPS = [
    "34.214.107.125",
    "54.185.89.113",
    "54.212.238.192"
]

USERNAME = "ubuntu"

# ==== Private Key Dummy (tempel langsung di sini) ====
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA5ivWiKj2hF4wFhbf1f3ymTmDA0GjU81a5kPm5Nnpl0qDlEiq
s/5IkJw8RUlOFy9vty6KeyB1rX1rAzck+IsfIwIpdGmHQn7t9vJFm9+BPA6BpgEv
NdnX65Q46vG6uTrT0qAd6RdR7qeBDy4Mz2/v/wD3jrg6m9hVdI6xcsM9HGU8j4zY
ERBvZrqLrKGKFHFlVeaUvz3f0UMAsjXj0nxayISbXOnHtu1m5DwoZS/8B4bLDaHx
lhH1SPEK/HeQWqy8pI47lYx5KCp52KOj9w46Hp7bWQQMz6HK5lC+d5SgdcNAbcbd
K/gi10UnO2IbKArFuFkzq5zda648uLBo6SxSuwIDAQABAoIBAGXx9rRSudUI7p1q
Bjv+nUvWWDvB/7gnVWJ1orer+LUksMClqs3MC5HZUSyS+j50qTNmLrm4N8berN4g
t4RKAkF8PKYt81W1aGqfBcuzI8dY2X2QOrvMP8E8xjTxWfWeo6E/f9/0jzp4AEab
69qYxqCYag1Rdcv+9mKIrPmald+T9EXuZx/ecQR9Ge3xf++cnfb8ULm76czqTImN
sauUWSbERDea99VXRs6ELj29Xc45SIqXn7HnG6412ePkpiH09f8ebEwislCECYnL
4mjMm1HKmsG4Sm18AHLqGSDW8M038l8iH087iVQqiU3WppKRCtaQYH5L26yYU2OP
J/sO+mECgYEA86dAr2VSY6SRDkVkbc8hv4gLkNqMx6wPo42ScLLvZe+1kYQgfx6g
R0K+e4mSrO7U4K4jfbDZ5UM6cQQx9/ixjeanw0Skn+ADDDvHG96dhwv3bF4kkVRB
NznEqX6XmlPt3oqe2DeDt77pIDE8+q3NQ4pVs6kMjIGPAuSsh34F+MsCgYEA8dWx
BEneZ7x/vVon4h1jxvfuJ+J/ukF5hJownFMwGX/Mx+WL2AxT91G8x62kffCVbBSm
um/aPKeEhi5vijsqkcqfeGh62t4SS+XSBqN+w+6Xn9YhjAdxWhWQQMvwOu6u8Tyb
XTLM3yknG2r7bx4yIwNqCJk7GD79ppJ0uD0u/9ECgYAB5HGnKxVJutR5lOZjx/EO
KMNWO6xOPLLeZVIW1/zuAL+bQrhx5E4AX69VDEt8VlqG6DNUXZRDqJMCn7K3p1HR
tVHmPVk9+KJtbOVt/PuiOeCREeYczte20xcI7ffFdhNp4A+9xCicu7nZyygbFlB6
zs89lvmG+dafgiEo6DypowKBgQDOdzJ6BtbqmfQ1JROH6K+W33Vkd+u0iNHGdB2s
WRlnq8SZpVCPU3ccX5xcndMh8pSfgcIWygf4YMy0AlEYIwtlDSi5E/pPgej9A2kc
YdmITdsFizt44aHU1zQhHfwrVDvnmWbLWuOuYuQQdHXVmGIVooSUcr4RJTZJUCB2
a0YFAQKBgBIGeBIGzIFEpnZTVja/VDMss85/42ncSUiwEVEfb3IypkzCjy5pAp6X
GQjfICp5JKvl02G8FdJKDw+ss+tvVzU2X+lxHLO0FOvh6cdrweMdZahj9EGnsMaX
9csabZfPeX9mNU74n8xWl2sQkD5nvLyZ2qYu5j0QgxGC+/PWc7LG
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
