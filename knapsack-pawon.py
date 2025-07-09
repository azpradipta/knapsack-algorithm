import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import io
import re

# --- DATA & KNAPSACK ---
menu_lauk = [
    {"nama": "Ayam Goreng", "harga": 10, "kenyang": 4},
    {"nama": "Ayam Rica-rica", "harga": 10, "kenyang": 4},
    {"nama": "Cumi Lada Hitam", "harga": 10, "kenyang": 2},
    {"nama": "Sapi Lada Hitam", "harga": 15, "kenyang": 3},
    {"nama": "Telur Bumbu Bali", "harga": 7, "kenyang": 3},
    {"nama": "Ikan Palumara", "harga": 15, "kenyang": 3},
    {"nama": "Ikan Tongkol Bumbu Merah", "harga": 10, "kenyang": 4},
    {"nama": "Sambel Goreng Ati Ampela", "harga": 10, "kenyang": 2},
    {"nama": "Ikan Suir Tuna", "harga": 10, "kenyang": 3},
    {"nama": "Udang Goreng Asam Manis", "harga": 10, "kenyang": 3},
    {"nama": "Kulit Ayam Crispy", "harga": 10, "kenyang": 2},
    {"nama": "Gongso Paru", "harga": 15, "kenyang": 2},
    {"nama": "Ceker tanpa Tulang", "harga": 10, "kenyang": 2},
    {"nama": "Perkedel Jagung", "harga": 2, "kenyang": 3},
    {"nama": "Perkedel Kentang", "harga": 3, "kenyang": 2},
    {"nama": "Tahun Bulat", "harga": 2, "kenyang": 1},
    {"nama": "Tempe Mendoan", "harga": 2, "kenyang": 2}
]

def pilih_lauk(budget, total_kenyang_maksimal, list_lauk):
    jumlah_lauk = len(list_lauk)
    dp = [[0 for kapasitas in range(budget + 1)]
          for indeks_lauk in range(jumlah_lauk + 1)]

    for indeks_lauk in range(1, jumlah_lauk + 1):
        for kapasitas in range(1, budget + 1):
            harga_lauk = list_lauk[indeks_lauk - 1]["harga"]
            nilai_kenyang = list_lauk[indeks_lauk - 1]["kenyang"]

            if harga_lauk <= kapasitas:
                ambil_lauk = nilai_kenyang + dp[indeks_lauk - 1][kapasitas - harga_lauk]
                tidak_ambil_lauk = dp[indeks_lauk - 1][kapasitas]
                dp[indeks_lauk][kapasitas] = max(ambil_lauk, tidak_ambil_lauk)
            else:
                dp[indeks_lauk][kapasitas] = dp[indeks_lauk - 1][kapasitas]

    total_kenyang_maksimal = dp[jumlah_lauk][budget]
    sisa_kapasitas = budget
    list_lauk_terpilih = []

    for indeks_lauk in range(jumlah_lauk, 0, -1):
        if dp[indeks_lauk][sisa_kapasitas] != dp[indeks_lauk - 1][sisa_kapasitas]:
            lauk = list_lauk[indeks_lauk - 1]
            list_lauk_terpilih.append(lauk)
            sisa_kapasitas -= lauk["harga"]

    total_harga = sum(lauk["harga"] for lauk in list_lauk_terpilih)

    hasil_terpilih = {
        "lauk": list(reversed(list_lauk_terpilih)),
        "total_harga": total_harga,
        "total_kenyang": total_kenyang_maksimal,
    }

    print("\n\033[33m------------ Hasil Pilihan Lauk ------------\033[0m")
    for lauk in hasil_terpilih["lauk"]:
        print(f"\033[36m{lauk['nama']} (Rp{(lauk['harga'])*1000}, Kenyang {lauk['kenyang']})\033[0m")
    print()
    print(f"Total harga\t: Rp{(hasil_terpilih['total_harga'])*1000}")
    print(f"Total kenyang\t: {hasil_terpilih['total_kenyang']}")
    print(f"Sisa uang\t: Rp{(budget*1000) - (hasil_terpilih['total_harga'])*1000}")
    print(f"\n\033[35mKompleksitas: O(n × budget) = O({len(menu_lauk)} × {budget_user}) = O({len(menu_lauk) * budget_user})\033[0m\n")
    print("\033[32mWorst Case\t= O(n x W)")
    print("Best Case\t= O(n)")
    print("Average Case\t= O(n)\033[0m\n")


# --- GUI ---
root = tk.Tk()
root.title("Pilih Lauk - Rumah Makan Pawon")

tk.Label(root, text="Masukkan Budget (Rupiah):").pack()
budget_entry = tk.Entry(root)
budget_entry.pack()

nasi_var = tk.BooleanVar()
tk.Checkbutton(root, text="Pakai Nasi?", variable=nasi_var).pack()

output_text = scrolledtext.ScrolledText(root, width=70, height=25)
output_text.pack()

# --- Buat TAG Warna ---
output_text.tag_config("yellow", foreground="orange")
output_text.tag_config("cyan", foreground="cyan")
output_text.tag_config("magenta", foreground="magenta")
output_text.tag_config("green", foreground="green")
output_text.tag_config("red", foreground="red")
output_text.tag_config("reset", foreground="black")

# --- Fungsi Render ANSI ke Tag ---
def insert_with_ansi(text):
    pattern = re.compile(r'\033\[(\d+)m')
    parts = pattern.split(text)
    tag = "reset"
    for i, part in enumerate(parts):
        if i % 2 == 0:
            output_text.insert(tk.END, part, tag)
        else:
            code = int(part)
            if code == 33:
                tag = "yellow"
            elif code == 36:
                tag = "cyan"
            elif code == 35:
                tag = "magenta"
            elif code == 32:
                tag = "green"
            elif code == 31:
                tag = "red"
            elif code == 0:
                tag = "reset"

def jalankan():
    try:
        global budget_user
        budget_user = int(budget_entry.get()) // 1000
        if budget_user < 2:
            output_text.insert(tk.END, "\nBudget terlalu kecil...\n")
            return

        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()

        pilih_lauk(budget_user, -1, menu_lauk)

        sys.stdout = old_stdout
        output_text.delete(1.0, tk.END)  # bersihkan output lama
        insert_with_ansi(mystdout.getvalue())

    except ValueError:
        messagebox.showerror("Error", "Masukkan angka budget yang valid!")

tk.Button(root, text="Proses", command=jalankan).pack(pady=10)

root.mainloop()
