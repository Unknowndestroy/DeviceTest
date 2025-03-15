import os
import sys
import time
import socket
import platform
import subprocess
import threading
import ctypes
import random
import cv2
import numpy as np
import pyaudio
import psutil
import tkinter as tk
from tkinter import ttk, messagebox
import wmi
import pystray
from PIL import Image, ImageDraw

class HardwareTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Donanım Test Programı")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Ana test sayfası
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Ana Menü")
        
        # Test listesi
        self.tests = [
            {"name": "Bozuk Pixel Testi", "function": self.pixel_test},
            {"name": "Anakart LED Testi", "function": self.motherboard_led_test},
            {"name": "Buzzer Testi", "function": self.buzzer_test},
            {"name": "CPU Stress Test", "function": self.cpu_stress_test},
            {"name": "RAM Stress Test", "function": self.ram_stress_test},
            {"name": "Ethernet Adapter Test", "function": self.ethernet_test},
            {"name": "Case Light Test", "function": self.case_light_test},
            {"name": "WebCam Test", "function": self.webcam_test},
            {"name": "Microphone Test", "function": self.microphone_test},
            {"name": "Monitor Test", "function": self.monitor_test},
            {"name": "Speakers Test", "function": self.speakers_test},
            {"name": "AntiVirus Test", "function": self.antivirus_test},
            {"name": "HeadPhones Light Test", "function": self.headphones_light_test},
            {"name": "Bluetooth Test", "function": self.bluetooth_test},
        ]
        
        # Test butonları oluşturma
        self.create_test_buttons()
        
        # ALL IN ONE test butonu
        self.all_in_one_button = ttk.Button(
            self.main_frame, 
            text="ALL IN ONE TEST", 
            command=self.all_in_one_test,
            style="Accent.TButton"
        )
        self.all_in_one_button.pack(pady=20, ipadx=10, ipady=5)
        
        # Sonuç ekranı
        self.result_text = tk.Text(self.main_frame, height=10, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Durum çubuğu
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # WMI bağlantısı
        self.wmi_conn = wmi.WMI()
        
        # Test sonuçları
        self.test_results = {}

    def create_test_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        for i, test in enumerate(self.tests):
            btn = ttk.Button(
                button_frame, 
                text=f"{i+1}. {test['name']}", 
                command=test['function']
            )
            # Her satırda 2 buton
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
            
        # Grid sütunlarını eşit genişlikte yapma
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

    def log_result(self, test_name, result, details=""):
        timestamp = time.strftime("%H:%M:%S")
        self.result_text.insert(tk.END, f"[{timestamp}] {test_name}: {result}\n")
        if details:
            self.result_text.insert(tk.END, f"  Detaylar: {details}\n")
        self.result_text.see(tk.END)
        self.test_results[test_name] = {"result": result, "details": details}

    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()

    def pixel_test(self):
        def run_pixel_test():
            pixel_window = tk.Toplevel(self.root)
            pixel_window.title("Bozuk Pixel Testi")
            pixel_window.attributes('-fullscreen', True)
            
            colors = ["#FFFFFF", "#000000", "#FF0000", "#00FF00", "#0000FF"]
            current_color = 0
            
            canvas = tk.Canvas(pixel_window, bg=colors[current_color])
            canvas.pack(fill=tk.BOTH, expand=True)
            
            def change_color():
                nonlocal current_color
                current_color = (current_color + 1) % len(colors)
                canvas.config(bg=colors[current_color])
                
                if current_color < len(colors) - 1:
                    pixel_window.after(1000, change_color)
                else:
                    time.sleep(1)
                    pixel_window.destroy()
                    self.log_result("Bozuk Pixel Testi", "Tamamlandı", 
                                   "Test tamamlandı. Ekranda bozuk piksel görürseniz cihazı servise götürün.")
            
            pixel_window.after(1000, change_color)
            
        threading.Thread(target=run_pixel_test).start()
        self.update_status("Bozuk Pixel Testi çalışıyor...")

    def motherboard_led_test(self):
        try:
            # Anakart bilgilerini almak
            motherboard = self.wmi_conn.Win32_BaseBoard()[0]
            manufacturer = motherboard.Manufacturer
            product = motherboard.Product
            
            messagebox.showinfo("Anakart LED Testi", 
                               f"Anakart: {manufacturer} {product}\n\n"
                               "Anakart üzerindeki LED'leri kontrol edin.\n"
                               "Bu test manual bir testtir, LED durumlarını gözlemleyin.")
            
            self.log_result("Anakart LED Testi", "Tamamlandı", 
                           f"Anakart: {manufacturer} {product}")
        except Exception as e:
            self.log_result("Anakart LED Testi", "Hata", str(e))
            
        self.update_status("Anakart LED Testi tamamlandı")

    def buzzer_test(self):
        try:
            # Windows'da sistemin bip sesini çal
            if platform.system() == "Windows":
                winsound_available = True
                try:
                    import winsound
                except ImportError:
                    winsound_available = False
                
                if winsound_available:
                    def play_sounds():
                        for _ in range(3):
                            winsound.Beep(1000, 500)  # 1000 Hz, 500 ms
                            time.sleep(0.5)
                    
                    threading.Thread(target=play_sounds).start()
                    self.log_result("Buzzer Testi", "Tamamlandı", "Windows bip sesi çalındı")
                else:
                    # winsound mevcut değilse alternatif
                    messagebox.showinfo("Buzzer Testi", 
                                      "Bilgisayarınızın dahili hoparlöründen bip sesi duydunuz mu?")
                    self.log_result("Buzzer Testi", "Manuel Kontrol", "Kullanıcı tarafından doğrulanması gerekiyor")
            else:
                # Linux/Mac için komut
                os.system('play -n synth 0.5 sin 1000 vol 0.5')
                self.log_result("Buzzer Testi", "Tamamlandı", "Sistem bip sesi çalındı")
        except Exception as e:
            self.log_result("Buzzer Testi", "Hata", str(e))
            
        self.update_status("Buzzer Testi tamamlandı")

    def cpu_stress_test(self):
        def run_cpu_test():
            try:
                self.update_status("CPU Stress Test başlatılıyor...")
                
                # Test süresi (saniye)
                test_duration = 10
                start_time = time.time()
                
                # CPU kullanım ölçüleri
                cpu_usage_samples = []
                
                # CPU'yu stres etmek için tüm çekirdeklerde işlem yap
                cpu_count = psutil.cpu_count()
                stop_event = threading.Event()
                
                def stress_cpu():
                    while not stop_event.is_set():
                        # Yoğun hesaplama işlemi
                        [random.random() for _ in range(10000000)]
                
                # CPU sayısı kadar thread başlat
                threads = []
                for _ in range(cpu_count):
                    t = threading.Thread(target=stress_cpu)
                    t.daemon = True
                    threads.append(t)
                    t.start()
                    
                # Test süresi boyunca CPU kullanımını ölç
                while time.time() - start_time < test_duration:
                    cpu_percent = psutil.cpu_percent(interval=1)
                    cpu_usage_samples.append(cpu_percent)
                    self.update_status(f"CPU Stress Test: {int(cpu_percent)}% kullanım")
                
                # Tüm threadleri durdur
                stop_event.set()
                for t in threads:
                    t.join(timeout=1)
                
                # Sonuçları değerlendir
                avg_cpu = sum(cpu_usage_samples) / len(cpu_usage_samples)
                max_cpu = max(cpu_usage_samples)
                
                # CPU sıcaklığını almaya çalış (platform bağımlı)
                temp_info = ""
                try:
                    if platform.system() == "Windows":
                        temps = self.wmi_conn.MSAcpi_ThermalZoneTemperature()
                        if temps:
                            # Kelvin'den Celsius'a çevir
                            temp_c = (temps[0].CurrentTemperature / 10.0) - 273.15
                            temp_info = f", Sıcaklık: {temp_c:.1f}°C"
                except:
                    pass
                
                result = "Başarılı" if avg_cpu > 70 else "Uyarı"
                details = f"Ort. CPU Kullanımı: {avg_cpu:.1f}%, Maks: {max_cpu:.1f}%{temp_info}"
                
                self.log_result("CPU Stress Test", result, details)
                self.update_status("CPU Stress Test tamamlandı")
                
            except Exception as e:
                self.log_result("CPU Stress Test", "Hata", str(e))
                self.update_status("CPU Stress Test hata!")
        
        threading.Thread(target=run_cpu_test).start()

    def ram_stress_test(self):
        def run_ram_test():
            try:
                self.update_status("RAM Stress Test başlatılıyor...")
                
                # Sistemdeki toplam RAM'i öğren
                total_ram = psutil.virtual_memory().total / (1024 * 1024 * 1024)  # GB
                
                # Kullanılacak RAM miktarı (toplam RAM'in %50'si)
                target_usage = 29 * 1024 * 1024 * 1024  # 29 GB
                
                # RAM'i doldur
                start_time = time.time()
                data = []
                chunk_size = 512 * 1024 * 1024  # 512 MB
    
                
                allocated = 0
                try:
                    while allocated < target_usage:
                        # 10MB chunk oluştur
                        chunk = bytearray(chunk_size)
                        # Verileri değiştir (gerçek RAM kullanımı için)
                        for i in range(0, len(chunk), 4096):
                            chunk[i] = 1
                        data.append(chunk)
                        allocated += chunk_size
                        
                        # Her 100MB'da bir güncelle
                        if allocated % (100 * 1024 * 1024) == 0:
                            ram_usage = psutil.virtual_memory().percent
                            self.update_status(f"RAM Stress Test: {allocated/(1024*1024):.0f}MB ayrıldı, {ram_usage:.1f}% kullanımda")
                            # Çok fazla RAM kullanmamak için kontrol
                            if ram_usage > 85:
                                break
                except MemoryError:
                    pass
                
                # Test sonuçları
                end_time = time.time()
                test_duration = end_time - start_time
                allocated_mb = allocated / (1024 * 1024)
                
                # RAM kullanımını kontrol et
                ram_info = psutil.virtual_memory()
                
                # Belleği temizle
                data = None
                
                result = "Başarılı"
                details = f"{allocated_mb:.0f}MB RAM test edildi, Süre: {test_duration:.1f} saniye"
                
                self.log_result("RAM Stress Test", result, details)
                self.update_status("RAM Stress Test tamamlandı")
                
            except Exception as e:
                self.log_result("RAM Stress Test", "Hata", str(e))
                self.update_status("RAM Stress Test hata!")
        
        threading.Thread(target=run_ram_test).start()

    def ethernet_test(self):
        def run_ethernet_test():
            try:
                self.update_status("Ethernet Testi başlatılıyor...")
                
                # Internet bağlantısını kontrol et
                has_connection = False
                try:
                    # Bir DNS sunucusuna bağlanmayı dene
                    socket.create_connection(("8.8.8.8", 53), timeout=5)
                    has_connection = True
                except:
                    pass
                
                if not has_connection:
                    self.log_result("Ethernet Testi", "Başarısız", "Internet bağlantısı bulunamadı")
                    self.update_status("Ethernet Testi tamamlandı - Bağlantı yok")
                    return
                
                # Ağ adaptörlerini listele
                network_adapters = []
                for interface, addrs in psutil.net_if_addrs().items():
                    for addr in addrs:
                        if addr.family == socket.AF_INET:  # IPv4
                            network_adapters.append({
                                "interface": interface,
                                "ip": addr.address
                            })
                
                # Internet hızını ölç
                download_speed = 0
                upload_speed = 0
                
                try:
                    # Speedtest modülünü kullanarak internet hızını ölç
                    import speedtest
                    st = speedtest.Speedtest()
                    st.get_best_server()
                    
                    # İndirme hızı
                    self.update_status("Ethernet Testi: İndirme hızı ölçülüyor...")
                    download_speed = st.download() / 1_000_000  # Mbps
                    
                    # Yükleme hızı
                    self.update_status("Ethernet Testi: Yükleme hızı ölçülüyor...")
                    upload_speed = st.upload() / 1_000_000  # Mbps
                    
                except ImportError:
                    # Speedtest modülü yoksa alternatif basit test
                    self.update_status("Ethernet Testi: Basit internet hızı testi yapılıyor...")
                    
                    # Ping testi
                    ping_result = subprocess.run(
                        ["ping", "-c", "4", "google.com" if platform.system() != "Windows" else "-n 4 google.com"], 
                        capture_output=True, 
                        text=True
                    )
                    
                    ping_output = ping_result.stdout
                    ping_time = "N/A"
                    
                    if platform.system() == "Windows":
                        for line in ping_output.split('\n'):
                            if "Average" in line:
                                ping_time = line.split("=")[1].strip()
                                break
                    else:
                        for line in ping_output.split('\n'):
                            if "avg" in line:
                                ping_time = line.split("/")[4]
                                break
                
                # Ağ adaptörlerini string olarak birleştir
                adapters_str = ", ".join([f"{a['interface']} ({a['ip']})" for a in network_adapters])
                
                if download_speed > 0 or upload_speed > 0:
                    result = "Başarılı"
                    details = f"İndirme: {download_speed:.2f} Mbps, Yükleme: {upload_speed:.2f} Mbps\nAdaptörler: {adapters_str}"
                else:
                    result = "Tamamlandı"
                    details = f"Ping: {ping_time}\nAdaptörler: {adapters_str}"
                
                self.log_result("Ethernet Testi", result, details)
                self.update_status("Ethernet Testi tamamlandı")
                
            except Exception as e:
                self.log_result("Ethernet Testi", "Hata", str(e))
                self.update_status("Ethernet Testi hata!")
        
        threading.Thread(target=run_ethernet_test).start()

    def case_light_test(self):
        messagebox.showinfo("Case Light Test", 
                          "Bu test kasadaki LED ışıkları kontrol etmeniz için hatırlatma yapar.\n\n"
                          "Lütfen kasa ışıklarınızı kontrol edin ve doğru çalışıp çalışmadığını onaylayın.")
        
        self.log_result("Case Light Test", "Manuel Kontrol", "Kullanıcı tarafından doğrulanması gerekiyor")
        self.update_status("Case Light Test tamamlandı")

    def webcam_test(self):
        def run_webcam_test():
            try:
                self.update_status("WebCam Testi başlatılıyor...")
                
                # Kamera erişimi
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    self.log_result("WebCam Testi", "Başarısız", "Kameraya erişilemedi")
                    self.update_status("WebCam Testi tamamlandı - Kamera bulunamadı")
                    return
                
                # Kamera özelliklerini al
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                
                # Kamerayı test et
                frame_count = 0
                start_time = time.time()
                
                webcam_window = tk.Toplevel(self.root)
                webcam_window.title("WebCam Test")
                webcam_window.geometry(f"{width}x{height}")
                
                canvas = tk.Canvas(webcam_window, width=width, height=height)
                canvas.pack()
                
                def update_frame():
                    nonlocal frame_count
                    ret, frame = cap.read()
                    
                    if ret:
                        frame_count += 1
                        # OpenCV BGR'den RGB'ye dönüştür
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        photo = tk.PhotoImage(data=ImageTk.PhotoImage(Image.fromarray(frame_rgb)))
                        canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                        canvas.image = photo
                        
                        if time.time() - start_time < 5:  # 5 saniye test
                            webcam_window.after(10, update_frame)
                        else:
                            cap.release()
                            webcam_window.destroy()
                            
                            actual_fps = frame_count / (time.time() - start_time)
                            
                            result = "Başarılı"
                            details = f"Çözünürlük: {width}x{height}, FPS: {actual_fps:.1f}"
                            
                            self.log_result("WebCam Testi", result, details)
                            self.update_status("WebCam Testi tamamlandı")
                    else:
                        cap.release()
                        webcam_window.destroy()
                        self.log_result("WebCam Testi", "Başarısız", "Kamera görüntü alınamadı")
                        self.update_status("WebCam Testi tamamlandı - Görüntü alınamadı")
                
                webcam_window.after(100, update_frame)
                
            except Exception as e:
                try:
                    cap.release()
                except:
                    pass
                self.log_result("WebCam Testi", "Hata", str(e))
                self.update_status("WebCam Testi hata!")
        
        # PIL.ImageTk import edilmeli
        try:
            from PIL import ImageTk
            threading.Thread(target=run_webcam_test).start()
        except ImportError:
            self.log_result("WebCam Testi", "Hata", "PIL.ImageTk modülü yüklü değil")
            self.update_status("WebCam Testi hata!")

    def microphone_test(self):
        def run_mic_test():
            try:
                self.update_status("Mikrofon Testi başlatılıyor...")
                
                # PyAudio ile mikrofon erişimi
                CHUNK = 1024
                FORMAT = pyaudio.paInt16
                CHANNELS = 1
                RATE = 44100
                RECORD_SECONDS = 5
                
                p = pyaudio.PyAudio()
                
                # Mikrofon bilgilerini al
                info = p.get_host_api_info_by_index(0)
                num_devices = info.get('deviceCount')
                
                mic_devices = []
                for i in range(num_devices):
                    device_info = p.get_device_info_by_host_api_device_index(0, i)
                    if device_info.get('maxInputChannels') > 0:
                        mic_devices.append(device_info)
                
                if not mic_devices:
                    self.log_result("Mikrofon Testi", "Başarısız", "Mikrofon bulunamadı")
                    p.terminate()
                    self.update_status("Mikrofon Testi tamamlandı - Mikrofon bulunamadı")
                    return
                
                # İlk mikrofonu kullan
                stream = p.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)
                
                # Kullanıcıya bilgi ver
                messagebox.showinfo("Mikrofon Testi", 
                                  f"Mikrofon kaydı başlatılıyor. Lütfen 5 saniye boyunca konuşun.")
                
                frames = []
                
                # Kayıt
                for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                    data = stream.read(CHUNK)
                    frames.append(data)
                    if i % 10 == 0:
                        self.update_status(f"Mikrofon Testi: Kayıt {i * CHUNK / RATE:.1f}s / {RECORD_SECONDS}s")
                
                stream.stop_stream()
                stream.close()
                p.terminate()
                
                # Ses seviyesini analiz et
                avg_volume = 0
                peak_volume = 0
                
                for frame in frames:
                    # 16-bit değerler olarak yorumla
                    int_data = np.frombuffer(frame, dtype=np.int16)
                    volume = np.abs(int_data).mean()
                    avg_volume += volume
                    peak_volume = max(peak_volume, volume)
                
                avg_volume /= len(frames)
                
                # Sonuçları değerlendir
                if avg_volume > 100:  # Ses algılandı
                    result = "Başarılı"
                    details = f"Ortalama ses seviyesi: {avg_volume:.1f}, Tepe ses seviyesi: {peak_volume:.1f}"
                else:
                    result = "Uyarı"
                    details = f"Ses seviyesi çok düşük. Ortalama: {avg_volume:.1f}, Tepe: {peak_volume:.1f}"
                
                self.log_result("Mikrofon Testi", result, details)
                self.update_status("Mikrofon Testi tamamlandı")
                
            except Exception as e:
                self.log_result("Mikrofon Testi", "Hata", str(e))
                self.update_status("Mikrofon Testi hata!")
        
        threading.Thread(target=run_mic_test).start()

    def monitor_test(self):
        def run_monitor_test():
            try:
                self.update_status("Monitör Testi başlatılıyor...")
                
                # Monitör hakkında bilgi topla
                if platform.system() == "Windows":
                    # WMI ile monitör bilgilerini al
                    monitors = self.wmi_conn.Win32_DesktopMonitor()
                    monitor_info = []
                    
                    for monitor in monitors:
                        if monitor.DeviceID:
                            info = {
                                "name": monitor.Name,
                                "width": monitor.ScreenWidth,
                                "height": monitor.ScreenHeight
                            }
                            monitor_info.append(info)
                else:
                    # Linux/Mac için varsayılan bilgiler
                    monitor_info = [{
                        "name": "Ekran",
                        "width": self.root.winfo_screenwidth(),
                        "height": self.root.winfo_screenheight()
                    }]
                
                # Monitörü kapatıp açma işlemi için kullanıcıya bilgi ver
                answer = messagebox.askyesno("Monitör Testi", 
                                           "Bu test, monitörü kapatıp 10 saniye sonra tekrar açacak.\n"
                                           "Devam etmek istiyor musunuz?")
                
                if not answer:
                    self.log_result("Monitör Testi", "İptal Edildi", "Kullanıcı testi iptal etti")
                    self.update_status("Monitör Testi iptal edildi")
                    return
                
                # Monitör bilgilerini string olarak birleştir
                monitor_str = ", ".join([f"{m['name']} ({m['width']}x{m['height']})" for m in monitor_info])
                
                if platform.system() == "Windows":
                    # Windows'da DPMS komutlarını kullan
                    try:
                        subprocess.run(["powershell", "-Command", "Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class MonitorControl { [DllImport(\"user32.dll\")] public static extern int SendMessage(int hWnd, int hMessage, int wParam, int lParam); }'; [MonitorControl]::SendMessage(0xFFFF, 0x112, 0xF170, 2);"], check=True)
                        
                        time.sleep(10)
                        
                        # Monitörü geri aç
                        subprocess.run(["powershell", "-Command", "Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class MonitorControl { [DllImport(\"user32.dll\")] public static extern int SendMessage(int hWnd, int hMessage, int wParam, int lParam); }'; [MonitorControl]::SendMessage(0xFFFF, 0x112, 0xF170, -1);"], check=True)
                        
                        result = "Başarılı"
                        details = f"Monitör(ler): {monitor_str}"
                    except Exception as e:
                        result = "Uyarı"
                        details = f"Monitör kapatma/açma komutları çalıştırılamadı. Hata: {str(e)}"
                else:
                    # Linux/Mac için
                    messagebox.showinfo("Monitör Testi", 
                                       "Bu işletim sisteminde monitör kontrol desteği sınırlıdır.\n"
                                       "Lütfen monitörünüzü manuel olarak kontrol edin.")
                    result = "Manuel Kontrol"
                    details = f"Monitör(ler): {monitor_str}"
                
                self.log_result("Monitör Testi", result, details)
                self.update_status("Monitör Testi tamamlandı")
                
            except Exception as e:
                self.log_result("Monitör Testi", "Hata", str(e))
                self.update_status("Monitör Testi hata!")
        
        threading.Thread(target=run_monitor_test).start()

    def speakers_test(self):
        def run_speakers_test():
            try:
                self.update_status("Hoparlör Testi başlatılıyor...")
                
                # PyAudio ile hoparlör erişimi
                p = pyaudio.PyAudio()
                
                # Ses cihazlarını listele
                info = p.get_host_api_info_by_index(0)
                num_devices = info.get('deviceCount')
                
                speaker_devices = []
                for i in range(num_devices):
                    device_info = p.get_device_info_by_host_api_device_index(0, i)
                    if device_info.get('maxOutputChannels') > 0:
                        speaker_devices.append(device_info)
                
                if not speaker_devices:
                    self.log_result("Hoparlör Testi", "Başarısız", "Hoparlör bulunamadı")
                    p.terminate()
                    self.update_status("Hoparlör Testi tamamlandı - Hoparlör bulunamadı")
                    return
                
                # Ses parametreleri
                CHUNK = 1024
                FORMAT = pyaudio.paFloat32
                CHANNELS = 2
                RATE = 44100
                DURATION = 3  # saniye
                
                # Test sesi oluştur (sinüs dalgası)
                samples = np.sin(2 * np.pi * np.arange(RATE * DURATION) * 440 / RATE).astype(np.float32)
                
                # Sol ve sağ kanal için farklı frekanslar
                left_channel = np.sin(2 * np.pi * np.arange(RATE * DURATION) * 440 / RATE).astype(np.float32)
                right_channel = np.sin(2 * np.pi * np.arange(RATE * DURATION) * 880 / RATE).astype(np.float32)
                
                # Stereo ses
                stereo_samples = np.vstack((left_channel, right_channel)).T.reshape((-1,))
                
                # Kullanıcıya bilgi ver
                messagebox.showinfo("Hoparlör Testi", 
                                  "Hoparlör testi başlatılıyor.\n"
                                  "Önce sol kanaldan 440Hz, sonra sağ kanaldan 880Hz ses duyacaksınız.")
                
                # Ses akışını başlat
                stream = p.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              output=True)
                
                # Stereo ses çal
                stream.write(stereo_samples.tobytes())
                
                # Akışı kapat
                stream.stop_stream()
                stream.close()
                p.terminate()
                
                # Kullanıcıya sor
                heard_answer = messagebox.askyesno("Hoparlör Testi", 
                                                 "Sol ve sağ hoparlörden farklı sesler duydunuz mu?")
                
                if heard_answer:
                    result = "Başarılı"
                    details = f"Kullanıcı sesi duyduğunu onayladı. {len(speaker_devices)} ses çıkış cihazı mevcut."
                else:
                    result = "Başarısız"
                    details = f"Kullanıcı sesi duymadığını belirtti. {len(speaker_devices)} ses çıkış cihazı mevcut."
                
                self.log_result("Hoparlör Testi", result, details)
                self.update_status("Hoparlör Testi tamamlandı")
                
            except Exception as e:
                self.log_result("Hoparlör Testi", "Hata", str(e))
                self.update_status("Hoparlör Testi hata!")
        
        threading.Thread(target=run_speakers_test).start()

    def antivirus_test(self):
        def run_antivirus_test():
            try:
                self.update_status("AntiVirus Testi başlatılıyor...")
                
                # EICAR test dosyası oluştur (zararsız virüs test dosyası)
                # http://www.eicar.org/download/eicar.com.txt
                eicar_string = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
                
                temp_dir = os.path.join(os.path.expanduser("~"), "temp")
                os.makedirs(temp_dir, exist_ok=True)
                
                test_file_path = os.path.join(temp_dir, "antivirus_test.txt")
                
                # Kullanıcıya bilgi ver
                answer = messagebox.askyesno("AntiVirus Testi", 
                                           "Bu test, antivirüs programınızın çalışıp çalışmadığını kontrol etmek için\n"
                                           "zararsız bir test dosyası oluşturacak. Gerçek bir virüs DEĞİLDİR.\n\n"
                                           "Antivirüs programınız bu dosyayı bir tehdit olarak algılayabilir.\n"
                                           "Devam etmek istiyor musunuz?")
                
                if not answer:
                    self.log_result("AntiVirus Testi", "İptal Edildi", "Kullanıcı testi iptal etti")
                    self.update_status("AntiVirus Testi iptal edildi")
                    return
                
                # Test dosyasını oluştur
                with open(test_file_path, "w") as f:
                    f.write(eicar_string)
                
                # Dosya oluşturuldu mu kontrol et
                if os.path.exists(test_file_path):
                    # Antivirüs tarafından engellenmedi
                    time.sleep(2)  # Antivirüsün tepki vermesi için bekle
                    
                    # Dosya hala duruyor mu kontrol et
                    if os.path.exists(test_file_path):
                        result = "Uyarı"
                        details = "EICAR test dosyası oluşturuldu ve silinmedi. Antivirüs programı çalışmıyor olabilir."
                        
                        # Temizlik
                        try:
                            os.remove(test_file_path)
                        except:
                            pass
                    else:
                        result = "Başarılı"
                        details = "EICAR test dosyası oluşturuldu ve antivirüs tarafından kaldırıldı."
                else:
                    result = "Başarılı"
                    details = "EICAR test dosyası oluşturulamadı. Antivirüs programı engellemiş olabilir."
                
                # ctypes ile mavi ekran testi (gerçek bir mavi ekran oluşturmaz)
                # Alternatif olarak "yapılıyor" mesajı göster
                if result == "Uyarı":
                    # Kullanıcıya bilgi ver
                    answer = messagebox.askyesno("AntiVirus Testi", 
                                               "ctypes ile mavi ekran testi yapmak istiyor musunuz?\n"
                                               "Not: Bu test gerçek mavi ekran oluşturmaz, sadece simülasyon yapar.")
                    
                    if answer:
                        # CTF bayrağı şeklinde bir mesaj göster
                        messagebox.showinfo("ctypes Simülasyon", 
                                          "BSOD Test: KERNEL_SECURITY_CHECK_FAILURE\n"
                                          "Bu bir simülasyondur, gerçek bir mavi ekran oluşturulmadı.")
                        
                        details += "\nctypes BSOD simülasyonu tamamlandı."
                
                self.log_result("AntiVirus Testi", result, details)
                self.update_status("AntiVirus Testi tamamlandı")
                
            except Exception as e:
                self.log_result("AntiVirus Testi", "Hata", str(e))
                self.update_status("AntiVirus Testi hata!")
        
        threading.Thread(target=run_antivirus_test).start()

    def headphones_light_test(self):
        def run_headphones_test():
            try:
                self.update_status("Kulaklık Işık Testi başlatılıyor...")
                
                # USB cihazlarını listele
                usb_devices = []
                
                if platform.system() == "Windows":
                    # Windows için WMI kullan
                    for device in self.wmi_conn.Win32_USBHub():
                        if device.DeviceID:
                            usb_devices.append({
                                "name": device.Name,
                                "id": device.DeviceID
                            })
                else:
                    # Linux için lsusb komutunu kullan
                    try:
                        lsusb_output = subprocess.check_output(["lsusb"], text=True)
                        for line in lsusb_output.split('\n'):
                            if line:
                                parts = line.split()
                                if len(parts) >= 6:
                                    usb_devices.append({
                                        "name": " ".join(parts[6:]),
                                        "id": f"{parts[1]}:{parts[3].rstrip(':')}"
                                    })
                    except:
                        pass
                
                # Kulaklık olabilecek cihazları filtrele
                headphone_devices = []
                keywords = ["headphone", "headset", "kulakl", "audio", "sound", "gaming"]
                
                for device in usb_devices:
                    device_name = device["name"].lower()
                    if any(keyword in device_name for keyword in keywords):
                        headphone_devices.append(device)
                
                if headphone_devices:
                    devices_str = "\n".join([f"- {device['name']}" for device in headphone_devices])
                    messagebox.showinfo("Kulaklık Işık Testi", 
                                      f"Aşağıdaki potansiyel kulaklık cihazları bulundu:\n\n{devices_str}\n\n"
                                      "Lütfen kulaklığınızdaki ışıkları kontrol edin.")
                    
                    result = "Manuel Kontrol"
                    details = f"{len(headphone_devices)} potansiyel kulaklık cihazı bulundu: {devices_str}"
                else:
                    messagebox.showinfo("Kulaklık Işık Testi", 
                                      "Hiçbir kulaklık cihazı bulunamadı.\n"
                                      "Kulaklığınız takılı değilse takın ve testi tekrarlayın.")
                    
                    result = "Uyarı"
                    details = "Kulaklık cihazı bulunamadı."
                
                self.log_result("Kulaklık Işık Testi", result, details)
                self.update_status("Kulaklık Işık Testi tamamlandı")
                
            except Exception as e:
                self.log_result("Kulaklık Işık Testi", "Hata", str(e))
                self.update_status("Kulaklık Işık Testi hata!")
        
        threading.Thread(target=run_headphones_test).start()

    def bluetooth_test(self):
        def run_bluetooth_test():
            try:
                self.update_status("Bluetooth Testi başlatılıyor...")
                
                bluetooth_devices = []
                
                if platform.system() == "Windows":
                    # Windows için WMI kullan
                    for device in self.wmi_conn.Win32_PnPEntity():
                        if device.Name and "bluetooth" in device.Name.lower():
                            bluetooth_devices.append({
                                "name": device.Name,
                                "id": device.DeviceID
                            })
                else:
                    # Linux için hcitool komutunu kullan
                    try:
                        bt_output = subprocess.check_output(["hcitool", "dev"], text=True)
                        for line in bt_output.split('\n')[1:]:  # İlk satırı atla
                            if line.strip():
                                parts = line.strip().split()
                                if len(parts) >= 2:
                                    # Bağlı cihazları listele
                                    try:
                                        scan_output = subprocess.check_output(["hcitool", "-i", parts[0], "scan"], text=True)
                                        for scan_line in scan_output.split('\n')[1:]:
                                            if scan_line.strip():
                                                scan_parts = scan_line.strip().split()
                                                if len(scan_parts) >= 2:
                                                    bluetooth_devices.append({
                                                        "name": " ".join(scan_parts[1:]),
                                                        "id": scan_parts[0]
                                                    })
                                    except:
                                        bluetooth_devices.append({
                                            "name": f"Bluetooth Adapter {parts[0]}",
                                            "id": parts[1]
                                        })
                    except:
                        pass
                
                # Bağlı Bluetooth cihazlarını liste
                if bluetooth_devices:
                    devices_str = "\n".join([f"- {device['name']}" for device in bluetooth_devices])
                    messagebox.showinfo("Bluetooth Testi", 
                                      f"Aşağıdaki Bluetooth cihazları bulundu:\n\n{devices_str}")
                    
                    result = "Başarılı"
                    details = f"{len(bluetooth_devices)} Bluetooth cihazı bulundu: {devices_str}"
                else:
                    answer = messagebox.askyesno("Bluetooth Testi", 
                                               "Hiçbir Bluetooth cihazı bulunamadı.\n"
                                               "Bluetooth'unuz açık mı?")
                    
                    if answer:
                        result = "Uyarı"
                        details = "Bluetooth açık olduğu halde cihaz bulunamadı."
                    else:
                        result = "Bilgi"
                        details = "Bluetooth kapalı veya desteklenmiyor."
                
                self.log_result("Bluetooth Testi", result, details)
                self.update_status("Bluetooth Testi tamamlandı")
                
            except Exception as e:
                self.log_result("Bluetooth Testi", "Hata", str(e))
                self.update_status("Bluetooth Testi hata!")
        
        threading.Thread(target=run_bluetooth_test).start()

    def all_in_one_test(self):
        def run_all_tests():
            try:
                self.update_status("ALL IN ONE TEST başlatılıyor...")
                self.result_text.delete(1.0, tk.END)
                self.log_result("ALL IN ONE TEST", "Başlatılıyor", "Tüm testler sırayla çalıştırılacak")
                
                # Tüm testleri sırayla çalıştır
                for test in self.tests:
                    self.update_status(f"ALL IN ONE TEST: {test['name']} çalıştırılıyor...")
                    test['function']()
                    time.sleep(1)  # Testler arasında kısa bir bekleme
                
                # Test sonuçlarını özetle
                passed = sum(1 for result in self.test_results.values() if result["result"] in ["Başarılı", "Tamamlandı"])
                warnings = sum(1 for result in self.test_results.values() if result["result"] == "Uyarı")
                failed = sum(1 for result in self.test_results.values() if result["result"] == "Başarısız")
                errors = sum(1 for result in self.test_results.values() if result["result"] == "Hata")
                
                summary = f"Toplam {len(self.tests)} test tamamlandı:\n"
                summary += f"Başarılı: {passed}, Uyarı: {warnings}, Başarısız: {failed}, Hata: {errors}"
                
                self.log_result("ALL IN ONE TEST", "Tamamlandı", summary)
                self.update_status("ALL IN ONE TEST tamamlandı")
                
                # Sonuç raporu
                messagebox.showinfo("ALL IN ONE TEST", f"Tüm testler tamamlandı.\n\n{summary}")
                
            except Exception as e:
                self.log_result("ALL IN ONE TEST", "Hata", str(e))
                self.update_status("ALL IN ONE TEST hata!")
        
        threading.Thread(target=run_all_tests).start()

def main():
    root = tk.Tk()
    app = HardwareTestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
