import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import base64

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

dt = pd.read_csv('dt.csv')
# dt_forward = pd.read_csv('dt_forward.csv')
# dt_attack = pd.read_csv('dt_attack.csv')
# dt_winger = pd.read_csv('dt_winger.csv')
# dt_midfielder = pd.read_csv('dt_midfielder.csv')
# dt_fullback = pd.read_csv('dt_fullback.csv')
# dt_CB = pd.read_csv('dt_CB.csv')

# unique_pos = ['Forward', 'Attacking 10', 'Midfielder', 'Winger', 'Fullback', 'Center Back']
# selected_pos = st.selectbox('Posisi', unique_pos, unique_pos)

# Preprocessing data
data_encoded = pd.get_dummies(dt.drop(['Name'], axis=1))

# Fungsi untuk melakukan klasterisasi
def kmeans_clustering(data, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    return kmeans.labels_

# Sidebar untuk memilih posisi pemain dan jumlah klaster
st.sidebar.header('Pilih posisi pemain yang ingin Diklasterisasi')
posisi_pemain = st.sidebar.selectbox('Posisi Pemain', dt['Position'].unique())
st.sidebar.subheader('Pilih jumlah klaster yang diinginkan')
jumlah_klaster = st.sidebar.slider('Jumlah Klaster', min_value=2, max_value=5, value=3, step=1)

# Filter data berdasarkan posisi pemain yang dipilih
filtered_data = dt[dt['Position'] == posisi_pemain]

# Fitur-fitur yang sesuai dengan posisi pemain
fitur_per_posisi = {
    'Forward': ['Shots Total', 'Goal', 'Create Chance', 'Shot On%', 'Conversion Ratio', 'Assist', 'Pass Accuracy', 'Dribble', 'Tackle', 'Intercept', 'Recovery', 'Aerial Won%'],
    'Attacking 10': ['Shots Total', 'Goal', 'Create Chance', 'Shot On%', 'Conversion Ratio', 'Assist', 'Pass Accuracy', 'Dribble', 'Cross', 'Tackle', 'Intercept', 'Recovery'],
    'Winger': ['Shots Total', 'Goal', 'Create Chance', 'Shot On%', 'Conversion Ratio', 'Assist', 'Pass Accuracy', 'Dribble', 'Cross', 'Tackle', 'Intercept', 'Recovery'],
    'Midfielder': ['Shots Total', 'Goal', 'Create Chance', 'Shot On%', 'Conversion Ratio', 'Assist', 'Pass Accuracy', 'Dribble', 'Tackle', 'Intercept', 'Recovery', 'Block'],
    'Fullback': ['Shots Total', 'Goal', 'Create Chance', 'Assist', 'Pass Accuracy', 'Dribble', 'Cross', 'Tackle', 'Intercept', 'Recovery', 'Block', 'Aerial Won%'],
    'Center Back': ['Shots Total', 'Goal', 'Assist', 'Pass Accuracy', 'Tackle', 'Intercept', 'Recovery', 'Block', 'Aerial Won%']
}

# Memilih fitur sesuai dengan posisi pemain
fitur = fitur_per_posisi[posisi_pemain]

# Filter data berdasarkan fitur yang dipilih
filtered_data = filtered_data[['Name', 'Position'] + fitur]

# Klasterisasi
labels = kmeans_clustering(filtered_data.drop(['Name', 'Position'], axis=1), jumlah_klaster)

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
filtered_data['Klaster'] = labels
st.write(filtered_data)

# Visualisasi hasil klasterisasi
fig, ax = plt.subplots()
scatter = ax.scatter(filtered_data[fitur[0]], filtered_data[fitur[1]], c=labels, cmap='rainbow')
ax.set_xlabel(fitur[0])
ax.set_ylabel(fitur[1])
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
    st.markdown(filedownload(filtered_data), unsafe_allow_html=True)

