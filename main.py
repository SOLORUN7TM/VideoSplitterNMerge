from component.about import show_about
from component.merge import merge_videos
from component.split import split_video
from component.utils import clear_console, set_console_title
import sys

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
