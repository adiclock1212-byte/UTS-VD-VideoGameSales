# 🎮 Dashboard Interaktif Penjualan Video Game Dunia

**UTS Visualisasi Data – Ganjil TA 2026/2027**
**Nama:** Muhammad Alva Gustav Al Fallah | **NIM:** 241041007
**Program Studi:** Manajemen Informatika – Universitas Dirgantara Marsekal Suryadarma
**Dosen:** Muryan Awaludin, S.Kom., M.Kom.

## 🔗 Tautan
- **Live Dashboard:** https://GANTI-DENGAN-URL-STREAMLIT-KAMU.streamlit.app
- **Dataset Kaggle (sumber asli):** https://www.kaggle.com/datasets/gregorut/videogamesales

## Latar Belakang
Dataset *Video Game Sales* memuat 16.598 judul game dengan penjualan ≥100 ribu kopi (hasil scraping vgchartz.com), berisi platform, tahun rilis, genre, publisher, dan penjualan per wilayah (NA, EU, JP, Other, Global) dalam juta unit.
Dashboard ini menjawab: *kapan industri game mencapai puncak, genre/platform/publisher apa yang mendominasi, dan apakah selera pasar tiap wilayah berbeda?*

## Fitur Dashboard
| Komponen | Isi |
|---|---|
| KPI Cards (5) | Total Penjualan, Jumlah Judul, Rata-rata/Judul, Platform Terlaris, Genre Terlaris |
| Jenis Chart (5) | Line (tren per wilayah), Bar horizontal (genre, platform, game, publisher), Donut (proporsi wilayah), Heatmap (genre × produsen), Scatter (NA vs EU) |
| Filter (4) | Rentang tahun, Genre, Produsen konsol, Ukuran penjualan (Global/NA/EU/JP/Other) |
| Desain | Palet konsisten (satu warna tetap per wilayah), 5 tab sebagai hirarki informasi, layout responsif |
| Storytelling | Kotak 💡 Insight dinamis per tab + anotasi tahun puncak pada line chart |

## 🔑 Key Insights (tanpa filter)
1. **Puncak industri sekitar 2008–2009** – penjualan total per tahun rilis memuncak lalu menurun tajam setelahnya.
2. **Action, Sports, dan Shooter** adalah tiga genre dengan penjualan terbesar secara global.
3. **PS2 platform terlaris sepanjang masa**, disusul X360, PS3, Wii, dan DS; Nintendo adalah publisher terbesar.
4. **North America ±49% pasar**, Eropa ±27%, Jepang ±14%, lainnya ±9%.
5. **Selera Jepang berbeda** – genre Role-Playing terkuat di Jepang, sedangkan Action di North America; Wii Sports menjadi game terlaris (±82 juta unit).

> Angka detail dapat diverifikasi langsung di dashboard (reset semua filter).

## 🛠️ Struktur Repositori
```
├── app.py                    # aplikasi dashboard Streamlit
├── requirements.txt          # dependensi deployment
├── .streamlit/config.toml    # tema warna
├── data/
│   ├── clean_data.py         # skrip pembersihan data
│   └── vgsales_clean.csv     # data bersih hasil pra-pemrosesan
└── README.md
```

## 🧹 Pra-pemrosesan Data
- Hapus duplikat; baris dengan `Year` kosong (~1,6%) dibuang karena analisis tren butuh tahun.
- `Publisher` kosong diisi `Unknown`; `Year` diubah ke integer.
- Tahun >2016 dikeluarkan karena hanya segelintir judul (data tidak lengkap).
- Tambah kolom `Manufacturer` (Nintendo, Sony, Microsoft, Sega, Atari, PC, Lainnya) hasil pengelompokan platform.

## ▶️ Menjalankan Secara Lokal
```bash
git clone https://github.com/USERNAME/REPO.git
cd REPO
pip install -r requirements.txt
streamlit run app.py
```
Buka http://localhost:8501. (Opsional: unduh `vgsales.csv` dari Kaggle ke folder `data/`, lalu `python data/clean_data.py data/vgsales.csv`.)

## Teknologi
Python 3.13 • Streamlit • Pandas • Plotly
