import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np # Import numpy

# Fungsi untuk memuat data
# Memuat data dari file CSV yang sudah dibersihkan
@st.cache_data
def load_data():
    day_df = pd.read_csv("Dashboard/day_cleaned.csv")
    hour_df = pd.read_csv("Dashboard/hour_cleaned.csv")
    # Kolom 'dteday' seharusnya sudah dalam format datetime di file cleaned,
    # tapi kita konversi ulang untuk memastikan jika diperlukan.
    # Jika yakin sudah datetime, baris ini bisa dihapus.
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return day_df, hour_df

day_df, hour_df = load_data()

# Mapping nilai weathersit ke label yang lebih deskriptif
weather_labels = {
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Salju Ringan/Hujan Ringan',
    4: 'Hujan Lebat/Salju Lebat (Tidak ada data di weathersit 4 untuk day_df)'
}

# --- Sidebar ---
with st.sidebar:
    st.header("Filter Data")

    # Filter berdasarkan Kondisi Cuaca
    selected_weather = st.selectbox(
        'Pilih Kondisi Cuaca:',
        options=['Semua'] + list(weather_labels.values())
    )

    # Filter berdasarkan Tahun
    selected_year = st.selectbox(
        'Pilih Tahun:',
        options=['Semua'] + list(day_df['yr'].map({0: 2011, 1: 2012}).unique())
    )

# --- Main Content ---
# Judul Aplikasi Streamlit
st.title('Dashboard Analisis Penyewaan Sepeda')

st.markdown("""
Dashboard ini menyajikan hasil analisis data penyewaan sepeda berdasarkan:
1. Pengaruh Kondisi Cuaca (`weathersit`) terhadap jumlah penyewaan.
2. Tren Penyewaan Sepeda dari waktu ke waktu (per bulan dan tahun).
""")

# Menerapkan Filter
filtered_day_df = day_df.copy()

if selected_weather != 'Semua':
    # Temukan weathersit number berdasarkan label
    weather_num = [k for k, v in weather_labels.items() if v == selected_weather][0]
    filtered_day_df = filtered_day_df[filtered_day_df['weathersit'] == weather_num]

if selected_year != 'Semua':
    # Temukan yr number berdasarkan tahun
    year_num = 0 if selected_year == 2011 else 1
    filtered_day_df = filtered_day_df[filtered_day_df['yr'] == year_num]


# Analisis dan Visualisasi menggunakan data yang sudah difilter
st.header("Analisis Pengaruh Cuaca")

if not filtered_day_df.empty:
    # Analisis pengaruh cuaca (menggunakan filtered_day_df)
    weather_impact_total_filtered = filtered_day_df.groupby('weathersit').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    weather_impact_mean_filtered = filtered_day_df.groupby('weathersit').agg({
        'cnt': 'mean',
        'casual': 'mean',
        'registered': 'mean'
    }).reset_index()

    weather_impact_total_filtered['weathersit_label'] = weather_impact_total_filtered['weathersit'].map(weather_labels)
    weather_impact_mean_filtered['weathersit_label'] = weather_impact_mean_filtered['weathersit'].map(weather_labels)

    # Visualisasi Jumlah Total Penyewaan berdasarkan Cuaca
    st.subheader('Jumlah Total Penyewaan Berdasarkan Kondisi Cuaca (Filter Diterapkan)')
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    bar_width = 0.25
    index = np.arange(len(weather_impact_total_filtered['weathersit_label']))

    ax1.bar(index, weather_impact_total_filtered['cnt'], bar_width, label='Total', color='skyblue')
    ax1.bar(index + bar_width, weather_impact_total_filtered['casual'], bar_width, label='Kasual', color='lightcoral')
    ax1.bar(index + 2 * bar_width, weather_impact_total_filtered['registered'], bar_width, label='Terdaftar', color='lightgreen')

    ax1.set_xlabel('Kondisi Cuaca')
    ax1.set_ylabel('Jumlah Total Penyewaan Sepeda')
    ax1.set_title('Jumlah Total Penyewaan Sepeda Berdasarkan Kondisi Cuaca (Filter Diterapkan)')
    ax1.set_xticks(index + bar_width)
    ax1.set_xticklabels(weather_impact_total_filtered['weathersit_label'])
    ax1.legend()
    st.pyplot(fig1)

    # Visualisasi Rata-rata Penyewaan Harian berdasarkan Cuaca
    st.subheader('Rata-rata Penyewaan Harian Berdasarkan Kondisi Cuaca (Filter Diterapkan)')
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    index = np.arange(len(weather_impact_mean_filtered['weathersit_label']))

    ax2.bar(index, weather_impact_mean_filtered['cnt'], bar_width, label='Total', color='skyblue')
    ax2.bar(index + bar_width, weather_impact_mean_filtered['casual'], bar_width, label='Kasual', color='lightcoral')
    ax2.bar(index + 2 * bar_width, weather_impact_mean_filtered['registered'], bar_width, label='Terdaftar', color='lightgreen')

    ax2.set_xlabel('Kondisi Cuaca')
    ax2.set_ylabel('Rata-rata Penyewaan Harian')
    ax2.set_title('Rata-rata Penyewaan Harian Berdasarkan Kondisi Cuaca (Filter Diterapkan)')
    ax2.set_xticks(index + bar_width)
    ax2.set_xticklabels(weather_impact_mean_filtered['weathersit_label'])
    ax2.legend()
    st.pyplot(fig2)
else:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")


st.header("Analisis Tren Waktu")

# Analisis tren penyewaan berdasarkan bulan dan tahun (menggunakan filtered_day_df)
monthly_yearly_trend_filtered = filtered_day_df.groupby(['yr', 'mnth']).agg({
    'cnt': 'sum',
    'casual': 'sum',
    'registered': 'sum'
}).reset_index()

if not monthly_yearly_trend_filtered.empty:
    # Menggabungkan tahun dan bulan untuk sumbu x
    monthly_yearly_trend_filtered['year_month'] = pd.to_datetime((monthly_yearly_trend_filtered['yr'] + 2011).astype(str) + '-' + monthly_yearly_trend_filtered['mnth'].astype(str) + '-01')

    # Visualisasi Tren Penyewaan Total per Bulan dan Tahun
    st.subheader('Tren Jumlah Total Penyewaan Sepeda per Bulan dan Tahun (Filter Diterapkan)')
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    ax3.plot(monthly_yearly_trend_filtered['year_month'], monthly_yearly_trend_filtered['cnt'], marker='o', linestyle='-', color='blue')
    ax3.set_xlabel('Waktu (Bulan-Tahun)')
    ax3.set_ylabel('Jumlah Total Penyewaan Sepeda')
    ax3.set_title('Tren Jumlah Total Penyewaan Sepeda per Bulan dan Tahun (Filter Diterapkan)')
    ax3.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # Visualisasi Tren Penyewaan Kasual dan Terdaftar per Bulan dan Tahun
    st.subheader('Tren Jumlah Penyewaan Sepeda (Kasual vs Terdaftar) per Bulan dan Tahun (Filter Diterapkan)')
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    ax4.plot(monthly_yearly_trend_filtered['year_month'], monthly_yearly_trend_filtered['casual'], marker='o', linestyle='-', color='lightcoral', label='Kasual')
    ax4.plot(monthly_yearly_trend_filtered['year_month'], monthly_yearly_trend_filtered['registered'], marker='o', linestyle='-', color='lightgreen', label='Terdaftar')
    ax4.set_xlabel('Waktu (Bulan-Tahun)')
    ax4.set_ylabel('Jumlah Penyewaan Sepeda')
    ax4.set_title('Tren Jumlah Penyewaan Sepeda (Kasual vs Terdaftar) per Bulan dan Tahun (Filter Diterapkan)')
    ax4.grid(True)
    ax4.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig4)
else:
     st.warning("Tidak ada data yang sesuai dengan filter yang dipilih untuk analisis tren waktu.")


st.header("Ringkasan Data")
st.write("Day Data (first 5 rows):")
st.dataframe(day_df.head())
st.write("Hour Data (first 5 rows):")
st.dataframe(hour_df.head())

st.header("Kesimpulan Utama")
st.markdown("""
**Pengaruh Cuaca:**
- Cuaca cerah/sedikit berawan (weathersit 1) memiliki penyewaan tertinggi.
- Cuaca buruk (salju/hujan ringan - weathersit 3) memiliki penyewaan terendah.
- Pengguna terdaftar mendominasi jumlah penyewaan di semua kondisi cuaca, tetapi pengguna kasual lebih sensitif terhadap cuaca buruk.

**Tren Waktu:**
- Ada peningkatan tren penyewaan dari tahun 2011 ke 2012.
- Penyewaan menunjukkan pola musiman dengan puncak di musim panas/gugur dan rendah di musim dingin.
- Pola musiman ini lebih menonjol pada pengguna kasual dibandingkan terdaftar.
""")
