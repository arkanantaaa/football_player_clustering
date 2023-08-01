import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from math import pi
import numpy as np
import base64

tab1, tab2 = st.tabs(["Melihat Pemain", "Klastering Pemain"])
with tab1:    
    # Fungsi untuk mengambil data dari dataframe berdasarkan kategori tipe defence
    def get_players_by_defence(df, defence_type):
        return df[df['Defence'] == defence_type]
    
    # Fungsi untuk mengambil data dari dataframe berdasarkan kategori tipe attack
    def get_players_by_attack(df, attack_type):
        return df[df['Attack'] == attack_type]

    df_CF = pd.read_excel('df_CF.xlsx')
    df_CB = pd.read_excel('df_CB.xlsx')
    df_AM = pd.read_excel('df_AM.xlsx')
    df_CM = pd.read_excel('df_CM.xlsx')
    df_Sideback = pd.read_excel('df_Sideback.xlsx')
    df_Winger = pd.read_excel('df_Winger.xlsx')

    # Tampilkan aplikasi Streamlit
    st.title('Melihat pemain berdasarkan posisi dan gaya bermain tertentu')

    # Pilihan untuk memilih dataframe posisi
    dataframe_choice = st.selectbox("Pilih Posisi Pemain", ['CF', 'CB', 'AM', 'CM', 'Sideback', 'Winger'], key='dataframe_choice')

    # Pilihan untuk memilih kategori tipe defence atau attack
    type_choice = st.radio("Pilih kategori pemain", ['Defence', 'Attack'])

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

    # Jika pilihan adalah 'Defence', tampilkan opsi untuk memilih jenis pertahanan
    if type_choice == 'Defence':
        defence_type = st.radio("Pilih gaya bermain", df['Defence'].dropna().unique())
        selected_players = get_players_by_defence(df, defence_type)
        st.subheader('Pemain dengan Kategori Defence dan gaya bermain : ' + defence_type)
        st.table(selected_players[['Name', 'Defence']])

    # Jika pilihan adalah 'Attack', tampilkan opsi untuk memilih jenis serangan
    elif type_choice == 'Attack':
        attack_type = st.radio("Pilih gaya bermain", df['Attack'].dropna().unique())
        selected_players = get_players_by_attack(df, attack_type)
        st.subheader('Pemain dengan Kategori Attack dan gaya bermain : ' + attack_type)
        st.table(selected_players[['Name', 'Attack']])

    with tab2:
        df_CF = pd.read_excel('df_CF(1).xlsx')
        df_CB = pd.read_excel('df_CB(1).xlsx')
        df_AM = pd.read_excel('df_AM(1).xlsx')
        df_CM = pd.read_excel('df_CM(1).xlsx')
        df_Sideback = pd.read_excel('df_Sideback(1).xlsx')
        df_Winger = pd.read_excel('df_Winger(1).xlsx')

        # Preprocessing data
        data_encoded = pd.get_dummies(df.drop(['Name', 'Position', 'Defence', 'Attack'], axis=1))

        # Fungsi untuk melakukan klasterisasi
        def kmeans_clustering(data, n_clusters):
            kmeans = KMeans(n_clusters=n_clusters)
            kmeans.fit(data)
            return kmeans.labels_
        
        pilih_df = st.selectbox("Pilih Posisi Pemain", ['CF', 'CB', 'AM', 'CM', 'Sideback', 'Winger'], key='pilih_df')
        st.subheader('Pilih jumlah klaster yang diinginkan')
        jumlah_klaster = st.slider('Jumlah Klaster', min_value=2, max_value=5, value=3, step=1)

        if pilih_df == 'CF':
            df = df_CF
            xlabel = 'Shots Total'
            ylabel = 'Goal'
        elif pilih_df == 'CB':
            df = df_CB
            xlabel = 'ClearInter 1A-2E'
            ylabel = 'Long Ball Ratio'
        elif pilih_df == 'AM':
            df = df_AM
            xlabel = 'Key Pass'
            ylabel = 'Pass Completion%'
        elif pilih_df == 'CM':
            df = df_CM
            xlabel = 'Pass Total'
            ylabel = 'Pass Completion%'
        elif pilih_df == 'Sideback':
            df = df_Sideback
            xlabel = 'ClearInter 1A-2E'
            ylabel = 'Cross 5A-6E'
        else: 
            df = df_Winger
            xlabel = 'Cross 4A-6E'
            ylabel = 'Key Pass'
            
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
        scatter = ax.scatter(df[xlabel], df[ylabel], c=labels, cmap='rainbow')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title('Klasterisasi Pemain Sepak Bola Berdasarkan Posisi')
        ax.legend(*scatter.legend_elements(), title='Klaster')
        st.pyplot(fig)
        download_btn = st.button('Download Hasil Klasterisasi')

        # Fungsi untuk menghasilkan tautan unduhan file CSV
        def filedownload(df):
            csv = df.to_excel(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="hasil_klasterisasi.xlsx">Unduh CSV</a>'
            return href

        # Mengunduh hasil klasterisasi
        if download_btn:
            st.write('')
            st.subheader('Download Hasil Klasterisasi')
            st.markdown(filedownload(df), unsafe_allow_html=True)
