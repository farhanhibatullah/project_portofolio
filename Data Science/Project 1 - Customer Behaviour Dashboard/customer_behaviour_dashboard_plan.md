
# 📊 Proyek Dashboard Customer Behaviour

## 🎯 Tujuan
Membuat dashboard interaktif menggunakan **Streamlit** untuk menampilkan insight perilaku pelanggan berdasarkan data transaksi.

---

## 📚 Tech Stack
- **Python** (pandas, numpy, matplotlib/seaborn, plotly)
- **Streamlit** (dashboard)
- **scikit-learn** (untuk segmentasi klien jika diperlukan)
- **CRISP-DM** sebagai metodologi

---

## 🧱 Struktur Halaman Dashboard
Berikut adalah 4 halaman utama yang akan dibuat di Streamlit:

1. **Homepage (Overview)**  
   - Menjelaskan proyek dan highlight insight penting
2. **Customer Analysis**  
   - Jumlah pelanggan, segmentasi RFM, negara asal
3. **Purchase Behaviour**  
   - Frekuensi belanja, waktu belanja, produk terlaris
4. **Revenue Insights**  
   - Total revenue, revenue by country, revenue over time

---

## 🗓️ Breakdown Pekerjaan 5 Hari (CRISP-DM Framework)

### 📅 Hari 1: Business Understanding & Data Understanding
**Goal:**  
Pahami bisnis, tujuan analisis, dan eksplorasi dataset.

**Task:**
- Pahami tujuan analisis perilaku pelanggan (misal: untuk segmentasi, strategi retensi)
- Load dataset dari Excel (`OnlineRetail.xlsx`)
- EDA awal:
  - Jumlah transaksi
  - Jumlah pelanggan unik
  - Produk terbanyak dibeli
  - Negara dengan transaksi terbanyak
- Visualisasi awal dengan matplotlib/seaborn

---

### 📅 Hari 2: Data Preparation
**Goal:**  
Bersihkan dan siapkan data untuk analisis

**Task:**
- Hapus nilai `null` dan transaksi dengan kuantitas atau harga negatif
- Buat kolom `TotalPrice = Quantity * UnitPrice`
- Konversi `InvoiceDate` menjadi datetime
- Filter transaksi yang valid (misal hanya yang memiliki CustomerID)
- Buat `recency`, `frequency`, dan `monetary` untuk analisis RFM
- Simpan dataset siap pakai sebagai `cleaned_data.csv`

---

### 📅 Hari 3: Modeling (Optional RFM Segmentation)
**Goal:**  
Buat segmentasi sederhana berbasis RFM

**Task:**
- Hitung Recency (hari sejak terakhir beli)
- Hitung Frequency (jumlah pembelian unik)
- Hitung Monetary (jumlah uang yang dibelanjakan)
- Skoring RFM (misalnya 1–5)
- Segmentasi pelanggan (misal: Best Customers, At Risk, etc.)
- Visualisasi heatmap RFM

> 📌 Kalau tidak ingin terlalu kompleks, RFM bisa disimpan sebagai insight tanpa clustering model.

---

### 📅 Hari 4: Dashboard Development (Streamlit)
**Goal:**  
Bangun dashboard interaktif 4 halaman.

**Task:**
- Struktur multi-page Streamlit (`streamlit >=1.10`)
- Tambahkan sidebar navigasi halaman:
  - Overview: highlight insight
  - Customer Analysis: RFM, distribusi negara
  - Purchase Behaviour: jam favorit, produk laris
  - Revenue: tren revenue mingguan/bulanan
- Gunakan **plotly** untuk interaktivitas
- Tambahkan filter per negara, waktu, dll.

---

### 📅 Hari 5: Evaluation & Deployment
**Goal:**  
Uji, dokumentasi, dan deploy lokal/Cloud.

**Task:**
- Uji seluruh fungsi dashboard
- Dokumentasi penggunaan (README.md)
- Simpan file proyek:
  - `main.py` (streamlit)
  - `data/cleaned_data.csv`
  - `notebooks/EDA.ipynb`
- Opsi: deploy ke Streamlit Cloud

---

## ✅ Output Akhir
- Dashboard interaktif perilaku pelanggan
- Insight RFM dan revenue
- File siap deploy
- Dokumentasi lengkap

---

## 📂 Struktur Folder yang Disarankan
```
customer-behaviour-dashboard/
│
├── data/
│   └── OnlineRetail.xlsx
│   └── cleaned_data.csv
│
├── notebooks/
│   └── EDA.ipynb
│
├── main.py
├── utils.py
└── README.md
```
