
import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import itertools
import threading
import time
import sys

def show_about():
    """Menampilkan informasi lengkap tentang aplikasi."""
    clear_console()
    print("=" * 40)
    print("              Tentang Video Splitter              ")
    print("=" * 40)

    # 📌 Pengenalan
    print("\n📌 Pengenalan")
    print("   Video Splitter adalah aplikasi yang membantu pengguna")
    print("   membagi (split) dan menggabungkan (merge) video dengan")
    print("   mudah menggunakan FFmpeg.")

    # ⚙️ Cara Kerja
    print("\n⚙️  Cara Kerja")
    print("   - Untuk *split*, video akan dipotong menjadi beberapa bagian")
    print("     berdasarkan ukuran yang ditentukan.")
    print("   - Untuk *merge*, beberapa file video akan digabungkan menjadi satu.")

    # 🛠️ Langkah-Langkah Penggunaan
    print("\n🛠️  Langkah-Langkah")
    print("   1️⃣ Pilih opsi yang diinginkan:")
    print("      - *Split Video*: Memisahkan video menjadi beberapa bagian.")
    print("      - *Merge Video*: Menggabungkan beberapa video menjadi satu.")
    print("   2️⃣ Pilih file yang ingin diolah.")
    print("   3️⃣ Ikuti petunjuk di layar untuk menyelesaikan proses.")
    print("   4️⃣ Hasil akan tersimpan di lokasi yang sama dengan file asli.")

    # 🎉 Pesan Terima Kasih
    print("\n🎉 Terima Kasih")
    print("   Terima kasih telah menggunakan Video Splitter!")
    print("   Jika ada masukan atau pertanyaan, kunjungi halaman GitHub kami.")

    # 🔗 Info Developer & GitHub
    print("\n👤 Dibuat oleh: Developer Anda")
    print("📅 Versi: 1.0.0")
    print("🔗 GitHub: https://github.com/username/video-splitter")

    print("=" * 40)
    input("Tekan Enter untuk kembali ke menu...")
    clear_console()


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

def get_video_duration(video_path):
    """Mengambil durasi video dalam detik."""
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "format=duration", "-of", "csv=p=0",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def get_video_codec(video_path):
    """Mengambil codec video untuk memastikan kompatibilitas saat merge."""
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "csv=p=0",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def validate_path(path, should_be_file=True):
    """Memeriksa apakah path valid dan sesuai tipe yang diharapkan."""
    if not os.path.exists(path):
        print(f"Error: Path tidak ditemukan - {path}")
        return False
    if should_be_file and not os.path.isfile(path):
        print(f"Error: Path harus berupa file, bukan folder - {path}")
        return False
    if not should_be_file and not os.path.isdir(path):
        print(f"Error: Path harus berupa folder, bukan file - {path}")
        return False
    return True


def clear_console():
    """Membersihkan semua output di console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def set_console_title(title):
    """Mengatur title pada console."""
    os.system(f"title {title}" if os.name == "nt" else f'echo -ne "\033]0;{title}\007"')


def loading_animation(message="Loading", delay=0.1):
    """Menampilkan animasi loading hingga dihentikan."""
    stop_loading = False

    def animate():
        for frame in itertools.cycle(["|", "/", "-", "\\"]):
            if stop_loading:
                break
            sys.stdout.write(f"\r{message} {frame}")
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\r\033[K")  # Hapus seluruh baris setelah animasi berhenti
        sys.stdout.flush()

    thread = threading.Thread(target=animate)
    thread.start()

    def stop():
        nonlocal stop_loading
        stop_loading = True
        thread.join()

    return stop


if __name__ == "__main__":
    clear_console()
    set_console_title("Video Splitter")

    while True:
        print("=" * 40)
        print("         Selamat Datang di Video Splitter         ")
        print("=" * 40)
        print("Aplikasi ini memungkinkan Anda untuk membagi atau\nmenggabungkan video dengan mudah.")
        print("=" * 40)

        print("\nPilih opsi:")
        print("1. Split Video")
        print("2. Merge Video")
        print("3. About")
        print("4. Keluar")

        choice = input("Masukkan pilihan (1/2/3/4): ").strip()

        if choice == "1":
            split_video()
        elif choice == "2":
            merge_videos()
        elif choice == "3":
            show_about()
        elif choice == "4":
            print("\nTerima kasih telah menggunakan Video Splitter! ")
            sys.exit(0)  # Keluar dengan aman
        else:
            clear_console()
            print("Pilihan tidak valid! \n")