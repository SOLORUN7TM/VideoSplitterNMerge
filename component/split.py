import os
import subprocess
import time
import tkinter as tk
from tkinter import filedialog

from component.utils import validate_path, get_video_duration, clear_console, loading_animation


def split_video():
    """Membagi video menjadi beberapa bagian sesuai ukuran per part (MB) dengan fallback ke CLI."""
    clear_console()
    video_path = ""
    try:
        root = tk.Tk()
        root.withdraw()
        video_path = filedialog.askopenfilename(title="Pilih file video untuk di-split")
    except:
        print("Gagal membuka file dialog, silakan masukkan path file secara manual.")

    if not video_path:
        video_path = input("Masukkan path ke file video: ")

    if not validate_path(video_path, should_be_file=True):
        return

    part_size_mb = float(input("Masukkan ukuran per part (MB): "))
    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    duration = get_video_duration(video_path)

    if file_size_mb <= part_size_mb:
        print("File sudah lebih kecil dari ukuran yang diminta.")
        return

    num_parts = int(file_size_mb // part_size_mb) + 1
    part_duration = duration / num_parts

    base_name, ext = os.path.splitext(video_path)
    part_files = [f"{base_name}_part{i + 1}{ext}" for i in range(num_parts)]

    clear_console()
    print(f"File yang dipilih: {video_path} ({file_size_mb:.2f} MB)")
    print("File hasil split:")
    for i, file in enumerate(part_files):
        # Simulate the size of each part
        if i < num_parts - 1:
            part_file_size_mb = part_size_mb
        else:
            part_file_size_mb = file_size_mb - (part_size_mb * (num_parts - 1))
        print(f" - {file} ({part_file_size_mb:.2f} MB)")

    confirm = input("Lanjutkan? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Dibatalkan.")
        return

    # Cek apakah ada file hasil split yang sudah ada
    existing_files = [file for file in part_files if os.path.exists(file)]

    if existing_files:
        pilihan = input(f"{len(existing_files)} file hasil split sudah ada. Overwrite semua? (y/n): ").strip().lower()
        if pilihan != 'y':
            print("Split dibatalkan.")
            return  # Keluar dari fungsi jika pengguna tidak ingin overwrite

    # Proses split
    for i in range(num_parts):
        start_time = i * part_duration
        output_file = part_files[i]

        cmd = [
            "ffmpeg", "-i", video_path, "-ss", str(start_time), "-t", str(part_duration),
            "-c", "copy", output_file, "-y", "-loglevel", "quiet"
        ]

        stop_loading = loading_animation("Splitting video")  # Mulai animasi
        try:
            subprocess.run(cmd)
        finally:
            stop_loading()  # Hentikan animasi
            print("\033[K", end="")  # Paksa hapus baris animasi secara eksplisit


    clear_console()
    print("Split selesai.")
    print("File hasil split disimpan di:")
    for file in part_files:
        print(f" - {os.path.abspath(file)}")

