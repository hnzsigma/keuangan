import json
import os
from datetime import datetime

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "keuangan.json")
WISHLIST_FILE = os.path.join(DATA_DIR, "wishlist.json")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"transaksi": [], "saldo": 0}
    return {"transaksi": [], "saldo": 0}

def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_wishlist():
    if os.path.exists(WISHLIST_FILE):
        try:
            with open(WISHLIST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_wishlist(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(WISHLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def format_rupiah(jumlah):
    return f"Rp {jumlah:,}".replace(",", ".")

def hari_indonesia(hari):
    mapping = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
    }
    return mapping.get(hari, hari)

def jeda():
    input("\n[Tekan Enter untuk melanjutkan...]")

def header(judul):
    clear_screen()
    print("=" * 42)
    print(f" {judul.center(40)} ")
    print("=" * 42)

def tambah_transaksi(data):
    header("TAMBAH TRANSAKSI BARU")
    print("  [1] Pemasukan")
    print("  [2] Pengeluaran")
    
    jenis_pil = input("\n[?] Pilih jenis [1/2]: ").strip()
    if jenis_pil == "1":
        jenis = "pemasukan"
    elif jenis_pil == "2":
        jenis = "pengeluaran"
    else:
        print("\n[-] Pilihan tidak valid.")
        jeda()
        return

    try:
        jumlah_input = input("[?] Jumlah (contoh: 50000 atau 50.000): ").replace(".", "").replace("Rp", "").strip()
        jumlah = int(jumlah_input)
        if jumlah <= 0:
            raise ValueError
    except ValueError:
        print("\n[-] Jumlah harus berupa angka positif yang valid.")
        jeda()
        return

    keterangan = input("[?] Keterangan / Deskripsi: ").strip()
    if not keterangan:
        print("\n[-] Keterangan wajib diisi.")
        jeda()
        return

    waktu = datetime.now()
    transaksi = {
        "tanggal": waktu.strftime("%Y-%m-%d"),
        "waktu": waktu.strftime("%H:%M:%S"),
        "hari": hari_indonesia(waktu.strftime("%A")),
        "jenis": jenis,
        "jumlah": jumlah,
        "keterangan": keterangan
    }

    data["transaksi"].append(transaksi)
    data["saldo"] += jumlah if jenis == "pemasukan" else -jumlah
    save_data(data)

    print("\n[+] Transaksi berhasil ditambahkan!")
    jeda()

def lihat_riwayat(data):
    header("RIWAYAT TRANSAKSI")
    if not data["transaksi"]:
        print("\n[i] Belum ada catatan transaksi.")
        jeda()
        return

    print(f"{'No':<3} | {'Tanggal':<10} | {'Jenis':<11} | {'Jumlah':<15} | {'Keterangan'}")
    print("-" * 65)

    total_masuk = 0
    total_keluar = 0

    for i, t in enumerate(data["transaksi"], 1):
        if t["jenis"] == "pemasukan":
            jml_str = "+" + format_rupiah(t["jumlah"])
            total_masuk += t["jumlah"]
        else:
            jml_str = "-" + format_rupiah(t["jumlah"])
            total_keluar += t["jumlah"]
            
        print(f"{i:<3} | {t['tanggal']:<10} | {t['jenis']:<11} | {jml_str:<15} | {t['keterangan']}")

    print("-" * 65)
    print(f" Total Pemasukan  : {format_rupiah(total_masuk)}")
    print(f" Total Pengeluaran: {format_rupiah(total_keluar)}")
    print(f" Saldo Akhir      : {format_rupiah(data['saldo'])}")
    print("=" * 65)
    jeda()

def hapus_transaksi(data):
    header("HAPUS TRANSAKSI")
    if not data["transaksi"]:
        print("\n[i] Belum ada transaksi untuk dihapus.")
        jeda()
        return

    for i, t in enumerate(data["transaksi"], 1):
        tanda = "+" if t["jenis"] == "pemasukan" else "-"
        print(f"[{i}] {t['tanggal']} | {t['jenis'].upper()} | {tanda}{format_rupiah(t['jumlah'])} | {t['keterangan']}")

    try:
        no = int(input("\n[?] Masukkan nomor transaksi yang ingin dihapus (0 untuk batal): "))
        if no == 0:
            return
        if no < 1 or no > len(data["transaksi"]):
            raise ValueError
        
        tr = data["transaksi"].pop(no - 1)
        data["saldo"] += -tr["jumlah"] if tr["jenis"] == "pemasukan" else tr["jumlah"]
        save_data(data)
        print("\n[+] Transaksi berhasil dihapus!")
    except ValueError:
        print("\n[-] Nomor transaksi tidak valid.")
    jeda()

def menu_wishlist(data):
    while True:
        wishlist = load_wishlist()
        header("DAFTAR WISHLIST IMPIAN")
        print("  [1] Tambah Wishlist")
        print("  [2] Lihat Wishlist & Status")
        print("  [3] Hapus Wishlist")
        print("  [0] Kembali ke Menu Utama")

        pil = input("\n[?] Pilih menu [0-3]: ").strip()

        if pil == "1":
            nama = input("[?] Nama barang/impian: ").strip()
            if not nama:
                print("\n[-] Nama tidak boleh kosong.")
                jeda()
                continue
            try:
                harga = int(input("[?] Estimasi harga: ").replace(".", "").replace("Rp", "").strip())
                if harga <= 0:
                    raise ValueError
            except ValueError:
                print("\n[-] Harga tidak valid.")
                jeda()
                continue

            wishlist.append({"nama": nama, "harga": harga})
            save_wishlist(wishlist)
            print("\n[+] Wishlist berhasil ditambahkan!")
            jeda()

        elif pil == "2":
            header("STATUS WISHLIST")
            if not wishlist:
                print("\n[i] Wishlist masih kosong.")
                jeda()
                continue

            print(f"{'No':<3} | {'Nama Barang':<20} | {'Harga':<15} | {'Status'}")
            print("-" * 55)
            for i, w in enumerate(wishlist, 1):
                tercapai = data["saldo"] >= w["harga"]
                status = "TERCAPAI [✔]" if tercapai else "BELUM [X]"
                print(f"{i:<3} | {w['nama']:<20} | {format_rupiah(w['harga']):<15} | {status}")
            print("-" * 55)
            jeda()

        elif pil == "3":
            header("HAPUS WISHLIST")
            if not wishlist:
                print("\n[i] Wishlist kosong.")
                jeda()
                continue

            for i, w in enumerate(wishlist, 1):
                print(f"[{i}] {w['nama']} - {format_rupiah(w['harga'])}")

            try:
                no = int(input("\n[?] Nomor wishlist yang dihapus (0 untuk batal): "))
                if no == 0:
                    continue
                if no < 1 or no > len(wishlist):
                    raise ValueError
                wishlist.pop(no - 1)
                save_wishlist(wishlist)
                print("\n[+] Wishlist berhasil dihapus!")
            except ValueError:
                print("\n[-] Input tidak valid.")
            jeda()

        elif pil == "0":
            break
        else:
            print("\n[-] Pilihan tidak valid.")
            jeda()

def menu():
    while True:
        data = load_data()
        header("APLIKASI MANAJEMEN KEUANGAN")
        print(f" Saldo Saat Ini : {format_rupiah(data['saldo'])}")
        print("-" * 42)
        print("  [1] Tambah Transaksi")
        print("  [2] Riwayat Transaksi")
        print("  [3] Hapus Transaksi")
        print("  [4] Kelola Wishlist")
        print("  [0] Keluar")
        print("-" * 42)

        pilih = input("[?] Pilih menu [0-4]: ").strip()

        if pilih == "1":
            tambah_transaksi(data)
        elif pilih == "2":
            lihat_riwayat(data)
        elif pilih == "3":
            hapus_transaksi(data)
        elif pilih == "4":
            menu_wishlist(data)
        elif pilih == "0":
            clear_screen()
            print("Terima kasih telah menggunakan aplikasi keuangan!\n")
            break
        else:
            print("\n[-] Pilihan tidak valid.")
            jeda()

if __name__ == "__main__":
    menu()