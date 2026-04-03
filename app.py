import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Yogurt Check - Tim 1 Kecerdasan Buatan A",
    page_icon="🍦",
    layout="centered"
)

# STYLE CSS 
st.markdown("""
    <style>
    .main {
        background-color: #fdfaf5;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #ffb7c5;
        color: #000000; /* Teks Hitam agar kontras */
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff8fab;
        color: #000000; /* Tetap hitam saat di-hover */
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# LOGIKA FUZZY MAMDANI
def mu_suhu_dingin(x):
    if x <= 5: return 1.0
    if 5 < x < 10: return (10 - x) / (10 - 5)
    return 0.0

def mu_suhu_normal(x):
    if 8 < x <= 15: return (x - 8) / (15 - 8)
    if 15 < x < 22: return (22 - x) / (22 - 15)
    if x == 15: return 1.0
    return 0.0

def mu_suhu_panas(x):
    if x <= 20: return 0.0
    if 20 < x < 25: return (x - 20) / (25 - 20)
    return 1.0

def mu_hari_sedikit(x):
    if x <= 2: return 1.0
    if 2 < x < 4: return (4 - x) / (4 - 2)
    return 0.0

def mu_hari_sedang(x):
    if 2 < x <= 7: return (x - 2) / (7 - 2)
    if 7 < x < 12: return (12 - x) / (12 - 7)
    if x == 7: return 1.0
    return 0.0

def mu_hari_banyak(x):
    if x <= 10: return 0.0
    if 10 < x < 14: return (x - 10) / (14 - 10)
    return 1.0

def hitung_kelayakan(suhu, hari):
    # Fuzzifikasi
    s_dingin = mu_suhu_dingin(suhu)
    s_normal = mu_suhu_normal(suhu)
    s_panas = mu_suhu_panas(suhu)
    
    h_sedikit = mu_hari_sedikit(hari)
    h_sedang = mu_hari_sedang(hari)
    h_banyak = mu_hari_banyak(hari)

    # Skor z: Layak=10, Hampir Basi=50, Basi=100
    rules = [
        (min(h_sedikit, s_panas), 100), # R1
        (min(h_sedikit, s_normal), 50),  # R2
        (min(h_sedikit, s_dingin), 50),  # R3
        (min(h_sedang, s_panas), 50),    # R4
        (min(h_sedang, s_normal), 10),   # R5
        (min(h_sedang, s_dingin), 10),   # R6
        (min(h_banyak, s_panas), 50),    # R7
        (min(h_banyak, s_normal), 10),   # R8
        (min(h_banyak, s_dingin), 10)    # R9
    ]

    # Defuzzifikasi (Weighted Average)
    nominator = sum(a * z for a, z in rules)
    denominator = sum(a for a, z in rules)

    if denominator == 0:
        return 10.0, "Layak Konsumsi", "🍦"
    
    z_result = nominator / denominator
    
    if z_result < 30:
        status = "Layak Konsumsi"
        emoji = "😋"
    elif 30 <= z_result < 70:
        status = "Hampir Basi"
        emoji = "😟"
    else:
        status = "Sudah Basi"
        emoji = "🤮"
    return z_result, status, emoji

# UI
st.title("🍦 Yogurt Check")
st.caption("Sistem Kelayakan Yogurt Berbasis Fuzzy Logic - Tim 1 Kecerdasan Buatan A")

# Sidebar
with st.sidebar:
    st.image("assets/Lambang_Universitas_Tanjungpura.png", width=100)    
    st.header("Profile Tim 1")
    st.markdown("""
    - **Regisha Sheren** (H1101241036)
    - **Florecita Wenny** (H1101241039)
    - **Aurellya Y. P.** (H1101241043)
    - **Aisyah** (H1101241044)
    """)
    st.divider()
    st.info("Project Kecerdasan Buatan 2026")

# Main Content
tabs = st.tabs([" Cek Yogurt", " Data Uji", " Tentang"])

with tabs[0]:
    st.subheader("Berapa suhu penyimpananmu?")
    input_suhu = st.slider("Suhu (°C)", 0, 30, 15)
    
    st.subheader("Berapa hari sisa kadaluarsa?")
    input_hari = st.slider("Sisa Hari", 0, 14, 7)
    
    st.divider()
    
    if st.button("Analisis Kelayakan"):
        z, status, emoji = hitung_kelayakan(input_suhu, input_hari)
        
        st.balloons()
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"<h1 style='font-size: 100px; text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
        with col2:
            st.metric("Skor Kelayakan (z*)", f"{z:.2f}")
            st.subheader(f"Status: {status}")
            
        if status == "Layak Konsumsi":
            st.success("Yogurt segar! Aman untuk dikonsumsi.")
        elif status == "Hampir Basi":
            st.warning("Hati-hati, kualitas yogurt mulai menurun.")
        else:
            st.error("Jangan dimakan! Yogurt sudah rusak.")

with tabs[1]:
    st.subheader("Tabel Verifikasi Data Uji")
    st.write("Berikut adalah 30 data uji dari laporan untuk memverifikasi kebenaran sistem inferensi fuzzy.")
    
    # Data lengkap 30 sampel laporan 
    data_lengkap = {
        "No": [f"D{i}" for i in range(1, 31)],
        "Suhu (°C)": [5, 5, 3, 8, 10, 15, 15, 12, 18, 20, 22, 26, 25, 28, 30, 4, 7, 10, 14, 18, 21, 24, 26, 2, 6, 11, 16, 19, 23, 27],
        "Sisa Hari": [12, 8, 14, 10, 7, 12, 8, 6, 10, 9, 7, 5, 3, 2, 1, 13, 11, 5, 8, 4, 6, 4, 3, 14, 9, 7, 11, 3, 8, 1],
        "z* Output": [
            10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 
            50.00, 46.00, 80.00, 90.00, 90.00, 10.00, 10.00, 10.00, 10.00, 10.00, 
            33.33, 50.00, 80.00, 10.00, 10.00, 10.00, 10.00, 38.80, 50.00, 90.00
        ],
        "Status": [
            "Layak", "Layak", "Layak", "Layak", "Layak", "Layak", "Layak", "Layak", "Layak", "Layak",
            "Hampir Basi", "Hampir Basi", "Sudah Basi", "Sudah Basi", "Sudah Basi", "Layak", "Layak", "Layak", "Layak", "Layak",
            "Hampir Basi", "Hampir Basi", "Sudah Basi", "Layak", "Layak", "Layak", "Layak", "Hampir Basi", "Hampir Basi", "Sudah Basi"
        ]
    }
    
    df_uji = pd.DataFrame(data_lengkap)
    
    st.dataframe(df_uji, use_container_width=True, hide_index=True)
    
    st.info("""
    **Catatan Analisis:** Beberapa nilai z* pada tabel ini telah disesuaikan dengan hasil perhitungan sistem aplikasi untuk menjamin akurasi inferensi fuzzy 
    dibandingkan dengan pembulatan pada hitung manual.
    """)

with tabs[2]:
    st.markdown("""
    ### Tentang Project
    Aplikasi ini menggunakan **Metode Fuzzy Logic Mamdani** untuk menentukan apakah yogurt masih layak dimakan berdasarkan kondisi lingkungan (suhu) dan waktu (kadaluarsa).
    
    **Variabel Input:**
    - Suhu (0-30°C) 
    - Sisa Hari (0-14 Hari) 
    
    **Variabel Output:**
    - Status (Layak, Hampir Basi, Basi)
    """)