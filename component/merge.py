import os
import subprocess
import tkinter as tk
from tkinter import filedialog

from component.utils import validate_path, clear_console, loading_animation


def merge_videos():
    """Menggabungkan beberapa file video yang dipilih pengguna dengan fallback ke CLI."""
    clear_console()
    selected_files = []  # Inisialisasi variabel lebih awal

    try:
        root = tk.Tk()
        root.withdraw()
        files = filedialog.askopenfilenames(title="Pilih file video yang akan digabungkan")
        if files:
            selected_files = list(files)
    except:
        print("Gagal membuka file dialog, silakan masukkan path folder secara manual.")

    if not selected_files:
        folder_path = input("Masukkan path folder yang berisi file: ")
        if not validate_path(folder_path, should_be_file=False):
            return

        all_files = os.listdir(folder_path)
        if not all_files:
            print("Tidak ada file di folder tersebut.")
            return

        print("Pilih file yang ingin digabungkan dengan memasukkan nomor (pisahkan dengan koma):")
        for idx, file in enumerate(all_files, start=1):
            print(f"{idx}. {file}")

        selected_numbers = input("Masukkan nomor file yang ingin digabungkan (contoh: 1,2,3): ")
        try:
            selected_indices = [int(num.strip()) - 1 for num in selected_numbers.split(",") if num.strip().isdigit()]
            selected_files = [os.path.join(folder_path, all_files[i]) for i in selected_indices if
                              0 <= i < len(all_files)]
        except:
            print("Input tidak valid.")
            return

    if len(selected_files) < 2:
        print("Merge membutuhkan minimal 2 file.")
        return

    for file in selected_files:
        if not validate_path(file, should_be_file=True):
            return

    clear_console()
    print("File yang dipilih:")
    total_size_mb = 0
    for file in selected_files:
        file_size_mb = os.path.getsize(file) / (1024 * 1024)
        total_size_mb += file_size_mb
        print(f" - {file} ({file_size_mb:.2f} MB)")

    base_name, ext = os.path.splitext(selected_files[0])
    output_file = f"{base_name}_merged{ext}"
    # Simulate the merged file size as the sum of all selected files
    print(f"File hasil merge: {output_file} ({total_size_mb:.2f} MB)")

    confirm = input("Lanjutkan? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Dibatalkan.")
        return

    list_file = "file_list.txt"
    with open(list_file, "w") as f:
        for file in selected_files:
            f.write(f"file '{file}'\n")

    # Cek apakah file hasil merge sudah ada
    if os.path.exists(output_file):
        pilihan = input(f"File {output_file} sudah ada. Overwrite? (y/n): ").strip().lower()
        if pilihan != 'y':
            print("Merge dibatalkan.")
            return  # Keluar dari fungsi jika pengguna tidak ingin overwrite

    cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", output_file, "-y", "-loglevel", "quiet"]
    stop_loading = loading_animation("Splitting video")  # Mulai animasi
    subprocess.run(cmd)
    stop_loading()  # Hentikan animasi
    print("\033[K", end="")  # Paksa hapus baris animasi secara eksplisit
    os.remove(list_file)

    clear_console()
    print(f"Merge selesai: {output_file}")
