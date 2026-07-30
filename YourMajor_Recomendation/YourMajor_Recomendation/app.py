import sys
import os

# Tambah path biar bisa import eda.py & prediction.py dari folder yang sama
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import base64
import eda
import prediction
from PIL import Image

# =========================
# Path Asset
# =========================
LOGO_PATH = os.path.join(BASE_DIR, "logo_removebg.png")
KAMPUS_PATH = os.path.join(BASE_DIR, "gambar_kampus.jpeg")
WE_PATH = os.path.join(BASE_DIR, "WEARE003.jpeg")

# =========================
# Page Config
# =========================
icon = Image.open(LOGO_PATH)
st.set_page_config(
    page_title="YourMajor Recommendation",
    page_icon=icon,
    layout="wide"
)


# =========================
# Helper: encode gambar ke base64 (biar bisa dipakai di <img> HTML)
# =========================
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# =========================
# Global CSS
# =========================
def inject_css():
    st.markdown("""
    <style>
        .stApp { background-color: #0E1117; }

        .hero {
            position: relative;
            border-radius: 18px;
            overflow: hidden;
            margin-bottom: 28px;
        }
        .hero img {
            width: 100%;
            height: 320px;
            object-fit: cover;
            filter: brightness(45%);
        }
        .hero-overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 0 48px;
        }
        .hero-title {
            font-size: 42px;
            font-weight: 800;
            color: #FFFFFF;
            margin: 0;
        }
        .hero-subtitle {
            font-size: 17px;
            color: #E0E0E0;
            margin-top: 10px;
            max-width: 560px;
        }
        .hero2 {
            display: flex;
            justify-content: center;
            margin-top: 30px;
            margin-bottom: 30px;
        }

        .hero2 img {
            width: 80%;
            max-width: 900px;
            height: auto;
            border-radius: 18px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.35);
        }
        
        .section-title {
            font-size: 22px;
            font-weight: 700;
            color: #FAFAFA;
            margin: 6px 0 16px 0;
            border-left: 5px solid #FF6B4A;
            padding-left: 12px;
        }

        .card {
            background: #1A1D24;
            border: 1px solid #2A2E37;
            border-radius: 14px;
            padding: 22px 22px;
            height: 100%;
        }
        .card h4 {
            color: #FF6B4A;
            margin: 0 0 8px 0;
            font-size: 17px;
        }
        .card p {
            color: #C9CDD3;
            font-size: 14px;
            line-height: 1.55;
            margin: 0;
        }

        .step-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 30px; height: 30px;
            border-radius: 50%;
            background: #FF6B4A;
            color: white;
            font-weight: 700;
            font-size: 14px;
            margin-right: 10px;
            flex-shrink: 0;
        }
        .step-row {
            display: flex;
            align-items: flex-start;
            margin-bottom: 14px;
        }
        .step-text {
            color: #E4E6EA;
            font-size: 14.5px;
            padding-top: 3px;
        }
        .step-text b { color: #FAFAFA; }

        .stat-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        .stat-table td {
            padding: 10px 8px;
            border-bottom: 1px solid #2A2E37;
            color: #E4E6EA;
        }
        .stat-table td:first-child { color: #9AA0AA; }
        .stat-table td:last-child {
            text-align: right;
            font-weight: 700;
            color: #FF6B4A;
        }

        .footer-note {
            text-align: center;
            color: #6B7078;
            font-size: 13px;
            margin-top: 36px;
            padding-top: 18px;
            border-top: 1px solid #2A2E37;
        }

        section[data-testid="stSidebar"] .sidebar-credit {
            font-size: 13px;
            color: #000000;
            line-height: 1.7;
        }
        section[data-testid="stSidebar"] .sidebar-credit b { color: #000000; }
        section[data-testid="stSidebar"] .sidebar-tag {
            font-size: 12.5px;
            color: #000000;
            line-height: 1.5;
        }
        section[data-testid="stSidebar"] label {
            color: #000000 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def main():
    inject_css()

    # Logo
    st.sidebar.image(LOGO_PATH, use_container_width=True)
    st.sidebar.markdown("---")

    page = st.sidebar.selectbox(
        "Pilih Halaman",
        ("Home", "EDA", "Prediksi")
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div class="sidebar-tag">
        Rekomendasi Jurusan &amp; Universitas<br>
        Berdasarkan Nilai UTBK 2019 Saintek
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <br>
    <div class="sidebar-credit">
        <i>Created by:</i><br>
        • Muhammad Izzat<br>
        • Ridhan Firdaus<br>
        • Nicholas Calvin
    </div>
    """, unsafe_allow_html=True)

    if page == "Home":
        show_home()
    elif page == "EDA":
        eda.run()
    elif page == "Prediksi":
        prediction.run()


def show_home():
    # ---------- HERO ----------
    kampus_b64 = img_to_base64(KAMPUS_PATH)
    st.markdown(f"""
    <div class="hero">
        <img src="data:image/jpeg;base64,{kampus_b64}">
        <div class="hero-overlay">
            <p class="hero-title">🎓 YourMajor Recommendation</p>
            <p class="hero-subtitle">
                Temukan jurusan dan universitas yang paling sesuai dengan nilai UTBK kamu,
                berbasis data 86.569 peserta UTBK 2019 Saintek.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- WELCOME + WORKFLOW ----------
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown('<div class="section-title">Workflow</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="step-row">
            <div class="step-badge">1</div>
            <div class="step-text"><b>Input</b> 8 nilai UTBK kamu (KMB, KPU, KUA, PPU, Matematika, Fisika, Kimia, Biologi)</div>
        </div>
        <div class="step-row">
            <div class="step-badge">2</div>
            <div class="step-text"><b>Cari</b> 100 siswa dengan profil nilai paling mirip dari 86.569 data UTBK 2019 Saintek</div>
        </div>
        <div class="step-row">
            <div class="step-badge">3</div>
            <div class="step-text"><b>Ranking</b> jurusan berdasarkan pola pilihan siswa-siswa yang mirip denganmu</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="margin-top:28px;">Pages</div>', unsafe_allow_html=True)
        pcol1, pcol2, pcol3 = st.columns(3)
        with pcol1:
            st.markdown("""
            <div class="card">
                <h4>🏠 Home</h4>
                <p>Beranda & informasi umum project ini.</p>
            </div>
            """, unsafe_allow_html=True)
        with pcol2:
            st.markdown("""
            <div class="card">
                <h4>📊 EDA</h4>
                <p>Eksplorasi & visualisasi data UTBK 2019.</p>
            </div>
            """, unsafe_allow_html=True)
        with pcol3:
            st.markdown("""
            <div class="card">
                <h4>🎯 Prediksi</h4>
                <p>Dapatkan rekomendasi jurusan sesuai nilaimu.</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Info Dataset</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <table class="stat-table">
                <tr><td>Sumber</td><td>UTBK 2019 Saintek</td></tr>
                <tr><td>Jumlah Siswa</td><td>86.569</td></tr>
                <tr><td>Nilai Diinput</td><td>8 mata uji</td></tr>
                <tr><td>Pilihan Jurusan</td><td>279</td></tr>
                <tr><td>Kategori Bidang</td><td>7</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        WE_PATH_b64 = img_to_base64(WE_PATH)
    st.markdown(f"""
    <div class="hero2">
        <img src="data:image/jpeg;base64,{WE_PATH_b64}">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="footer-note">© 2026 YourMajor — Muhammad Izzat, Ridhan Firdaus, Nicholas Calvin</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
