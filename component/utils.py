import os
import subprocess
import itertools
import threading
import time
import sys

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
