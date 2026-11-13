# Program Daftar Nama Mahasiswa (data tersimpan + pakai tuple)

NAMA_FILE = "mahasiswa.txt"

# TUPLE: isinya tidak bisa diubah, cocok untuk data yang tetap
DAFTAR_AWAL = ("Umar", "Fazli", "Hilal", "Eza", "Edo")
MENU = ("Lihat daftar", "Tambah nama", "Hapus nama", "Keluar")

# LIST: isinya bisa berubah (tambah/hapus), jadi dipakai untuk daftar utama
mahasiswa = []


def simpan_semua():
    # Mode "w" = tulis ulang seluruh isi file (dipakai setelah menghapus nama)
    with open(NAMA_FILE, "w") as file:
        for nama in mahasiswa:
            file.write(nama + "\n")


# Saat program dibuka: baca data dari file
try:
    with open(NAMA_FILE, "r") as file:
        for baris in file:
            nama = baris.strip()
            if nama != "":
                mahasiswa.append(nama)
except FileNotFoundError:
    # Pertama kali dijalankan: ubah tuple jadi list supaya bisa diubah-ubah
    mahasiswa = list(DAFTAR_AWAL)
    simpan_semua()


def tampilkan():
    print("\n=== DAFTAR NAMA MAHASISWA ===")
    if len(mahasiswa) == 0:
        print("Daftar masih kosong.")
    else:
        for nomor, nama in enumerate(mahasiswa, start=1):
            print(f"{nomor}. {nama}")
        print(f"Total: {len(mahasiswa)} mahasiswa")


def tambah():
    nama = input("Masukkan nama yang ingin ditambahkan: ").strip().title()
    if nama == "":
        print("Nama tidak boleh kosong!")
    elif nama in mahasiswa:
        print(f"{nama} sudah ada di daftar.")
    else:
        mahasiswa.append(nama)
        # Mode "a" (append) = tambah di akhir file tanpa menghapus isi lama
        with open(NAMA_FILE, "a") as file:
            file.write(nama + "\n")
        print(f"{nama} berhasil ditambahkan dan disimpan.")


def hapus():
    nama = input("Masukkan nama yang ingin dihapus: ").strip().title()
    if nama in mahasiswa:
        mahasiswa.remove(nama)
        simpan_semua()
        print(f"{nama} berhasil dihapus dan disimpan.")
    else:
        print(f"{nama} tidak ditemukan.")


# Program utama: menu berulang sampai pengguna memilih keluar
while True:
    print("\n--- MENU ---")
    # Menu diambil dari tuple MENU, nomornya otomatis
    for nomor, isi_menu in enumerate(MENU, start=1):
        print(f"{nomor}. {isi_menu}")

    pilihan = input(f"Pilih menu (1-{len(MENU)}): ")

    if pilihan == "1":
        tampilkan()
    elif pilihan == "2":
        tambah()
    elif pilihan == "3":
        hapus()
    elif pilihan == "4":
        print("Terima kasih!")
        break
    else:
        print("Pilihan tidak valid, coba lagi.")