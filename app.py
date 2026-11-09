"""Dashboard Interaktif Penjualan Video Game Dunia - UTS Visualisasi Data (Ganjil 2026/2027)
Muhammad Alva Gustav Al Fallah | NIM 241041007
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

NAMA, NIM = "Muhammad Alva Gustav Al Fallah", "241041007"
DATA = Path(__file__).parent / "data" / "vgsales_clean.csv"

# ---- Palet warna konsisten ----
BLUE, ORANGE, GREEN, GREY = "#1F4E79", "#F28E2B", "#59A14F", "#8A94A6"
REGION_COLORS = {"North America": BLUE, "Europe": ORANGE, "Japan": "#E15759", "Other": GREY}
REGION_COLS = {"North America": "NA_Sales", "Europe": "EU_Sales", "Japan": "JP_Sales", "Other": "Other_Sales"}
METRICS = {"Global": "Global_Sales", **REGION_COLS}

st.set_page_config(page_title="Dashboard Video Game Sales", page_icon="🎮", layout="wide")
st.markdown(
    """<style>
    .block-container {padding-top: 1.5rem;}
    div[data-testid="stMetric"] {background:#F3F6FA; border-left:5px solid #1F4E79;
        padding:12px 16px; border-radius:8px;}
    .insight {background:#FFF8EC; border-left:5px solid #F28E2B; padding:10px 14px;
        border-radius:6px; margin:6px 0 14px 0; font-size:0.95rem;}
    </style>""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA)


def insight(text: str) -> None:
    st.markdown(f'<div class="insight">💡 <b>Insight:</b> {text}</div>', unsafe_allow_html=True)


if not DATA.exists():
    st.error("File data/vgsales_clean.csv belum ada. Jalankan: python data/clean_data.py data/vgsales.csv")
    st.stop()

full = load_data()

# ---------------- Sidebar: filter ----------------
st.sidebar.header("🎛️ Filter Data")
ymin, ymax = int(full["Year"].min()), int(full["Year"].max())
yr = st.sidebar.slider("Rentang tahun rilis", ymin, ymax, (ymin, ymax))
genres_all = sorted(full["Genre"].unique())
genres = st.sidebar.multiselect("Genre", genres_all, default=genres_all)
mf_all = sorted(full["Manufacturer"].unique())
mfs = st.sidebar.multiselect("Produsen konsol", mf_all, default=mf_all)
metric_name = st.sidebar.selectbox("Ukuran penjualan (wilayah)", list(METRICS), index=0)
M = METRICS[metric_name]
st.sidebar.caption("Satuan: juta unit terjual. Semua grafik & KPI mengikuti filter.")

df = full[full["Year"].between(*yr) & full["Genre"].isin(genres) & full["Manufacturer"].isin(mfs)]

# ---------------- Header ----------------
st.title("🎮 Dashboard Penjualan Video Game Dunia")
st.caption(f"UTS Visualisasi Data • {NAMA} • NIM {NIM} • Sumber: Kaggle – Video Game Sales (vgchartz)")

if df.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini. Ubah filter di sidebar.")
    st.stop()

# ---------------- KPI ----------------
total = df[M].sum()
top_plat = df.groupby("Platform")[M].sum().idxmax()
top_genre = df.groupby("Genre")[M].sum().idxmax()
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric(f"Total Penjualan ({metric_name})", f"{total:,.0f} jt")
k2.metric("Jumlah Judul Game", f"{len(df):,}")
k3.metric("Rata-rata / Judul", f"{df[M].mean():.2f} jt")
k4.metric("Platform Terlaris", top_plat)
k5.metric("Genre Terlaris", top_genre)
st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Tren", "🕹️ Genre & Platform", "🏆 Game & Publisher", "🌍 Wilayah & Korelasi", "🗂️ Data"])

# ---------------- Tab 1: Tren ----------------
with tab1:
    yearly = df.groupby("Year")[list(REGION_COLS.values())].sum().rename(columns={v: k for k, v in REGION_COLS.items()})
    long = yearly.reset_index().melt("Year", var_name="Wilayah", value_name="Penjualan")
    fig = px.line(long, x="Year", y="Penjualan", color="Wilayah", color_discrete_map=REGION_COLORS, markers=True,
                  title="Tren Penjualan per Tahun Rilis, per Wilayah (juta unit)")
    tot_year = yearly.sum(axis=1)
    py_, pv = tot_year.idxmax(), tot_year.max()
    fig.add_annotation(x=py_, y=yearly.loc[py_, "North America"], text=f"Puncak total: {py_}<br>{pv:,.0f} jt unit",
                       showarrow=True, arrowhead=2, ax=-70, ay=-40, bgcolor="#FFF8EC", bordercolor=ORANGE)
    fig.update_layout(xaxis_title="Tahun rilis", yaxis_title="Juta unit", hovermode="x unified",
                      legend=dict(orientation="h", y=1.12), margin=dict(t=80))
    st.plotly_chart(fig, width="stretch")
    after = tot_year[tot_year.index > py_]
    drop = (1 - after.iloc[-1] / pv) if len(after) else 0
    insight(f"Penjualan total memuncak pada tahun rilis <b>{py_}</b> ({pv:,.0f} juta unit)."
            + (f" Setelah itu turun hingga <b>{drop:.0%}</b> pada {after.index[-1]}." if len(after) else ""))

# ---------------- Tab 2: Genre & Platform ----------------
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        g = df.groupby("Genre", as_index=False)[M].sum().sort_values(M)
        f = px.bar(g, x=M, y="Genre", orientation="h", title=f"Penjualan per Genre ({metric_name}, juta unit)",
                   color_discrete_sequence=[BLUE])
        f.update_layout(xaxis_title="Juta unit", yaxis_title="")
        st.plotly_chart(f, width="stretch")
    with c2:
        p = df.groupby("Platform", as_index=False)[M].sum().nlargest(10, M).sort_values(M)
        f = px.bar(p, x=M, y="Platform", orientation="h", title="10 Platform Terlaris (juta unit)",
                   color_discrete_sequence=[ORANGE])
        f.update_layout(xaxis_title="Juta unit", yaxis_title="")
        st.plotly_chart(f, width="stretch")
    piv = df.pivot_table(index="Genre", columns="Manufacturer", values=M, aggfunc="sum").fillna(0)
    f = px.imshow(piv, text_auto=".0f", aspect="auto", color_continuous_scale="Blues",
                  title="Heatmap Penjualan: Genre × Produsen Konsol (juta unit)")
    f.update_layout(xaxis_title="", yaxis_title="", coloraxis_colorbar_title="Juta unit")
    st.plotly_chart(f, width="stretch")
    gt, gs = g.iloc[-1], g[M].sum()
    insight(f"Genre terlaris: <b>{gt['Genre']}</b> ({gt[M] / gs:.0%} dari total). Platform terlaris: <b>{p.iloc[-1]['Platform']}</b>. "
            "Heatmap menunjukkan genre mana yang dominan di tiap produsen (warna lebih gelap = penjualan lebih besar).")

# ---------------- Tab 3: Game & Publisher ----------------
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        tg = df.nlargest(10, M)[["Name", "Platform", M]].copy()
        tg["Label"] = tg["Name"] + " (" + tg["Platform"] + ")"
        f = px.bar(tg.sort_values(M), x=M, y="Label", orientation="h", title="10 Game Terlaris (juta unit)",
                   color_discrete_sequence=[GREEN])
        f.update_layout(xaxis_title="Juta unit", yaxis_title="")
        st.plotly_chart(f, width="stretch")
    with c2:
        pb = df[df["Publisher"] != "Unknown"].groupby("Publisher", as_index=False)[M].sum().nlargest(10, M).sort_values(M)
        f = px.bar(pb, x=M, y="Publisher", orientation="h", title="10 Publisher Terbesar (juta unit)",
                   color_discrete_sequence=[BLUE])
        f.update_layout(xaxis_title="Juta unit", yaxis_title="")
        st.plotly_chart(f, width="stretch")
    best = tg.sort_values(M).iloc[-1]
    insight(f"Game terlaris: <b>{best['Name']}</b> ({best['Platform']}) dengan {best[M]:.1f} juta unit. "
            f"Publisher terbesar: <b>{pb.iloc[-1]['Publisher']}</b> ({pb.iloc[-1][M]:,.0f} juta unit).")

# ---------------- Tab 4: Wilayah & Korelasi ----------------
with tab4:
    c1, c2 = st.columns(2)
    with c1:
        reg = pd.Series({k: df[v].sum() for k, v in REGION_COLS.items()}).reset_index()
        reg.columns = ["Wilayah", "Penjualan"]
        f = px.pie(reg, names="Wilayah", values="Penjualan", hole=0.55, title="Proporsi Penjualan per Wilayah",
                   color="Wilayah", color_discrete_map=REGION_COLORS)
        f.update_traces(textinfo="percent+label")
        st.plotly_chart(f, width="stretch")
    with c2:
        samp = df[(df["NA_Sales"] > 0) & (df["EU_Sales"] > 0)].sample(min(len(df), 3000), random_state=1)
        f = px.scatter(samp, x="NA_Sales", y="EU_Sales", color="Genre", opacity=0.6, log_x=True, log_y=True,
                       hover_data=["Name", "Platform"], title="Penjualan NA vs Eropa per Game (skala log, sampel ≤3.000)")
        f.update_layout(xaxis_title="North America (juta unit)", yaxis_title="Europe (juta unit)")
        st.plotly_chart(f, width="stretch")
    jp = df.groupby("Genre")["JP_Sales"].sum()
    na = df.groupby("Genre")["NA_Sales"].sum()
    corr = df["NA_Sales"].corr(df["EU_Sales"])
    insight(f"North America menyumbang <b>{reg.loc[0, 'Penjualan'] / reg['Penjualan'].sum():.0%}</b> penjualan. "
            f"Korelasi NA–Eropa = <b>{corr:.2f}</b> (selera pasar serupa). Di Jepang genre teratas adalah <b>{jp.idxmax()}</b>, "
            f"sedangkan di North America <b>{na.idxmax()}</b>.")

# ---------------- Tab 5: Data ----------------
with tab5:
    st.caption(f"{len(df):,} baris sesuai filter")
    st.dataframe(df, width="stretch", height=400)
    st.download_button("⬇️ Unduh data terfilter (CSV)", df.to_csv(index=False).encode("utf-8"), "vgsales_filtered.csv", "text/csv")
