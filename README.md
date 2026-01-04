# 🧺 LaundryDesk  

*A Thoughtful Desktop App for Learning Real-World Data Flow*

**Tech Stack:** Python · PyQt6 · SQLite  

> *“Good software starts with understanding how data moves — not how fancy the UI looks.”*

LaundryDesk adalah aplikasi desktop manajemen laundry yang dibangun sebagai project UAS, dengan pendekatan **product-oriented engineering**: sederhana, terstruktur, dan fokus pada alur data yang nyata.

Project ini menjadi latihan dalam merancang software yang **mudah dipahami, mudah dijelaskan, dan siap didemokan** — kualitas yang krusial dalam lingkungan profesional dan tim produk.

---

## 🧠 What I Intentionally Focused On

Dalam LaundryDesk, secara sadar memprioritaskan:

- Clear data ownership (customer, package, transaction)
- Relational thinking melalui **Primary Key & Foreign Key**
- Separation of concerns antara **UI, logic, dan database**
- Predictable user flow yang mudah dijelaskan saat demo

Tanpa framework berat.  
Tanpa overengineering.  
Hanya fondasi yang kuat.

---

## 🗃️ Data Model as the Core

Aplikasi ini dibangun di atas **SQLite relational database** dengan tiga entitas utama:

- `customers`
- `packages`
- `transactions`

Relasi antar tabel memastikan bahwa:

- Setiap transaksi selalu terhubung ke customer yang valid
- Setiap transaksi mereferensikan paket laundry yang tersedia

Pendekatan ini melatih berpikir sebagai engineer yang bertanggung jawab terhadap **data integrity**, bukan hanya tampilan UI.

---

## 📊 How the App Works

### Table View — Seeing the Big Picture

Pengguna dapat melihat daftar transaksi dalam bentuk tabel dengan:

- Filter berdasarkan **nama customer**
- Filter berdasarkan **status transaksi**

Fitur ini merepresentasikan kebutuhan dunia nyata: *find data fast*.

---

### Record View — One Data at a Time

Setiap transaksi dapat dilihat secara detail melalui navigasi:

- First  
- Previous  
- Next  
- Last  

Pendekatan ini membantu saya memahami **state management dan navigation flow** pada aplikasi desktop.

---

### Add & Edit — Real Interaction

Pengguna dapat:

- Menambahkan transaksi baru
- Mengedit transaksi yang sudah ada

Semua perubahan langsung tersimpan ke database tanpa mock data atau file perantara.

---

## 📋 Ketentuan UAS & Pemenuhan

Project LaundryDesk dikembangkan dengan mengacu pada seluruh ketentuan UAS Pemrograman Desktop.  
Berikut adalah daftar ketentuan beserta status pemenuhannya:

| Ketentuan UAS | Status |
|--------------|--------|
| 2 tabel dibuat & diisi (min. 5 record) menggunakan SQL | ✅ |
| Hanya 1 file Python dijalankan saat demo | ✅ |
| Semua tabel memiliki relasi RDB (Primary Key – Foreign Key) | ✅ |
| Table View dengan 2 input filter | ✅ |
| Tampilan per-record dengan tombol navigasi | ✅ |
| Fungsi edit & tambah record | ✅ |

---

## 🚀 How to Run

```bash
pip install PyQt6
python laundry_uas.py
