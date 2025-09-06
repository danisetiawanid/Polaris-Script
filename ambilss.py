import pyautogui
import time

print("🖱️ Arahkan mouse ke TENGAH tombol dalam 5 detik...")
time.sleep(5)

# Ambil posisi mouse
x, y = pyautogui.position()
print(f"📍 Posisi mouse terdeteksi di: ({x}, {y})")

# Tentukan ukuran kotak sekitar tombol
width = 140   # lebar area screenshot
height = 70   # tinggi area screenshot

# Hitung pojok kiri atas area
left = x - width // 2
top = y - height // 2

# Ambil screenshot area tombol
screenshot = pyautogui.screenshot("button.png", region=(left, top, width, height))
print("✅ Screenshot tombol disimpan sebagai button.png")
