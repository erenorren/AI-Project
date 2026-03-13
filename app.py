import streamlit as st

# --- LOGIKA FUZZY
def hitung_fuzzy(suhu, hari):
    def mu_suhu(x):
        dingin = max(0, min(1, (10 - x) / (10 - 0))) if x < 10 else 0
        normal = max(0, min((x - 8) / (22 - 8), (30 - x) / (30 - 22)))
        panas = max(0, min((x - 20) / (30 - 20), 1)) if x > 20 else 0
        return {"Dingin": dingin, "Normal": normal, "Panas": panas}

    def mu_hari(x):
        sedikit = max(0, min(1, (4 - x) / (4 - 0))) if x < 4 else 0
        sedang = max(0, min((x - 2) / (7 - 2), (12 - x) / (12 - 7)))
        banyak = max(0, min((x - 10) / (14 - 10), 1)) if x > 10 else 0
        return {"Sedikit": sedikit, "Sedang": sedang, "Banyak": banyak}

    s = mu_suhu(suhu)
    h = mu_hari(hari)

    # 9 Aturan (Rule Base)
    rules = [
        (min(h["Sedikit"], s["Panas"]), 100), (min(h["Sedikit"], s["Normal"]), 50),
        (min(h["Sedikit"], s["Dingin"]), 50), (min(h["Sedang"], s["Panas"]), 50),
        (min(h["Sedang"], s["Normal"]), 10), (min(h["Sedang"], s["Dingin"]), 10),
        (min(h["Banyak"], s["Panas"]), 50), (min(h["Banyak"], s["Normal"]), 10),
        (min(h["Banyak"], s["Dingin"]), 10)
    ]

    pembilang = sum([r[0] * r[1] for r in rules])
    penyebut = sum([r[0] for r in rules])
    return pembilang / penyebut if penyebut != 0 else 0

# --- TAMPILAN UI ---
st.set_page_config(page_title="Yogurt Freshness AI", page_icon="🐮")
st.title("🐮 Yogurt Freshness AI")
st.write("Cek kelayakan yogurtmu dengan bantuan AI kami!")

suhu = st.slider("Suhu Penyimpanan (°C)", 0, 30, 22)
hari = st.slider("Sisa Hari Expired", 0, 14, 5)

if st.button("Cek Kesegaran!"):
    hasil = hitung_fuzzy(suhu, hari)
    if hasil < 30:
        st.success(f"Status: Layak Konsumsi! (Skor: {hasil:.2f})")
    elif hasil < 75:
        st.warning(f"Status: Hampir Basi. Segera konsumsi! (Skor: {hasil:.2f})")
    else:
        st.error(f"Status: Basi. Jangan dikonsumsi! (Skor: {hasil:.2f})")