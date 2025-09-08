import subprocess
import pyautogui
import time
import pyperclip
import pytesseract
import cv2
import numpy as np

# Judul jendela aplikasi
WINDOW_TITLE = "Polaris Node Manager"

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
    """Fokus ke window dengan judul tertentu (Linux, via xdotool)"""
    try:
        result = subprocess.check_output(["xdotool", "search", "--name", title])
        window_ids = result.decode().strip().split("\n")
        if not window_ids:
            raise Exception("Window tidak ditemukan")

        # Fokus ke window pertama yang cocok
        subprocess.run(["xdotool", "windowactivate", "--sync", window_ids[0]])
        time.sleep(1)
        print(f"✅ Fokus ke jendela: {title}")

    except subprocess.CalledProcessError:
        raise Exception(f"Tidak ditemukan window dengan judul mengandung '{title}'")

def click_button_add_machine():
    """Cari tombol 'Add Machine' via OCR (tanpa gambar)"""
    for attempt in range(5):  # retry max 5x
        screenshot = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        data = pytesseract.image_to_data(
            img, output_type=pytesseract.Output.DICT, config="--psm 6"
        )

        words = [t.lower() for t in data["text"] if t.strip()]
        print(f"[DEBUG OCR percobaan {attempt+1}]:", words)

        for i, t in enumerate(data["text"]):
            if "add" in t.lower():
                # cek apakah ada 'mach' juga di OCR
                if any("mach" in w for w in words):
                    x, y, w, h = (
                        data["left"][i],
                        data["top"][i],
                        data["width"][i],
                        data["height"][i],
                    )
                    center_x, center_y = x + w // 2, y + h // 2
                    pyautogui.click(center_x, center_y)
                    print(f"✅ Klik tombol 'Add Machine' di ({center_x},{center_y})")
                    return True

        time.sleep(0.5)

    print("❌ Gagal menemukan tombol 'Add Machine' setelah 5x percobaan")
    return False

def fill_form(ip, username, password, nama_mesin):
    time.sleep(0.4)

    if not click_button_add_machine():
        raise Exception("Tombol 'Add Machine' tidak ditemukan!")

    pyautogui.press("tab")
    pyautogui.press("tab")
    pyperclip.copy(ip)
    pyautogui.hotkey("ctrl", "v")
    print(f"✅ IP Address {ip} dimasukkan")

    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyperclip.copy(username)
    pyautogui.hotkey("ctrl", "v")
    print("✅ Username dimasukkan")

    pyautogui.press("tab")
    pyautogui.press("tab")
    print("✅ SSH key method dipilih")

    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    pyperclip.copy(password)
    pyautogui.hotkey("ctrl", "v")
    print("✅ SSH Key dipaste")

    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("enter")
    print("✅ Submit / OK ditekan")

    time.sleep(15)
    pyautogui.press("enter")
    print("✅ Submit SSH Ditekan")

    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(17)
    print("✅ Validate Network")

    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(25)
    print("✅ Validate POW")

    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("enter")
    print("✅ Submit / OK ditekan")

    pyautogui.press("tab")
    pyautogui.press("tab")
    pyperclip.copy(nama_mesin)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("tab")
    pyautogui.press("space")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("enter")
    print(f"✅ Naming mesin '{nama_mesin}' berhasil")

    time.sleep(15)
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("enter")
    print("✅ Mesin berhasil ditambahkan")

    time.sleep(0.6)

if __name__ == "__main__":
    focus_window(WINDOW_TITLE)
    for i, ip in enumerate(ip_list_baru, start=1):
        nama_mesin = f"boro-{i}"
        fill_form(ip, USERNAME, PASSWORD, nama_mesin)
