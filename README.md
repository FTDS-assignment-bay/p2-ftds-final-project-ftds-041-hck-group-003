# Your Major Recommendation (Sistem Rekomendasi Jurusan)

Aplikasi berbasis web untuk membantu calon mahasiswa menemukan jurusan dan universitas yang paling relevan berdasarkan simulasi profil nilai UTBK (Saintek) mereka. Proyek ini dibangun menggunakan **K-Nearest Neighbors (KNN)** dan di-*deploy* menggunakan **Streamlit**.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

---

## Latar Belakang
Pemilihan jurusan kuliah seringkali menjadi fase yang membingungkan bagi calon mahasiswa. Sistem ini hadir untuk memberikan rekomendasi yang objektif dan berbasis data (*data-driven*). Dengan membandingkan profil nilai 8 mata uji pengguna terhadap lebih dari 86.000 data historis UTBK 2019, sistem akan mencari pola kecenderungan (mirip alumni) untuk menghasilkan daftar rekomendasi jurusan yang paling realistis.

## Dataset
Model ini dilatih menggunakan dataset **UTBK 2019 Domain Saintek (IPA)** dengan rincian:
* **Jumlah Data:** 86.569 siswa
* **Fitur Nilai (8 Mata Uji):** Biologi, Fisika, Kimia, Matematika, KMB, KPU, KUA, PPU.
* **Target:** 279 pilihan Jurusan dan 7 Kategori Bidang (Teknik, Kesehatan, Science, Pendidikan, dll.)

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
├── app.py                      # Router utama Streamlit (Sidebar navigation)
├── eda.py                      # Halaman Exploratory Data Analysis
├── prediction.py               # Halaman input model & output rekomendasi
├── requirements.txt            # Daftar library (Streamlit, Pandas, Scikit-Learn, dll)
├── your_major_recomendation_pipeline.pkl  # Artefak model ML (Scaler + KNN + Data)
└── /assets                     # Direktori penyimpanan gambar/plot untuk EDA
