import pygetwindow as gw
import pyautogui
import time
import pyperclip

# Judul jendela aplikasi
WINDOW_TITLE = "Polaris Node Manager"

USERNAME = "root"
PASSWORD = """Azura042AA"""

ip_list_baru = [
    "129.212.179.11",
    "134.199.201.255",
    "129.212.178.42",
    "129.212.176.218",
    "134.199.204.250",
    "129.212.178.43"
]


def focus_window(title):
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        raise Exception(f"Tidak ditemukan window dengan judul mengandung '{title}'")
    win = windows[0]
    win.activate()
    time.sleep(1)
    print(f"✅ Fokus ke jendela: {win.title}")


def fill_form(ip, username, password, nama_mesin):
    time.sleep(0.4)

    button_image = 'add_button.png'  # Nama file screenshot tombol

    # Cari tombol berdasarkan gambar
    location = pyautogui.locateOnScreen(button_image, confidence=0.6)

    if location:
        center = pyautogui.center(location)
        pyautogui.click(center)
        print("Button clicked!")
    else:
        print("Button not found!")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.write(ip)
    print(f"✅ IP Address {ip} dimasukkan")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.write(username)
    print("✅ Username dimasukkan")

    pyautogui.press('tab')
    pyautogui.press('tab')
    print("✅ SSH key method dipilih")

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(password)
    pyautogui.hotkey('ctrl', 'v')
    print("✅ SSH Key dipaste")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("✅ Submit / OK ditekan")

    time.sleep(14)
    pyautogui.press('enter')
    print("✅ Submit SSH Ditekan")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(17)
    print("✅ Validate Network")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(25)
    print("✅ Validate POW")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("✅ Submit / OK ditekan")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.write(nama_mesin)
    pyautogui.press('tab')
    pyautogui.press('space')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print(f"✅ Naming mesin '{nama_mesin}' berhasil")

    time.sleep(15)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("✅ Mesin berhasil ditambahkan")

    time.sleep(0.6)


if __name__ == "__main__":
    focus_window(WINDOW_TITLE)
    for i, ip in enumerate(ip_list_baru, start=1):
        nama_mesin = f"boro-{i}"
        # click_add_machine()
        fill_form(ip, USERNAME, PASSWORD, nama_mesin)
