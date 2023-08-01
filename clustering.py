import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from math import pi
import numpy as np
import base64

tab1, tab2, tab3 = st.tabs(["Melihat Pemain", "Klastering Pemain", "Perbandingan Pemain"])
with tab1:
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1599204606350-d7fb87de75f6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80");
            background-size: cover;
            }
        </style>
        """,
        unsafe_allow_html=True)
    
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
    dataframe_choice = st.selectbox("Pilih Posisi Pemain", ['CF', 'CB', 'AM', 'CM', 'Sideback', 'Winger'])

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
        data_encoded = pd.get_dummies(df.drop(['Name'], axis=1))

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

    with tab3:
        df_CF = pd.read_excel('df_CF.xlsx')
        df_CB = pd.read_excel('df_CB.xlsx')
        df_AM = pd.read_excel('df_AM.xlsx')
        df_CM = pd.read_excel('df_CM.xlsx')
        df_Sideback = pd.read_excel('df_Sideback.xlsx')
        df_Winger = pd.read_excel('df_Winger.xlsx')
        
        dataframe_choice = st.selectbox("Pilih Posisi Pemain", ['CF', 'CB', 'AM', 'CM', 'Sideback', 'Winger'])
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

        def get_similar_players(player_name):
            player_index = [list(df['Name']).index(x) for x in list(df['Name']) if player_name in x]
            player_index = int(player_index[0])
            df = df.iloc[:, 1:]
            cos = cosine_similarity(df, df)
            player_cos = sorted(list(cos[player_index]))[-4:-1]
            indexes = [list(cos[player_index]).index(x) for x in player_cos]
            indexes.append(player_index)
            plot_df = df.iloc[indexes]
            plot_df1 = plot_df
            plot_df1.reset_index(drop=True, inplace=True)
            plot_df1.reindex(index=range(0, 5))
            plot_categories = list(plot_df1)[1:]
            plot_values = plot_df1.mean().values.flatten().tolist()
            plot_values += plot_values[:1]
            angles = [n / float(len(plot_categories)) * 2 * pi for n in range(len(plot_categories))]
            angles += angles[:1]
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10), subplot_kw=dict(polar=True))
            plt.xticks(angles[:-1], plot_categories, color='grey', size=12)
            plt.yticks(np.arange(0.0, 1.2, 0.2), ['0', '20', '40', '60', '80', '100'], color='grey', size=12)
            plt.ylim(0, 1)
            ax.set_rlabel_position(30)
            for i in range(len(plot_df1)):
                val_c1 = plot_df1.loc[i].drop('Name').values.flatten().tolist()
                val_c1 += val_c1[:1]
                ax.plot(angles, val_c1, linewidth=1.5, linestyle='solid', label=plot_df1.loc[i]["Name"])
                ax.fill(angles, val_c1, alpha=0.1)
            plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
            st.pyplot(fig)

        # Streamlit app starts here
        st.title('Player Similarity Analysis')
        player_name = st.text_input('Enter player name:')
        if player_name:
            player_cos, similar_players_df, _ = get_similar_players(player_name)
            st.write('Most similar players:')
            st.write(similar_players_df)
