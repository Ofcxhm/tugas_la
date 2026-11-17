import csv
import re
from datetime import datetime
from pathlib import Path

FILE_TXT = Path("data_mahasiswa.txt")
FILE_CSV = Path("data_mahasiswa.csv")
GARIS = "=" * 50
TIPIS = "=" * 50
JURUSAN = ["Teknik Informatika", "Teknik Elektro", "Teknik Mesin", "Teknik Industri", "Argoteknologi"]

#penyimpanan 
KUNCI = [("nama", "Nama"), ("npm", "NPM"), ("jurusan", "Jurusan"), ("email", "Email"), ("ipk", "IPK"), ("dibuat", "Dibuat")]

def muat_data():
    """Baca File TXT: Agar Tiap Mahasiswa di pisah oleh garis '----',"""
    if not FILE_TXT.exists():
        return []
    data, rec = [], {}
    try:
        with open(FILE_TXT, "r", encoding="utf-8") as f:
            for baris in f:
                baris = baris.strip()
                if baris.startswith("----"):
                    if rec:
                        data.append(rec)
                        rec = {}
                elif ":" in baris:
                    kunci, _, nilai = baris.partition(":")
                    for k, label in KUNCI:
                        if kunci.strip() == label:
                            rec[k] = float(nilai) if k == "ipk" else nilai.strip()
    except (OSError, ValueError) as e:
        print(f"[!] Gagal Membaca {FILE_TXT}: {e}")
        return []
    return data

def simpan_data(data):
    """Tulis seluruh data ke file TXT"""
    try:
        with open(FILE_TXT, "w", encoding="utf-8") as f:
            f.write(f"DATA MAHASISWA\n{GARIS}\n")
            for m in data:
                for k, label in KUNCI:
                    nilai = f"{m[k]:.2f}" if k == "ipk" else m[k]
                    f.write(f"{label:<8}: {nilai}\n")
                f.write(TIPIS + "\n")
        return True
    except OSError as e:
        print(f"[!] Gagal menyimpan data: {e}")
        return False

#validasi data
def valid_nama(s):
    return len(s) >= 3 and all(c.isalpha() or c in " .'-" for c in s)

def valid_npm(s):
    return s.isdigit() and 8 <= len(s) <= 12

def valid_email(s):
    return re.fullmatch(r"[\w+-]+@[\w-]+(\.[\w-]+)+", s) is not None

def valid_ipk(s):
    try:
        return 0.0 <= float(s.replace(",", ".")) <= 4.0
    except ValueError:
        return False

#inputtt
def input_wajib(label, validator=None, error="Input tidak valid.", default=None):
    """Ulangi input sampai valid. Enter memakai default jika ada."""
    while True:
        hint = f" [{default}]" if default is not None else ""
        nilai = input(f"{label}{hint}: ").strip()
        if not nilai and default is not None:
            return str(default)
        if not nilai:
            print("  -> Tidak boleh kosong.")
        elif validator and not validator(nilai):
            print(f"  -> {error}")
        else:
            return nilai

def pilih_jurusan(default=None):
    print("Silahkan Pilih Jurusan Anda")
    for i, j in enumerate(JURUSAN, 1):
        print(f" {i}, {j}")
    while True:
        teks = input("Nomor" + (f" [{default}]" if default else"") + ": ").strip()
        if not teks and default:
            return default
        if teks.isdigit() and 1 <= int(teks) <= len(JURUSAN):
            return JURUSAN[int(teks) - 1]
        print(" -> Pilihan Jurusan Tidak Tersedia")

def konfirmasi(tanya):
    return input(f"{tanya} (y/n): ").strip().lower() == "y"

def judul(teks):
    print(f"\n{GARIS}\n {teks}\n{GARIS}")

#Tampilan nya
def cetak(m, nomor=None):
    awal = f"[{nomor}] " if nomor else ""
    print(f"{awal}Nama    : {m['nama']}")
    print(f"    NPM     : {m['npm']}")
    print(f"    Jurusan : {m['jurusan']}")
    print(f"    Email   : {m['email']}")
    print(f"    IPK     : {m['ipk']:.2f}")
    print(TIPIS)

def cari_npm(data, npm):
    return next((m for m in data if m["npm"] == npm), None)

#Fitur
def tambah(data):
    judul("TAMBAH DATA MAHASISWA")
    npm = input_wajib("NPM (8-12 Digit)", valid_npm, "NPM Harus 8-12 Digit")
    if cari_npm(data, npm):
        print("[!] NPM Sudah terdaftar.")
        return
    nama = input_wajib("Nama", valid_nama, "Minimal 3 Huruf tanpa angka.").title()
    jurusan = pilih_jurusan()
    email = input_wajib("Email", valid_email, "Format email tidak valid.")
    ipk = float(input_wajib("IPK (0-4)", valid_ipk, "IPK harus 0-4.").replace(",", "."))
    data.append({
        "npm": npm, "nama": nama, "jurusan": jurusan, "email": email,
        "ipk": ipk, "dibuat": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    if simpan_data(data):
        print("\nData berhasil disimpan!")

def tampilkan(data):
    judul(f"DAFTAR MAHASISWA ({len(data)} data)")
    if not data:
        print("Belum ada data.")
    for i, m in enumerate(sorted(data, key=lambda x: x["nama"]), 1):
        cetak(m, i)

def cari(data):
    judul("CARI MAHASISWA")
    kata = input("NPM atau sebagian nama: ").strip().lower()
    hasil = [m for m in data if kata in m["npm"] or kata in m["nama"].lower()]
    if not hasil:
        print("Data tidak ditemukan.")
        return
    print(f"Ditemukan {len(hasil)} data:\n")
    for i, m in enumerate(hasil, 1):
        cetak(m, i)

def ubah(data):
    judul("UBAH DATA MAHASISWA")
    m = cari_npm(data, input("NPM Yang diubah: ").strip())
    if not m:
        print("Data tidak ditemukan!")
        return
    print("Tekan Enter untuk mempertahankan nilai lama.\n")
    m["nama"] = input_wajib("Nama", valid_nama, "Nama tidak valid.", m["nama"]).title()
    m["jurusan"] = pilih_jurusan(m["jurusan"])
    m["email"] = input_wajib("Email", valid_email, "Email tidak valid.", m["email"])
    m["ipk"] = float(input_wajib("IPK", valid_ipk, "IPK harus 0-4.", m["ipk"]).replace(",", "."))
    if simpan_data(data):
        print("\nData berhasil diperbarui!")

def hapus(data):
    judul("HAPUS DATA MAHASISWA")
    m = cari_npm(data, input("NPM yang dihapus: ").strip())
    if not m:
        print("Data tidak ditemukan.")
        return
    cetak(m)
    if konfirmasi("Yakin ingin menghapus?"):
        data.remove(m)
        if simpan_data(data):
            print("Data berhasil dihapus.")
    else:
        print("Dibatalkan.")

def ekspor_csv(data):
    if not data:
        print("Tidak ada data untuk diekspor.")
        return
    try:
        with open(FILE_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(data[0].keys()))
            w.writeheader()
            w.writerows(data)
        print(f"Berhasil diekspor ke '{FILE_CSV}'.")
    except OSError as e:
        print(f"[!] Gagal ekspor: {e}")


def statistik(data):
    judul("STATISTIK")
    if not data:
        print("Belum ada data.")
        return
    ipk = [m["ipk"] for m in data]
    terbaik = max(data, key=lambda m: m["ipk"])
    print(f"Jumlah mahasiswa : {len(data)}")
    print(f"Rata-rata IPK    : {sum(ipk) / len(ipk):.2f}")
    print(f"IPK tertinggi    : {terbaik['ipk']:.2f} ({terbaik['nama']})")
    print(f"IPK terendah     : {min(ipk):.2f}")


# ---------- Menu ----------
MENU = {
    "1": ("Tambah data", tambah),
    "2": ("Tampilkan semua data", tampilkan),
    "3": ("Cari data", cari),
    "4": ("Ubah data", ubah),
    "5": ("Hapus data", hapus),
    "6": ("Ekspor ke CSV", ekspor_csv),
    "7": ("Statistik", statistik),
}


def main():
    data = muat_data()
    while True:
        judul("APLIKASI DATA MAHASISWA")
        for kode, (nama, _) in MENU.items():
            print(f" {kode}. {nama}")
        print(" 0. Keluar")
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "0":
            print("Terima kasih. Sampai jumpa!")
            break
        if pilihan in MENU:
            MENU[pilihan][1](data)
        else:
            print("[!] Menu tidak tersedia.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan oleh pengguna.")
