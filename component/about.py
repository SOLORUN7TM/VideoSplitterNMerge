from component.utils import clear_console


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
