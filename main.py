import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import os
import webbrowser
import platform

def download_content():
    url = url_entry.get()
    save_path = os.path.join(os.getcwd(), 'downloads')  # İndirme dizini
    os.makedirs(save_path, exist_ok=True)  # Klasör yoksa oluştur

    if not url:
        messagebox.showwarning("Input Error", "Please enter a YouTube video URL.")
        return

    download_button.config(state=tk.DISABLED)
    progress_bar.pack(fill=tk.X, padx=20, pady=10)
    progress_label.pack(fill=tk.X, padx=20, pady=(0, 10))

    def run_download():
        download_type = download_type_var.get()

        if download_type == "Video":
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': f'{save_path}/%(title)s.%(ext)s',
                'noplaylist': True,
                'progress_hooks': [progress_hook],
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                },
            }
        elif download_type == "Audio":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{save_path}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                },
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Download Complete", f"{download_type} downloaded successfully to {save_path}!")
            update_download_list()  # Listeyi güncelle
        except Exception as e:
            messagebox.showerror("Download Error", str(e))
        finally:
            progress_bar.pack_forget()
            progress_label.pack_forget()
            download_button.config(state=tk.NORMAL)

    threading.Thread(target=run_download).start()

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
        if total > 0:
            percentage = downloaded / total * 100
            progress_bar['value'] = percentage
            progress_label.config(text=f"{percentage:.2f}%")
            app.update_idletasks()
    elif d['status'] == 'finished':
        progress_label.config(text="Completed")
        progress_bar['value'] = 100
        app.update_idletasks()

def enable_ctrl_a(event):
    event.widget.select_range(0, tk.END)
    return 'break'

def open_website(event):
    webbrowser.open_new("https://emreylmz.com")

def update_download_list():
    download_listbox.delete(0, tk.END)  # Mevcut listeyi temizle
    download_dir = os.path.join(os.getcwd(), 'downloads')
    if os.path.exists(download_dir):
        for file_name in os.listdir(download_dir):
            download_listbox.insert(tk.END, file_name)

def open_folder(event):
    selected_file = download_listbox.get(download_listbox.curselection())
    file_path = os.path.join(os.getcwd(), 'downloads', selected_file)
    if os.path.exists(file_path):
        folder_path = os.path.dirname(file_path)
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{folder_path}"')
        else:  # Linux
            os.system(f'xdg-open "{folder_path}"')

# Ana Pencere
app = tk.Tk()
app.title("YouTube Downloader")
app.geometry("600x500")

# Modern ve aydınlık tema renkleri
bg_color = "#EAEAEA"
fg_color = "#333333"
button_color = "#4CAF50"
button_hover = "#45A049"
entry_bg = "#FFFFFF"
entry_fg = "#000000"

app.configure(bg=bg_color)

# Stiller
style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Arial", 12))
style.configure("TButton", background=button_color, foreground="#FFFFFF", font=("Arial", 12), padding=10, relief="flat")
style.map("TButton", background=[('active', button_hover)])
style.configure("TEntry", fieldbackground=entry_bg,foreground=entry_fg, font=("Arial", 12), insertcolor=entry_fg, relief="flat")
style.configure("TProgressbar", background=button_color, troughcolor=bg_color, relief="flat")

# Başlık
title_label = ttk.Label(app, text="YouTube Downloader", font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)

# URL Label and Entry
url_label = ttk.Label(app, text="Video URL:")
url_label.pack(anchor=tk.W, padx=20, pady=(10, 0))

url_entry = ttk.Entry(app, width=60)
url_entry.pack(fill=tk.X, padx=20, pady=(0, 10))
url_entry.bind("<Control-a>", enable_ctrl_a)

# Download Type Selection
download_type_var = tk.StringVar(value="Video")
download_type_frame = ttk.Frame(app)
download_type_frame.pack(fill=tk.X, padx=20, pady=10)

video_radio = ttk.Radiobutton(download_type_frame, text="Video", variable=download_type_var, value="Video")
audio_radio = ttk.Radiobutton(download_type_frame, text="Audio (MP3)", variable=download_type_var, value="Audio")

video_radio.pack(side=tk.LEFT, padx=10)
audio_radio.pack(side=tk.LEFT, padx=10)

# Download Button
download_button = ttk.Button(app, text="Download", command=download_content)
download_button.pack(pady=10)

# Progress Bar and Label
progress_bar = ttk.Progressbar(app, orient=tk.HORIZONTAL, mode='determinate', length=400, style="TProgressbar")
progress_label = ttk.Label(app, text="", width=10, background=bg_color)

# İndirilen Videolar Listesi ve Scrollbar
list_frame = ttk.Frame(app)
list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

download_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
download_listbox.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=download_listbox.yview)

download_listbox.bind('<Double-1>', open_folder)

# Emre YILMAZ hayratıdır label
footer_label = tk.Label(app, text="Emre YILMAZ hayratıdır", fg="blue", cursor="hand2", bg=bg_color)
footer_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)
footer_label.bind("<Button-1>", open_website)

# Uygulama başladığında indirilen dosyaları listele
update_download_list()

app.mainloop()
