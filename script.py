import pygetwindow as gw
import pyautogui
import time
import pyperclip

# Judul jendela aplikasi
WINDOW_TITLE = "Polaris Node Manager"
ADD_BUTTON_POS = (1437, 139)  # Koordinat tombol 'Add Machine'

# Data awal
IP_ADDRESS_AWAL = "54.151.202.98"
USERNAME = "ubuntu"
SSH_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAzDRF/26lOlQYWscpXooi8p+AbXxsOHetvNnACS4ha149CLBv
5YD53+x3itQFEcOlbXBfF284FbN0u7wHsKjY3wHPXV8KWqdT+wjlCPty4PJaFUpd
tR9OITm53At6DCKL4qtlBCFm//rQ0HI+wdp0Pyq2c/UJ1s0nDfuhoqb80B/VD+W5
0RslzPhT3HscsL8PL/DicOWgyLY4EBXC6VnJsyWAk1K/l90ksWY6qD/sCMDEdaxk
Sid5zHVTtLAA7xyl3JCkkGhxGy3Hb6X7TjoUO4bIrrAPjlYoS0hQRLZHMWLmSGyI
ZA75JrI0p7XvCWDdyySM7OTcR5NuXWr8OnMcKQIDAQABAoIBABuxmyyhHNdkQElP
aVTg9wxghVJT5XljAbTy8xBLqUyeYziidQpzC3BK6YtyZZ2bIvxMmRjchIas58/u
GDzlKURVQoIvOYBB4SnScv1c3J+VPpJUm5DMxhPLeGFXTR4IMWB0TibZQNbGdTtP
wyMXNVy7tjLTsJnpCLrkvW8Jpo+zA1u/TCuzJAXTQlgnT8h2IisQglo50559QNRF
HpEaYh/PepcAFJStmiG/nnknLl/zeXwhhW2v8zAykCWvwciPunsvWtSsWHOO/Vk1
DM3NN3OcL9K+6khWJtbtM/6A/VsJhWGCwEt/Ah7WopN76siq0NMMh8K4MpIk+G3s
AKDM8uECgYEA8i8B9enbfsZneHktBDczGI4QUwOeJcam5LswPSjRS92J/SzV5oMH
eP51aWU060U1KGuHlWLp57zBF/hhXA1Lsqfa9RH3W25xMdPugaBumk/zN1kvjt+x
dNGlsc1/bNf2lTygL7MAogrwaSobhH7slHBdfPbwWKPwLeVWOrDwCQsCgYEA19qX
f2GfhDQ11cJsDWvIBzAzlkLC0aNUs9XDG5QIvoUkxrpI5k8RnW50YfIAasiPtz2s
BYlNrMlCZPlfP/KX8qlAOheyYJCkIikgmwISS5TVI67xQ99AB6noWmJVKFjDoodN
GdYsmCZVr4xkxwnyg/GM6jFnzcSZ9fWIs1fPeBsCgYEArQwBrqFHATLrRB3xmI2I
qQb5ixeOrRdgsRc/xLOhuT+3FXwv6uG9OSs44fI6+dEdxp/u5UMkNz2cC3CiwI+P
gzyFK4+G24Hyx9PTHDRyUzjFZMsJPGGB/yK97moTnsZBnykOnIae8So31i0MNIQs
r3QKmPwpiGy7dU/laVJ8cTkCgYAXbyDhcGzMAosRsPDgKCJoPWBsYMUb01qfx4ZO
GS012eibNqAxeMYVzGcQNyC6dxm7MBPb6gMnzhXKNpSTsbezXZKee/Ier7VSDBsB
GSF5WSgmnpiM4NDnxBd4sJJENhbPL1c8hdcDka3dyCUswrS0hGXjCwgU+9InNMfp
iI/6nwKBgQCo/9HDdpWedJHyuAcoMqTe4R6mnzo5UZqESV3XkrCyMGEN38Y6upR/
vDfUGeD2QZM1KsPcysz3htd3+4qOV6zto87Y15iLctC+v6MlGcQXTs1AAWYwJ6dO
E7kdqpJqW+Jh/+/ONYBxoWiqk8YO7lCYT3+d6PUz+Rvn96RYsXP+gQ==
-----END RSA PRIVATE KEY-----"""

# List nama yang akan di-loop
ip_list_baru = [
    "129.212.183.45",
    "129.212.183.191",
    "129.212.183.227",
    "129.212.183.192",
    "129.212.182.67"
]


def focus_window(title):
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        raise Exception(f"Tidak ditemukan window dengan judul mengandung '{title}'")
    win = windows[0]
    win.activate()
    time.sleep(1)
    print(f"✅ Fokus ke jendela: {win.title}")


def click_add_machine():
    pyautogui.moveTo(ADD_BUTTON_POS)
    time.sleep(0.5)
    pyautogui.click()
    print("✅ Klik tombol 'Add Machine'")


def fill_form(ip, username, ssh_key, nama):  
    time.sleep(1.2)

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.write(ip)
    print("✅ IP Address dimasukkan")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.write(username)
    print("✅ Username dimasukkan")

    pyautogui.press('tab')
    pyautogui.press('down')
    print("✅ SSH key method dipilih")

    pyautogui.press('tab')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(ssh_key)
    pyautogui.hotkey('ctrl', 'v')
    print("✅ SSH Key dipaste")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("✅ Submit / OK ditekan")

    time.sleep(20)
    pyautogui.press('enter')
    print("✅ Submit SSH Ditekan")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(15)
    print("✅ Validate Network")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(28)
    print("✅ Validate POW")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("✅ Go Back 1")

    pyautogui.press('enter')
    print("✅ Go Back 2")

    # Tulis IP BARU
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.write(nama)
    print(f"✅ Nama node ditulis: {nama}")

    # Tab 3x, lalu tulis root
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.write('root')
    print("✅ Hewan ditulis: root")

    # Lanjut isi password
    pyautogui.press('tab')
    pyautogui.press('up')  # Pilih password method
    pyautogui.press('tab')
    pyautogui.write('Azura042AA')
    print("✅Passwoord ditulis: Azura042AA")
    
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(13)
    print("✅Lanjut Check SSH")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("✅Lanjut")

    pyautogui.press('enter')
    print("✅Lanjut")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.write('chuyamachine')
    pyautogui.press('tab')
    pyautogui.press('space')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("Naming Mesin Berhasil")

    time.sleep(5)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("✅ Mesin berhasil tambahkan")
    
    time.sleep(1)


if __name__ == "__main__":
    focus_window(WINDOW_TITLE)
    for i, nama in enumerate(ip_list_baru):
        ip = IP_ADDRESS_AWAL  # Ganti jika pakai IP berbeda per nama
        click_add_machine()
        fill_form(ip, USERNAME, SSH_KEY, nama)
