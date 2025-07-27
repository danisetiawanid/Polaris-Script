import pygetwindow as gw
import pyautogui
import time
import pyperclip

# Judul jendela aplikasi
WINDOW_TITLE = "Polaris Node Manager"
ADD_BUTTON_POS = (1437, 139)  # Koordinat tombol 'Add Machine'

# Data awal
IP_ADDRESS_AWAL = "162.243.70.165"
USERNAME = "root"
SSH_KEY = """-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----"""

# List nama yang akan di-loop
ip_list_baru = [
    "104.248.2.254",
    "165.227.123.227",
    "138.197.33.60",
    "68.183.62.186",
    "159.203.127.187",
    "167.172.247.136",
    "165.227.106.82",
    "174.138.53.120"
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
    time.sleep(0.4)

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

    time.sleep(10)
    pyautogui.press('enter')
    print("✅ Submit SSH Ditekan")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(10)
    print("✅ Validate Network")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(15)
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
    pyautogui.write('boromachine')
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
    
    time.sleep(0.3)


if __name__ == "__main__":
    focus_window(WINDOW_TITLE)
    for i, nama in enumerate(ip_list_baru):
        ip = IP_ADDRESS_AWAL  # Ganti jika pakai IP berbeda per nama
        click_add_machine()
        fill_form(ip, USERNAME, SSH_KEY, nama)
