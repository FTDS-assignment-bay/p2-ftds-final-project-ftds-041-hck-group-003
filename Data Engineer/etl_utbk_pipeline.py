'''
DAG — ETL UTBK Pipeline
Mengambil data dari PostgreSQL, merge, cleaning, output ke CSV
Output: /opt/airflow/output/data_nilai_peserta.csv
'''

import datetime as dt
import pandas as pd
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator


# Fungsi Extract: ambil + join dari postgres

def extract_from_postgres():
    connection = psycopg2.connect(
        user="airflow",
        password="airflow",
        host="postgres",
        port="5432",
        dbname="utbk_data"
    )

    df = pd.read_sql('SELECT * FROM scores_science_merged ', connection)

    # Simpan raw ke file
    df.to_csv('/opt/airflow/dags/data_merge.csv', index=False)


# Fungsi Load: baca csv dari extract

def clean():
    # Membaca dataset
    df = pd.read_csv('/opt/airflow/dags/data_merge.csv')
    
    # Drop baris yang kosong
    df = df.dropna()

    # Drop duplikat
    df = df.drop_duplicates()

    # Buat dictionary pemetaan nama kolom (lama: baru)
    rename_columns = {
        'score_bio': 'nilai_biologi',
        'score_fis': 'nilai_fisika',
        'score_kim': 'nilai_kimia',
        'score_mat': 'nilai_matematika',
        'score_kmb': 'nilai_kmb',
        'score_kpu': 'nilai_kpu',
        'score_kua': 'nilai_kua',
        'score_ppu': 'nilai_ppu',
        'major_name': 'jurusan_tujuan',
        'university_name': 'universitas_tujuan'
    }

    # Rename kolom pada DataFrame
    df.rename(columns=rename_columns, inplace=True)

    # Dictionary penggantian singkatan
    replace_dict = {
        'PEND.': 'PENDIDIKAN',
        'FAK.': 'FAKULTAS',
        'SEK.': 'SEKOLAH',
        'TEK.': 'TEKNOLOGI',
        'TEKNO.': 'TEKNOLOGI',
        'PROG.': 'PROGRAM'
    }

    # Perulangan standarisasi
    for old, new in replace_dict.items():
        df['jurusan_tujuan'] = df['jurusan_tujuan'].str.replace(old, new, regex=False)

    # Bersihin spasi berlebih
    df['jurusan_tujuan'] = df['jurusan_tujuan'].str.replace(r'\s+', ' ', regex=True).str.strip()
    df['universitas_tujuan'] = df['universitas_tujuan'].str.replace(r'\s+', ' ', regex=True).str.strip()

    
    # Mapping kategori jurusan
    
    def kategori_jurusan(jurusan):
        jurusan = str(jurusan).upper()

        # ================== KESEHATAN ==================
        if any(x in jurusan for x in [
            "KEDOKTERAN",
            "DOKTER",
            "DOKTER GIGI",
            "GIGI",
            "FARMASI",
            "APOTEKER",
            "KEPERAWATAN",
            "NERS",
            "KEBIDANAN",
            "BIDAN",
            "GIZI",
            "KESEHATAN",
            "FISIOTERAPI",
            "BIOMEDIK",
            "BIOMEDIS",
            "HIGIENE GIGI",
            "FISOTERAPI"
        ]):
            return "Kesehatan"

        # ================== TEKNOLOGI ==================
        elif any(x in jurusan for x in [
            "INFORMATIKA",
            "ILMU KOMPUTER",
            "KOMPUTER",
            "SISTEM INFORMASI",
            "SISTEM KOMPUTER",
            "TEKNOLOGI INFORMASI",
            "PERANGKAT LUNAK",
            "STEI"
        ]):
            return "Teknologi"

        # ================== TEKNIK ==================
        elif any(x in jurusan for x in [
            "TEKNIK",
            "ARSITEKTUR",
            "METALURGI",
            "MATERIAL",
            "ELEKTRO",
            "MESIN",
            "SIPIL",
            "KIMIA",
            "PERTAMBANGAN",
            "PERMINYAKAN",
            "PERKAPALAN",
            "MANUFAKTUR",
            "MEKATRONIKA",
            "GEODESI",
            "GEOMATIKA",
            "TRANSPORTASI",
            "ENERGI",
            "NUKLIR",
            "KEBAKARAN",
            "FTI",
            "FITB",
            "DESAIN",
            "DKV"
        ]):
            return "Teknik"

        # ================== PENDIDIKAN ==================
        elif "PENDIDIKAN" in jurusan or jurusan.startswith("PEND "):
            return "Pendidikan"

        # ================== BISNIS ==================
        elif any(x in jurusan for x in [
            "MANAJEMEN",
            "AKUNTANSI",
            "EKONOMI",
            "AKTUARIA",
            "AGRIBISNIS",
            "BISNIS",
            "MANAJAMEN"
        ]):
            return "Bisnis"

        # ================== SOSIAL ==================
        elif any(x in jurusan for x in [
            "HUKUM",
            "PSIKOLOGI",
            "PARIWISATA",
            "KOMUNIKASI",
            "SOSIAL",
            "PERENCANAAN WILAYAH",
            "PEMBANGUNAN WILAYAH",
            "KOTA"
        ]):
            return "Sosial"

        # ================== SCIENCE ==================
        elif any(x in jurusan for x in [
            "BIOLOGI",
            "BIOKIMIA",
            "BIOTEKNOLOGI",
            "MATEMATIKA",
            "FISIKA",
            "KIMIA",
            "STATISTIKA",
            "STATISTIK",
            "GEOFISIKA",
            "GEOLOGI",
            "GEOGRAFI",
            "OCEANOGRAFI",
            "KELAUTAN",
            "ILMU",
            "SAINS",
            "AGRO",
            "PERTANIAN",
            "TANAMAN",
            "PETERNAKAN",
            "PERIKANAN",
            "BUDIDAYA",
            "AKUAKULTUR",
            "KEHUTANAN",
            "LINGKUNGAN",
            "METEOROLOGI",
            "ATMOSFIR",
            "HORTIKULTURA",
            "TANAH",
            "SILVIKULTUR",
            "MIKROBIOLOGI",
            "PANGAN",
            "NUTRISI",
            "PAKAN",
            "KARTOGRAFI",
            "BIOPROSES",
            "HASIL HUTAN",
            "HASIL TERNAK",
            "HASIL PERAIRAN",
            "INSTRUMENTASI",
            "KONSERVASI",
            "PENGELOLAAN HUTAN",
            "PRODUKSI TERNAK",
            "SUMBERDAYA AKUATIK",
            "BUDI DAYA",
            "PEMANFAATAN"
        ]):
            return "Science"

        else:
            return "Lainnya"

    # Terapkan fungsi kategori
    df['kategori_jurusan'] = df['jurusan_tujuan'].apply(kategori_jurusan)
    
    # Simpan hasil cleaning
    df.to_csv('/opt/airflow/dags/data_merge_clean.csv', index=False)


# Fungsi Load: simpan ke output final

def load():
    df = pd.read_csv('/opt/airflow/dags/data_clean.csv')
    
    df.to_csv('/opt/airflow/output/data_nilai_peserta.csv', index=False)
    print(f"✅ data_nilai_peserta.csv tersimpan — {len(df)} baris, {len(df.columns)} kolom")
    print(f"   Kolom: {list(df.columns)}")
    print(f"   Distribusi kategori:\n{df['kategori_jurusan'].value_counts().to_string()}")


# Definisi DAG

default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2026, 7, 28),
    'retries': 1,
}

with DAG(
    dag_id='etl_utbk_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['utbk', 'final-project'],
) as dag:

    extract_data = PythonOperator(
        task_id='extract',
        python_callable=extract_from_postgres,
    )

    clean_data = PythonOperator(
        task_id='clean',
        python_callable=clean,
    )

    load_data = PythonOperator(
        task_id='load',
        python_callable=load,
    )

    extract_data >> clean_data >> load_data
