import subprocess
import pyautogui
import time
import pyperclip

# Judul jendela aplikasi
WINDOW_TITLE = "Polaris Node Manager"
# ADD_BUTTON_POS = (1358, 177)

USERNAME = "root"
PASSWORD = """Azura042AA"""

ip_list_baru = [
    "129.212.188.160",
    "129.212.188.46",
    "134.199.193.90",
    "129.212.188.168",
    "129.212.188.161",
    "134.199.206.233",
    "134.199.206.164",
    "129.212.188.167",
    "134.199.203.29"          
]

def focus_window(title):
    try:
        result = subprocess.check_output(["xdotool", "search", "--name", title])
        window_ids = result.decode().strip().split("\n")
        if not window_ids:
            raise Exception("Window tidak ditemukan")

        # Fokus ke window pertama yang cocok
        subprocess.run(["xdotool", "windowactivate", "--sync", window_ids[0]])
        time.sleep(1)
        print(f"? Fokus ke jendela: {title}")

    except subprocess.CalledProcessError:
        raise Exception(f"Tidak ditemukan window dengan judul mengandung '{title}'")

# def click_add_machine():
#     pyautogui.moveTo(ADD_BUTTON_POS)
#     time.sleep(0.5)
#     pyautogui.click()
#     print("? Klik tombol 'Add Machine'")

def fill_form(ip, username, password, nama_mesin):
    time.sleep(0.4)

    button_image = 'add_button.png'  # Nama file screenshot tombol

    # Cari tombol berdasarkan gambar
    location = pyautogui.locateOnScreen(button_image, confidence=0.6)

    if location:
        center = pyautogui.center(location)
        pyautogui.click(center)
        print("? Tombol Add diklik")
    else:
        print("? Tombol tidak ditemukan!")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyperclip.copy(ip)
    pyautogui.hotkey('ctrl', 'v')
    print(f"? IP Address {ip} dimasukkan")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyperclip.copy(username)
    pyautogui.hotkey('ctrl', 'v')
    print("? Username dimasukkan")

    pyautogui.press('tab')
    pyautogui.press('tab')
    print("? SSH key method dipilih")

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(password)
    pyautogui.hotkey('ctrl', 'v')
    print("? SSH Key dipaste")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("? Submit / OK ditekan")

    time.sleep(10)
    pyautogui.press('enter')
    print("? Submit SSH Ditekan")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(6)
    print("? Validate Network")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(17)
    print("? Validate POW")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("? Submit / OK ditekan")

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyperclip.copy(nama_mesin)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('tab')
    pyautogui.press('space')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print(f"? Naming mesin '{nama_mesin}' berhasil")

    time.sleep(7)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    print("? Mesin berhasil ditambahkan")

    time.sleep(0.6)

if __name__ == "__main__":
    focus_window(WINDOW_TITLE)
    for i, ip in enumerate(ip_list_baru, start=1):
        nama_mesin = f"boro-{i}"
        # click_add_machine()
        fill_form(ip, USERNAME, PASSWORD, nama_mesin)
