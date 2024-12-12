import tkinter as tk
from tkinter import messagebox
import os
import requests
import subprocess
import sys
import shutil
import time
from urllib.parse import urlsplit

# Ana pencereyi oluşturuyoruz
root = tk.Tk()
root.title("Advanced Toolbox Uygulaması")
root.geometry("600x400")

# Pencere arka planını siyah yapıyoruz
root.configure(bg='black')

# Yardımcı fonksiyonlar
def show_message(message, title="Mesaj"):
    messagebox.showinfo(title, message)

def download_application(url, save_path):
    """ Uygulama indirip belirtilen dizine kaydeder. """
    try:
        # URL'den dosyayı indiriyoruz
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Hata olursa istisna fırlat
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        show_message(f"{os.path.basename(save_path)} başarıyla indirildi.")
    except Exception as e:
        show_message(f"Hata: {str(e)}", "İndirme Hatası")

def start_application(app_name):
    """ Uygulamayı başlatır. """
    try:
        os.system(f"start {app_name}")
    except Exception as e:
        show_message(f"Hata: {str(e)}", "Başlatma Hatası")

def stop_application(app_name):
    """ Uygulamayı kapatır. """
    try:
        os.system(f"taskkill /f /im {app_name}")
        show_message(f"{app_name} başarıyla kapatıldı.")
    except Exception as e:
        show_message(f"Hata: {str(e)}", "Kapatma Hatası")

def update_system():
    """ Windows güncellemelerini kontrol etme (Yalnızca basit bir kontrol). """
    try:
        result = subprocess.run("powershell Get-WindowsUpdate", capture_output=True, text=True)
        if result.returncode == 0:
            show_message("Güncellemeler kontrol edildi.\n" + result.stdout)
        else:
            show_message("Güncellemeler kontrol edilirken bir hata oluştu.", "Güncelleme Hatası")
    except Exception as e:
        show_message(f"Hata: {str(e)}", "Sistem Güncelleme Hatası")

def disable_windows_update():
    """ Windows güncellemelerini devre dışı bırakır. """
    try:
        result = subprocess.run("powershell Stop-Service wuauserv", capture_output=True, text=True)
        if result.returncode == 0:
            show_message("Windows güncellemeleri devre dışı bırakıldı.")
        else:
            show_message("Güncellemeler devre dışı bırakılırken bir hata oluştu.", "Hata")
    except Exception as e:
        show_message(f"Hata: {str(e)}", "Güncelleme Durdurma Hatası")

def system_info():
    """ Sistem bilgilerini gösterir. """
    try:
        result = subprocess.run("systeminfo", capture_output=True, text=True)
        show_message(result.stdout, "Sistem Bilgisi")
    except Exception as e:
        show_message(f"Hata: {str(e)}", "Sistem Bilgisi Hatası")

def file_management(operation, src, dest=None):
    """ Dosya yönetimi (kopyalama, taşıma, silme) """
    try:
        if operation == 'copy' and dest:
            shutil.copy(src, dest)
            show_message(f"{src} dosyası {dest} dizinine kopyalandı.")
        elif operation == 'move' and dest:
            shutil.move(src, dest)
            show_message(f"{src} dosyası {dest} dizinine taşındı.")
        elif operation == 'delete':
            os.remove(src)
            show_message(f"{src} dosyası silindi.")
        else:
            show_message("Geçersiz işlem", "Hata")
    except Exception as e:
        show_message(f"Hata: {str(e)}", "Dosya Yönetimi Hatası")

# GUI Düzeni
frame = tk.Frame(root, bg='black')  # Frame arka planını siyah yapıyoruz
frame.pack(pady=20)

# Butonları düzenleyelim
button_style = {
    'width': 30,
    'bg': 'darkred',  # Koyu kırmızı arka plan
    'fg': 'white',  # Beyaz metin
    'font': ('Arial', 10, 'bold'),
    'activebackground': 'red',  # Buton aktifken kırmızı
    'activeforeground': 'white'  # Buton aktifken beyaz metin
}

# İndirme Butonu
download_button = tk.Button(frame, text="Uygulama İndir", command=lambda: download_application("https://example.com/app.exe", "C:/Users/Downloads/app.exe"), **button_style)
download_button.grid(row=0, column=0, pady=5)

# Sistem Bilgisi Butonu
sys_info_button = tk.Button(frame, text="Sistem Bilgisi", command=system_info, **button_style)
sys_info_button.grid(row=1, column=0, pady=5)

# Uygulama Başlatma Butonu
start_button = tk.Button(frame, text="Uygulama Başlat", command=lambda: start_application("notepad.exe"), **button_style)
start_button.grid(row=2, column=0, pady=5)

# Uygulama Kapatma Butonu
stop_button = tk.Button(frame, text="Uygulama Kapat", command=lambda: stop_application("notepad.exe"), **button_style)
stop_button.grid(row=3, column=0, pady=5)

# Güncelleme Yönetimi Butonu
update_button = tk.Button(frame, text="Güncellemeleri Kontrol Et", command=update_system, **button_style)
update_button.grid(row=4, column=0, pady=5)

# Güncelleme Devre Dışı Butonu
disable_update_button = tk.Button(frame, text="Güncellemeleri Devre Dışı Bırak", command=disable_windows_update, **button_style)
disable_update_button.grid(row=5, column=0, pady=5)

# Çıkış Butonu
exit_button = tk.Button(frame, text="Çıkış", command=root.quit, **button_style)
exit_button.grid(row=6, column=0, pady=5)

# Pencereyi başlatıyoruz
root.mainloop()
