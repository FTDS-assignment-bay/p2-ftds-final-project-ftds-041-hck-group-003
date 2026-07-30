import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import prediction
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Path ke model pipeline
PIPELINE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'your_major_recomendation_pipeline.pkl')
ASSET_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_resource
def load_model():
    """Load pipeline artefacts"""
    pipe = joblib.load(PIPELINE_PATH)
    return pipe['scaler'], pipe['knn_model'], pipe['nilai_cols'], pipe['dataset_lengkap']


def kategori_nilai(avg):
    if avg > 800:
        return "🔥 OUTLIER!!"
    elif avg > 700:
        return "💪 Kamu OP! Nilai kamu di atas rata-rata!"
    elif avg > 550:
        return "✅ Good job, Nilai kamu sudah berada di ranah rata-rata."
    elif avg > 400:
        return "⚠️ Nilai kamu di ambang masalah. Masih ada peluang!"
    else:
        return "😬 Kamu mending mandiri ajalah. Semangat! Tapi tetep kok kita rekomendasikan 😏" 


def run():
    st.markdown("""
        <style>

        div[data-testid="stTextInput"] input{
            color: black !important;
            -webkit-text-fill-color: black !important;
            font-weight: bold !important;
        }
        
        div[data-testid="stNumberInput"] input{
            color: black !important;
            -webkit-text-fill-color: black !important;
            font-weight: bold !important;
        }
        
        div[data-testid="stTextInput"] input::placeholder{
            color:#666 !important;
            font-weight:600 !important;
        }
        button{
        color:black !important;
        
        </style>                   
        <div style='display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 10px;'>
            <img src="https://raw.githubusercontent.com/ridhanmf/YourMajor_Recomendation/main/YourMajor_Recomendation/logo_remove(1).png"width='90' style='flex-shrink: 0;'>
            <h1 style='margin: 0;'>Prediksi & Rekomendasi Jurusan</h1>
        </div>
        
    """, unsafe_allow_html=True)
    
    st.markdown('---')

    scaler, nn, nilai_cols, df = load_model()

    # Input nama
    nama = st.text_input('📋 Nama Peserta', placeholder='Masukkan nama kamu...')

    st.subheader('📝 Masukkan Nilai UTBK')

    col1, col2 = st.columns(2)

    with col1:
        nilai_biologi = st.number_input('🧬 Biologi', min_value=0, max_value=1000, value=600, step=10)
        nilai_fisika = st.number_input('⚡ Fisika', min_value=0, max_value=1000, value=600, step=10)
        nilai_kimia = st.number_input('🧪 Kimia', min_value=0, max_value=1000, value=600, step=10)
        nilai_matematika = st.number_input('📐 Matematika', min_value=0, max_value=1000, value=600, step=10)

    with col2:
        nilai_kmb = st.number_input('🧠 KMB', min_value=0, max_value=1000, value=600, step=10)
        nilai_kpu = st.number_input('📊 KPU', min_value=0, max_value=1000, value=600, step=10)
        nilai_kua = st.number_input('📏 KUA', min_value=0, max_value=1000, value=600, step=10)
        nilai_ppu = st.number_input('📝 PPU', min_value=0, max_value=1000, value=600, step=10)

    inputs = [nilai_biologi, nilai_fisika, nilai_kimia, nilai_matematika,
              nilai_kmb, nilai_kpu, nilai_kua, nilai_ppu]

    st.markdown('---')

    if st.button(' LETS GOO!!', type='primary', use_container_width=True):
        with st.spinner('Mencari siswa dengan nilai paling mirip...'):

            # Rata-rata + status
            avg = np.mean(inputs)
            msg = kategori_nilai(avg)

            # Transform input
            vals = np.array(inputs).reshape(1, -1)
            vals_scaled = scaler.transform(vals)

            # Cari tetangga
            distances, indices = nn.kneighbors(vals_scaled)
            neighbors = df.iloc[indices[0]].copy()
            neighbors['_distance'] = distances[0]

            # Ranking jurusan
            jurusan_rank = neighbors['jurusan_tujuan'].value_counts().head(10)
            total = len(neighbors)

            # Distribusi kategori
            kategori_dist = neighbors['kategori_jurusan'].value_counts()
            kategori_dominan = kategori_dist.index[0]
            kategori_pct = kategori_dist.iloc[0] / total * 100

            # Top kategori
            top_kategori = [(cat, round(cnt / total * 100, 1))
                           for cat, cnt in kategori_dist.head(4).items()]

            # === TAMPILKAN HASIL ===
            nama_tampil = nama if nama.strip() else "Peserta"
            st.success(f'✅ Rekomendasi untuk *{nama_tampil}* ditemukan!')

            # Baris 0: Status nilai
            rata_rata = round(avg, 1)
            st.info(f'📊 *Rata-rata nilai kamu: {rata_rata}*')
            st.markdown(f'### {msg}')

            # Baris 1: Bidang
            st.subheader('Bidang yang Direkomendasikan')

            col_cat = st.columns(len(top_kategori))
            for i, (cat, pct) in enumerate(top_kategori):
                with col_cat[i]:
                    if cat == kategori_dominan:
                        st.markdown(f"*🟢 {cat}*")
                    else:
                        st.markdown(f"⚪ {cat}")
                    st.progress(pct / 100, text=f'{pct:.0f}%')

            # Baris 2: Rekomendasi Jurusan
            st.subheader('🏆 Rekomendasi Jurusan Terbaik')

            for rank, (jurusan, cnt) in enumerate(jurusan_rank.items(), start=1):
                pct = cnt / total * 100
                if rank == 1:
                    icon = '🥇'
                elif rank == 2:
                    icon = '🥈'
                elif rank == 3:
                    icon = '🥉'
                else:
                    icon = f'{rank}.'

                st.markdown(f'{icon} *{jurusan}* — {cnt} siswa ({pct:.1f}%)')

    st.markdown('---')
    st.markdown('<div class="footer-note">© 2026 YourMajor — Muhammad Izzat, Ridhan Firdaus, Nicholas Calvin</div>', unsafe_allow_html=True)
