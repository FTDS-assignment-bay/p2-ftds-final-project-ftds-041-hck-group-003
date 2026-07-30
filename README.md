# Your Major Recommendation (Sistem Rekomendasi Jurusan)

Aplikasi berbasis web untuk membantu calon mahasiswa menemukan jurusan dan universitas yang paling relevan berdasarkan simulasi profil nilai UTBK (Saintek) mereka. Proyek ini dibangun menggunakan **K-Nearest Neighbors (KNN)** dan di-*deploy* menggunakan **Streamlit**.

---

## Latar Belakang
Pemilihan jurusan kuliah seringkali menjadi fase yang membingungkan bagi calon mahasiswa. Sistem ini hadir untuk memberikan rekomendasi yang objektif dan berbasis data (*data-driven*). Dengan membandingkan profil nilai 8 mata uji pengguna terhadap lebih dari 86.000 data historis UTBK 2019, sistem akan mencari pola kecenderungan (mirip alumni) untuk menghasilkan daftar rekomendasi jurusan yang paling realistis.

## Dataset
Model ini dilatih menggunakan dataset **UTBK 2019 Domain Saintek (IPA)** dengan rincian:
* **Jumlah Data:** 86.569 siswa
* **Fitur Nilai (8 Mata Uji):** Biologi, Fisika, Kimia, Matematika, KMB, KPU, KUA, PPU.
* **Target:** 279 pilihan Jurusan dan 7 Kategori Bidang (Teknik, Kesehatan, Science, Pendidikan, dll.)

## Flow ETL
Sebelum data dipakai untuk modeling, ada tahap ETL yang jalan di lokal:

1. **Extract** — data mentah di-query dari PostgreSQL (via pgAdmin) dan disimpan sebagai CSV mentah (`data_merge.csv`). Karena data asli masih terpisah antar tabel, perlu JOIN manual agar ID siswa bisa bersambung ke nama jurusan & universitas.
2. **Clean** — dibersihin menggunakan Python: rename kolom, standarisasi singkatan seperti `PEND. → PENDIDIKAN`, `TEK. → TEKNOLOGI` memakai `replace_dict`, drop baris NULL yang gagal JOIN, plus mapping tiap jurusan ke 7 kategori bidang utama (Kesehatan, Teknik, Science, dll).
3. **Load** — hasil bersih disimpan sebagai `data_nilai_peserta.csv` yang siap dipake untuk training model KNN.

## Fitur Aplikasi
Aplikasi ini memiliki 3 halaman utama (Sistem Navigasi Multi-Halaman):
1. **Home:** Pengenalan aplikasi, cara kerja, dan informasi sekilas tentang dataset.
2. **EDA (Exploratory Data Analysis):** Visualisasi data eksploratif seperti distribusi siswa per bidang, *box plot* sebaran nilai, *heatmap*, hingga *ranking* jurusan paling diminati.
3. **Prediksi & Rekomendasi:** Antarmuka interaktif di mana pengguna dapat menginput 8 nilai UTBK mereka dan mendapatkan hasil *Top-Ranking* jurusan terbaik secara *real-time*.

## Cara Kerja Model (Pipeline)
1. **Pemrosesan Input:** Menerima 8 skor UTBK siswa dan menyetarakan skalanya menggunakan `StandardScaler` agar pembobotan nilai merata.
2. **Pencarian Pola:** Mencari **100 data alumni** historis (K=100) dengan profil kemampuan paling identik menggunakan jarak *Euclidean* (`NearestNeighbors`).
3. **Hasil Analisis:** Melakukan sistem *majority voting* dari 100 alumni tersebut untuk menentukan probabilitas dan rekomendasi kategori serta jurusan terbaik.

## Struktur Direktori

```bash
Data Analyst/                        # Folder untuk visualisasi & presentasi
├── Plot_1.jpeg                      # Plot distribusi kategori jurusan
├── Plot_2.jpeg                      # Plot rata-rata nilai per kategori
├── Plot_3.jpeg                      # Plot box plot sebaran nilai
├── Plot_4.jpeg                      # Plot heatmap korelasi nilai
├── Plot_5.jpeg                      # Plot jurusan paling diminati
├── Streamlit.jpeg                   # Screenshot aplikasi Streamlit
└── YourMajor_Presentation.pdf       # Slide presentasi final

Data Engineer/              # Folder untuk pipeline ETL & data mentah
├── data-raw/               # Data mentah dari PostgreSQL
├── .env                    # Environment variables (koneksi DB, dll)
├── airflow.yaml            # Docker Compose untuk Airflow
├── data_merge.csv          # Hasil extract dari PostgreSQL (mentah)
├── data_merge_clean.csv    # Data setelah proses cleaning
├── data_nilai_peserta.csv  # Dataset final siap pakai
├── ddl.txt                 # Script DDL untuk VIEW di pgAdmin
└── etl_utbk_pipeline.py    # DAG Airflow (extract >> clean >> load)

Data Science/               # Folder untuk modeling & rekomendasi
├── model_your_major.ipynb  # Notebook training KNN
└── your_major_recomendation_pipeline.pkl  # Artefak model (Scaler + KNN + Data)

Deployment/                          # Folder untuk deploy aplikasi Streamlit
├── WEARE003.jpeg                    # Logo/icon app
├── app.py                           # Router utama Streamlit
├── avg_nilai_nilai.jpeg             # Plot rata-rata nilai per kategori
├── box_plot.jpeg                    # Plot box plot sebaran nilai
├── data_nilai_peserta.csv           # Dataset final untuk training
├── eda.py                           # Halaman Exploratory Data Analysis
├── gambar_kampus.jpeg               # Banner halaman Home
├── heatmap_kategori.jpeg            # Plot heatmap korelasi nilai
├── kategori_jurusan.jpeg            # Plot distribusi kategori jurusan
├── logo_removebg.png                # Logo utama aplikasi
├── minat_terbanyak.jpeg             # Plot jurusan paling diminati
├── prediction.py                    # Halaman Prediksi & Rekomendasi
├── requirements.txt                 # Library dependencies
└── your_major_recomendation_pipeline.pkl  # Artefak model (Scaler + KNN + Data)
```
