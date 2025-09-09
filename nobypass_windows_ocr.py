import pygetwindow as gw
import pyautogui
import time
import pyperclip
import pytesseract
import cv2
import numpy as np
from PIL import Image

# === CONFIG TESSERACT ===
# Windows: pastikan path ini sesuai dengan lokasi instalasi tesseract.exe
# Linux: cukup install dengan `sudo apt install tesseract-ocr`
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# === APP CONFIG ===
WINDOW_TITLE = "Polaris Node Manager"
USERNAME = "root"
PASSWORD = """Azura042AA"""

ip_list_baru = [
# "143.198.237.246",
# "24.199.102.1",
# "147.182.206.186",
# "64.23.172.7",
# "64.23.229.16",


"147.182.245.240",
"146.190.117.74",
"24.144.88.28",
"134.199.221.222",
"146.190.161.111",

]

# === TOOLS ===
def focus_window(title):
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        raise Exception(f"Tidak ditemukan window dengan judul mengandung '{title}'")
    win = windows[0]
    win.activate()
    time.sleep(1)
    print(f"✅ Fokus ke jendela: {win.title}")


def click_button_add_machine():
    """Cari tombol 'Add Machine' dengan OCR, toleransi jika kata kepotong"""
    win = gw.getWindowsWithTitle(WINDOW_TITLE)[0]
    region = (win.left, win.top, win.width, win.height)

    for attempt in range(5):
        screenshot = pyautogui.screenshot(region=region)
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        data = pytesseract.image_to_data(
            img, output_type=pytesseract.Output.DICT, config="--psm 6"
        )

        words = [t.lower() for t in data["text"] if t.strip()]
        joined = " ".join(words)
        print(f"[DEBUG] OCR percobaan {attempt+1}:", joined)

        for i, t in enumerate(data["text"]):
            if "add" in t.lower():  # fokus ke kata ADD
                # kalau ada 'machine' / 'machi' di hasil OCR global
                if any("mach" in w for w in words):
                    x, y, w, h = (
                        data["left"][i] + win.left,
                        data["top"][i] + win.top,
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




# === FORM AUTOMATION ===
def fill_form(ip, username, password, nama_mesin):
    time.sleep(0.4)

    # Klik tombol Add Machine (ubah sesuai teks tombol di aplikasi kamu)
    click_button_add_machine()


    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.write(ip)
    print(f"✅ IP Address {ip} dimasukkan")

    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.write(username)
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

    time.sleep(14)
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
    pyautogui.write(nama_mesin)
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


# === MAIN ===
if __name__ == "__main__":
    # Debug: pastikan tesseract terdeteksi
    print("🔍 Menggunakan Tesseract di:", pytesseract.pytesseract.tesseract_cmd)
    print("🔍 Versi Tesseract:", pytesseract.get_tesseract_version())

    focus_window(WINDOW_TITLE)
    for i, ip in enumerate(ip_list_baru, start=1):
        nama_mesin = f"boro-{i}"
        fill_form(ip, USERNAME, PASSWORD, nama_mesin)
