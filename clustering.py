import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import base64
import openpyxl

st.markdown(
"""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1647272553054-ab568a5366c7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1075&q=80");
    background-size: cover;
}
</style>
""",
  unsafe_allow_html=True
)

df_CF = pd.read_excel('df_CF.xlsx')
df_CB = pd.read_excel('df_CB.xlsx')
df_AM = pd.read_excel('df_AM.xlsx')
df_CM = pd.read_excel('df_CM.xlsx')
df_Sideback = pd.read_excel('df_Sideback.xlsx')
df_Winger = pd.read_excel('df_Winger.xlsx')

# Preprocessing data
data_encoded = pd.get_dummies(dt.drop(['Name'], axis=1))

# Fungsi untuk melakukan klasterisasi
def kmeans_clustering(data, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    return kmeans.labels_

# Sidebar untuk memilih posisi pemain dan jumlah klaster
st.sidebar.header('Pilih posisi pemain yang ingin Diklasterisasi')
dataframe_choice = st.sidebar.selectbox("Pilih Posisi Pemain", ['CF', 'CB', 'AM', 'CM', 'Sideback', 'Winger'])
st.sidebar.subheader('Pilih jumlah klaster yang diinginkan')
jumlah_klaster = st.sidebar.slider('Jumlah Klaster', min_value=2, max_value=5, value=3, step=1)

if dataframe_choice == 'CF':
    df = df_CF
elif dataframe_choice == 'CB':
    df = df_CB
elif dataframe_choice == 'AM':
    df = df_AM
elif dataframe_choice == 'CM':
    df = df_CM
elif dataframe_choice == 'Sideback':
    df = df_Sideback
else: 
    df = df_Winger

# Klasterisasi
labels = kmeans_clustering(df.drop(['Name', 'Position'], axis=1), jumlah_klaster)

# Menampilkan hasil klasterisasi
st_title = '<p style="font-family:sans-serif ;font-weight:800; color:#FFD700; font-size: 50px;">Klasterisasi Pemain Sepak Bola Berdasarkan Posisi</p>'
st.markdown(st_title, unsafe_allow_html=True)
st_note = '<p style="font-family:sans-serif ;font-weight:600; color:#FFD700; font-size: 20px;">Dibuat oleh : Arkanantaaa | Data : Lapangbola.com</p>'
st.markdown(st_note, unsafe_allow_html=True)

is_note_clicked = st.button('Note')

# Menampilkan pesan pemberitahuan saat tombol "Note" dipencet
if is_note_clicked:
    st.info('Tentukan posisi pemain dan jumlah klaster yang ingin anda lakukan terlebih dahulu yang terletak pada bagian sidebar')


# Tampilkan tabel dengan data pemain dan klaster
df['Klaster'] = labels
st.write(df)

# Visualisasi hasil klasterisasi
fig, ax = plt.subplots()
scatter = ax.scatter(df['Name'], df['MoP'], c=labels, cmap='rainbow')
ax.set_xlabel(df['Name'])
ax.set_ylabel(df['MoP'])
ax.set_title('Klasterisasi Pemain Sepak Bola Berdasarkan Posisi')
ax.legend(*scatter.legend_elements(), title='Klaster')
st.pyplot(fig)

download_btn = st.button('Download Hasil Klasterisasi')

# Fungsi untuk menghasilkan tautan unduhan file CSV
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="hasil_klasterisasi.csv">Unduh CSV</a>'
    return href

# Mengunduh hasil klasterisasi
if download_btn:
    st.write('')
    st.subheader('Download Hasil Klasterisasi')
    st.markdown(filedownload(df), unsafe_allow_html=True)

