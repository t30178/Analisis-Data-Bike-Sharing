import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")
st.title("🚲 Bike Sharing Visualization Analysis")

# Load dataset
df = pd.read_csv("main_data.csv")
st.success("Dataset 'main_data.csv' loaded successfully!")

st.header("🔍 Data Preview")
st.write(df.head())

# Mapping season
season_mapping = {1: 'Winter', 2: 'Summer', 3: 'Fall', 4: 'Spring'}
df['season_label'] = df['season'].map(season_mapping)

# ✅ ANALISIS 1: Pola Penggunaan Berdasarkan Musim
st.subheader("✅ Analisis 1: Pola Penggunaan Layanan Berdasarkan Musim")
season_data = df.groupby('season_label')['cnt'].mean().reset_index()

# Urutkan sesuai insight: Fall, Summer, Spring, Winter
season_order = ['Fall', 'Summer', 'Spring', 'Winter']

# 🔸 BARPLOT Seaborn
fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.barplot(data=season_data, x='season_label', y='cnt', 
            order=season_order, palette='YlOrBr', ax=ax1)
ax1.set_xlabel("Season")
ax1.set_ylabel("Average Bike Rentals")
ax1.set_title("Average Bike Rentals by Season (Seaborn)")
st.pyplot(fig1)

# 🔸 PIE CHART Matplotlib
st.subheader("✅ Pie Chart Distribusi Musiman")
fig_pie, ax_pie = plt.subplots()
ax_pie.pie(season_data['cnt'], labels=season_order, autopct='%1.1f%%', colors=sns.color_palette('YlOrBr'))
ax_pie.set_title("Bike Rental Distribution by Season")
st.pyplot(fig_pie)

# 🔸 Insight Text
st.info("📌 **Kesimpulan:**\n\n"
        "- **Fall** tertinggi, diikuti **Summer**.\n"
        "- **Spring** dan **Winter** rendah.\n"
        "- Cuaca nyaman diduga alasan utama.")

# ✅ ANALISIS 2: Hari Kerja vs Akhir Pekan
st.subheader("✅ Analisis 2: Distribusi Penyewaan Sepeda - Hari Kerja vs Akhir Pekan")
workingday_data = df.groupby('workingday')['cnt'].mean().reset_index()
workingday_data['Label'] = workingday_data['workingday'].map({1: 'Working Day', 0: 'Weekend'})

# 🔸 BAR CHART seaborn
fig2, ax2 = plt.subplots(figsize=(6,4))
sns.barplot(data=workingday_data, x='Label', y='cnt', palette='Blues', ax=ax2)
ax2.set_xlabel("Day Type")
ax2.set_ylabel("Average Bike Rentals")
ax2.set_title("Average Rentals: Working Day vs Weekend")
st.pyplot(fig2)

# 🔸 PIE CHART
fig_pie2, ax_pie2 = plt.subplots()
ax_pie2.pie(workingday_data['cnt'], labels=workingday_data['Label'], autopct='%1.1f%%', colors=sns.color_palette('Blues'))
ax_pie2.set_title("Bike Rental Share: Working Day vs Weekend")
st.pyplot(fig_pie2)

st.info("📌 **Kesimpulan:**\n\n"
        "- Penyewaan lebih banyak di **Working Day**.\n"
        "- Sepeda banyak digunakan untuk aktivitas rutin seperti kerja/sekolah.")

# ✅ BONUS: Hari dengan Permintaan Tertinggi
st.subheader("✅ Hari dengan Permintaan Tertinggi")
weekday_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                   4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
df['weekday_label'] = df['weekday'].map(weekday_mapping)

weekday_data = df.groupby('weekday_label')['cnt'].mean().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(data=weekday_data, x='weekday_label', y='cnt', palette='mako', ax=ax3)
ax3.set_xlabel("Day of the Week")
ax3.set_ylabel("Average Rentals")
ax3.set_title("Average Rentals by Day of the Week")
st.pyplot(fig3)

max_day = weekday_data.loc[weekday_data['cnt'].idxmax()]
st.success(f"📌 Hari dengan permintaan tertinggi adalah **{max_day['weekday_label']}** "
           f"dengan rata-rata penyewaan **{max_day['cnt']:.0f} sepeda**.")
