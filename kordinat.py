import pyautogui
import time

print("⏳ Arahkan kursor ke tombol 'Add Machine' dalam 5 detik...")
time.sleep(5)

pos = pyautogui.position()
print(f"📍 Koordinat mouse: {pos}")
