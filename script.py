import pygetwindow as gw
import pyautogui
import time
import pyperclip

# Judul jendela aplikasi
WINDOW_TITLE = "Polaris Node Manager"
ADD_BUTTON_POS = (1437, 139)  # Koordinat tombol 'Add Machine'

# Data awal
IP_ADDRESS_AWAL = "13.229.95.51"
USERNAME = "ubuntu"
SSH_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA4dcKlmgs7U2i9S5FCHVVi5ZYa7eu9jOpE857hNse65J7MNwn
8G5O8E0qc7+sJ/HtoeRZ9Ip387T9ivlt7976hILhMsVZ67rc2zYmIHbB7K84LkJY
DqkS87CXDbiZyBgxAlCfjjT++jCPXWmn8IKk10qdIGFmuHqzLNqh1NE2UZLH1vw6
zj81987Z8kdTQKzI44sUAxwh2ShZVFUXmgRP1XWPXORkbEzcFOXnk/XROTc33yG6
uyVw8x8QY/GcbMCLu0c+fnCJigb23XHRX1Pa3PlGTg23aew0KIGacvlrnbYItfLK
vYLcCq6o8rqBV3m5ugu1XZh7RzrWW3dOtV+B1wIDAQABAoIBAFpqe6Sn5ITFNl6u
vZibUTpnYNMPYQ7Us/ZoDm+sQn7R0FxJZ/wMTbJLUpmwvT3oz9im0ZTj8w4xAekn
32nPfcCbnYl0FYIY998TmMQah504sWdjzFliO2Iw6ujlZTwE42on2RlYAlUsJ9mg
OUpDI7fF+Y5DMJrfFOj6Rxwq/nI9bxSu0aP/myqb+y4nCEvFAjMVUwP2djiqoK24
ZnMB4cLdicHfi66p5oMT6r+Sbz/GqcybjSkQ9qdO462+wUYh+pbSKrf66lMf13V/
rsZC5kAOvaa4ded1fyIglySwnnRLaqnWlRtkV+Fm+B91nIYXZp8Qg2zt/UWoU1xg
ocxpjKECgYEA834FJN8HuHKXCxqx/yVvHZ3qwTLv+//qmTO9R1AK3c8gBMN0DZ62
qTWLurrrkKyULJGPpm/AjLRSYhwdtdIjQnJUwmxLjqr7ffqh7dpdBcE/RV9PVN8R
KakzS72GbSOYitXC3rn9O0RwNmlXLy3Ek1DCD8ptjGL3LQW70hT5QSkCgYEA7XDj
0pCzKBtdVbgqCbZhpw5eP8tWkZyVm4QpK113ICNWm8vycO4KwxGsgU7aJJWONSq+
upWGfzNocunsdWV8Zg9Q4HejgPMLcm7yvM4GzyW1OcL+MEakQqROeH6eOacxbOL3
Krshr6B1CCTWKLz/ZITPd4ItT9bNxPWbqIWsCv8CgYBJ7YcuTLERZWlKq85DQ2Bb
Q6kVA5wtjOPzo+viDQFfmxWDnLxNrlSTR3inNz1ybZOHfKJ6zA9QKSeiNhsnKygd
co0dgrfmFy/IbiJgDx6TMrs9GtUBVcDmP0MdyetYk6gq7v/9k8a5Cexv+MfJwUGf
4LMrDDD6oMmfV9BQ1qFfEQKBgHJcNg57zR5bF7gqjGzDIAODIxfcyuQ1I8WUgPO2
/6JGAvfk4e9MZ3iOsaRSIzUNp0GqRdS+IdpwGzWFv3LHn4PUiqKiXOjFptTF5TnU
jWkGA2Q/q4f67jB+zKCyc2jXQzHrmxpEqTPat6NlgpR6exOh9/7afxJ+JftgREmF
oFhnAoGBAMFlP6MNKwYB2ZH+yCBy6RT4W5Fki4sN1WxNGp0NYWNJoQiWB49EJx52
GFP6JkzjaZ/L6sknyzpkpzAn/Kcd3fdl4UhVVIGCXmaMywJB+9WFETTLZpHoA6Ns
491AUWduUTtxMCJ1MKu0mQSfDcrufjcHPUzBHWEuXD53zSq8ZfCh
-----END RSA PRIVATE KEY-----"""

# List nama yang akan di-loop
ip_list_baru = [
    "129.212.179.100",
    "129.212.180.214"
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
    time.sleep(20)
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
    time.sleep(15)
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


if __name__ == "__main__":
    focus_window(WINDOW_TITLE)
    for i, nama in enumerate(ip_list_baru):
        ip = IP_ADDRESS_AWAL  # Ganti jika pakai IP berbeda per nama
        click_add_machine()
        fill_form(ip, USERNAME, SSH_KEY, nama)
