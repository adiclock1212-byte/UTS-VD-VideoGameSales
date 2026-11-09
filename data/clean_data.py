"""Pra-pemrosesan Video Game Sales (Kaggle) -> data/vgsales_clean.csv

Cara pakai:
  1. Unduh vgsales.csv dari Kaggle, taruh di folder data/
  2. Jalankan:  python data/clean_data.py data/vgsales.csv
"""
import sys
from pathlib import Path
import pandas as pd

src = Path(sys.argv[1] if len(sys.argv) > 1 else "data/vgsales.csv")
out = Path(__file__).parent / "vgsales_clean.csv"

df = pd.read_csv(src)
print(f"Baris awal: {len(df):,} | Kolom: {df.shape[1]}")
print("Missing value:\n", df.isna().sum()[lambda s: s > 0])

df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# 1) Year kosong (~1,6%) dibuang karena analisis tren butuh tahun; 2) Publisher kosong -> 'Unknown'
df = df.dropna(subset=["Year"])
df["Year"] = df["Year"].astype(int)
df["Publisher"] = df["Publisher"].fillna("Unknown").str.strip()

# Tahun >2016 hanya segelintir judul (data belum lengkap) -> dikeluarkan agar tren tidak bias
df = df[df["Year"] <= 2016]

# Fitur turunan: kelompok produsen konsol
FAMILY = {
    **dict.fromkeys(["Wii", "NES", "GB", "DS", "SNES", "GBA", "3DS", "N64", "GC", "WiiU"], "Nintendo"),
    **dict.fromkeys(["PS", "PS2", "PS3", "PS4", "PSP", "PSV"], "Sony"),
    **dict.fromkeys(["XB", "X360", "XOne"], "Microsoft"),
    **dict.fromkeys(["GEN", "SCD", "DC", "GG", "SAT"], "Sega"),
    "2600": "Atari", "PC": "PC",
}
df["Manufacturer"] = df["Platform"].map(FAMILY).fillna("Lainnya")

df = df.sort_values("Year").reset_index(drop=True)
df.to_csv(out, index=False)
print(f"Selesai: {len(df):,} baris -> {out}")
