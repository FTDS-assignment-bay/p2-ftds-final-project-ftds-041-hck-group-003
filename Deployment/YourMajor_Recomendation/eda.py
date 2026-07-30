import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

sns.set_style('whitegrid')

# Path ke model pipeline
PIPELINE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'your_major_recomendation_pipeline.pkl')
ASSET_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_resource
def load_model():
    df = joblib.load(PIPELINE_PATH)['dataset_lengkap']
    return df


def inject_css():
    st.markdown("""
    <style>
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
            padding: 20px 22px;
            height: 100%;
        }
        .card h4 {
            color: #FF6B4A;
            margin: 0 0 10px 0;
            font-size: 15px;
        }
        .card ul { margin: 0; padding-left: 18px; }
        .card li { color: #E4E6EA; font-size: 14px; line-height: 1.9; }
        .card li b { color: #FAFAFA; }

        .insight-box {
            background: #201A14;
            border-left: 4px solid #FF6B4A;
            border-radius: 10px;
            padding: 14px 18px;
            margin: 14px 0 6px 0;
        }
        .insight-box .insight-label {
            color: #FF6B4A;
            font-weight: 700;
            font-size: 13px;
            margin-bottom: 6px;
            display: block;
        }
        .insight-box p {
            color: #D6D9DE;
            font-size: 14px;
            line-height: 1.65;
            margin: 0;
        }
        .insight-box b { color: #FAFAFA; }

        .html-table-wrap {
            background: #1A1D24;
            border: 1px solid #2A2E37;
            border-radius: 14px;
            padding: 6px 20px;
            overflow-x: auto;
        }
        table.html-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13.5px;
        }
        table.html-table th {
            text-align: left;
            color: #FF6B4A;
            font-weight: 700;
            padding: 10px 8px;
            border-bottom: 2px solid #2A2E37;
        }
        table.html-table td {
            color: #E4E6EA;
            padding: 9px 8px;
            border-bottom: 1px solid #23262E;
        }
        table.html-table tr:last-child td { border-bottom: none; }

        .stat-pill-row { display: flex; gap: 12px; flex-wrap: wrap; }
        .stat-pill {
            background: #1A1D24;
            border: 1px solid #2A2E37;
            border-radius: 12px;
            padding: 14px 18px;
            flex: 1;
            min-width: 150px;
        }
        .stat-pill .label { color: #9AA0AA; font-size: 12.5px; }
        .stat-pill .value { color: #FF6B4A; font-size: 20px; font-weight: 800; margin-top: 4px; }

        .footer-note {
            text-align: center;
            color: #6B7078;
            font-size: 13px;
            margin-top: 30px;
            padding-top: 18px;
            border-top: 1px solid #2A2E37;
        }
    </style>
    """, unsafe_allow_html=True)


def df_to_html_table(df: pd.DataFrame, index_label: str = None) -> str:
    """Render DataFrame jadi tabel HTML bergaya kartu gelap (konsisten dengan tema app)."""
    headers = ([index_label] if index_label else ['']) + list(df.columns)
    thead = ''.join(f'<th>{h}</th>' for h in headers)

    rows = ''
    for idx, row in df.iterrows():
        cells = f'<td><b>{idx}</b></td>' + ''.join(f'<td>{v}</td>' for v in row)
        rows += f'<tr>{cells}</tr>'

    return f"""
    <div class="html-table-wrap">
        <table class="html-table">
            <thead><tr>{thead}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """


def insight_box(text_html: str):
    st.markdown(f"""
    <div class="insight-box">
        <span class="insight-label">💡 INSIGHT</span>
        <p>{text_html}</p>
    </div>
    """, unsafe_allow_html=True)


def run():
    inject_css()

    st.title('📊 Exploratory Data Analysis (EDA)')
    st.markdown("""
    Halaman ini menampilkan eksplorasi data dari <b>86.569 siswa UTBK 2019 Saintek</b>
    dengan <b>279 jurusan</b> dan <b>7 kategori bidang</b>.
    """, unsafe_allow_html=True)
    st.markdown('---')

    df = load_model()
    total = len(df)
    nilai_cols = ['nilai_biologi', 'nilai_fisika', 'nilai_kimia', 'nilai_matematika',
                  'nilai_kmb', 'nilai_kpu', 'nilai_kua', 'nilai_ppu']


    # 1. DISTRIBUSI SISWA PER BIDANG (Kategori Jurusan)
    st.markdown('<div class="section-title">1️⃣ Distribusi Siswa per Bidang</div>', unsafe_allow_html=True)

    col_img, _ = st.columns([3, 1])
    with col_img:
        st.image(os.path.join(ASSET_DIR, 'kategori_jurusan.jpeg'),
                 caption='Kategori Jurusan — Distribusi siswa per bidang (Saintek)',
                 use_container_width=True)

    cat_dist = df['kategori_jurusan'].value_counts()
    col1, col2 = st.columns(2)
    with col1:
        items = ''.join(
            f'<li><b>{cat}</b>: {cnt:,} ({cnt/total*100:.2f}%)</li>'
            for cat, cnt in cat_dist.items()
        )
        st.markdown(f"""
        <div class="card">
            <h4>Distribusi Siswa</h4>
            <ul>{items}</ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-pill-row" style="flex-direction:column;">
            <div class="stat-pill"><div class="label">TOTAL SISWA</div><div class="value">{total:,}</div></div>
            <div class="stat-pill"><div class="label">DOMAIN</div><div class="value" style="font-size:16px;">Saintek (IPA)</div></div>
            <div class="stat-pill"><div class="label">TAHUN</div><div class="value" style="font-size:16px;">2019</div></div>
        </div>
        """, unsafe_allow_html=True)

    insight_box(
        "<b>Teknik</b> (29,12%) mendominasi diikuti <b>Kesehatan</b> (26,04%) dan <b>Science</b> (22,38%). "
        "Ketiganya mencakup <b>77,54%</b> dari total siswa. Sementara <b>Sosial</b> (2,92%) paling sedikit diminati — "
        "wajar karena dataset ini khusus Saintek."
    )

    st.markdown('---')

    
    # 2. RATA-RATA NILAI KESELURUHAN (AVG Nilai-Nilai)
    st.markdown('<div class="section-title">2️⃣ Rata-rata Nilai Keseluruhan (86.569 Siswa)</div>', unsafe_allow_html=True)

    col_img, _ = st.columns([3, 1])
    with col_img:
        st.image(os.path.join(ASSET_DIR, 'avg_nilai_nilai.jpeg'),
                 caption='AVG Nilai-Nilai — Rata-rata 8 mata uji seluruh siswa',
                 use_container_width=True)

    avg_values = df[nilai_cols].mean().sort_values(ascending=False)
    avg_list = list(avg_values.items())

    col1, col2 = st.columns(2)
    with col1:
        items = ''.join(
            f'<li>{i}. <b>{col.replace("nilai_", "").upper()}</b>: {val:.2f}</li>'
            for i, (col, val) in enumerate(avg_list, 1)
        )
        st.markdown(f"""
        <div class="card">
            <h4>Rata-rata per Mata Uji (descending)</h4>
            <ul>{items}</ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-pill-row" style="flex-direction:column;">
            <div class="stat-pill"><div class="label">📈 TERTINGGI</div><div class="value" style="font-size:16px;">{avg_list[0][0].replace("nilai_", "").upper()} ({avg_list[0][1]:.2f})</div></div>
            <div class="stat-pill"><div class="label">📉 TERENDAH</div><div class="value" style="font-size:16px;">{avg_list[-1][0].replace("nilai_", "").upper()} ({avg_list[-1][1]:.2f})</div></div>
            <div class="stat-pill"><div class="label">📊 RATA-RATA TOTAL</div><div class="value">{avg_values.mean():.2f}</div></div>
        </div>
        """, unsafe_allow_html=True)

    insight_box(
        "Nilai <b>KPU</b> (569,94) dan <b>KUA</b> (569,15) konsisten paling tinggi, "
        "sementara <b>Matematika</b> (529,49) dan <b>Biologi</b> (537,14) paling rendah. "
        "Ini menarik karena Matematika sering dianggap mata uji tersulit di Saintek."
    )

    st.markdown('---')

    # 3. BOX PLOT — SEBARAN NILAI PER MATA UJI
    st.markdown('<div class="section-title">3️⃣ Sebaran Nilai per Mata Uji (Box Plot)</div>', unsafe_allow_html=True)

    col_img, _ = st.columns([3, 1])
    with col_img:
        st.image(os.path.join(ASSET_DIR, 'box_plot.jpeg'),
                 caption='Box Plot Outlier Numeric — Sebaran nilai per mata uji',
                 use_container_width=True)

    nama_nilai = ['Nilai Biologi', 'Nilai Fisika', 'Nilai Kimia', 'Nilai Matematika',
                  'Nilai KMB', 'Nilai KPU', 'Nilai KUA', 'Nilai PPU']
    stats_df = df[nilai_cols].describe().T
    stats_df.index = nama_nilai
    stats_df = stats_df[['min', '25%', '50%', '75%', 'max', 'mean', 'std']]
    stats_df = stats_df.round(1)
    stats_df.columns = ['Min', 'Q1', 'Median', 'Q3', 'Max', 'Mean', 'Std']
    st.markdown(df_to_html_table(stats_df, index_label='Mata Uji'), unsafe_allow_html=True)

    insight_box(
        "Nilai maksimum mencapai <b>1.123</b> (Matematika — kemungkinan nilai bonus/eksperimen), "
        "sementara nilai minimum ada di <b>193</b> (KPU). Box plot menunjukkan distribusi cukup simetris "
        "dengan median di kisaran 520-570. Banyak outlier di atas, tapi jarang di bawah — artinya "
        "siswa cenderung punya nilai tinggi di beberapa mata uji tertentu."
    )

    st.markdown('---')

    # 4. HEATMAP — RATA-RATA NILAI PER KATEGORI
    st.markdown('<div class="section-title">4️⃣ Rata-rata Nilai per Bidang (Heatmap)</div>', unsafe_allow_html=True)

    col_img, _ = st.columns([3, 1])
    with col_img:
        st.image(os.path.join(ASSET_DIR, 'heatmap_kategori.jpeg'),
                 caption='AVG Nilai Pada Kategori Jurusan — Rata-rata nilai per bidang',
                 use_container_width=True)

    cols_short = ['Bio', 'Fis', 'Kim', 'Mat', 'KMB', 'KPU', 'KUA', 'PPU']
    avg_df = df.groupby('kategori_jurusan')[nilai_cols].mean().round(2)
    avg_df.columns = cols_short

    max_val = avg_df.max().max()
    max_loc = avg_df.stack().idxmax()
    min_val = avg_df.min().min()
    min_loc = avg_df.stack().idxmin()

    insight_box(
        f"<b>{max_loc[0]}</b> punya nilai rata-rata tertinggi di <b>{max_loc[1]}</b> ({max_val:.2f}), "
        f"sementara <b>{min_loc[0]}</b> punya nilai terendah di <b>{min_loc[1]}</b> ({min_val:.2f}). "
        f"Menariknya, <b>Pendidikan</b> konsisten lebih rendah di hampir semua mata uji, "
        f"sementara <b>Teknik</b> dan <b>Kesehatan</b> mendominasi nilai-nilai tertinggi."
    )

    st.markdown('---')

    # 5. TOP JURUSAN PALING DIMINATI
    st.markdown('<div class="section-title">5️⃣ Jurusan Dengan Minat Terbanyak</div>', unsafe_allow_html=True)

    col_img, _ = st.columns([3, 1])
    with col_img:
        st.image(os.path.join(ASSET_DIR, 'minat_terbanyak.jpeg'),
                 caption='Jurusan Dengan Minat Terbanyak — Top 40 jurusan paling diminati',
                 use_container_width=True)

    top10 = df['jurusan_tujuan'].value_counts().head(10).reset_index()
    top10.columns = ['Jurusan', 'Jumlah Siswa']
    top10.index = range(1, len(top10) + 1)
    st.markdown(df_to_html_table(top10, index_label='#'), unsafe_allow_html=True)

    insight_box(
        "<b>PENDIDIKAN DOKTER</b> sekitar 6.000 siswa menjadi jurusan paling diminati — "
        "hampir <b>2x lipat</b> dari <b>Teknik Sipil</b> menjadi ke nominasi ke 2 sekitar 3.800. Menariknya, <b>Kedokteran</b> 1.700 "
        "hanya di peringkat #12, menunjukkan siswa lebih memilih <b>Pendidikan Dokter</b> yang jenjangnya "
        "lebih pendek. Jurusan IT/komputer seperti <b>Teknik Informatika</b> skitar 3.000 dan "
        "<b>Sistem Informasi</b> juga masuk 15 besar."
    )

    st.markdown('<div class="footer-note">© 2026 YourMajor — Muhammad Izzat, Ridhan Firdaus, Nicholas Calvin</div>', unsafe_allow_html=True)
