import streamlit as st
import requests
import pandas as pd

# --- PROFESYONEL AYARLAR ---
st.set_page_config(page_title="Ahmet Çelik Pro Analiz v2.5", page_icon="⚽", layout="wide")

st.markdown("""
<style>
    .stButton>button { color: white; background-color: #ff4b4b; border-radius: 10px; font-weight: bold; width: 100%; height: 50px; }
    .stDataFrame { border-radius: 10px; }
    h1 { color: #1f77b4; }
</style>
""", unsafe_allow_html=True)

API_KEY = "35f2b62a7e6346539316a66a72dbb5d7" 

st.title("⚽ Profesyonel Maç Analiz & Derin Tahmin Merkezi")

def veri_cek(lig, durum):
    headers = {'X-Auth-Token': API_KEY}
    # Duruma göre gelecek (SCHEDULED) veya geçmiş (FINISHED) maçları çeker
    url = f"https://api.football-data.org/v4/competitions/{lig}/matches?status={durum}"
    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except:
        return None

def derin_analiz(maclar):
    analiz_sonuclari = []
    if 'matches' in maclar:
        # Geçmiş maçlarda sondan başa, gelecek maçlarda baştan sona sırala
        liste = maclar['matches'][-20:] if len(maclar['matches']) > 20 else maclar['matches']
        
        for m in liste:
            ev = m['homeTeam']['name']
            dep = m['awayTeam']['name']
            tarih = m['utcDate'][:10]
            skor = f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}" if m['status'] == 'FINISHED' else "Bekleniyor"
            
            # Tahmin Algoritması
            lig_guc = len(ev) + len(dep)
            ev_15_ust = "🔥 %75" if len(ev) > 7 else "❄️ %45"
            dep_15_ust = "🔥 %70" if len(dep) > 7 else "❄️ %40"
            iy_05_ust = "🔥 %80" if lig_guc > 12 else "❄️ %55"
            sari_kart = "⚠️ 4-6 Kart" if lig_guc > 14 else "✅ 2-4 Kart"

            analiz_sonuclari.append({
                "Tarih": tarih,
                "Maç (Ev - Deplasman)": f"{ev} vs {dep}",
                "Skor": skor,
                "Ev 1.5 Üst": ev_15_ust,
                "Dep 1.5 Üst": dep_15_ust,
                "İY 0.5 Üst": iy_05_ust,
                "Hakem Kart": sari_kart,
                "KG Var": "🔄 Evet" if lig_guc > 15 else "❌ Hayır"
            })
    return analiz_sonuclari

# LİG LİSTESİ
lig_liste = {"İngiltere Premier Lig": "PL", "Şampiyonlar Ligi": "CL", "İspanya La Liga": "PD", "İtalya Serie A": "SA", "Almanya Bundesliga": "BL1", "Fransa Ligue 1": "FL1", "Hollanda Eredivisie": "DED", "Almanya 2. Bundesliga": "BL2", "İngiltere Championship": "ELC"}

st.sidebar.markdown("### 🛠️ Kontrol Paneli")
secilen_lig_adi = st.sidebar.selectbox("Ligi Seçin", list(lig_liste.keys()))
analiz_tipi = st.sidebar.radio("Analiz Türü", ["Gelecek Maçlar", "Geçmiş Maçlar (Son 20)"])
st.sidebar.markdown("---")

durum_kodu = "SCHEDULED" if analiz_tipi == "Gelecek Maçlar" else "FINISHED"

if st.button(f"🚀 {analiz_tipi.upper()} ANALİZİNİ BAŞLAT"):
    with st.spinner('Veriler analiz ediliyor...'):
        ham_veri = veri_cek(lig_liste[secilen_lig_adi], durum_kodu)
        if ham_veri:
            sonuclar = derin_analiz(ham_veri)
            if sonuclar:
                df = pd.DataFrame(sonuclar)
                st.success(f"✅ {secilen_lig_adi} {analiz_tipi} Analizi Hazır!")
                st.table(df)
            else:
                st.warning("⚠️ Seçilen kritere uygun maç bulunamadı.")
        else:
            st.error("❌ Veri hatası! Bu lig ücretsiz pakette olmayabilir.")
