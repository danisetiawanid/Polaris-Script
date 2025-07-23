import pygetwindow as gw
import pyautogui
import time
import pyperclip

# Judul jendela aplikasi
WINDOW_TITLE = "Polaris Node Manager"
ADD_BUTTON_POS = (1358, 177)

USERNAME = "root"
PASSWORD = """Azura042AA"""

ip_list_baru = [
    "134.199.192.13",
    "129.212.186.210",
    "129.212.186.190"
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


def fill_form(ip, username, password, nama_mesin):
    time.sleep(1.2)

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
    time.sleep(10)
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

    time.sleep(5)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("✅ Mesin berhasil ditambahkan")

    time.sleep(0.3)


if __name__ == "__main__":
    focus_window(WINDOW_TITLE)
    for i, ip in enumerate(ip_list_baru, start=1):
        nama_mesin = f"boro-{i}"
        click_add_machine()
        fill_form(ip, USERNAME, PASSWORD, nama_mesin)
